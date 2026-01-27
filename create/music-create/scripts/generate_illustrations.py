#!/usr/bin/env python3
"""
Illustration Generator for Suno Lyrics
Generates anime-style illustrations for each section of parsed lyrics.
Uses the image-generator skill to create images.
"""

import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, List


class IllustrationGenerator:
    """Generator for lyric section illustrations."""

    def __init__(
        self, parsed_lyrics_file: Path, output_dir: Path, image_generator_script: Path
    ):
        self.parsed_lyrics_file = parsed_lyrics_file
        self.output_dir = output_dir
        self.image_generator_script = image_generator_script
        self.parsed_data = self._load_parsed_lyrics()

    def _load_parsed_lyrics(self) -> Dict[str, Any]:
        """Load parsed lyrics JSON file."""
        with open(self.parsed_lyrics_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_all(self) -> List[Dict[str, Any]]:
        """Generate illustrations for all sections."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        sections = self.parsed_data["sections"]

        print(
            f"Generating {len(sections)} illustrations for '{self.parsed_data['song_title']}'...\n"
        )

        for i, section in enumerate(sections, 1):
            print(
                f"[{i}/{len(sections)}] Generating: {section['name']} ({section['id']})"
            )
            print(f"  Prompt: {section['prompt'][:80]}...")

            output_path = self.output_dir / f"{section['id']}.png"

            try:
                self._generate_image(section["prompt"], output_path)
                print(f"  [OK] Saved: {output_path.name}\n")

                results.append(
                    {
                        "id": section["id"],
                        "name": section["name"],
                        "lyrics": section["lyrics"],
                        "image_path": output_path.name,
                        "prompt": section["prompt"],
                    }
                )

            except Exception as e:
                print(f"  [ERROR] {e}\n")
                results.append(
                    {
                        "id": section["id"],
                        "name": section["name"],
                        "lyrics": section["lyrics"],
                        "image_path": None,
                        "error": str(e),
                    }
                )

        return results

    def _generate_image(self, prompt: str, output_path: Path):
        """Call image-generator skill to create an image."""
        cmd = [
            "uv",
            "run",
            "python",
            str(self.image_generator_script),
            prompt,
            "--style",
            "anime",
            "--provider",
            "jiekou",
            "--width",
            "2304",
            "--height",
            "1728",
            "--output",
            str(output_path),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")

        if result.returncode != 0:
            raise RuntimeError(f"Image generation failed: {result.stderr}")

    def save_metadata(self, results: List[Dict[str, Any]]):
        """Save metadata JSON file."""
        metadata = {"song_title": self.parsed_data["song_title"], "sections": results}

        metadata_path = self.output_dir / "metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        print(f"Metadata saved: {metadata_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate illustrations for parsed lyrics"
    )
    parser.add_argument(
        "parsed_lyrics", type=Path, help="Path to parsed lyrics JSON file"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output/illustrations"),
        help="Output directory for illustrations",
    )
    parser.add_argument(
        "--image-generator",
        type=Path,
        default=Path(".claude/skills/image-generator/scripts/generate_image.py"),
        help="Path to image generator script",
    )

    args = parser.parse_args()

    if not args.parsed_lyrics.exists():
        print(f"Error: Parsed lyrics file not found: {args.parsed_lyrics}")
        return 1

    if not args.image_generator.exists():
        print(f"Error: Image generator script not found: {args.image_generator}")
        return 1

    # Generate illustrations
    generator = IllustrationGenerator(
        args.parsed_lyrics, args.output_dir, args.image_generator
    )
    results = generator.generate_all()

    # Save metadata
    generator.save_metadata(results)

    # Print summary
    successful = sum(1 for r in results if r.get("image_path"))
    print(f"\n{'=' * 50}")
    print(f"Generation complete: {successful}/{len(results)} images created")
    print(f"Output directory: {args.output_dir}")
    print(f"{'=' * 50}")

    return 0


if __name__ == "__main__":
    exit(main())
