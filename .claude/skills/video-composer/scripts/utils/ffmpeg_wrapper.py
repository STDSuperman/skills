"""
FFmpeg Wrapper
Builds and executes FFmpeg commands for video composition.
"""

import subprocess
from pathlib import Path
from typing import List, Dict, Any


class FFmpegWrapper:
    """Wrapper for FFmpeg video composition commands."""

    def __init__(
        self,
        metadata: Dict[str, Any],
        audio_path: Path,
        subtitle_path: Path,
        output_path: Path,
    ):
        """
        Initialize FFmpeg wrapper.

        Args:
            metadata: Timestamped metadata with sections
            audio_path: Path to audio file
            subtitle_path: Path to SRT subtitle file
            output_path: Path for output video
        """
        self.metadata = metadata
        self.audio_path = audio_path
        self.subtitle_path = subtitle_path
        self.output_path = output_path
        self.sections = metadata.get("sections", [])
        # Get actual audio duration from file
        self.total_duration = self._get_audio_duration()

    def _get_audio_duration(self) -> float:
        """Get actual audio duration using ffprobe."""
        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "csv=p=0",
                    str(self.audio_path),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            return float(result.stdout.strip())
        except:
            return 0.0

    def build_command(self) -> List[str]:
        """
        Build FFmpeg command for video composition.

        Returns:
            List of command arguments
        """
        cmd = ["ffmpeg", "-y"]  # -y to overwrite output file

        # Add image inputs with loop and duration
        for section in self.sections:
            if section.get("image_path"):
                cmd.extend(
                    [
                        "-loop",
                        "1",
                        "-t",
                        str(section["duration"]),
                        "-i",
                        section["image_path"],
                    ]
                )

        # Add audio input
        cmd.extend(["-i", str(self.audio_path)])

        # Build filter complex for fades and concatenation
        filter_complex = self._build_filter_complex()
        cmd.extend(["-filter_complex", filter_complex])

        # Map output video and audio
        cmd.extend(
            [
                "-map",
                "[outv_sub]",
                "-map",
                f"{len(self.sections)}:a",  # Audio is the last input
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                "-pix_fmt",
                "yuv420p",
                "-t",
                str(self.total_duration),
                str(self.output_path),
            ]
        )

        return cmd

    def _build_filter_complex(self) -> str:
        """Build filter_complex string for fades, keyframes, concatenation, and subtitles."""
        filters = []
        fade_duration = 1.0
        zoom_factor = 1.1
        move_range = 50

        for i, section in enumerate(self.sections):
            if not section.get("image_path"):
                continue

            duration = section["duration"]

            if i == 0:
                if duration > fade_duration:
                    fade_filter = (
                        f"fade=t=out:st={duration - fade_duration}:d={fade_duration}"
                    )
                else:
                    fade_filter = "copy"
            elif i == len(self.sections) - 1:
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

            if fade_filter == "copy":
                filters.append(f"[{i}:v]scale=iw*{zoom_factor}:-2[v{i}]")
            else:
                filters.append(f"[{i}:v]scale=iw*{zoom_factor}:-2,{fade_filter}[v{i}]")

        concat_inputs = "".join(f"[v{i}]" for i in range(len(self.sections)))
        filters.append(f"{concat_inputs}concat=n={len(self.sections)}:v=1:a=0[outv]")

        subtitle_path_escaped = (
            str(self.subtitle_path).replace("\\", "\\\\").replace(":", "\\:")
        )
        filters.append(
            f"[outv]subtitles='{subtitle_path_escaped}':force_style='FontName=Arial,FontSize=24,"
            f"PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=3,Outline=2,Shadow=1,"
            f"MarginV=50'[outv_sub]"
        )

        return ";".join(filters)

    def execute(self):
        """Execute FFmpeg command."""
        cmd = self.build_command()

        print("Building video with FFmpeg...")
        print(f"Output: {self.output_path}")

        try:
            result = subprocess.run(
                cmd, check=True, capture_output=True, text=True, encoding="utf-8"
            )

            print("Video composition complete!")
            return True

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e.stderr}")
            return False

    def check_ffmpeg(self) -> bool:
        """Check if FFmpeg is available."""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"], capture_output=True, text=True, encoding="utf-8"
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
