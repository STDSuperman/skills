---
name: video-composer
description: Compose MP4 videos from images, audio, and subtitles using FFmpeg. Supports Aliyun FunASR and Qwen3-ASR for audio transcription with accurate timestamps, keyframe animations, fade transitions, sentence-level subtitles, and audio synchronization. Use when users want to create music videos, lyric videos, or slideshow videos with audio.
license: MIT
metadata:
  author: STDSuperman
  version: "3.0.0"
  category: video
  tags: video, ffmpeg, composition, subtitles, music-video, transcription, funasr, qwen3-asr
---

# Video Composer Skill

Compose professional MP4 videos from images, audio, and lyrics with automatic transcription-based timing.

## Features

- **Automatic Transcription**: Uses Aliyun FunASR or Qwen3-ASR to transcribe audio and generate accurate timestamps
- **Multiple Transcription Options**:
  - FunASR: Cloud-based API, optimized for Chinese speech recognition
  - Qwen3-ASR: Cloud-based API, optimized for music transcription with accurate word-level timestamps
- **Lyrics Synchronization**: Matches transcribed audio with original lyrics to determine section timing
- **Subtitle Generation**: Creates SRT subtitle files with sentence-level timestamps based on punctuation
- **Keyframe Animations**: Automatic zoom (1.1x) and vertical movement effects for images
- **Fade Transitions**: Smooth 1-second fade transitions between images
- **Audio Synchronization**: Perfect sync between images, subtitles, and audio
- **Chinese Language Support**: Optimized for Chinese lyrics and subtitles

## Quick Start

```bash
# Basic usage with FunASR (default)
python scripts/compose_video.py \
  --audio https://example.com/audio.mp3 \
  --lyrics path/to/lyrics.md \
  --images path/to/illustrations/ \
  --output path/to/output.mp4

# With FunASR API (requires DASHSCOPE_API_KEY, public URL required)
python scripts/compose_video.py \
  --audio https://example.com/audio.mp3 \
  --lyrics lyrics.md \
  --images illustrations/ \
  --output video.mp4 \
  --transcription-engine funasr

# With Qwen3-ASR (recommended for music)
python scripts/compose_video.py \
  --audio https://example.com/audio.mp3 \
  --lyrics lyrics.md \
  --images illustrations/ \
  --output video.mp4 \
  --transcription-engine qwen3-asr \
  --qwen3-asr-model qwen3-asr-flash
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

### For FunASR (Cloud API)

- **Aliyun DashScope API Key**: Required for FunASR transcription
   - Get API key from: https://bailian.console.aliyun.com/cn-beijing/?tab=api#/api/?type=model&url=2978300
   - Set as environment variable: `export DASHSCOPE_API_KEY=your_key_here`
     - Or create `.env` file with: `DASHSCOPE_API_KEY=your_key_here`

## FunASR Transcription

This skill also supports Aliyun FunASR API for cloud-based audio transcription.

### Available Models

| Model  | Type | Speed | Accuracy | Use Case |
|--------|------|-------|----------|----------|
| fun-asr | Cloud API (Stable) | Fast | Excellent | Chinese/English transcription, singing recognition (Recommended) |
| fun-asr-2025-11-07 | Cloud API (Snapshot) | Fast | Excellent | Same as fun-asr, stable version |
| fun-asr-2025-08-25 | Cloud API (Snapshot) | Fast | Good | Previous version snapshot |
| fun-asr-mtl | Cloud API (Stable) | Fast | Excellent | Multi-language: Chinese, Cantonese, English, Japanese, Thai, Vietnamese, Indonesian |
| fun-asr-mtl-2025-08-25 | Cloud API (Snapshot) | Fast | Good | Previous MTL version snapshot |

**Default**: `fun-asr` model (stable version, currently equivalent to fun-asr-2025-11-07)

**Note**: 
- `fun-asr` is the stable version and automatically points to the latest stable model
- `fun-asr-mtl` supports multiple languages including Chinese dialects
- Singing recognition (with BGM) is supported by fun-asr and fun-asr-2025-11-07 models

### Transcription Process (FunASR)

**IMPORTANT**: FunASR only supports public URLs. Audio files must be accessible via HTTP/HTTPS from the internet.

1. Audio file URL is submitted to DashScope API
2. FunASR API processes audio in the cloud asynchronously
3. Task is polled until completion (PENDING → RUNNING → SUCCEEDED)
4. Transcription results are downloaded via transcription_url
5. Returns transcribed text with sentence-level timestamps
6. Transcription is matched with original lyrics sections
7. Section boundaries are identified automatically

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
4. Provide a **public URL** for the audio file (not a local file path)

## Qwen3-ASR Transcription

This skill supports Aliyun Qwen3-ASR API for music-optimized audio transcription.

### Available Models

| Model  | Type | Speed | Accuracy | Use Case |
|--------|------|-------|----------|----------|
| qwen3-asr-flash | Cloud API | Fast | Excellent | Music transcription (Recommended) |
| qwen3-asr-flash-us | Cloud API | Fast | Excellent | Music transcription (US region) |

**Default**: `qwen3-asr-flash` model

### Transcription Process (Qwen3-ASR)

**IMPORTANT**: Qwen3-ASR only supports public URLs. Audio files must be accessible via HTTP/HTTPS from the internet.

1. Audio file URL is uploaded to Aliyun DashScope
2. Qwen3-ASR processes audio with music-optimized recognition
3. Returns transcribed text with sentence-level timestamps
4. Transcription is matched with original lyrics sections
5. Section boundaries are identified automatically

### Setting up Qwen3-ASR

1. Get API Key from Aliyun DashScope console
2. Set environment variable or create `.env` file:
    ```bash
    # Environment variable
    export DASHSCOPE_API_KEY=sk-xxxxxxxx

    # Or in .env file
    DASHSCOPE_API_KEY=sk-xxxxxxxx
    ```

3. Use `--transcription-engine qwen3-asr` flag when running scripts
4. Provide a **public URL** for the audio file (not a local file path)

### When to Use Qwen3-ASR

| Scenario | Recommendation |
|----------|----------------|
| Music transcription | Qwen3-ASR (music-optimized) |
| Chinese lyrics | Qwen3-ASR (best accuracy) |
| Sentence-level timestamps | Qwen3-ASR (natural segmentation) |
| Fast cloud processing | Qwen3-ASR |
| No GPU available | Qwen3-ASR |

### Transcription Engine Comparison

| Scenario | Recommendation |
|----------|----------------|
| Chinese audio only | FunASR (better accuracy) |
| Multi-language (Cantonese, Japanese, Thai, etc.) | FunASR-MTL |
| Singing/lyrics with BGM | FunASR (singing recognition) |
| Fast transcription without GPU | FunASR or Qwen3-ASR |
| Music transcription | Qwen3-ASR (recommended) |
| Sentence-level lyrics sync | Qwen3-ASR |

## Script Usage

### Main Composition Script

```bash
python scripts/compose_video.py \
  --audio <audio_url> \
  --lyrics <lyrics_file> \
  --images <images_directory> \
  --output <output_video>
