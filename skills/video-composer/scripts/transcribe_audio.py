#!/usr/bin/env python3
"""
Audio Transcription Script
Uses Aliyun FunASR or Qwen3-ASR to transcribe audio files with timestamps.
"""

import os
import argparse
from pathlib import Path
import sys

# Load .env before importing dashscope
from dotenv import load_dotenv

load_dotenv()

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.funasr_processor import FunASRProcessor
from utils.qwen3_asr_processor import Qwen3ASRProcessor


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio with FunASR or Qwen3-ASR"
    )
    parser.add_argument(
        "--audio",
        type=str,
        required=True,
        help="Path to audio file or URL (for FunASR)",
    )
    parser.add_argument(
        "--output", type=Path, required=True, help="Output JSON file path"
    )
    parser.add_argument(
        "--engine",
        type=str,
        default="funasr",
        choices=["funasr", "qwen3-asr"],
        help="Transcription engine to use (default: funasr)",
    )

    # FunASR options
    parser.add_argument(
        "--funasr-model",
        type=str,
        default="fun-asr",
        choices=[
            "fun-asr",
            "fun-asr-2025-11-07",
            "fun-asr-2025-08-25",
            "fun-asr-mtl",
            "fun-asr-mtl-2025-08-25",
        ],
        help="FunASR model to use (default: fun-asr, stable version equivalent to fun-asr-2025-11-07)",
    )

    parser.add_argument(
        "--qwen3-asr-model",
        type=str,
        default="qwen3-asr-flash",
        choices=["qwen3-asr-flash", "qwen3-asr-flash-us"],
        help="Qwen3-ASR model to use (default: qwen3-asr-flash)",
    )

    args = parser.parse_args()

    # Check audio source based on engine
    # Both FunASR and Qwen3-ASR require public URLs
    if not args.audio.startswith(("http://", "https://")):
        print(f"Error: {args.engine} requires a public URL, got: {args.audio}")
        return 1

    # Transcribe audio
    try:
        if args.engine == "qwen3-asr":
            processor = Qwen3ASRProcessor(model=args.qwen3_asr_model)
            transcription = processor.transcribe(args.audio, language="zh")
        else:
            processor = FunASRProcessor(model_id=args.funasr_model)
            transcription = processor.transcribe(args.audio, language="zh")

        # Save transcription
        processor.save_transcription(transcription, args.output)

        # Print summary
        print(f"\n{'=' * 50}")
        print(f"Transcription Summary:")
        print(f"  Engine: {args.engine.upper()}")
        print(f"  Model: {transcription.get('model', 'N/A')}")
        print(f"  Duration: {transcription['duration']:.2f} seconds")
        print(f"  Segments: {len(transcription['segments'])}")
        print(f"  Language: {transcription['language']}")
        print(f"  Output: {args.output}")
        print(f"{'=' * 50}")

        return 0

    except Exception as e:
        print(f"Error during transcription: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
