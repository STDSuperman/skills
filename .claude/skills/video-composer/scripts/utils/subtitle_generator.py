"""
Subtitle Generator
Generates SRT subtitle files from timestamped metadata.
"""

import json
import re
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
        Generate SRT subtitle content with sentence-level timestamps.

        Returns:
            SRT formatted subtitle string
        """
        sections = self.metadata.get("sections", [])
        srt_content = []
        subtitle_index = 1

        for section in sections:
            start_time = section.get("start_time", 0)
            end_time = section.get("end_time", 0)
            lyrics = section.get("lyrics", "")
            segments = section.get("transcription_segments", [])

            sentences = self._split_by_punctuation(lyrics)

            if not sentences or not lyrics.strip():
                # Skip sections with no lyrics (like Intro)
                continue

            sentence_times = self._calculate_sentence_times(
                sentences, segments, start_time, end_time
            )

            for sentence, (sent_start, sent_end) in zip(sentences, sentence_times):
                start_srt = self._format_timestamp(sent_start)
                end_srt = self._format_timestamp(sent_end)

                srt_entry = f"{subtitle_index}\n{start_srt} --> {end_srt}\n{sentence.strip()}\n\n"
                srt_content.append(srt_entry)
                subtitle_index += 1

        return "".join(srt_content)

    def _split_by_punctuation(self, text: str) -> List[str]:
        """Split text by punctuation marks."""
        if not text.strip():
            return []

        punctuation_pattern = r"([。！？；，\n])"
        parts = re.split(punctuation_pattern, text)

        sentences = []
        current_sentence = ""

        for part in parts:
            if part in ["。", "！", "？", "；"]:
                current_sentence += part
                if current_sentence.strip():
                    sentences.append(current_sentence)
                current_sentence = ""
            elif part == "，":
                current_sentence += part
            elif part == "\n":
                if current_sentence.strip():
                    sentences.append(current_sentence)
                current_sentence = ""
            else:
                current_sentence += part

        if current_sentence.strip():
            sentences.append(current_sentence)

        sentences = [s for s in sentences if s.strip()]

        return sentences

    def _calculate_sentence_times(
        self,
        sentences: List[str],
        segments: List[Dict[str, Any]],
        section_start: float,
        section_end: float,
    ) -> List[tuple]:
        """
        Calculate start/end times for each sentence.

        Args:
            sentences: List of sentence texts
            segments: Transcription segments with word-level timestamps
            section_start: Section start time
            section_end: Section end time

        Returns:
            List of (start_time, end_time) tuples for each sentence
        """
        if not segments:
            # No segments - distribute time evenly
            duration = section_end - section_start
            sentence_duration = duration / len(sentences) if sentences else 0
            return [
                (
                    section_start + i * sentence_duration,
                    section_start + (i + 1) * sentence_duration,
                )
                for i in range(len(sentences))
            ]

        # Filter segments within section bounds
        section_segments = [
            seg
            for seg in segments
            if seg.get("start", 0) >= section_start and seg.get("end", 0) <= section_end
        ]

        if not section_segments:
            duration = section_end - section_start
            sentence_duration = duration / len(sentences) if sentences else 0
            return [
                (
                    section_start + i * sentence_duration,
                    section_start + (i + 1) * sentence_duration,
                )
                for i in range(len(sentences))
            ]

        sentence_times = []
        total_segment_duration = (
            section_segments[-1]["end"] - section_segments[0]["start"]
        )

        if total_segment_duration == 0 or len(sentences) == 0:
            sentence_times.append((section_start, section_end))
            return sentence_times

        # Try to match sentences with segments based on text content
        if len(sentences) == len(section_segments):
            # One-to-one mapping
            for i, sentence in enumerate(sentences):
                sentence_times.append(
                    (section_segments[i]["start"], section_segments[i]["end"])
                )
        elif len(section_segments) >= 2:
            # Distribute based on text length within segment boundaries
            segment_texts = [seg.get("text", "") for seg in section_segments]
            all_text = "".join(segment_texts)

            # Use section boundary instead of segment boundary for total time
            total_time = section_end - section_start

            # Calculate time for each sentence proportionally
            sentence_times = []
            cumulative_time = section_start

            for i, sentence in enumerate(sentences):
                if i == len(sentences) - 1:
                    # Last sentence: extend to section end
                    sentence_start = cumulative_time
                    sentence_end = max(section_end, sentence_start + 0.5)
                    sentence_times.append((sentence_start, sentence_end))
                else:
                    # Calculate how much time this sentence needs based on text length
                    sentence_chars = len(sentence)
                    time_needed = (sentence_chars / len(all_text)) * total_time

                    sentence_start = cumulative_time
                    sentence_end = cumulative_time + time_needed

                    # Ensure minimum duration
                    if sentence_end - sentence_start < 0.3:
                        sentence_end = sentence_start + 0.3

                    # Clamp to section end
                    sentence_end = min(sentence_end, section_end)
                    sentence_times.append((sentence_start, sentence_end))
                    cumulative_time = sentence_end
        else:
            # Fallback: distribute evenly
            duration = section_end - section_start
            sentence_duration = duration / len(sentences) if sentences else 0
            for i in range(len(sentences)):
                sentence_times.append(
                    (
                        section_start + i * sentence_duration,
                        section_start + (i + 1) * sentence_duration,
                    )
                )

        return sentence_times

        # Estimate sentence positions based on segment timing
        for i, sentence in enumerate(sentences):
            if len(sentences) == 1:
                sentence_times.append((section_start, section_end))
            else:
                # Distribute time proportionally
                proportion = i / (len(sentences) - 1)
                sent_start = (
                    section_segments[0]["start"] + proportion * total_segment_duration
                )
                sent_end = (
                    section_segments[0]["start"]
                    + ((i + 1) / len(sentences)) * total_segment_duration
                )
                sentence_times.append((sent_start, sent_end))

        return sentence_times

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
        with open(output_path, "w", encoding="utf-8-sig") as f:
            f.write(srt_content)

        print(f"Subtitles saved: {output_path}")

    @staticmethod
    def load_metadata(metadata_path: Path) -> Dict[str, Any]:
        """Load metadata from JSON file."""
        with open(metadata_path, "r", encoding="utf-8") as f:
            return json.load(f)
