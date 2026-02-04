#!/usr/bin/env python3
"""
Qwen3 ASR Processor
Uses Aliyun Qwen3-ASR-Flash model for audio transcription with timestamps.
"""

import os
import json
import dashscope
from pathlib import Path
from typing import Dict, Any, Optional

dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"


class Qwen3ASRProcessor:
    """Qwen3-ASR API processor for music transcription."""

    def __init__(self, model: str = "qwen3-asr-flash", api_key: Optional[str] = None):
        """
        Initialize Qwen3-ASR processor.

        Args:
            model: Model name (qwen3-asr-flash, qwen3-asr-flash-us, etc.)
            api_key: DashScope API Key (defaults to DASHSCOPE_API_KEY env var)
        """
        self.model = model
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")

        if not self.api_key:
            raise ValueError(
                "未提供 API Key。请通过参数传递或设置环境变量 DASHSCOPE_API_KEY"
            )

        dashscope.api_key = self.api_key

    def transcribe(self, audio_file: str, language: str = "zh") -> Dict[str, Any]:
        """
        Transcribe audio file.

        Args:
            audio_file: Audio file path or URL
            language: Language code (default: zh)

        Returns:
            Transcription result with duration, language, segments, model
        """
        # Convert Path to string if necessary
        if isinstance(audio_file, Path):
            audio_file = str(audio_file)

        print(f"正在使用 Qwen3-ASR 转录: {audio_file}")
        print(f"模型: {self.model}")

        system_prompt = "你是专业的音乐语音识别助手。请准确识别音频中的歌词内容，特别注意：1. 保持歌词的准确性和完整性 2. 准确标注每个词的时间戳 3. 正确处理音乐中的停顿和重复 4. 保持原始语言的特性"

        messages = [
            {"role": "system", "content": [{"text": system_prompt}]},
            {"role": "user", "content": [{"audio": audio_file}]},
        ]

        try:
            response = dashscope.MultiModalConversation.call(
                api_key=self.api_key,
                model=self.model,
                messages=messages,
                result_format="message",
                asr_options={
                    "enable_itn": False,
                },
            )

            if response.status_code != 200:
                raise Exception(
                    f"API 调用失败 (HTTP {response.status_code}): {response.message}"
                )

            return self._parse_response(response)

        except Exception as e:
            print(f"转录过程中发生错误: {e}")
            raise

    def _parse_response(self, response) -> Dict[str, Any]:
        """Parse Qwen3-ASR response to standard transcription format."""
        output = response.output
        choices = output.get("choices", [])

        segments = []

        if choices:
            message = choices[0].get("message", {})
            content_list = message.get("content", [])

            for content in content_list:
                if "transcription" in content:
                    transcription_data = content["transcription"]

                    if "sentences" in transcription_data:
                        for sentence in transcription_data["sentences"]:
                            segments.append(
                                {
                                    "start": sentence.get("begin_time", 0) / 1000.0,
                                    "end": sentence.get("end_time", 0) / 1000.0,
                                    "text": sentence.get("text", ""),
                                }
                            )
                    elif "segments" in transcription_data:
                        for seg in transcription_data["segments"]:
                            segments.append(
                                {
                                    "start": seg.get("start_time", 0),
                                    "end": seg.get("end_time", 0),
                                    "text": seg.get("text", ""),
                                }
                            )

        if not segments:
            print("警告: 无法从响应中提取标准 segments，尝试备用解析方法")
            segments = self._parse_alternative_format(response)

        duration = max((s["end"] for s in segments), default=0)

        return {
            "duration": duration,
            "language": "zh",
            "segments": segments,
            "model": self.model,
        }

    def _parse_alternative_format(self, response) -> list:
        """Fallback parser for alternative response formats."""
        output = response.output
        choices = output.get("choices", [])

        segments = []

        if choices:
            message = choices[0].get("message", {})
            content_list = message.get("content", [])

            for content in content_list:
                if "text" in content:
                    text = content["text"]
                    segments.append({"start": 0, "end": 300, "text": text})
                    break

        return segments

    def save_transcription(
        self, transcription: Dict[str, Any], output_path: Path
    ) -> None:
        """Save transcription to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transcription, f, ensure_ascii=False, indent=2)

        print(f"✓ 转录结果已保存: {output_path}")

    @staticmethod
    def get_transcription(transcription_path: Path) -> Dict[str, Any]:
        """Load transcription from JSON file."""
        with open(transcription_path, "r", encoding="utf-8") as f:
            return json.load(f)
