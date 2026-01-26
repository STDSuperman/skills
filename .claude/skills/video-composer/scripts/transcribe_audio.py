#!/usr/bin/env python3
"""
Audio Transcription Script
Uses OpenAI Whisper or Aliyun FunASR to transcribe audio files with timestamps.
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

from utils.whisper_processor import WhisperProcessor
from utils.funasr_processor import FunASRProcessor
from utils.qwen3_asr_processor import Qwen3ASRProcessor


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio with Whisper or FunASR"
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
        default="whisper",
        choices=["whisper", "funasr", "qwen3-asr"],
        help="Transcription engine to use (default: whisper)",
    )

    # Whisper options
    parser.add_argument(
        "--whisper-model",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model to use (default: base)",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="zh",
        help="Language code for Whisper (default: zh for Chinese)",
    )

    # FunASR options
    parser.add_argument(
        "--funasr-model",
        type=str,
        default="fun-asr",
        choices=["fun-asr", "fun-asr-2025-11-07"],
        help="FunASR model to use (default: fun-asr)",
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
    if args.engine == "whisper":
        if not Path(args.audio).exists():
            print(f"Error: Audio file not found: {args.audio}")
            return 1
    else:
        # FunASR uses URL, no file existence check needed
        if not args.audio.startswith(("http://", "https://")):
            print(f"Error: FunASR requires a public URL, got: {args.audio}")
            return 1

    # Transcribe audio
    try:
        if args.engine == "whisper":
            processor = WhisperProcessor(model_name=args.whisper_model)
            transcription = processor.transcribe(args.audio, language=args.language)
        elif args.engine == "qwen3-asr":
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
