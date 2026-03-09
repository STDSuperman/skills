#!/usr/bin/env python3
"""
文档合并器
根据智能策略合并文档，支持增量合并
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
MAX_DOCS = 50  # 最大文档数量限制


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
        threshold: Group 数量阈值（初始值，会动态调整）

    Returns:
        合并文档字典
    """
    # 第一步：预估文档数量，动态调整 threshold
    estimated_docs = 0
    for tab_name, tab_data in docs_structure.items():
        groups = tab_data['groups']
        if len(groups) <= threshold:
            estimated_docs += 1  # 整个 Tab 合并为一个文件
        else:
            estimated_docs += len(groups)  # 每个 Group 一个文件

    # 如果预估超过 MAX_DOCS，提高 threshold
    adjusted_threshold = threshold
    while estimated_docs > MAX_DOCS and adjusted_threshold < 100:
        adjusted_threshold += 1
        estimated_docs = 0
        for tab_name, tab_data in docs_structure.items():
            groups = tab_data['groups']
            if len(groups) <= adjusted_threshold:
                estimated_docs += 1
            else:
                estimated_docs += len(groups)

    # 如果还是超过，强制所有 Tab 都合并为一个文件
    if estimated_docs > MAX_DOCS:
        adjusted_threshold = 999  # 设置一个很大的值，强制所有 Tab 合并
        estimated_docs = len(docs_structure)
        print(f"警告: 即使提高阈值仍超过 {MAX_DOCS} 个文档，强制所有 Tab 合并为单个文件")

    if adjusted_threshold != threshold:
        print(f"自动调整阈值: {threshold} -> {adjusted_threshold} (预估文档数: {estimated_docs})")

    # 第二步：执行合并
    result = {}
    for tab_name, tab_data in docs_structure.items():
        groups = tab_data['groups']
        strategy, merge_specs = decide_merge_strategy(tab_name, groups, adjusted_threshold)
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

    # 第三步：验证文档数量
    if len(result) > MAX_DOCS:
        raise ValueError(f"合并后文档数量 {len(result)} 超过限制 {MAX_DOCS}，请检查合并逻辑")

    return result


def process_incremental_merge(
    docs_structure: Dict,
    docs_dir: Path,
    affected_files: Set[str],
    merge_cache: Dict,
    threshold: int = 5
) -> Dict:
    """
    增量合并：只重新合并受影响的文档

    Args:
        docs_structure: parse_docs_json 返回的结构
        docs_dir: docs 目录路径
        affected_files: 受影响的合并文档文件名集合
        merge_cache: 合并缓存
        threshold: Group 数量阈值

    Returns:
        更新后的合并文档字典
    """
    if not affected_files:
        # 没有变更，直接返回缓存
        print("没有文件变更，使用缓存")
        result = {}
        for filename, doc_info in merge_cache.get('merged_docs', {}).items():
            result[filename] = {
                "merge_type": doc_info["merge_type"],
                "source_files": doc_info["source_files"],
                "content": "",  # 不需要内容，后续从文件读取
                "content_hash": doc_info["content_hash"],
                "last_updated": doc_info["last_updated"]
            }
        return result

    print(f"增量合并: 需要重新合并 {len(affected_files)} 个文档")

    # 执行完整合并（包含动态阈值调整）
    all_merged = process_all_tabs(docs_structure, docs_dir, threshold)

    # 标记哪些是新合并的，哪些是从缓存复用的
    result = {}
    for filename, doc_info in all_merged.items():
        if filename in affected_files:
            # 新合并的文档
            result[filename] = doc_info
            print(f"  [重新合并] {filename}")
        else:
            # 从缓存复用
            cached_info = merge_cache.get('merged_docs', {}).get(filename)
            if cached_info:
                result[filename] = {
                    "merge_type": cached_info["merge_type"],
                    "source_files": cached_info["source_files"],
                    "content": doc_info["content"],  # 使用新生成的内容（因为可能阈值变了）
                    "content_hash": doc_info["content_hash"],
                    "last_updated": cached_info["last_updated"]
                }
                print(f"  [复用缓存] {filename}")
            else:
                # 新文档
                result[filename] = doc_info
                print(f"  [新文档] {filename}")

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

    # 保存合并后的文件到 merged 目录
    merged_dir = SKILL_DIR / 'merged'
    merged_dir.mkdir(exist_ok=True)

    print(f"\n正在保存合并文件到: {merged_dir}")
    for filename, doc_info in merged_docs.items():
        output_file = merged_dir / filename
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(doc_info['content'])
        print(f"  [OK] {filename}")

    # 保存到 merge_cache.json
    cache_file = SKILL_DIR / 'cache' / 'merge_cache.json'
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
