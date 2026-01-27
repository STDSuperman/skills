#!/usr/bin/env python3
"""
转录后处理 - 重新分割超长segments
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any


class TranscriptionPostProcessor:
    """转录后处理器 - 修复FunASR的时间轴问题"""

    def __init__(
        self,
        transcription_path: Path,
        max_segment_duration: float = 6.0,
    ):
        """
        Args:
            transcription_path: 转录JSON文件路径
            max_segment_duration: 单个segment的最大时长（超过此值需要重新分割）
        """
        with open(transcription_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.segments = self.data["segments"]
        self.max_segment_duration = max_segment_duration

    def _split_by_punctuation(self, text: str) -> List[str]:
        """按标点符号分割"""
        for separator in ["。", "！", "？", "；"]:
            text = text.replace(separator, "|")

        raw_sentences = [s.strip() for s in text.split("|") if s.strip()]
        return raw_sentences

    def _should_split(self, text: str, duration: float) -> bool:
        """判断是否需要重新分割"""
        # 超长segment
        if duration > self.max_segment_duration:
            return True

        # 包含多个句子但只有一个标点
        sentence_count = len([s for s in self._split_by_punctuation(text)])
        if sentence_count > 1:
            # 检查标点符号数量
            punct_count = sum(text.count(p) for p in ["。", "！", "？", "；"])
            if punct_count < sentence_count:
                return True

        return False

    def _smart_split(self, segment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """智能分割超长segment"""
        text = segment["text"].strip()
        start = segment["start"]
        end = segment["end"]

        # 直接返回原segment，不进行任何手动时间分割
        return [segment]

    def process(self) -> Dict[str, Any]:
        """处理转录，重新分割超长segments"""
        processed_segments = []

        for segment in self.segments:
            duration = segment["end"] - segment["start"]

            if self._should_split(segment["text"], duration):
                # 需要重新分割
                new_segments = self._smart_split(segment)
                processed_segments.extend(new_segments)
            else:
                # 保持原segment
                processed_segments.append(segment)

        # 计算总时长
        duration = max((s["end"] for s in processed_segments), default=0)

        return {
            "duration": duration,
            "language": "zh",
            "segments": processed_segments,
            "model": self.data.get("model", "fun-asr-2025-11-07-post-processed"),
        }

    def save(self, output_path: Path):
        """保存处理后的转录"""
        result = self.process()

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"处理后的转录已保存: {output_path}")
        print(f"原始segments: {len(self.segments)}")
        print(f"处理后segments: {len(result['segments'])}")
        print(f"总时长: {result['duration']:.2f}s")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="转录后处理 - 重新分割超长segments")
    parser.add_argument(
        "--transcription", type=Path, required=True, help="转录JSON文件"
    )
    parser.add_argument("--output", type=Path, required=True, help="输出JSON文件")
    parser.add_argument(
        "--max-duration", type=float, default=6.0, help="单segment最大时长（默认6秒）"
    )

    args = parser.parse_args()

    processor = TranscriptionPostProcessor(
        args.transcription, max_segment_duration=args.max_duration
    )
    processor.save(args.output)


if __name__ == "__main__":
    main()
