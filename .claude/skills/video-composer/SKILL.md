---
name: video-composer
description: Compose MP4 videos from images, audio, and subtitles using FFmpeg. Supports both OpenAI Whisper and Aliyun FunASR for audio transcription with accurate timestamps, fade transitions, subtitle burning, and audio synchronization. Use when users want to create music videos, lyric videos, or slideshow videos with audio.
license: MIT
metadata:
  author: STDSuperman
  version: "2.0.0"
  category: video
  tags: video, ffmpeg, composition, subtitles, music-video, whisper, transcription, funasr
---

# Video Composer Skill

Compose professional MP4 videos from images, audio, and lyrics with automatic transcription-based timing.

## Features

- **Automatic Transcription**: Uses OpenAI Whisper or Aliyun FunASR to transcribe audio and generate accurate timestamps
- **Multiple Transcription Options**:
  - Whisper: Local processing, various model sizes (tiny/base/small/medium/large)
  - FunASR: Cloud-based API, optimized for Chinese speech recognition
- **Lyrics Synchronization**: Matches transcribed audio with original lyrics to determine section timing
- **Subtitle Generation**: Creates SRT subtitle files with accurate timestamps
- **Fade Transitions**: Smooth 1-second fade transitions between images
- **Audio Synchronization**: Perfect sync between images, subtitles, and audio
- **Chinese Language Support**: Optimized for Chinese lyrics and subtitles

## Quick Start

```bash
# Basic usage (default: Whisper with base model)
python scripts/compose_video.py \
  --audio path/to/audio.mp3 \
  --lyrics path/to/lyrics.md \
  --images path/to/illustrations/ \
  --output path/to/output.mp4

# With FunASR API (requires DASHSCOPE_API_KEY)
python scripts/compose_video.py \
  --audio audio.mp3 \
  --lyrics lyrics.md \
  --images illustrations/ \
  --output video.mp4 \
  --transcription-engine funasr

# With specific Whisper model
python scripts/compose_video.py \
  --audio audio.mp3 \
  --lyrics lyrics.md \
  --images illustrations/ \
  --output video.mp4 \
  --transcription-engine whisper \
  --whisper-model medium
```

## System Requirements

### Required Software

1. **FFmpeg**: Video encoding and composition
   ```bash
   # Check installation
   ffmpeg -version

   # Install on Windows (via Chocolatey)
   choco install ffmpeg

   # Install on macOS
   brew install ffmpeg

   # Install on Linux
   sudo apt install ffmpeg
   ```

2. **Python 3.8+**: Script execution
   ```bash
   python --version
   ```

3. **Python Dependencies**: Install from requirements.txt
   ```bash
   pip install -r scripts/requirements.txt
   ```

### Optional (Recommended)

- **CUDA/GPU**: Significantly faster Whisper transcription
   - CPU transcription works but is slower
   - GPU can be 10-20x faster for large audio files

### For FunASR (Cloud API)

- **Aliyun DashScope API Key**: Required for FunASR transcription
   - Get API key from: https://bailian.console.aliyun.com/cn-beijing/?tab=api
   - Set as environment variable: `export DASHSCOPE_API_KEY=your_key_here`
   - Or create `.env` file with: `DASHSCOPE_API_KEY=your_key_here`

## Whisper Transcription

This skill uses OpenAI Whisper for automatic audio transcription with word-level timestamps.

### Available Models

| Model  | Size | Speed | Accuracy | Use Case |
|--------|------|-------|----------|----------|
| tiny   | 39M  | Fast  | Low      | Quick tests |
| base   | 74M  | Fast  | Good     | **Recommended** |
| small  | 244M | Medium| Better   | Higher accuracy needed |
| medium | 769M | Slow  | High     | Professional quality |
| large  | 1550M| Very Slow | Highest | Maximum accuracy |

**Default**: `base` model (good balance of speed and accuracy)

### Transcription Process (Whisper)

1. Audio file is loaded and preprocessed
2. Whisper transcribes with word-level timestamps
3. Transcription is matched with original lyrics sections
4. Section boundaries are identified automatically
5. Accurate start/end times are calculated for each section

## FunASR Transcription

This skill also supports Aliyun FunASR API for cloud-based audio transcription.

### Available Models

| Model  | Type | Speed | Accuracy | Use Case |
|--------|------|-------|----------|----------|
| paraformer-8k-v1 | Cloud API | Fast | Good | 8kHz audio files |
| paraformer-16k-v1 | Cloud API | Fast | Excellent | 16kHz audio files (Recommended) |

**Default**: `paraformer-16k-v1` model

### Transcription Process (FunASR)

1. Audio file is encoded to base64
2. FunASR API processes audio in the cloud
3. Returns transcribed text with timestamps
4. Transcription is matched with original lyrics sections
5. Section boundaries are identified automatically

### Setting up FunASR

1. Get API Key from Aliyun DashScope console
2. Set environment variable or create `.env` file:
   ```bash
   # Environment variable
   export DASHSCOPE_API_KEY=sk-xxxxxxxx

   # Or in .env file
   DASHSCOPE_API_KEY=sk-xxxxxxxx
   ```

3. Use `--transcription-engine funasr` flag when running scripts

### When to Use FunASR vs Whisper

