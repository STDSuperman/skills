"""
Subtitle Generator
Generates SRT subtitle files from timestamped metadata.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import timedelta


class SubtitleGenerator:
    """Generate SRT subtitle files from timestamped sections."""

    def __init__(self, metadata: Dict[str, Any]):
        """
        Initialize subtitle generator.

        Args:
            metadata: Timestamped metadata with sections
        """
        self.metadata = metadata

    def generate_srt(self) -> str:
        """
        Generate SRT subtitle content.

        Returns:
            SRT formatted subtitle string
        """
        sections = self.metadata.get('sections', [])
        srt_content = []

        for i, section in enumerate(sections, 1):
            start_time = section.get('start_time', 0)
            end_time = section.get('end_time', 0)
            lyrics = section.get('lyrics', '')

            # Format timestamps
            start_srt = self._format_timestamp(start_time)
            end_srt = self._format_timestamp(end_time)

            # Create SRT entry
            srt_entry = f"{i}\n{start_srt} --> {end_srt}\n"

            # Add section name if no lyrics (like Intro)
            if not lyrics.strip():
                srt_entry += f"[{section['name']}]\n"
            else:
                srt_entry += f"{lyrics}\n"

            srt_entry += "\n"
            srt_content.append(srt_entry)

        return ''.join(srt_content)

    def _format_timestamp(self, seconds: float) -> str:
        """
        Format timestamp for SRT format (HH:MM:SS,mmm).

        Args:
            seconds: Time in seconds

        Returns:
            SRT formatted timestamp
        """
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((td.total_seconds() % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def save_srt(self, output_path: Path):
        """
        Save SRT subtitle file.

        Args:
            output_path: Path to save SRT file
        """
        srt_content = self.generate_srt()

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write with UTF-8 BOM for better Chinese character support
        with open(output_path, 'w', encoding='utf-8-sig') as f:
            f.write(srt_content)

        print(f"Subtitles saved: {output_path}")

    @staticmethod
    def load_metadata(metadata_path: Path) -> Dict[str, Any]:
        """Load metadata from JSON file."""
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
