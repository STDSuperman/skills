#!/usr/bin/env python3
"""
FunASR Processor
Uses Aliyun FunASR API for audio transcription with timestamps.
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from http import HTTPStatus
import dashscope
from dashscope.audio.asr import Transcription

# 初始化 dashscope 配置
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"


class FunASRProcessor:
    """FunASR API 处理器"""

    def __init__(self, model_id: str = "fun-asr", api_key: Optional[str] = None):
        """
        初始化 FunASR 处理器

        Args:
            model_id: 模型 ID (fun-asr, fun-asr-2025-11-07)
            api_key: DashScope API Key (默认从环境变量读取)
        """
        self.model_id = model_id
        self.api_key = api_key or dashscope.api_key

        if not self.api_key:
            raise ValueError(
                "未提供 API Key。请通过参数传递或设置环境变量 DASHSCOPE_API_KEY"
            )

    def transcribe(self, audio_url: str, language: str = "zh") -> Dict[str, Any]:
        """
        转录音频文件（通过公网 URL）

        Args:
            audio_url: 音频文件的公网可访问 URL
            language: 语言代码 (默认 zh)

        Returns:
            转录结果字典，包含 duration, language, segments, model
        """
        print(f"正在使用 FunASR 转录: {audio_url}")
        print(f"模型: {self.model_id}")

        # 提交异步任务
        task_response = Transcription.async_call(
            model=self.model_id, file_urls=[audio_url]
        )

        if task_response.status_code != HTTPStatus.OK:
            raise Exception(f"提交任务失败: {task_response.message}")

        task_id = task_response.output.task_id
        print(f"✓ 任务已提交，ID: {task_id}")

        # 等待任务完成
        print(f"正在等待任务完成...")
        transcribe_response = Transcription.wait(task=task_id)

        if transcribe_response.status_code != HTTPStatus.OK:
            raise Exception(f"转录失败: {transcribe_response.message}")

        # 解析结果
        return self._parse_response(transcribe_response)

    def _parse_response(self, response) -> Dict[str, Any]:
        """解析 Transcription 响应，转换为标准转录格式"""
        output = response.output

        segments = []

        # 检查任务是否成功
        if output.task_status == "SUCCEEDED" and output.results:
            # 获取第一个成功的结果
            for result in output.results:
                if (
                    result.get("subtask_status") == "SUCCEEDED"
                    and "transcription_url" in result
                ):
                    # 下载识别结果
                    transcription_data = self._download_transcription(
                        result["transcription_url"]
                    )

                    # 解析转录数据
                    if "transcripts" in transcription_data:
                        for transcript in transcription_data["transcripts"]:
                            if "sentences" in transcript:
                                for sentence in transcript["sentences"]:
                                    segments.append(
                                        {
                                            "start": sentence.get("begin_time", 0)
                                            / 1000.0,  # 转换为秒
                                            "end": sentence.get("end_time", 0) / 1000.0,
                                            "text": sentence.get("text", ""),
                                        }
                                    )
                    break  # 只处理第一个成功的结果

        # 计算总时长
        duration = max((s["end"] for s in segments), default=0)

        return {
            "duration": duration,
            "language": "zh",
            "segments": segments,
            "model": self.model_id,
        }

    def _download_transcription(self, transcription_url: str) -> Dict[str, Any]:
        """下载转录结果 JSON"""
        response = requests.get(transcription_url)
        response.raise_for_status()
        return response.json()

    def save_transcription(
        self, transcription: Dict[str, Any], output_path: Path
    ) -> None:
        """保存转录结果到 JSON 文件"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transcription, f, ensure_ascii=False, indent=2)

        print(f"✓ 转录结果已保存: {output_path}")

    @staticmethod
    def get_transcription(transcription_path: Path) -> Dict[str, Any]:
        """从 JSON 文件加载转录结果"""
        import json

        with open(transcription_path, "r", encoding="utf-8") as f:
            return json.load(f)
