"""
Whisper Processor
Wrapper for OpenAI Whisper audio transcription with timestamp extraction.
"""

import whisper
import json
from pathlib import Path
from typing import Dict, Any, List


class WhisperProcessor:
    """Process audio files with Whisper for transcription and timestamps."""

    def __init__(self, model_name: str = "base"):
        """
        Initialize Whisper processor.

        Args:
            model_name: Whisper model to use (tiny, base, small, medium, large)
        """
        self.model_name = model_name
        self.model = None

    def load_model(self):
        """Load Whisper model (lazy loading)."""
        if self.model is None:
            print(f"Loading Whisper model: {self.model_name}...")
            self.model = whisper.load_model(self.model_name)
            print("Model loaded successfully")

    def transcribe(self, audio_path: Path, language: str = "zh") -> Dict[str, Any]:
        """
        Transcribe audio file with word-level timestamps.

        Args:
            audio_path: Path to audio file
            language: Language code (default: zh for Chinese)

        Returns:
            Dictionary with transcription results and timestamps
        """
        self.load_model()

        print(f"Transcribing audio: {audio_path}")
        print("This may take a few minutes depending on audio length and model size...")

        result = self.model.transcribe(
            str(audio_path),
            language=language,
            word_timestamps=True,
            verbose=False
        )

        print("Transcription complete")

        return self._format_result(result)

    def _format_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Format Whisper result for easier processing."""
        segments = []

        for segment in result.get('segments', []):
            segments.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'].strip(),
                'words': segment.get('words', [])
            })

        return {
            'text': result.get('text', ''),
            'language': result.get('language', ''),
            'segments': segments,
            'duration': segments[-1]['end'] if segments else 0
        }

    def save_transcription(self, transcription: Dict[str, Any], output_path: Path):
        """Save transcription to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(transcription, f, ensure_ascii=False, indent=2)
        print(f"Transcription saved: {output_path}")

    @staticmethod
    def load_transcription(transcription_path: Path) -> Dict[str, Any]:
        """Load transcription from JSON file."""
        with open(transcription_path, 'r', encoding='utf-8') as f:
            return json.load(f)
