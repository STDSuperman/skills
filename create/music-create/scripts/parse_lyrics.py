#!/usr/bin/env python3
"""
Suno Lyrics Parser
Parses Suno-generated lyrics markdown files and extracts sections with their content.
Generates descriptive prompts for anime-style illustration generation.
"""

import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any


class LyricsParser:
    """Parser for Suno lyrics markdown files."""

    # Section tags to extract
    SECTION_PATTERN = r'\[(Intro|Verse \d+|Pre-Chorus|Chorus|Bridge|Outro)\]'

    # Production hints to skip (lines that are only bracket tags)
    PRODUCTION_HINT_PATTERN = r'^\[(?!Intro|Verse|Pre-Chorus|Chorus|Bridge|Outro)[^\]]+\]$'

    def __init__(self, lyrics_file: Path):
        self.lyrics_file = lyrics_file
        self.song_title = self._extract_title()
        self.sections = []

    def _extract_title(self) -> str:
        """Extract song title from the markdown file."""
        with open(self.lyrics_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for title in format: 《站台》
            title_match = re.search(r'《(.+?)》', content)
            if title_match:
                return title_match.group(1)
            return "Untitled"

    def parse(self) -> List[Dict[str, Any]]:
        """Parse the lyrics file and extract sections."""
        with open(self.lyrics_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_section = None
        current_lyrics = []
        section_count = {}  # Track multiple occurrences of same section
        started_parsing = False  # Track if we've started parsing sections

        for line in lines:
            line = line.strip()

            # Check if this is a section tag
            section_match = re.match(self.SECTION_PATTERN, line)
            if section_match:
                started_parsing = True
                # Save previous section if exists
                if current_section:
                    self._save_section(current_section, current_lyrics, section_count)

                # Start new section
                current_section = section_match.group(1)
                current_lyrics = []
                continue

            # Stop at separator line ONLY after we've started parsing sections
            if started_parsing and (line.startswith('---') or line.startswith('═══')):
                # Save current section before breaking
                if current_section:
                    self._save_section(current_section, current_lyrics, section_count)
                break

            # Skip production hints (lines that are only bracket tags)
            if re.match(self.PRODUCTION_HINT_PATTERN, line):
                continue

            # Skip empty lines at the start of a section
            if not current_lyrics and not line:
                continue

            # Add lyrics to current section
            if current_section and line:
                current_lyrics.append(line)

        return self.sections

    def _save_section(self, section_name: str, lyrics: List[str], section_count: Dict[str, int]):
        """Save a section with its lyrics and generated prompt."""
        # Track section occurrences (e.g., Chorus appears twice)
        if section_name not in section_count:
            section_count[section_name] = 1
        else:
            section_count[section_name] += 1

        occurrence = section_count[section_name]
        section_id = f"{section_name.lower().replace(' ', '_')}"
        if occurrence > 1:
            section_id += f"_{occurrence}"

        lyrics_text = '\n'.join(lyrics)
        prompt = self._generate_prompt(section_name, lyrics_text, occurrence)

        self.sections.append({
            'id': section_id,
            'name': section_name,
            'lyrics': lyrics_text,
            'prompt': prompt
        })

    def _generate_prompt(self, section_name: str, lyrics: str, occurrence: int) -> str:
        """Generate anime-style illustration prompt based on section content."""
        base_theme = "地铁站台离别场景"
        style_tags = "anime style, melancholic atmosphere, emotional scene, cinematic lighting"

        # Generate contextual prompts based on section and lyrics
        prompts = {
            'Intro': f"空旷的地铁站台，钢琴琴键特写，月台灯光昏暗，{style_tags}",
            'Verse 1': f"地铁站台上，一个人的背影渐行渐远，另一个人站在原地，月台灯光昏暗，冷风吹拂，{style_tags}",
            'Pre-Chorus': f"地铁站台的灯光一盏盏熄灭，孤独的身影站在月台中央，{style_tags}",
            'Chorus': f"地铁车厢门关闭的瞬间，站台上的人伸手想要挽留但来不及，充满遗憾的画面，{style_tags}" if occurrence == 1
                     else f"空荡的地铁站台，列车驶向远方，孤独的身影困在原地，说不出再见，{style_tags}",
            'Verse 2': f"手机屏幕上显示\"晚安\"消息，手指悬停在拨号键上，昏暗的房间，{style_tags}",
            'Bridge': f"情感爆发的瞬间，想说的话堆积成山，时间的齿轮无情转动，人物痛苦的表情特写，{style_tags}",
            'Outro': f"新的列车进站，月台灯光重新亮起，但站台上的人知道车上不会有那个人，孤独而平静的画面，{style_tags}"
        }

        return prompts.get(section_name, f"{base_theme}，{lyrics[:30]}...，{style_tags}")

    def to_json(self) -> Dict[str, Any]:
        """Convert parsed data to JSON format."""
        return {
            'song_title': self.song_title,
            'sections': self.sections
        }


def main():
    parser = argparse.ArgumentParser(description='Parse Suno lyrics and generate illustration prompts')
    parser.add_argument('lyrics_file', type=Path, help='Path to Suno lyrics markdown file')
    parser.add_argument('--output', type=Path, help='Output JSON file path')

    args = parser.parse_args()

    if not args.lyrics_file.exists():
        print(f"Error: Lyrics file not found: {args.lyrics_file}")
        return 1

    # Parse lyrics
    lyrics_parser = LyricsParser(args.lyrics_file)
    lyrics_parser.parse()

    # Generate output
    output_data = lyrics_parser.to_json()

    # Print summary
    print(f"Parsed song: {output_data['song_title']}")
    print(f"Found {len(output_data['sections'])} sections:")
    for section in output_data['sections']:
        print(f"  - {section['name']} ({section['id']})")

    # Save to file if specified
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"\nSaved to: {args.output}")
    else:
        print("\nJSON output:")
        print(json.dumps(output_data, ensure_ascii=False, indent=2))

    return 0


if __name__ == '__main__':
    exit(main())
