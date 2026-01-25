---
name: video-composer
description: Compose MP4 videos from images, audio, and subtitles using FFmpeg and Whisper. Automatically transcribes audio to generate accurate timestamps, supports fade transitions, subtitle burning, and audio synchronization. Use when users want to create music videos, lyric videos, or slideshow videos with audio.
license: MIT
metadata:
  author: STDSuperman
  version: "1.0.0"
  category: video
  tags: video, ffmpeg, composition, subtitles, music-video, whisper, transcription
---

# Video Composer Skill

Compose professional MP4 videos from images, audio, and lyrics with automatic transcription-based timing.

## Features

- **Automatic Transcription**: Uses OpenAI Whisper to transcribe audio and generate accurate timestamps
- **Lyrics Synchronization**: Matches transcribed audio with original lyrics to determine section timing
- **Subtitle Generation**: Creates SRT subtitle files with accurate timestamps
- **Fade Transitions**: Smooth 1-second fade transitions between images
- **Audio Synchronization**: Perfect sync between images, subtitles, and audio
- **Chinese Language Support**: Optimized for Chinese lyrics and subtitles

## Quick Start

```bash
# Basic usage
python scripts/compose_video.py \
  --audio path/to/audio.mp3 \
  --lyrics path/to/lyrics.md \
  --images path/to/illustrations/ \
  --output path/to/output.mp4

# With specific Whisper model
python scripts/compose_video.py \
  --audio audio.mp3 \
  --lyrics lyrics.md \
  --images illustrations/ \
  --output video.mp4 \
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

### Transcription Process

1. Audio file is loaded and preprocessed
2. Whisper transcribes with word-level timestamps
3. Transcription is matched with original lyrics sections
4. Section boundaries are identified automatically
5. Accurate start/end times are calculated for each section

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
- `--whisper-model`: Whisper model to use (default: base)
- `--subtitle-style`: Subtitle style preset (default: bottom-center)

### Transcription Only

```bash
python scripts/transcribe_audio.py \
  --audio <audio_file> \
  --output <output_json> \
  [--model <model_name>] \
  [--language zh]
```

## Output Files

When you run the composition script, it generates:

1. **whisper_transcription.json**: Raw Whisper output with timestamps
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
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [SRT Subtitle Format](https://en.wikipedia.org/wiki/SubRip)

## License

MIT License - See LICENSE file for details
