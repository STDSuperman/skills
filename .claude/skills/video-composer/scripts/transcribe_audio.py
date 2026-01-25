#!/usr/bin/env python3
"""
Audio Transcription Script
Uses OpenAI Whisper to transcribe audio files with word-level timestamps.
"""

import argparse
from pathlib import Path
import sys

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.whisper_processor import WhisperProcessor


def main():
    parser = argparse.ArgumentParser(description='Transcribe audio with Whisper')
    parser.add_argument('--audio', type=Path, required=True, help='Path to audio file')
    parser.add_argument('--output', type=Path, required=True, help='Output JSON file path')
    parser.add_argument('--model', type=str, default='base',
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Whisper model to use (default: base)')
    parser.add_argument('--language', type=str, default='zh',
                        help='Language code (default: zh for Chinese)')

    args = parser.parse_args()

    if not args.audio.exists():
        print(f"Error: Audio file not found: {args.audio}")
        return 1

    # Initialize Whisper processor
    processor = WhisperProcessor(model_name=args.model)

    # Transcribe audio
    try:
        transcription = processor.transcribe(args.audio, language=args.language)

        # Save transcription
        processor.save_transcription(transcription, args.output)

        # Print summary
        print(f"\n{'='*50}")
        print(f"Transcription Summary:")
        print(f"  Duration: {transcription['duration']:.2f} seconds")
        print(f"  Segments: {len(transcription['segments'])}")
        print(f"  Language: {transcription['language']}")
        print(f"  Output: {args.output}")
        print(f"{'='*50}")

        return 0

    except Exception as e:
        print(f"Error during transcription: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
