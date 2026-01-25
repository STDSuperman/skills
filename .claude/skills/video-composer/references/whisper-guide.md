# Whisper Usage Guide

## Overview

OpenAI Whisper is a general-purpose speech recognition model that can transcribe audio with word-level timestamps.

## Installation

```bash
pip install openai-whisper
```

For GPU support (recommended):
```bash
pip install openai-whisper torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Available Models

| Model  | Parameters | Size  | Speed | Accuracy | VRAM Required |
|--------|-----------|-------|-------|----------|---------------|
| tiny   | 39M       | 39MB  | ~32x  | Low      | ~1GB          |
| base   | 74M       | 74MB  | ~16x  | Good     | ~1GB          |
| small  | 244M      | 244MB | ~6x   | Better   | ~2GB          |
| medium | 769M      | 769MB | ~2x   | High     | ~5GB          |
| large  | 1550M     | 1550MB| ~1x   | Highest  | ~10GB         |

Speed is relative to real-time (32x means 1 hour of audio in ~2 minutes).

## Basic Usage

```python
import whisper

# Load model
model = whisper.load_model("base")

# Transcribe with word timestamps
result = model.transcribe(
    "audio.mp3",
    language="zh",  # Chinese
    word_timestamps=True,
    verbose=False
)

# Access results
print(result["text"])  # Full transcription
for segment in result["segments"]:
    print(f"{segment['start']:.2f}s - {segment['end']:.2f}s: {segment['text']}")
```

## Language Support

Whisper supports 99 languages. For Chinese:
- Use `language="zh"` for Mandarin Chinese
- Whisper can auto-detect language if not specified
- Chinese transcription accuracy is generally high

## Word-Level Timestamps

```python
result = model.transcribe(audio_path, word_timestamps=True)

for segment in result["segments"]:
    for word in segment.get("words", []):
        print(f"{word['start']:.2f}s: {word['word']}")
```

## Performance Tips

1. **Use GPU**: 10-20x faster than CPU
2. **Choose appropriate model**: Base is good for most use cases
3. **Batch processing**: Process multiple files sequentially
4. **Audio preprocessing**: Convert to 16kHz mono WAV for best results

## Common Issues

### CUDA Out of Memory
- Use smaller model (tiny or base)
- Process shorter audio segments
- Reduce batch size

### Poor Transcription Quality
- Use larger model (medium or large)
- Ensure audio quality is good
- Specify correct language

### Slow Transcription
- Use GPU instead of CPU
- Use smaller model
- Upgrade hardware

## References

- [Whisper GitHub](https://github.com/openai/whisper)
- [Whisper Paper](https://arxiv.org/abs/2212.04356)
- [Model Card](https://github.com/openai/whisper/blob/main/model-card.md)
