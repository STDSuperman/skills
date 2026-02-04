# SRT Subtitle Format Specification

## Overview

SubRip (SRT) is a simple subtitle format that consists of four parts for each subtitle:

1. A numeric counter (starting at 1)
2. Start and end timestamps
3. Subtitle text
4. A blank line

## Format Structure

```
1
00:00:00,000 --> 00:00:05,000
First subtitle text

2
00:00:05,000 --> 00:00:10,000
Second subtitle text
Can span multiple lines

3
00:00:10,000 --> 00:00:15,000
Third subtitle
```

## Timestamp Format

```
HH:MM:SS,mmm --> HH:MM:SS,mmm
```

- `HH`: Hours (00-99)
- `MM`: Minutes (00-59)
- `SS`: Seconds (00-59)
- `mmm`: Milliseconds (000-999)

Note: Use comma (,) for milliseconds, not period (.)

## Examples

### Basic Example

```srt
1
00:00:00,000 --> 00:00:02,500
Hello, world!

2
00:00:02,500 --> 00:00:05,000
This is a subtitle.
```

### Multi-line Subtitle

```srt
1
00:00:00,000 --> 00:00:05,000
This is the first line
This is the second line
This is the third line
```

### Chinese Subtitles

```srt
1
00:00:00,000 --> 00:00:05,000
你好，世界！

2
00:00:05,000 --> 00:00:10,000
这是一个字幕。
```

## Encoding

### UTF-8 (Recommended)
- Use UTF-8 encoding for international characters
- Add BOM (Byte Order Mark) for better compatibility
- Python: `open(file, 'w', encoding='utf-8-sig')`

### Common Issues
- **Chinese characters not displaying**: Use UTF-8 with BOM
- **Special characters broken**: Check file encoding
- **Timing issues**: Verify timestamp format (comma for milliseconds)

## Styling (FFmpeg)

SRT files don't include styling, but FFmpeg can apply styles when burning subtitles:

```bash
ffmpeg -i video.mp4 \
  -vf "subtitles=subtitles.srt:force_style='FontName=Arial,FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=3,Outline=2,Shadow=1,MarginV=50'" \
  output.mp4
```

### Style Options

| Option | Description | Example |
|--------|-------------|---------|
| FontName | Font family | Arial, SimHei |
| FontSize | Font size in pixels | 24 |
| PrimaryColour | Text color (BGR) | &HFFFFFF (white) |
| OutlineColour | Outline color (BGR) | &H000000 (black) |
| BorderStyle | Border type | 1=outline, 3=box |
| Outline | Outline thickness | 2 |
| Shadow | Shadow depth | 1 |
| MarginV | Vertical margin | 50 |
| MarginL | Left margin | 20 |
| MarginR | Right margin | 20 |

### Color Format (BGR)

Colors are in BGR format with alpha channel:
- `&HFFFFFF` = White
- `&H000000` = Black
- `&HFF0000` = Blue
- `&H00FF00` = Green
- `&H0000FF` = Red

## Best Practices

1. **Timing**: Leave 0.5-1 second gaps between subtitles
2. **Length**: Keep subtitles under 2 lines when possible
3. **Duration**: Minimum 1 second, maximum 7 seconds per subtitle
4. **Reading Speed**: ~15-20 characters per second
5. **Encoding**: Always use UTF-8 with BOM for Chinese
6. **Line Breaks**: Use natural breaks in sentences

## Validation

### Check Format
```python
import re

def validate_srt_timestamp(timestamp):
    pattern = r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$'
    return bool(re.match(pattern, timestamp))

# Valid
validate_srt_timestamp("00:00:00,000 --> 00:00:05,000")  # True

# Invalid
validate_srt_timestamp("00:00:00.000 --> 00:00:05.000")  # False (period instead of comma)
```

## Tools

### Subtitle Editors
- Aegisub (advanced)
- Subtitle Edit (Windows)
- Jubler (cross-platform)

### Validation
- [Subtitle Validator](https://subtitletools.com/subtitle-validator)
- FFmpeg (will report errors when loading)

## References

- [SubRip Wikipedia](https://en.wikipedia.org/wiki/SubRip)
- [SRT Format Specification](https://www.matroska.org/technical/subtitles.html)
- [FFmpeg Subtitles](https://trac.ffmpeg.org/wiki/HowToBurnSubtitlesIntoVideo)
