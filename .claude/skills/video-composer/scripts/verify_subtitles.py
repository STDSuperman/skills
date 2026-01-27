#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.lyrics_matcher import LyricsMatcher
from utils.subtitle_generator import SubtitleGenerator


def main():
    lyrics_file = Path(
        "/Users/superman/Documents/TaoCode/github.com/STDSuperman/skills/create/music-create/resource/suno-params.md"
    )
    transcription_file = Path(
        "/Users/superman/Documents/TaoCode/github.com/STDSuperman/skills/create/music-create/output/transcription.json"
    )
    images_dir = Path(
        "/Users/superman/Documents/TaoCode/github.com/STDSuperman/skills/create/music-create/output/images"
    )
    output_dir = Path(
        "/Users/superman/Documents/TaoCode/github.com/STDSuperman/skills/create/music-create/output"
    )

    print("Loading transcription...")
    with open(transcription_file, "r", encoding="utf-8") as f:
        transcription = json.load(f)

    print("\nMatching lyrics with transcription...")
    matcher = LyricsMatcher(lyrics_file, transcription, images_dir)
    matched_sections = matcher.match_sections()
    metadata = matcher.create_metadata(matched_sections)

    metadata_path = output_dir / "timestamped_metadata.json"
    matcher.save_metadata(metadata, metadata_path)

    print("\nGenerating subtitles...")
    subtitle_gen = SubtitleGenerator(metadata)
    subtitle_path = output_dir / "subtitles.srt"
    subtitle_gen.save_srt(subtitle_path)

    print("\n" + "=" * 60)
    print("Subtitle Generation Summary")
    print("=" * 60)
    print(f"Total sections: {len(matched_sections)}")
    print(f"Total duration: {transcription['duration']:.2f}s")

    print("\nSections:")
    for section in matched_sections:
        print(f"\n  [{section['name']}]")
        print(f"    Time: {section['start_time']:.2f}s - {section['end_time']:.2f}s")
        print(f"    Duration: {section['duration']:.2f}s")
        print(f"    Lyrics: {section['lyrics'][:50]}...")

    print("\n" + "=" * 60)
    print("Subtitle Preview (first 10 entries)")
    print("=" * 60)
    with open(subtitle_path, "r", encoding="utf-8-sig") as f:
        content = f.read()
        lines = content.split("\n")
        entry_count = 0
        current_entry = []
        for line in lines:
            current_entry.append(line)
            if not line.strip() and current_entry:
                entry_count += 1
                if entry_count <= 10:
                    print("\n".join(current_entry))
                current_entry = []
            if entry_count >= 10:
                break

    print("\n" + "=" * 60)
    print("Files generated:")
    print(f"  - {metadata_path}")
    print(f"  - {subtitle_path}")
    print("=" * 60)
    print(f"Total sections: {len(matched_sections)}")
    print(f"Total duration: {transcription['duration']:.2f}s")

    print("\nSections:")
    for section in matched_sections:
        print(f"\n  [{section['name']}]")
        print(f"    Time: {section['start_time']:.2f}s - {section['end_time']:.2f}s")
        print(f"    Duration: {section['duration']:.2f}s")
        print(f"    Lyrics: {section['lyrics'][:50]}...")

    # Read and print subtitle preview
    print("\n" + "=" * 60)
    print("Subtitle Preview (first 10 entries)")
    print("=" * 60)
    with open(subtitle_path, "r", encoding="utf-8-sig") as f:
        content = f.read()
        # Print first 10 subtitle entries
        lines = content.split("\n")
        entry_count = 0
        current_entry = []
        for line in lines:
            current_entry.append(line)
            if not line.strip() and current_entry:
                entry_count += 1
                if entry_count <= 10:
                    print("\n".join(current_entry))
                current_entry = []
            if entry_count >= 10:
                break

    print("\n" + "=" * 60)
    print("Files generated:")
    print(f"  - {metadata_path}")
    print(f"  - {subtitle_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
