#!/usr/bin/env python3
"""
文档解析器
解析 docs.json，提取英文文档结构
"""

import json
import os
from pathlib import Path
from typing import Dict, List

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent


def parse_docs_json(docs_json_path: str) -> Dict[str, Dict]:
    """
    解析 docs.json，提取英文文档结构

    Args:
        docs_json_path: docs.json 文件路径

    Returns:
        {
            "Get started": {
                "groups": [
                    {"group": "Home", "pages": ["index"]},
                    {"group": "Overview", "pages": ["start/showcase"]}
                ]
            },
            ...
        }
    """
    with open(docs_json_path, encoding='utf-8') as f:
        config = json.load(f)

    result = {}

    # 遍历语言配置
    for lang in config.get('navigation', {}).get('languages', []):
        language = lang.get('language', '')

        # 只处理英文
        if language != 'en':
            continue

        # 遍历 tabs
        for tab in lang.get('tabs', []):
            tab_name = tab.get('tab')
            if not tab_name:
                continue

            groups = []

            # 遍历 groups
            for group in tab.get('groups', []):
                group_name = group.get('group')
                pages = group.get('pages', [])

                if group_name and pages:
                    groups.append({
                        'group': group_name,
                        'pages': pages
                    })

            if groups:
                result[tab_name] = {'groups': groups}

    return result


def resolve_doc_files(docs_dir: str, pages: List[str]) -> List[str]:
    """
    解析 pages 路径为实际文件路径

    Args:
        docs_dir: docs 目录路径
        pages: 页面路径列表，如 ["index", "start/showcase"]

    Returns:
        实际文件路径列表，如 ["docs/index.mdx", "docs/start/showcase.mdx"]
    """
    files = []
    docs_path = Path(docs_dir)

    for page in pages:
        # 尝试 .mdx 和 .md 扩展名
        for ext in ['.mdx', '.md']:
            file_path = docs_path / f"{page}{ext}"
            if file_path.exists():
                files.append(str(file_path))
                break

    return files


def get_all_doc_files(docs_structure: Dict[str, Dict], docs_dir: str) -> Dict[str, List[str]]:
    """
    获取所有文档文件路径

    Args:
        docs_structure: parse_docs_json 返回的结构
        docs_dir: docs 目录路径

    Returns:
        {
            "Get started": ["docs/index.mdx", "docs/start/showcase.mdx"],
            ...
        }
    """
    result = {}

    for tab_name, tab_data in docs_structure.items():
        all_pages = []

        for group in tab_data['groups']:
            all_pages.extend(group['pages'])

        files = resolve_doc_files(docs_dir, all_pages)
        result[tab_name] = files

    return result


if __name__ == '__main__':
    # 测试代码
    config_file = SKILL_DIR / 'references' / 'config.json'
    with open(config_file) as f:
        config = json.load(f)

    repo_path = SKILL_DIR / config['repo_path']
    docs_json = repo_path / 'docs' / 'docs.json'

    print("正在解析 docs.json...")
    structure = parse_docs_json(docs_json)

    print(f"\n找到 {len(structure)} 个 Tab:")
    for tab_name, tab_data in structure.items():
        group_count = len(tab_data['groups'])
        page_count = sum(len(g['pages']) for g in tab_data['groups'])
        print(f"  - {tab_name}: {group_count} groups, {page_count} pages")

    print("\n正在解析文档文件...")
    docs_dir = repo_path / 'docs'
    doc_files = get_all_doc_files(structure, docs_dir)

    print(f"\n文档文件统计:")
    total_files = 0
    for tab_name, files in doc_files.items():
        print(f"  - {tab_name}: {len(files)} files")
        total_files += len(files)
    print(f"\n总计: {total_files} 个文档文件")
