#!/usr/bin/env python3
"""
测试 FunASR 转录
"""

import sys
import json
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__).parent.parent.parent
        / ".claude"
        / "skills"
        / "video-composer"
        / "scripts"
    ),
)

from utils.funasr_processor import FunASRProcessor


def main():
    audio_url = "https://cdn1.suno.ai/36182814-3400-445f-ae1e-e8c6726f8ea6.mp3"
    output_path = Path("output/transcription.json")

    processor = FunASRProcessor(model_id="fun-asr-2025-11-07")

    try:
        transcription = processor.transcribe(audio_url, language="zh")
        processor.save_transcription(transcription, output_path)

        print("\n转录结果预览:")
        print(f"总时长: {transcription['duration']:.2f}s")
        print(f"段落数: {len(transcription['segments'])}")
        print("\n前 10 个段落:")
        for i, seg in enumerate(transcription["segments"][:10], 1):
            print(f"{i}. [{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text']}")

        return 0
    except Exception as e:
        print(f"错误: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