| Scenario | Recommendation |
|----------|----------------|
| Chinese audio only | FunASR (better accuracy) |
| Offline processing | Whisper |
| Mixed language | Whisper |
| Fast transcription without GPU | FunASR |
| Maximum control/quality | Whisper with medium/large models |

## Script Usage

### Main Composition Script

```bash
python scripts/compose_video.py \
  --audio <audio_file> \
  --lyrics <lyrics_file> \
  --images <images_directory> \
  --output <output_video> \
  [--whisper-model <model_name>] \
  [--subtitle-style <style>]
```

**Arguments:**
- `--audio`: Path to audio file (MP3, WAV, etc.)
- `--lyrics`: Path to Suno lyrics markdown file
- `--images`: Directory containing section images (PNG files)
- `--output`: Output video file path (MP4)
- `--transcription-engine`: Transcription engine to use - `whisper` or `funasr` (default: whisper)
- `--whisper-model`: Whisper model to use (default: base, ignored if using funasr)
- `--funasr-model`: FunASR model to use (default: paraformer-16k-v1, ignored if using whisper)
- `--subtitle-style`: Subtitle style preset (default: bottom-center)

### Transcription Only

```bash
# Whisper transcription
python scripts/transcribe_audio.py \
  --audio <audio_file> \
  --output <output_json> \
  --engine whisper \
  --model <model_name> \
  --language zh

# FunASR transcription
python scripts/transcribe_audio.py \
  --audio <audio_file> \
  --output <output_json> \
  --engine funasr \
  --model paraformer-16k-v1
```

## Output Files

When you run the composition script, it generates:

1. **transcription.json**: Raw transcription output with timestamps (Whisper or FunASR)
2. **timestamped_metadata.json**: Matched sections with accurate timing
3. **subtitles.srt**: SRT subtitle file
4. **[output].mp4**: Final video file

## Configuration

### Subtitle Styling

Subtitles are burned into the video with customizable styling:

```python
# Default style (bottom-center)
- Position: Bottom center
- Font: Arial, size 24
- Color: White with black outline
- Background: Semi-transparent black box
- Encoding: UTF-8 (supports Chinese characters)
```

### Transition Settings

```python
# Fade transitions
- Duration: 1 second
- Type: Crossfade between images
- Timing: Last 1s of each image fades to next
```

## Examples

### Example 1: Basic Music Video

```bash
python scripts/compose_video.py \
  --audio song.mp3 \
  --lyrics song_lyrics.md \
  --images illustrations/ \
  --output music_video.mp4
```

### Example 2: High-Quality with Medium Model

```bash
python scripts/compose_video.py \
  --audio song.mp3 \
  --lyrics song_lyrics.md \
  --images illustrations/ \
  --output music_video.mp4 \
  --whisper-model medium
```

### Example 3: Using FunASR API

```bash
python scripts/compose_video.py \
  --audio song.mp3 \
  --lyrics song_lyrics.md \
  --images illustrations/ \
  --output music_video.mp4 \
  --transcription-engine funasr \
  --funasr-model paraformer-16k-v1
```

### Example 3: Custom Output Directory

```bash
python scripts/compose_video.py \
  --audio ../audio/song.mp3 \
  --lyrics ../lyrics/song.md \
  --images ../illustrations/ \
  --output ../output/final_video.mp4
```

## Workflow Integration

This skill is designed to work with the Suno lyrics illustration workflow:

```
1. Parse lyrics → parse_lyrics.py
2. Generate illustrations → generate_illustrations.py
3. Review images (manual)
4. Compose video → video-composer skill
```

## Troubleshooting

### FFmpeg Not Found

```
Error: ffmpeg not found in PATH
Solution: Install FFmpeg and add to system PATH
```

### Whisper Model Download

First run will download the selected Whisper model:
- tiny: ~39 MB
- base: ~74 MB
- small: ~244 MB
- medium: ~769 MB
- large: ~1550 MB

### Chinese Characters in Subtitles

Subtitles use UTF-8 encoding with BOM for proper Chinese character display.

### GPU/CUDA Issues

If CUDA is not available, Whisper will automatically fall back to CPU mode.

### FunASR API Errors

```
Error: 未提供 API Key
Solution: Set DASHSCOPE_API_KEY environment variable or create .env file
```

```
Error: API 调用失败: 401 Unauthorized
Solution: Verify your API key is correct and has access to FunASR service
```

### Transcription Engine Selection

Choose the right engine based on your needs:
- Use **FunASR** for Chinese audio (better accuracy)
- Use **Whisper** for multi-language or offline processing
- Use **Whisper with GPU** for fastest local processing
- Use **FunASR** for cloud-based processing without GPU

## Technical Details

### Video Encoding Settings

```
- Video Codec: H.264 (libx264)
- Audio Codec: AAC
- Pixel Format: yuv420p (maximum compatibility)
- Frame Rate: 25 fps
- Audio Sample Rate: 44100 Hz
```

### Lyrics Matching Algorithm

1. Extract clean lyrics from each section
2. Compare Whisper segments with section lyrics using fuzzy matching
3. Identify section boundaries based on best matches
4. Calculate start/end timestamps for each section
5. Handle transcription variations and errors

## References

- [Whisper Documentation](https://github.com/openai/whisper)
- [Aliyun FunASR Documentation](https://help.aliyun.com/zh/dashscope/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [SRT Subtitle Format](https://en.wikipedia.org/wiki/SubRip)

## License

MIT License - See LICENSE file for details
