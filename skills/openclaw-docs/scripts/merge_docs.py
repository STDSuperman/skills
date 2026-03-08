#!/usr/bin/env python3
"""
文档合并器
根据智能策略合并文档
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent


def sanitize_filename(name: str) -> str:
    """
    清理文件名，替换特殊字符

    Args:
        name: 原始名称

    Returns:
        清理后的文件名
    """
    # 替换空格为下划线
    name = name.replace(' ', '_')
    # 移除其他特殊字符
    name = ''.join(c for c in name if c.isalnum() or c in ('_', '-'))
    return name


def decide_merge_strategy(tab_name: str, groups: List[Dict], threshold: int = 5) -> Tuple[str, List[Dict]]:
    """
    决定合并策略

    Args:
        tab_name: Tab 名称
        groups: Group 列表
        threshold: Group 数量阈值

    Returns:
        (策略类型, 合并规格列表)
        策略类型: "tab" 或 "group"
        合并规格: [{"name": "文件名", "groups": [...]}, ...]
    """
    if len(groups) <= threshold:
        # 整个 Tab 合并为一个文件
        return "tab", [{
            "name": sanitize_filename(tab_name),
            "groups": groups
        }]
    else:
        # 每个 Group 单独合并
        return "group", [
            {
                "name": sanitize_filename(f"{tab_name}_{g['group']}"),
                "groups": [g]
            }
            for g in groups
        ]


def merge_documents(merge_spec: Dict, docs_dir: Path) -> str:
    """
    合并文档

    Args:
        merge_spec: {"name": "Get_started", "groups": [...]}
        docs_dir: docs 目录路径

    Returns:
        合并后的 Markdown 内容
    """
    content = f"# {merge_spec['name'].replace('_', ' ')}\n\n"

    for group in merge_spec['groups']:
        content += f"## {group['group']}\n\n"

        for page in group['pages']:
            # 尝试找到文件
            file_path = None
            for ext in ['.mdx', '.md']:
                candidate = docs_dir / f"{page}{ext}"
                if candidate.exists():
                    file_path = candidate
                    break

            if file_path:
                try:
                    with open(file_path, encoding='utf-8') as f:
                        page_content = f.read()

                    content += f"### {page}\n\n"
                    content += page_content + "\n\n"
                except Exception as e:
                    print(f"警告: 无法读取文件 {file_path}: {e}")
            else:
                print(f"警告: 文件不存在: {page}")

    return content


def calculate_hash(content: str) -> str:
    """
    计算内容的 SHA256 哈希

    Args:
        content: 文档内容

    Returns:
        SHA256 哈希值
    """
    return hashlib.sha256(content.encode()).hexdigest()


def process_all_tabs(docs_structure, docs_dir, threshold=5):
    """
    处理所有 Tab，生成合并文档

    Args:
        docs_structure: parse_docs_json 返回的结构
        docs_dir: docs 目录路径
        threshold: Group 数量阈值

    Returns:
        合并文档字典
    """
    result = {}
    for tab_name, tab_data in docs_structure.items():
        groups = tab_data['groups']
        strategy, merge_specs = decide_merge_strategy(tab_name, groups, threshold)
        for merge_spec in merge_specs:
            content = merge_documents(merge_spec, docs_dir)
            source_files = []
            for group in merge_spec['groups']:
                for page in group['pages']:
                    for ext in ['.mdx', '.md']:
                        file_path = docs_dir / f"{page}{ext}"
                        if file_path.exists():
                            source_files.append(str(file_path.relative_to(docs_dir.parent)))
                            break
            filename = f"{merge_spec['name']}.md"
            result[filename] = {
                "merge_type": strategy,
                "source_files": source_files,
                "content": content,
                "content_hash": calculate_hash(content),
                "last_updated": datetime.now().isoformat()
            }
    return result


if __name__ == '__main__':
    import sys
    sys.path.append(str(SCRIPT_DIR))
    from parse_docs import parse_docs_json

    config_file = SKILL_DIR / 'references' / 'config.json'
    with open(config_file) as f:
        config = json.load(f)

    repo_path = SKILL_DIR / config['repo_path']
    docs_json = repo_path / 'docs' / 'docs.json'
    docs_dir = repo_path / 'docs'

    print("正在解析文档结构...")
    structure = parse_docs_json(docs_json)

    print("正在合并文档...")
    merged_docs = process_all_tabs(structure, docs_dir, config['group_threshold'])

    print(f"\n合并结果:")
    print(f"  生成文件数: {len(merged_docs)}")
    for filename, doc_info in merged_docs.items():
        content_size = len(doc_info['content'])
        source_count = len(doc_info['source_files'])
        print(f"  - {filename}: {content_size} bytes, {source_count} source files ({doc_info['merge_type']})")

    # 保存到 merge_cache.json
    cache_file = SKILL_DIR / 'references' / 'merge_cache.json'
    cache_data = {
        "merged_docs": {
            filename: {
                "merge_type": doc_info["merge_type"],
                "source_files": doc_info["source_files"],
                "content_hash": doc_info["content_hash"],
                "last_updated": doc_info["last_updated"]
            }
            for filename, doc_info in merged_docs.items()
        },
        "last_merge": datetime.now().isoformat()
    }

    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, indent=2, ensure_ascii=False)

    print(f"\n缓存已保存到: {cache_file}")
