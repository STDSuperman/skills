# Suno Lyrics Illustration & Video Composition Workflow

Complete workflow for generating anime-style illustrations from Suno lyrics and composing music videos with automatic transcription-based timing.

## Overview

This workflow consists of two main phases:

1. **Phase 1**: Lyrics parsing and illustration generation
2. **Phase 2**: Video composition with Whisper transcription

## Phase 1: Lyrics Parsing & Illustration Generation

### Step 1: Parse Lyrics

Parse Suno lyrics markdown file to extract sections and generate illustration prompts.

```bash
cd create/music-create
python scripts/parse_lyrics.py "站台-Suno生成参数.md" --output output/parsed_lyrics.json
```

**Output**: `output/parsed_lyrics.json` with sections and prompts

### Step 2: Generate Illustrations

Generate anime-style illustrations for each lyric section.

```bash
python scripts/generate_illustrations.py output/parsed_lyrics.json --output-dir output/illustrations
```

**Output**:
- `output/illustrations/*.png` - Section images
- `output/illustrations/metadata.json` - Image metadata

### Step 3: Review Images

Manually review the generated illustrations before proceeding to video composition.

## Phase 2: Video Composition

### Prerequisites

1. **Install FFmpeg**:
   ```bash
   # Windows (Chocolatey)
   choco install ffmpeg

   # macOS
   brew install ffmpeg

   # Linux
   sudo apt install ffmpeg
   ```

2. **Install Python Dependencies**:
   ```bash
   cd .claude/skills/video-composer
   pip install -r scripts/requirements.txt
   ```

### Compose Video

Automatically transcribe audio, match with lyrics, and compose video:

```bash
cd .claude/skills/video-composer
python scripts/compose_video.py \
  --audio ../../create/music-create/output/result-music.mp3 \
  --lyrics ../../create/music-create/站台-Suno生成参数.md \
  --images ../../create/music-create/output/illustrations \
  --output ../../create/music-create/output/站台-music-video.mp4
```

**Process**:
1. Transcribes audio with Whisper (word-level timestamps)
2. Matches transcription with original lyrics sections
3. Generates timestamped metadata
4. Creates SRT subtitle file
5. Composes video with FFmpeg (images + audio + subtitles)

**Output**:
- `whisper_transcription.json` - Raw Whisper output
- `timestamped_metadata.json` - Matched sections with timestamps
- `subtitles.srt` - SRT subtitle file
- `站台-music-video.mp4` - Final video

## Directory Structure

```
create/music-create/
├── scripts/
│   ├── parse_lyrics.py              # Lyrics parser
│   └── generate_illustrations.py   # Illustration generator
├── output/
│   ├── parsed_lyrics.json           # Parsed lyrics data
│   ├── illustrations/               # Generated images
│   │   ├── intro.png
│   │   ├── verse_1.png
│   │   ├── pre-chorus.png
│   │   ├── chorus.png
│   │   ├── verse_2.png
│   │   ├── bridge.png
│   │   ├── chorus_2.png
│   │   ├── outro.png
│   │   └── metadata.json
│   └── result-music.mp3             # Audio file
└── 站台-Suno生成参数.md              # Source lyrics

.claude/skills/video-composer/
├── SKILL.md                         # Skill documentation
├── .env.example                     # Environment template
├── scripts/
│   ├── compose_video.py             # Main composition script
│   ├── transcribe_audio.py          # Whisper transcription
│   ├── requirements.txt             # Python dependencies
│   └── utils/
│       ├── whisper_processor.py     # Whisper wrapper
│       ├── lyrics_matcher.py        # Lyrics matching
│       ├── subtitle_generator.py    # SRT generation
│       └── ffmpeg_wrapper.py        # FFmpeg wrapper
└── references/
    ├── whisper-guide.md             # Whisper reference
    ├── ffmpeg-guide.md              # FFmpeg reference
    └── subtitle-format.md           # SRT reference
```

## Features

### Lyrics Parser
- Extracts section tags: [Intro], [Verse], [Pre-Chorus], [Chorus], [Bridge], [Outro]
- Filters production hints: [Piano with subtle strings], [Emotional build]
- Generates contextual anime-style prompts for each section
- Handles multiple occurrences of same section (e.g., Chorus appears twice)

### Illustration Generator
- Calls image-generator skill with anime style
- Generates consistent visual style across all sections
- Creates metadata JSON with section info and image paths

### Video Composer
- **Whisper Transcription**: Automatic audio transcription with word-level timestamps
- **Lyrics Matching**: Fuzzy matching between transcription and original lyrics
- **Accurate Timing**: Each image displays for actual song section duration
- **Fade Transitions**: 1-second crossfade between images
- **Subtitle Burning**: Chinese subtitles with custom styling
- **Audio Sync**: Perfect synchronization between images, subtitles, and audio

## Whisper Models

| Model  | Size | Speed | Accuracy | Use Case |
|--------|------|-------|----------|----------|
| tiny   | 39M  | Fast  | Low      | Quick tests |
| base   | 74M  | Fast  | Good     | **Recommended** |
| small  | 244M | Medium| Better   | Higher accuracy |
| medium | 769M | Slow  | High     | Professional |
| large  | 1550M| Very Slow | Highest | Maximum accuracy |

Default: `base` (good balance of speed and accuracy)

## Customization

### Change Whisper Model

```bash
python scripts/compose_video.py \
  --whisper-model medium \
  ...
```

### Custom Working Directory

```bash
python scripts/compose_video.py \
  --work-dir /path/to/workdir \
  ...
```

## Troubleshooting

### FFmpeg Not Found
```
Error: FFmpeg not found. Please install FFmpeg and add to PATH.
```
**Solution**: Install FFmpeg and ensure it's in system PATH

### Whisper Model Download
First run will download the selected model:
- tiny: ~39 MB
- base: ~74 MB
- small: ~244 MB
- medium: ~769 MB
- large: ~1550 MB

### Chinese Characters in Subtitles
Subtitles use UTF-8 encoding with BOM for proper Chinese character display.

### GPU/CUDA Issues
If CUDA is not available, Whisper will automatically fall back to CPU mode (slower but works).

## Technical Details

### Video Encoding
- Video Codec: H.264 (libx264)
- Audio Codec: AAC
- Pixel Format: yuv420p (maximum compatibility)
- Frame Rate: 25 fps
- Audio Sample Rate: 44100 Hz

### Subtitle Styling
- Font: Arial, size 24
- Color: White with black outline
- Background: Semi-transparent black box
- Position: Bottom center
- Encoding: UTF-8 with BOM

### Transition Settings
- Duration: 1 second
- Type: Crossfade between images
- Timing: Last 1s of each image fades to next

## License

MIT License
