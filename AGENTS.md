# AGENTS.md - Repository Guidelines for AI Agents

This repository contains Python skills for audio, image, and video processing tasks.

## Build & Test Commands

**No formal test framework** - manual testing with sample data.

### Linting
```bash
ruff check .           # Check code
ruff check --fix .     # Auto-fix issues
```

### Running Scripts
Each script is a standalone CLI tool with `--help`:
```bash
python .claude/skills/video-composer/scripts/compose_video.py --help
python create/music-create/scripts/parse_lyrics.py --help
python .claude/skills/image-generator/scripts/generate_image.py --help
```

## Code Style Guidelines

### File Structure
- Use `#!/usr/bin/env python3` shebang for executable scripts
- Place scripts in `scripts/` subdirectories, utilities in `scripts/utils/` with `__init__.py`
- Each skill has `SKILL.md` with YAML frontmatter

### Imports
```python
# Standard library, then third-party, then local
import argparse
import json
from pathlib import Path
from typing import Dict, Any, List
import whisper
from dotenv import load_dotenv
from utils.ffmpeg_wrapper import FFmpegWrapper
```

### Type Hints
**Mandatory** for all function parameters and return values:
```python
def process_data(items: List[Dict[str, Any]]) -> Dict[str, str]:
    """Process data and return formatted result."""
    ...
```

### Naming Conventions
- Classes: `PascalCase` (e.g., `LyricsParser`)
- Functions/Methods: `snake_case` (e.g., `parse_lyrics`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `SECTION_PATTERN`)
- Private methods: `_leading_underscore` (e.g., `_load_model`)

### Docstrings
**Comprehensive docstrings** for all modules, classes, and public methods:
```python
class ClassName:
    """Brief description."""

    def method_name(self, param: str) -> int:
        """Brief description.

        Args:
            param: Description

        Returns:
            Description

        Raises:
            ValueError: When invalid input
        """
        ...
```

### File I/O
- **Always use `Path` from pathlib** for file paths
- **Specify encoding**: `encoding='utf-8'` for file operations
- **Create directories**: `Path(...).mkdir(parents=True, exist_ok=True)`

```python
def read_file(filepath: Path) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath: Path, content: str) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
```

### CLI Scripts
- Use `argparse` with `type=Path` for path arguments
- Include `--help` with clear descriptions
```python
def main():
    parser = argparse.ArgumentParser(description="Description")
    parser.add_argument("--input", type=Path, required=True, help="Input file")
    args = parser.parse_args()
if __name__ == "__main__":
    main()
```

### Error Handling
- Use descriptive error messages and appropriate exception types
```python
def process_file(filepath: Path) -> Dict[str, Any]:
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {filepath}: {e}")
    return data
```

### Class Structure
- Use `__init__` for all initialization
- Lazy-load heavy resources (models, APIs)
```python
class Processor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.resource = None  # Lazy-loaded
```

### SKILL.md Format
```yaml
---
name: skill-name
description: Brief description
license: MIT
metadata:
  author: YourName
  version: "1.0.0"
  category: category-name
  tags: tag1, tag2, tag3
---
# Skill Name
Detailed documentation...
```

### Chinese Language Support
- **Always** specify `encoding='utf-8'` for file operations
- Use UTF-8 with BOM for subtitles: `encoding='utf-8-sig'`

### Requirements Management
- Each skill has its own `scripts/requirements.txt`
- Pin minimum versions with `>=` notation, include comments

### Environment Variables
- Use `.env` files for API keys, `python-dotenv` to load
- Include `.env.example`, add `.env` to `.gitignore`

### Special Considerations
- **Video/Audio**: Use FFmpeg, check availability before use
- **Async Operations**: Use polling patterns, provide progress updates, implement timeouts
- **API Integration**: Handle errors gracefully, provide retry logic, validate responses


## 规范
- 输出语言必须为中文