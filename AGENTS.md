# AGENTS.md - AI 智能体代码库指南

本仓库包含用于音频、图像和视频处理任务的 Python 技能。

## 构建与测试命令

**无正式测试框架** - 使用示例数据手动测试。

### 代码检查
```bash
uv run ruff check .           # 检查代码
uv run ruff check --fix .     # 自动修复问题
```

### 运行脚本
每个脚本都是独立的 CLI 工具，支持 `--help` 参数：
```bash
uv run python .claude/skills/video-composer/scripts/compose_video.py --help
uv run python create/music-create/scripts/parse_lyrics.py --help
uv run python .claude/skills/image-generator/scripts/generate_image.py --help
```

## 代码风格指南

### 文件结构
- 可执行脚本使用 `#!/usr/bin/env python3` shebang
- 脚本放置在 `scripts/` 子目录中，工具类放在 `scripts/utils/` 中，并包含 `__init__.py`
- 每个技能都有 `SKILL.md` 文件，包含 YAML 前置元数据

### 导入顺序
```python
# 标准库，然后是第三方库，最后是本地模块
import argparse
import json
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv
from utils.ffmpeg_wrapper import FFmpegWrapper
```

### 类型注解
**强制要求**所有函数参数和返回值使用类型注解：
```python
def process_data(items: List[Dict[str, Any]]) -> Dict[str, str]:
    """处理数据并返回格式化结果。"""
    ...
```

### 命名规范
- 类名：`PascalCase`（例如：`LyricsParser`）
- 函数/方法：`snake_case`（例如：`parse_lyrics`）
- 常量：`UPPER_SNAKE_CASE`（例如：`SECTION_PATTERN`）
- 私有方法：`_leading_underscore`（例如：`_load_model`）

### 文档字符串
所有模块、类和公共方法都需要**完整的文档字符串**：
```python
class ClassName:
    """简要描述。"""

    def method_name(self, param: str) -> int:
        """简要描述。

        Args:
            param: 参数描述

        Returns:
            返回值描述

        Raises:
            ValueError: 当输入无效时抛出
        """
        ...
```

### 文件 I/O
- **始终使用 pathlib 的 `Path`** 来处理文件路径
- **指定编码**：文件操作使用 `encoding='utf-8'`
- **创建目录**：`Path(...).mkdir(parents=True, exist_ok=True)`

```python
def read_file(filepath: Path) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath: Path, content: str) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
```

### CLI 脚本
- 使用 `argparse` 并为路径参数指定 `type=Path`
- 包含清晰的 `--help` 描述
```python
def main():
    parser = argparse.ArgumentParser(description="描述")
    parser.add_argument("--input", type=Path, required=True, help="输入文件")
    args = parser.parse_args()
if __name__ == "__main__":
    main()
```

### 错误处理
- 使用描述性错误消息和适当的异常类型
```python
def process_file(filepath: Path) -> Dict[str, Any]:
    if not filepath.exists():
        raise FileNotFoundError(f"文件未找到: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"{filepath} 中的 JSON 无效: {e}")
    return data
```

### 类结构
- 使用 `__init__` 进行所有初始化
- 延迟加载重型资源（模型、API）
```python
class Processor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.resource = None  # 延迟加载
```

### SKILL.md 格式
```yaml
---
name: skill-name
description: 简要描述
license: MIT
metadata:
  author: YourName
  version: "1.0.0"
  category: category-name
  tags: tag1, tag2, tag3
---
# Skill 名称
详细文档...
```

### 中文语言支持
- **始终**为文件操作指定 `encoding='utf-8'`
- 字幕使用带 BOM 的 UTF-8：`encoding='utf-8-sig'`

### 依赖管理
- 项目使用 uv 统一管理 Python 依赖
- 每个技能都有自己的 `scripts/requirements.txt`
- 使用 `>=` 符号指定最低版本，并包含注释

### 环境变量
- 使用 `.env` 文件存储 API 密钥，使用 `python-dotenv` 加载
- 包含 `.env.example`，并将 `.env` 添加到 `.gitignore`

### 特殊注意事项
- **视频/音频**：使用 FFmpeg，使用前检查可用性
- **异步操作**：使用轮询模式，提供进度更新，实现超时
- **API 集成**：优雅地处理错误，提供重试逻辑，验证响应

## Skill 规范
- `.claude/skills` 是当前项目支持的所有技能，你应该加载它们的元数据用于判断是否需要使用某个 skill
- 修改对应 skill 的内容后，需要判断是否需要更新 SKILL.md 文档

## 全局规范
- 输出语言必须为中文
