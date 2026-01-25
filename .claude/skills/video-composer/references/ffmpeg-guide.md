# FFmpeg Usage Guide

## Overview

FFmpeg is a complete, cross-platform solution for recording, converting, and streaming audio and video.

## Installation

### Windows
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

### macOS
```bash
brew install ffmpeg
```

### Linux
```bash
sudo apt install ffmpeg  # Debian/Ubuntu
sudo yum install ffmpeg  # CentOS/RHEL
```

## Basic Video Composition

### Concatenate Images with Audio

```bash
ffmpeg -loop 1 -t 10 -i image1.png \
       -loop 1 -t 15 -i image2.png \
       -i audio.mp3 \
       -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[outv]" \
       -map "[outv]" -map 2:a \
       -c:v libx264 -c:a aac -shortest \
       output.mp4
```

### Add Fade Transitions

```bash
ffmpeg -loop 1 -t 10 -i image1.png \
       -loop 1 -t 10 -i image2.png \
       -filter_complex \
       "[0:v]fade=t=out:st=9:d=1[v0]; \
        [1:v]fade=t=in:st=0:d=1[v1]; \
        [v0][v1]concat=n=2:v=1:a=0[outv]" \
       -map "[outv]" \
       output.mp4
```

### Burn Subtitles

```bash
ffmpeg -i video.mp4 \
       -vf "subtitles=subtitles.srt:force_style='FontName=Arial,FontSize=24'" \
       output.mp4
```

## Filter Complex Syntax

### Fade Filter
```
fade=t=in:st=0:d=1        # Fade in at start for 1 second
fade=t=out:st=9:d=1       # Fade out at 9s for 1 second
```

### Concat Filter
```
[v0][v1][v2]concat=n=3:v=1:a=0[outv]
# n=3: number of segments
# v=1: one video stream
# a=0: no audio streams
```

### Subtitles Filter
```
subtitles=file.srt:force_style='FontName=Arial,FontSize=24,PrimaryColour=&HFFFFFF'
```

## Encoding Options

### Video Codec (H.264)
```bash
-c:v libx264              # Use H.264 codec
-pix_fmt yuv420p          # Pixel format (maximum compatibility)
-crf 23                   # Quality (0-51, lower is better, 23 is default)
-preset medium            # Encoding speed (ultrafast to veryslow)
```

### Audio Codec (AAC)
```bash
-c:a aac                  # Use AAC codec
-b:a 192k                 # Audio bitrate
-ar 44100                 # Sample rate
```

## Common Options

```bash
-y                        # Overwrite output file without asking
-i input.mp4              # Input file
-t 10                     # Duration (10 seconds)
-ss 5                     # Start time (5 seconds)
-loop 1                   # Loop input (for images)
-shortest                 # Finish when shortest input ends
-map                      # Select streams to include
```

## Subtitle Styling

### Force Style Options
```
FontName=Arial            # Font family
FontSize=24               # Font size
PrimaryColour=&HFFFFFF    # White text (BGR format)
OutlineColour=&H000000    # Black outline
BorderStyle=3             # Opaque box background
Outline=2                 # Outline thickness
Shadow=1                  # Shadow depth
MarginV=50                # Vertical margin from bottom
```

## Performance Tips

1. **Hardware Acceleration**: Use `-hwaccel` for GPU encoding
2. **Preset Selection**: Use faster presets for quicker encoding
3. **Two-Pass Encoding**: Better quality for same file size
4. **Resolution**: Scale down if needed with `-vf scale=1280:720`

## Troubleshooting

### "Unknown encoder 'libx264'"
- Install FFmpeg with libx264 support
- Use `-c:v h264` instead

### Subtitles Not Showing
- Check SRT file encoding (use UTF-8)
- Verify subtitle timing
- Check font availability

### Audio/Video Out of Sync
- Use `-async 1` to fix sync issues
- Check input file integrity

## References

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [FFmpeg Wiki](https://trac.ffmpeg.org/wiki)
- [Filter Documentation](https://ffmpeg.org/ffmpeg-filters.html)
