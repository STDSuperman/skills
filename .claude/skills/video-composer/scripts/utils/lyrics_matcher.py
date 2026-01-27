"""
Lyrics Matcher
Matches audio transcription with original Suno lyrics sections.
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from Levenshtein import distance as levenshtein_distance


class LyricsMatcher:
    """Match transcribed audio with original lyrics sections."""

    SECTION_PATTERN = r"\[(Intro|Verse \d+|Pre-Chorus|Chorus|Bridge|Outro)\]"
    PRODUCTION_HINT_PATTERN = (
        r"^\[(?!Intro|Verse|Pre-Chorus|Chorus|Bridge|Outro)[^\]]+\]$"
    )

    def __init__(
        self, lyrics_file: Path, transcription: Dict[str, Any], images_dir: Path
    ):
        """
        Initialize lyrics matcher.

        Args:
            lyrics_file: Path to Suno lyrics markdown file
            transcription: Audio transcription result
            images_dir: Directory containing section images
        """
        self.lyrics_file = lyrics_file
        self.transcription = transcription
        self.images_dir = images_dir
        self.song_title = self._extract_title()
        self.sections = self._parse_lyrics()
        self.transcription_segments = transcription.get("segments", [])

    def _extract_title(self) -> str:
        """Extract song title from lyrics file."""
        with open(self.lyrics_file, "r", encoding="utf-8") as f:
            content = f.read()
            title_match = re.search(r"《(.+?)》", content)
            if title_match:
                return title_match.group(1)
            return "Untitled"

    def _parse_lyrics(self) -> List[Dict[str, Any]]:
        """Parse lyrics file and extract sections."""
        with open(self.lyrics_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        sections = []
        current_section = None
        current_lyrics = []
        section_count = {}
        started_parsing = False

        for line in lines:
            line = line.strip()

            section_match = re.match(self.SECTION_PATTERN, line)
            if section_match:
                started_parsing = True
                if current_section:
                    sections.append(
                        self._create_section(
                            current_section, current_lyrics, section_count
                        )
                    )

                current_section = section_match.group(1)
                current_lyrics = []
                continue

            # Stop at separator line ONLY after we've started parsing sections
            if started_parsing and (line.startswith("---") or line.startswith("═══")):
                # Save current section before breaking
                if current_section:
                    sections.append(
                        self._create_section(
                            current_section, current_lyrics, section_count
                        )
                    )
                break

            if re.match(self.PRODUCTION_HINT_PATTERN, line):
                continue

            if not current_lyrics and not line:
                continue

            if current_section and line:
                current_lyrics.append(line)

        return sections

    def _create_section(
        self, section_name: str, lyrics: List[str], section_count: Dict[str, int]
    ) -> Dict[str, Any]:
        """Create section dictionary."""
        if section_name not in section_count:
            section_count[section_name] = 1
        else:
            section_count[section_name] += 1

        occurrence = section_count[section_name]
        section_id = f"{section_name.lower().replace(' ', '_')}"
        if occurrence > 1:
            section_id += f"_{occurrence}"

        lyrics_text = "\n".join(lyrics)

        return {
            "id": section_id,
            "name": section_name,
            "lyrics": lyrics_text,
            "clean_lyrics": self._clean_lyrics(lyrics_text),
        }

    def _clean_lyrics(self, lyrics: str) -> str:
        """Clean lyrics for matching (remove punctuation, normalize whitespace)."""
        # Remove punctuation and extra whitespace
        cleaned = re.sub(r'[，。！？、；：""' "（）【】《》\s]+", "", lyrics)
        return cleaned.lower()

    def match_sections(self) -> List[Dict[str, Any]]:
        """
        Match transcription segments with lyrics sections.

        Returns:
            List of sections with accurate timestamps
        """
        transcribed_text = self.transcription.get("text", "")
        segments = self.transcription.get("segments", [])
        total_duration = self.transcription.get("duration", 0)

        print(f"Matching {len(self.sections)} sections with transcription...")

        matched_sections = []
        current_time = 0.0

        for i, section in enumerate(self.sections):
            print(f"  Matching: {section['name']} ({section['id']})")

            if not section["clean_lyrics"]:
                # Empty section (like Intro), assign short duration
                duration = 8.0 if i == 0 else 5.0
                end_time = min(current_time + duration, total_duration)
            else:
                # Find best matching segment range
                start_time, end_time = self._find_section_timing(
                    section["clean_lyrics"], segments, current_time, total_duration
                )
                current_time = start_time

            # Find corresponding image
            image_path = self._find_image(section["id"])

            section_segments = [
                seg
                for seg in self.transcription_segments
                if seg.get("start", 0) >= current_time and seg.get("end", 0) <= end_time
            ]

            matched_sections.append(
                {
                    "id": section["id"],
                    "name": section["name"],
                    "lyrics": section["lyrics"],
                    "image_path": image_path,
                    "start_time": current_time,
                    "end_time": end_time,
                    "duration": end_time - current_time,
                    "transcription_segments": section_segments,
                }
            )

            current_time = end_time

        print("Matching complete")
        return matched_sections

    def _find_section_timing(
        self,
        clean_lyrics: str,
        segments: List[Dict[str, Any]],
        start_from: float,
        max_duration: float,
    ) -> Tuple[float, float]:
        """
        Find start and end time for a section based on lyrics matching.

        Args:
            clean_lyrics: Cleaned lyrics text to match
            segments: Audio transcription segments
            start_from: Minimum start time
            max_duration: Maximum duration

        Returns:
            Tuple of (start_time, end_time)
        """
        best_match_start = None
        best_match_end = None
        best_score = float("inf")

        for i in range(len(segments)):
            if segments[i]["start"] < start_from:
                continue

            if segments[i]["start"] - start_from > 60:
                continue

            for window_size in range(1, min(10, len(segments) - i + 1)):
                window_segments = segments[i : i + window_size]
                window_text = "".join(seg["text"] for seg in window_segments)
                window_clean = self._clean_lyrics(window_text)

                text_score = levenshtein_distance(clean_lyrics, window_clean)
                time_penalty = (segments[i]["start"] - start_from) * 0.5
                total_score = text_score + time_penalty

                if total_score < best_score:
                    best_score = total_score
                    best_match_start = window_segments[0]["start"]
                    best_match_end = window_segments[-1]["end"]

        if best_match_start is None:
            # Fallback: use remaining time
            best_match_start = start_from
            best_match_end = min(start_from + 20.0, max_duration)

        return best_match_start, best_match_end

    def _find_image(self, section_id: str) -> str:
        """Find image file for section."""
        image_path = self.images_dir / f"{section_id}.png"
        if image_path.exists():
            return str(image_path)
        return ""

    def create_metadata(self, matched_sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create timestamped metadata JSON."""
        return {
            "song_title": self.song_title,
            "total_duration": self.transcription.get("duration", 0),
            "sections": matched_sections,
        }

    def save_metadata(self, metadata: Dict[str, Any], output_path: Path):
        """Save metadata to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"Metadata saved: {output_path}")
