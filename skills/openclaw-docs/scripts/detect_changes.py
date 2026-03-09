#!/usr/bin/env python3
"""
文档变更检测器
检测原始文档文件的新增、修改、删除
"""

import hashlib
from pathlib import Path
from typing import Dict, List, Set


def calculate_file_hash(file_path: Path) -> str:
    """
    计算文件的 SHA256 哈希

    Args:
        file_path: 文件路径

    Returns:
        SHA256 哈希值
    """
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_current_source_files(docs_structure: Dict, docs_dir: Path) -> Dict[str, Dict]:
    """
    获取当前所有源文件及其元数据

    Args:
        docs_structure: parse_docs_json 返回的结构（只包含英文文档）
        docs_dir: docs 目录路径

    Returns:
        {
            "docs/index.mdx": {
                "file_hash": "abc123...",
                "mtime": 1234567890.0,
                "relative_path": "docs/index.mdx"
            },
            ...
        }
    """
    current_files = {}

    # 遍历 docs_structure（已过滤为英文文档）
    for tab_name, tab_data in docs_structure.items():
        for group in tab_data['groups']:
            for page in group['pages']:
                # 尝试找到文件
                for ext in ['.mdx', '.md']:
                    file_path = docs_dir / f"{page}{ext}"
                    if file_path.exists():
                        relative_path = str(file_path.relative_to(docs_dir.parent))
                        current_files[relative_path] = {
                            'file_hash': calculate_file_hash(file_path),
                            'mtime': file_path.stat().st_mtime,
                            'relative_path': relative_path
                        }
                        break

    return current_files


def detect_source_file_changes(
    docs_structure: Dict,
    docs_dir: Path,
    source_cache: Dict
) -> Dict[str, List[str]]:
    """
    检测原始文件的变更

    Args:
        docs_structure: parse_docs_json 返回的结构（只包含英文文档）
        docs_dir: docs 目录路径
        source_cache: 源文件缓存

    Returns:
        {
            "added": ["docs/new.mdx", ...],
            "modified": ["docs/changed.mdx", ...],
            "deleted": ["docs/removed.mdx", ...],
            "unchanged": ["docs/same.mdx", ...]
        }
    """
    current_files = get_current_source_files(docs_structure, docs_dir)
    cached_files = source_cache.get('source_files', {})

    added = []
    modified = []
    deleted = []
    unchanged = []

    # 检查新增和修改
    for file_path, file_info in current_files.items():
        if file_path not in cached_files:
            # 新增文件
            added.append(file_path)
        elif file_info['file_hash'] != cached_files[file_path].get('file_hash'):
            # 文件已修改
            modified.append(file_path)
        else:
            # 文件未变更
            unchanged.append(file_path)

    # 检查删除
    for file_path in cached_files:
        if file_path not in current_files:
            deleted.append(file_path)

    return {
        'added': added,
        'modified': modified,
        'deleted': deleted,
        'unchanged': unchanged
    }


def find_affected_merged_docs(
    changes: Dict[str, List[str]],
    merge_cache: Dict
) -> Set[str]:
    """
    找出受影响的合并文档

    Args:
        changes: detect_source_file_changes 返回的变更
        merge_cache: 合并缓存

    Returns:
        受影响的合并文档文件名集合
    """
    affected = set()
    changed_files = changes['added'] + changes['modified'] + changes['deleted']

    if not changed_files:
        return affected

    # 遍历所有合并文档
    for merged_filename, doc_info in merge_cache.get('merged_docs', {}).items():
        source_files = doc_info.get('source_files', [])

        # 检查是否有任何变更的文件在这个合并文档中
        for changed_file in changed_files:
            if changed_file in source_files:
                affected.add(merged_filename)
                break

    return affected


if __name__ == '__main__':
    import json
    import sys
    from pathlib import Path

    # 设置 UTF-8 输出
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    SCRIPT_DIR = Path(__file__).parent
    SKILL_DIR = SCRIPT_DIR.parent

    sys.path.append(str(SCRIPT_DIR))
    from parse_docs import parse_docs_json

    # 加载配置
    config_file = SKILL_DIR / 'references' / 'config.json'
    with open(config_file) as f:
        config = json.load(f)

    repo_path = SKILL_DIR / config['repo_path']
    docs_json = repo_path / 'docs' / 'docs.json'
    docs_dir = repo_path / 'docs'

    # 解析文档结构
    print("正在解析文档结构...")
    structure = parse_docs_json(docs_json)

    # 加载源文件缓存
    source_cache_file = SKILL_DIR / 'cache' / 'source_cache.json'
    if source_cache_file.exists():
        with open(source_cache_file) as f:
            source_cache = json.load(f)
    else:
        source_cache = {}

    # 检测变更
    print("正在检测文件变更...")
    changes = detect_source_file_changes(structure, docs_dir, source_cache)

    print(f"\n变更检测结果:")
    print(f"  新增: {len(changes['added'])} 个文件")
    for f in changes['added']:
        print(f"    + {f}")

    print(f"  修改: {len(changes['modified'])} 个文件")
    for f in changes['modified']:
        print(f"    ~ {f}")

    print(f"  删除: {len(changes['deleted'])} 个文件")
    for f in changes['deleted']:
        print(f"    - {f}")

    print(f"  未变更: {len(changes['unchanged'])} 个文件")

    # 加载合并缓存
    merge_cache_file = SKILL_DIR / 'cache' / 'merge_cache.json'
    if merge_cache_file.exists():
        with open(merge_cache_file) as f:
            merge_cache = json.load(f)
    else:
        merge_cache = {}

    # 找出受影响的合并文档
    affected = find_affected_merged_docs(changes, merge_cache)
    print(f"\n受影响的合并文档: {len(affected)} 个")
    for filename in affected:
        print(f"  - {filename}")
