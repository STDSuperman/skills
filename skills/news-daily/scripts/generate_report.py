#!/usr/bin/env python3
import json
import os
import re
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv
from fetch_news import fetch_all_news, strip_html

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

PLATFORM_NAMES = {
    "zhihu": "知乎",
    "wallstreetcn": "华尔街见闻",
    "hupu": "虎扑",
    "thepaper": "澎湃新闻",
    "hackernews": "Hacker News",
    "producthunt": "Product Hunt",
    "github": "GitHub",
    "sspai": "少数派"
}

PLATFORM_ICONS = {
    "zhihu": "📝",
    "wallstreetcn": "💰",
    "hupu": "⚽",
    "thepaper": "📰",
    "hackernews": "💻",
    "producthunt": "🚀",
    "github": "🐙",
    "sspai": "🎯"
}


def is_chinese(text: str) -> bool:
    """检查文本是否包含中文"""
    if not text:
        return False
    return any('\u4e00' <= char <= '\u9fff' for char in text)


def translate_text(text: str, max_length: int = 200) -> str:
    """翻译文本为中文"""
    if not text:
        return text
    
    if is_chinese(text):
        return text[:max_length]
    
    try:
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source='auto', target='zh')
        translated = translator.translate(text[:max_length * 2])
        return translated[:max_length]
    except Exception:
        return text[:max_length]


def generate_markdown_report(items: List[Any]) -> str:
    """生成 Markdown 日报"""
    if not items:
        return "# 无新闻数据"

    total = len(items)
    platform_counts = Counter(item.platform for item in items)

    platforms = defaultdict(list)
    for item in items:
        platforms[item.platform].append(item)

    lines = []
    lines.append("# 📅 每日资讯日报")
    lines.append("")
    lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**总新闻数**: {total} 条")
    lines.append("")
    lines.append("---")
    lines.append("")

    sorted_platforms = sorted(platform_counts.keys(), key=lambda x: platform_counts[x], reverse=True)

    for platform in sorted_platforms:
        platform_items = platforms[platform]
        icon = PLATFORM_ICONS.get(platform, "📌")
        platform_name = PLATFORM_NAMES.get(platform, platform)
        lines.append(f"## {icon} {platform_name} ({len(platform_items)} 条)")
        lines.append("")

        for idx, item in enumerate(platform_items, 1):
            title = item.title
            url = item.url
            translated_title = translate_text(title)

            if url:
                link_text = translated_title if translated_title else "查看详情"
                lines.append(f"{idx}. [{link_text}]({url})")
            else:
                lines.append(f"{idx}. {translated_title}")

            content = item.content
            if content:
                translated_content = translate_text(content, max_length=150)
                if translated_content:
                    lines.append(f"   > {translated_content}")
            lines.append("")

        lines.append("---")
        lines.append("")

    lines.append("*本日报由 OpenClaw News Daily Skill 自动生成*")

    return "\n".join(lines)


def main():
    """主函数"""
    print("📰 开始抓取新闻...")

    items = fetch_all_news()

    print(f"✅ 抓取完成，共 {len(items)} 条新闻")

    report = generate_markdown_report(items)

    filename = f"daily-news-{datetime.now().strftime('%Y%m%d')}.md"
    filepath = Path(__file__).parent.parent / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ 日报已生成: {filepath}")
    print(report)


if __name__ == "__main__":
    main()