```

**Arguments:**
- `--audio`: **public URL required** (audio must be accessible from internet for FunASR/Qwen3-ASR)
- `--lyrics`: Path to Suno lyrics markdown file
- `--images`: Directory containing section images (PNG files)
- `--output`: Output video file path (MP4)
- `--transcription-engine`: Transcription engine to use - `funasr` or `qwen3-asr` (default: funasr)
- `--funasr-model`: FunASR model to use (default: fun-asr, ignored if using qwen3-asr)
- `--qwen3-asr-model`: Qwen3-ASR model to use (default: qwen3-asr-flash, ignored if using funasr)
- `--subtitle-style`: Subtitle style preset (default: bottom-center)

### Transcription Only

```bash
# FunASR transcription (with public URL)
python scripts/transcribe_audio.py \
  --audio <audio_url> \
  --output <output_json> \
  --engine funasr \
  --model fun-asr

# Qwen3-ASR transcription (with public URL)
python scripts/transcribe_audio.py \
  --audio <audio_url> \
  --output <output_json> \
  --engine qwen3-asr \
  --model qwen3-asr-flash
```

## Output Files

When you run the composition script, it generates:

1. **transcription.json**: Raw transcription output with timestamps (FunASR or Qwen3-ASR)
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
- Segmentation: Sentence-level based on punctuation
```

### Transition Settings

```python
# Fade transitions
- Duration: 1 second
- Type: Crossfade between images
- Timing: Last 1s of each image fades to next

# Keyframe animations (automatic)
- Zoom: 1.1x scale
- Movement: Vertical up/down motion
- Direction: Alternates between images
- Timing: Matches image duration
```

### Subtitle Segmentation

Subtitles are automatically segmented by punctuation marks for better readability:

- **Sentence delimiters**: 。，！？；
- **Line breaks**: Create separate subtitle entries
- **Commas**: Preserve within sentences (，)
- **Empty sections**: Show section name (e.g., [Intro])

This ensures each subtitle appears and disappears independently, preventing text stacking.

## Examples

### Example 1: Basic Music Video with FunASR

```bash
python scripts/compose_video.py \
  --audio https://example.com/song.mp3 \
  --lyrics song_lyrics.md \
  --images illustrations/ \
  --output music_video.mp4
```

### Example 2: Using FunASR API (Chinese/English)

```bash
python scripts/compose_video.py \
  --audio https://example.com/song.mp3 \
  --lyrics song_lyrics.md \
  --images illustrations/ \
  --output music_video.mp4 \
  --transcription-engine funasr \
  --funasr-model fun-asr
```

### Example 4: Using FunASR-MTL (Multi-language)

```bash
python scripts/compose_video.py \
  --audio https://example.com/song.mp3 \
  --lyrics song_lyrics.md \
  --images illustrations/ \
  --output music_video.mp4 \
  --transcription-engine funasr \
  --funasr-model fun-asr-mtl
```

### Example 4: Using Qwen3-ASR (Recommended for Music)

```bash
python scripts/compose_video.py \
  --audio https://example.com/song.mp3 \
  --lyrics song_lyrics.md \
  --images illustrations/ \
  --output music_video.mp4 \
  --transcription-engine qwen3-asr \
  --qwen3-asr-model qwen3-asr-flash
```

### Example 5: Custom Output Directory

```bash
python scripts/compose_video.py \
  --audio https://example.com/song.mp3 \
  --lyrics song_lyrics.md \
  --images illustrations/ \
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

### Chinese Characters in Subtitles

Subtitles use UTF-8 encoding with BOM for proper Chinese character display.

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
- Use **FunASR** for cloud-based processing without GPU
- Use **Qwen3-ASR** for music transcription and lyrics

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
2. Compare transcription segments with section lyrics using fuzzy matching
3. Identify section boundaries based on best matches
4. Calculate start/end timestamps for each section
5. Handle transcription variations and errors

## References

- [Aliyun FunASR Documentation](https://help.aliyun.com/zh/dashscope/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [SRT Subtitle Format](https://en.wikipedia.org/wiki/SubRip)

## License

MIT License - See LICENSE file for details
