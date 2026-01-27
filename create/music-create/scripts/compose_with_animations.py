#!/usr/bin/env python3
"""
Simple Video Composer
Composes MP4 videos from images, audio, and subtitles with keyframe animations.
"""

import subprocess
from pathlib import Path
import json


def get_audio_duration(audio_path: Path) -> float:
    """Get audio duration using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "csv=p=0",
                str(audio_path),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return float(result.stdout.strip())
    except:
        return 0.0


def build_ffmpeg_command(
    images_dir: Path,
    audio_path: Path,
    subtitle_path: Path,
    output_path: Path,
    metadata: dict,
):
    """Build FFmpeg command with keyframe animations and fade transitions."""
    sections = metadata.get("sections", [])

    cmd = ["ffmpeg", "-y"]

    # Add image inputs
    for section in sections:
        image_path = images_dir / section["image_path"]
        duration = section["duration"]
        cmd.extend([
            "-loop", "1",
            "-t", str(duration),
            "-i", str(image_path),
        ])

    # Add audio input
    cmd.extend(["-i", str(audio_path)])

    # Build filter complex
    filters = []
    fade_duration = 1.0
    zoom_factor = 1.1

    # Apply zoom and fade to each image (加移动）
    for i, section in enumerate(sections):
        duration = section["duration"]

        # Determine movement direction: odd index (1,3,5...) = down, even index (0,2,4...) = up
        # 用户要求：奇数向下移动，偶数向上移动
        if i % 2 == 0:
            # Even index (0, 2, 4...) - move UP
            y_start = 100
            y_end = -100
        else:
            # Odd index (1, 3, 5...) - move DOWN
            y_start = -100
            y_end = 100

        # Fade transitions
        if i == 0:
            if duration > fade_duration:
                fade_filter = f"fade=t=out:st={duration - fade_duration}:d={fade_duration}"
            else:
                fade_filter = "copy"
        elif i == len(sections) - 1:
            fade_filter = f"fade=t=in:st=0:d={fade_duration}"
        else:
            if duration > 2 * fade_duration:
                fade_filter = (
                    f"fade=t=in:st=0:d={fade_duration},"
                    f"fade=t=out:st={duration - fade_duration}:d={fade_duration}"
                )
            elif duration > fade_duration:
                fade_filter = f"fade=t=in:st=0:d={duration / 2}"
            else:
                fade_filter = "copy"

        # Build filter: scale -> pad -> crop -> fade (实现移动）
        # 先放大大图，然后扩展画布，最后裁剪实现移动
        if fade_filter == "copy":
            # scale -> pad -> crop (no fade)
            filter_expr = (
                f"[{i}:v]scale=iw*{zoom_factor}:-2,"
                f"pad=iw:ih+200:0:100,"
                f"crop=iw:ih:0:100+(({y_end}-{y_start})*t/{duration})[v{i}]"
            )
            filters.append(filter_expr)
        else:
            # scale -> pad -> fade -> crop
            filter_expr = (
                f"[{i}:v]scale=iw*{zoom_factor}:-2,"
                f"pad=iw:ih+200:0:100,{fade_filter},"
                f"crop=iw:ih:0:100+(({y_end}-{y_start})*t/{duration})[v{i}]"
            )
            filters.append(filter_expr)

    # Concatenate all video streams
    concat_inputs = "".join([f"[v{i}]" for i in range(len(sections))])
    filters.append(f"{concat_inputs}concat=n={len(sections)}:v=1:a=0[outv]")

    # Add subtitles (no background)
    subtitle_path_escaped = str(subtitle_path).replace("\\", "\\\\").replace(":", "\\:")
    filters.append(
        f"[outv]subtitles='{subtitle_path_escaped}':force_style='"
        f"FontName=Microsoft YaHei,FontSize=24,"
        f"PrimaryColour=&HFFFFFF,OutlineColour=&H000000,"
        f"BorderStyle=1,Outline=2,MarginV=50'[outv_sub]"
    )

    filter_complex = ";".join(filters)

    # Add filter complex to command
    cmd.extend(["-filter_complex", filter_complex])

    # Map outputs
    cmd.extend([
        "-map", "[outv_sub]",
        "-map", f"{len(sections)}:a",  # Audio is the last input
        "-c:v", "libx264",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-t", str(get_audio_duration(audio_path)),
        str(output_path),
    ])

    return cmd


def main():
    # Paths
    images_dir = Path("output/images")
    audio_path = Path("output/audio.mp3")
    subtitle_path = Path("output/subtitles.srt")
    output_path = Path("output/station_final.mp4")
    metadata_path = Path("output/images/metadata.json")

    # Load metadata
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Calculate section durations based on audio
    total_duration = get_audio_duration(audio_path)
    sections = metadata["sections"]

    # Distribute time evenly among sections
    section_duration = total_duration / len(sections)
    for section in sections:
        section["duration"] = section_duration

    print(f"Total audio duration: {total_duration:.2f}s")
    print(f"Number of sections: {len(sections)}")
    print(f"Duration per section: {section_duration:.2f}s")

    # Build and execute FFmpeg command
    cmd = build_ffmpeg_command(
        images_dir, audio_path, subtitle_path, output_path, metadata
    )

    print("\nExecuting FFmpeg command...")
    print(f"Output: {output_path}")

    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

    if result.returncode == 0:
        print("\n[SUCCESS] Video composition complete!")
        print(f"Output: {output_path}")
    else:
        print("\n[ERROR] Video composition failed!")
        print(f"Error: {result.stderr}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
