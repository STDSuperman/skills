#!/usr/bin/env python3
"""
Create SRT subtitle file from user-provided transcription data.
"""

import json
import re
from pathlib import Path

# 用户提供的字幕数据（已根据 suno-params.md 修正错误）
TRANSCRIPTION_DATA = {
    "utterances": [
        {
            "attribute": {"event": "singing"},
            "end_time": 19860,
            "start_time": 15400,
            "text": "最后一班地铁 你没回头",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 25980,
            "start_time": 20520,
            "text": "我站在原地 数着秒",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 32800,
            "start_time": 27320,
            "text": "想追上去 可脚步怎么都迈不开",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 35360,
            "start_time": 32800,
            "text": "月台上的风很冷",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 41620,
            "start_time": 35360,
            "text": "吹散了 你说过 会等我的那些话",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 46220,
            "start_time": 41920,
            "text": "灯一盏盏熄灭",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 52980,
            "start_time": 48680,
            "text": "我还在这",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 57500,
            "start_time": 54200,
            "text": "如果重来",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 63340,
            "start_time": 57720,
            "text": "我不会让你一个人 走进车厢",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 71020,
            "start_time": 67720,
            "text": "如果重来",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 75360,
            "start_time": 71080,
            "text": "那些沉默的夜晚 我会开口说想你",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 80500,
            "start_time": 75360,
            "text": "可是没有如果",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 87780,
            "start_time": 81400,
            "text": "列车开走后 站台空了",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 95180,
            "start_time": 88080,
            "text": "只剩我 和没说出口的对不起",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 107300,
            "start_time": 103160,
            "text": "手机里还存着 你发的 最后一条消息",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 111840,
            "start_time": 107400,
            "text": "\"晚安\"之后 就再也没有然后了",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 115820,
            "start_time": 111840,
            "text": "我试着回拨你的号码",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 121420,
            "start_time": 116080,
            "text": "听着嘟嘟声",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 132360,
            "start_time": 125280,
            "text": "为什么当时 我没能说出那句留下来",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 140960,
            "start_time": 132400,
            "text": "现在想说的话堆积成山",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 143680,
            "start_time": 140960,
            "text": "却再也传不到你那边",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 148860,
            "start_time": 143680,
            "text": "时间它不听解释",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 155420,
            "start_time": 148860,
            "text": "就这样把我们推远",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 164180,
            "start_time": 157260,
            "text": "如果重来",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 170700,
            "start_time": 164180,
            "text": "我不会在车门关上前选择沉默",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 176420,
            "start_time": 170700,
            "text": "如果重来",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 179820,
            "start_time": 176420,
            "text": "会抓紧你的手",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 183680,
            "start_time": 179820,
            "text": "告诉你别走",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 190300,
            "start_time": 183680,
            "text": "可现实没有倒带键",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 197340,
            "start_time": 190300,
            "text": "列车驶向远方",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 205700,
            "start_time": 197340,
            "text": "而我困在这个 说不出再见的站台",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 210140,
            "start_time": 205700,
            "text": "月台的灯又亮了",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 214540,
            "start_time": 210140,
            "text": "下一班列车进站",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 220300,
            "start_time": 214540,
            "text": "可我知道",
        },
        {
            "attribute": {"event": "singing"},
            "end_time": 225380,
            "start_time": 220300,
            "text": "上面不会有你",
        },
    ]
}


def milliseconds_to_srt_time(ms: int) -> str:
    """Convert milliseconds to SRT time format (HH:MM:SS,mmm)."""
    total_seconds = ms / 1000
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int(ms % 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def create_srt(subtitle_data: dict) -> str:
    """Create SRT subtitle content from transcription data."""
    srt_lines = []

    for idx, utterance in enumerate(subtitle_data["utterances"], start=1):
        start_time = milliseconds_to_srt_time(utterance["start_time"])
        end_time = milliseconds_to_srt_time(utterance["end_time"])
        text = utterance["text"]

        srt_lines.append(f"{idx}")
        srt_lines.append(f"{start_time} --> {end_time}")
        srt_lines.append(text)
        srt_lines.append("")

    return "\n".join(srt_lines)


def main():
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate SRT content
    srt_content = create_srt(TRANSCRIPTION_DATA)

    # Save to file
    srt_path = output_dir / "subtitles.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

    print(f"Subtitle file created: {srt_path}")
    print(f"Total subtitles: {len(TRANSCRIPTION_DATA['utterances'])}")


if __name__ == "__main__":
    main()
