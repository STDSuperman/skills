#!/usr/bin/env python3
"""
Video Composition Script
Composes MP4 videos from images, audio, and lyrics with automatic transcription.
"""

import argparse
import json
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.lyrics_matcher import LyricsMatcher
from utils.subtitle_generator import SubtitleGenerator
from utils.ffmpeg_wrapper import FFmpegWrapper


def main():
    parser = argparse.ArgumentParser(
        description="Compose video from images, audio, and lyrics"
    )
    parser.add_argument("--audio", type=Path, required=True, help="Path to audio file")
    parser.add_argument(
        "--lyrics", type=Path, required=True, help="Path to Suno lyrics markdown file"
    )
    parser.add_argument(
        "--images", type=Path, required=True, help="Directory containing section images"
    )
    parser.add_argument(
        "--output", type=Path, required=True, help="Output video file path"
    )
    parser.add_argument(
        "--transcription",
        type=Path,
        default=None,
        help="Path to existing transcription JSON file (skip transcription step)",
    )

    parser.add_argument(
        "--transcription-engine",
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

    parser.add_argument(
        "--work-dir",
        type=Path,
        default=None,
        help="Working directory for intermediate files (default: same as output)",
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.audio.exists():
        print(f"Error: Audio file not found: {args.audio}")
        return 1

    if not args.lyrics.exists():
        print(f"Error: Lyrics file not found: {args.lyrics}")
        return 1

    if not args.images.exists():
        print(f"Error: Images directory not found: {args.images}")
        return 1

    # Set working directory
    work_dir = args.work_dir if args.work_dir else args.output.parent
    work_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Video Composition Workflow")
    print("=" * 60)
    print(f"Audio: {args.audio}")
    print(f"Lyrics: {args.lyrics}")
    print(f"Images: {args.images}")
    print(f"Output: {args.output}")
    print(f"Transcription Engine: {args.transcription_engine.upper()}")
    print("=" * 60)

    # Step 1: Check FFmpeg
    print("\n[Step 1/5] Checking FFmpeg...")
    ffmpeg_check = FFmpegWrapper({}, args.audio, Path("dummy.srt"), args.output)
    if not ffmpeg_check.check_ffmpeg():
        print("Error: FFmpeg not found. Please install FFmpeg and add to PATH.")
        return 1
    print("✓ FFmpeg is available")

    if args.transcription and args.transcription.exists():
        print("\n[Step 2/5] Loading existing transcription...")
        transcription_path = args.transcription
        try:
            with open(transcription_path, "r", encoding="utf-8") as f:
                transcription = json.load(f)
            print(f"✓ Transcription loaded ({transcription['duration']:.2f}s)")
        except Exception as e:
            print(f"Error loading transcription: {e}")
            return 1
    else:
        print(
            f"\n[Step 2/5] Transcribing audio with {args.transcription_engine.upper()}..."
        )
        transcription_path = work_dir / "transcription.json"

        try:
            if args.transcription_engine == "qwen3-asr":
                from utils.qwen3_asr_processor import Qwen3ASRProcessor

                processor = Qwen3ASRProcessor(model=args.qwen3_asr_model)
                transcription = processor.transcribe(args.audio, language="zh")
            else:
                from utils.funasr_processor import FunASRProcessor

                processor = FunASRProcessor(model_id=args.funasr_model)
                transcription = processor.transcribe(args.audio, language="zh")

            processor.save_transcription(transcription, transcription_path)
            print(f"✓ Transcription complete ({transcription['duration']:.2f}s)")
        except Exception as e:
            print(f"Error during transcription: {e}")
            return 1

    # Step 3: Match lyrics with transcription
    print("\n[Step 3/5] Matching lyrics with transcription...")
    metadata_path = work_dir / "timestamped_metadata.json"

    try:
        matcher = LyricsMatcher(args.lyrics, transcription, args.images)
        matched_sections = matcher.match_sections()
        metadata = matcher.create_metadata(matched_sections)
        matcher.save_metadata(metadata, metadata_path)
        print(f"✓ Matched {len(matched_sections)} sections")
    except Exception as e:
        print(f"Error during lyrics matching: {e}")
        return 1

    # Step 4: Generate subtitles
    print("\n[Step 4/5] Generating subtitles...")
    subtitle_path = work_dir / "subtitles.srt"

    try:
        subtitle_gen = SubtitleGenerator(metadata)
        subtitle_gen.save_srt(subtitle_path)
        print("✓ Subtitles generated")
    except Exception as e:
        print(f"Error during subtitle generation: {e}")
        return 1

    # Step 5: Compose video with FFmpeg
    print("\n[Step 5/5] Composing video with FFmpeg...")

    try:
        ffmpeg = FFmpegWrapper(metadata, args.audio, subtitle_path, args.output)
        success = ffmpeg.execute()

        if success:
            print("\n" + "=" * 60)
            print("✓ Video composition complete!")
            print(f"Output: {args.output}")
            print("=" * 60)
            return 0
        else:
            print("Error: Video composition failed")
            return 1

    except Exception as e:
        print(f"Error during video composition: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
