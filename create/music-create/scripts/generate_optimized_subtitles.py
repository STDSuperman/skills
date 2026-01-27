#!/usr/bin/env python3
"""
优化的字幕生成器 - 按原始歌词行结构分割
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from Levenshtein import distance as levenshtein_distance


class OptimizedSubtitleGenerator:
    """按原始歌词行结构生成字幕"""

    def __init__(self, transcription_path: Path, lyrics_path: Path):
        with open(transcription_path, "r", encoding="utf-8") as f:
            self.transcription = json.load(f)

        self.lyrics_path = lyrics_path
        self.segments = self.transcription.get("segments", [])
        self.lyric_lines = self._parse_lyrics_lines()

    def _parse_lyrics_lines(self) -> List[Dict[str, Any]]:
        """解析原始歌词，保留行号和所属section"""
        with open(self.lyrics_path, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")
        lyric_lines = []
        in_lyrics = False
        current_section = None

        section_pattern = r"^\[(Intro|Verse \d+|Pre-Chorus|Chorus|Bridge|Outro)\]$"
        hint_pattern = r"^\[(?!Intro|Verse|Pre-Chorus|Chorus|Bridge|Outro)[^\]]+\]$"

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            if in_lyrics and (
                line_stripped.startswith("---") or line_stripped.startswith("═══")
            ):
                break

            section_match = re.match(section_pattern, line_stripped)
            if section_match:
                in_lyrics = True
                current_section = section_match.group(1)
                continue

            if not in_lyrics:
                continue

            if re.match(hint_pattern, line_stripped) or not line_stripped:
                continue

            lyric_lines.append(
                {"line_number": i, "text": line_stripped, "section": current_section}
            )

        return lyric_lines

    def _clean_text(self, text: str) -> str:
        """清理文本用于匹配"""
        return re.sub(r'[，。！？、；：""' "（）【】《》\s]", "", text).lower()

    def _find_matching_lines(self, transcription_text: str) -> List[str]:
        """在原始歌词中找到匹配的行"""
        cleaned_trans = self._clean_text(transcription_text)

        # 尝试不同的匹配策略
        matches = []

        # 策略1: 精确匹配
        for lyric in self.lyric_lines:
            if self._clean_text(lyric["text"]) == cleaned_trans:
                return [lyric["text"]]

        # 策略2: 基于子串匹配
        remaining_text = transcription_text
        matched_lines = []
        unused_lyrics = [l for l in self.lyric_lines]

        while remaining_text:
            best_match = None
            best_score = float("inf")
            best_pos = len(remaining_text) + 1

            for lyric in unused_lyrics:
                pos = remaining_text.find(lyric["text"])
                if pos != -1:
                    score = pos / len(remaining_text)
                    if score < best_score:
                        best_score = score
                        best_match = lyric
                        best_pos = pos

            if best_match:
                matched_lines.append(best_match["text"])
                remaining_text = remaining_text[
                    best_pos + len(best_match["text"]) :
                ].lstrip("，。！？、；：")
                unused_lyrics.remove(best_match)
            else:
                # 无法匹配的部分，作为单独的行
                break

        return matched_lines

    def _split_transcription_to_lines(self, transcription_text: str) -> List[str]:
        """将转录文本分割成与歌词行匹配的片段"""
        # 先尝试按标点分割
        parts = re.split(r"([。！？；，])", transcription_text)

        sentences = []
        current = []

        for i in range(0, len(parts), 2):
            if i + 1 < len(parts):
                sentences.append(parts[i] + parts[i + 1])
            elif parts[i].strip():
                sentences.append(parts[i])

        # 清理句子：去掉尾部标点符号
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            # 去掉尾部的标点符号
            while sentence and sentence[-1] in "，。！？；":
                sentence = sentence[:-1].strip()
            if sentence:
                cleaned_sentences.append(sentence)

        return cleaned_sentences

    def generate_subtitles(self) -> List[Dict[str, Any]]:
        """生成字幕列表"""
        subtitles = []
        index = 1

        for segment in self.segments:
            transcribed_text = segment["text"].strip()
            start_time = segment["start"]
            end_time = segment["end"]

            if not transcribed_text:
                continue

            # 直接使用 ASR 转录的时间轴，不进行任何手动校准
            subtitles.append(
                {
                    "index": index,
                    "start_time": start_time,
                    "end_time": end_time,
                    "transcription": transcribed_text,
                    "lyric": transcribed_text,
                }
            )

            index += 1

        return subtitles

    def save_srt(self, subtitles: List[Dict[str, Any]], output_path: Path):
        """保存SRT文件"""
        lines = []

        for sub in subtitles:
            lines.append(f"{sub['index']}")
            lines.append(
                f"{self._format_timestamp(sub['start_time'])} --> {self._format_timestamp(sub['end_time'])}"
            )
            lines.append(sub["lyric"])
            lines.append("")

        with open(output_path, "w", encoding="utf-8-sig") as f:
            f.write("\n".join(lines))

        print(f"字幕已保存: {output_path}")

    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """格式化时间戳"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def main():
    import argparse

    parser = argparse.ArgumentParser(description="生成优化后的字幕")
    parser.add_argument(
        "--transcription", type=Path, required=True, help="转录JSON文件"
    )
    parser.add_argument("--lyrics", type=Path, required=True, help="原始歌词文件")
    parser.add_argument("--output", type=Path, required=True, help="输出SRT文件")
    parser.add_argument("--report", type=Path, required=True, help="输出报告文件")

    args = parser.parse_args()

    generator = OptimizedSubtitleGenerator(args.transcription, args.lyrics)
    subtitles = generator.generate_subtitles()
    generator.save_srt(subtitles, args.output)

    # 生成报告
    with open(args.report, "w", encoding="utf-8") as f:
        f.write("字幕生成报告（优化版）\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"总字幕数: {len(subtitles)}\n\n")

        for sub in subtitles:
            f.write(
                f"[字幕 {sub['index']}] {generator._format_timestamp(sub['start_time'])} - {generator._format_timestamp(sub['end_time'])}\n"
            )
            f.write(f"  文本: {sub['lyric']}\n")
            f.write("-" * 80 + "\n")

    print(f"报告已保存: {args.report}")


if __name__ == "__main__":
    main()
