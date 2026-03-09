#!/usr/bin/env python3
"""
同步管理器
负责将合并后的文档同步到 NotebookLM
支持增量更新和文档结构验证
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent

# 导入其他模块
sys.path.append(str(SCRIPT_DIR))
from init_repo import init_or_update_repo
from parse_docs import parse_docs_json
from merge_docs import process_all_tabs, process_incremental_merge
from validate_structure import validate_docs_structure, StructureValidationError
from detect_changes import detect_source_file_changes, find_affected_merged_docs, get_current_source_files


def check_notebooklm_cli() -> bool:
    """
    检查 notebooklm CLI 是否可用

    Returns:
        CLI 是否可用
    """
    try:
        result = subprocess.run(
            ['notebooklm', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_or_create_notebook_id(config: Dict) -> str:
    """
    获取或创建 Notebook ID

    Args:
        config: 配置字典

    Returns:
        Notebook ID
    """
    notebook_id = config.get('notebook_id', '')

    if notebook_id:
        print(f"使用现有 Notebook ID: {notebook_id}")
        return notebook_id

    # 提示用户输入或创建
    print("\n未找到 Notebook ID。")
    print("1. 输入现有 Notebook ID")
    print("2. 创建新的 Notebook")
    choice = input("请选择 (1/2): ").strip()

    if choice == '1':
        notebook_id = input("请输入 Notebook ID: ").strip()
    else:
        notebook_name = input("请输入 Notebook 名称 (默认: OpenClaw Docs): ").strip()
        if not notebook_name:
            notebook_name = "OpenClaw Docs"

        print(f"\n正在创建 Notebook: {notebook_name}")
        try:
            result = subprocess.run(
                ['notebooklm', 'create', notebook_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                # 从输出中提取 Notebook ID
                notebook_id = result.stdout.strip()
                print(f"Notebook 创建成功: {notebook_id}")
            else:
                raise Exception(f"创建失败: {result.stderr}")
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)

    return notebook_id


def upload_to_notebooklm(notebook_id: str, filename: str, content: str) -> bool:
    """
    上传文档到 NotebookLM

    Args:
        notebook_id: Notebook ID
        filename: 文件名
        content: 文档内容

    Returns:
        是否成功
    """
    # 创建临时文件
    temp_dir = SKILL_DIR / 'temp'
    temp_dir.mkdir(exist_ok=True)
    temp_file = temp_dir / filename

    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)

        result = subprocess.run(
            ['notebooklm', 'source', 'add', '--notebook', notebook_id, str(temp_file)],
            capture_output=True,
            text=True,
            timeout=60
        )

        success = result.returncode == 0
        if success:
            print(f"  [OK] 上传成功: {filename}")
        else:
            print(f"  [FAIL] 上传失败: {filename} - {result.stderr}")

        return success
    except Exception as e:
        print(f"  [FAIL] 上传失败: {filename} - {e}")
        return False
    finally:
        # 清理临时文件
        if temp_file.exists():
            temp_file.unlink()


def delete_from_notebooklm(notebook_id: str, filename: str) -> bool:
    """
    从 NotebookLM 删除文档

    Args:
        notebook_id: Notebook ID
        filename: 文件名

    Returns:
        是否成功
    """
    try:
        result = subprocess.run(
            ['notebooklm', 'source', 'delete', notebook_id, filename],
            capture_output=True,
            text=True,
            timeout=30
        )

        success = result.returncode == 0
        if success:
            print(f"  [OK] 删除成功: {filename}")
        else:
            print(f"  [FAIL] 删除失败: {filename} - {result.stderr}")

        return success
    except Exception as e:
        print(f"  [FAIL] 删除失败: {filename} - {e}")
        return False


def detect_changes(merged_docs: Dict, sync_cache: Dict) -> Dict:
    """
    检测文档变更

    Args:
        merged_docs: 合并后的文档字典
        sync_cache: 同步缓存

    Returns:
        {
            "to_upload": [filename, ...],
            "to_delete": [filename, ...],
            "unchanged": [filename, ...]
        }
    """
    synced_docs = sync_cache.get('synced_docs', {})

    to_upload = []
    to_delete = []
    unchanged = []

    # 检查需要上传的文档
    for filename, doc_info in merged_docs.items():
        if filename not in synced_docs:
            # 新文档
            to_upload.append(filename)
        elif doc_info['content_hash'] != synced_docs[filename].get('content_hash'):
            # 内容已变更
            to_upload.append(filename)
        else:
            # 未变更
            unchanged.append(filename)

    # 检查需要删除的文档
    for filename in synced_docs:
        if filename not in merged_docs:
            to_delete.append(filename)

    return {
        'to_upload': to_upload,
        'to_delete': to_delete,
        'unchanged': unchanged
    }


def sync_to_notebooklm(notebook_id: str, merged_docs: Dict, sync_cache: Dict) -> Dict:
    """
    同步文档到 NotebookLM

    Args:
        notebook_id: Notebook ID
        merged_docs: 合并后的文档字典
        sync_cache: 同步缓存

    Returns:
        更新后的同步缓存
    """
    changes = detect_changes(merged_docs, sync_cache)

    print(f"\n变更检测:")
    print(f"  需要上传: {len(changes['to_upload'])} 个文件")
    print(f"  需要删除: {len(changes['to_delete'])} 个文件")
    print(f"  未变更: {len(changes['unchanged'])} 个文件")

    # 删除旧文档
    if changes['to_delete']:
        print(f"\n正在删除 {len(changes['to_delete'])} 个文档...")
        for filename in changes['to_delete']:
            delete_from_notebooklm(notebook_id, filename)

    # 上传新文档或更新的文档
    if changes['to_upload']:
        print(f"\n正在上传 {len(changes['to_upload'])} 个文档...")
        for filename in changes['to_upload']:
            doc_info = merged_docs[filename]
            success = upload_to_notebooklm(notebook_id, filename, doc_info['content'])

            if success:
                # 更新缓存
                sync_cache.setdefault('synced_docs', {})[filename] = {
                    'content_hash': doc_info['content_hash'],
                    'last_synced': datetime.now().isoformat()
                }

    # 清理已删除的文档缓存
    for filename in changes['to_delete']:
        sync_cache.get('synced_docs', {}).pop(filename, None)

    sync_cache['last_sync'] = datetime.now().isoformat()

    return sync_cache


if __name__ == '__main__':
    print("=== OpenClaw Docs 同步管理器 ===\n")

    # 1. 检查 CLI
    print("1. 检查 notebooklm CLI...")
    if not check_notebooklm_cli():
        print("错误: notebooklm CLI 不可用")
        print("请先安装: pip install notebooklm-py")
        sys.exit(1)
    print("  [OK] CLI 可用\n")

    # 2. 加载配置
    print("2. 加载配置...")
    config_file = SKILL_DIR / 'references' / 'config.json'
    with open(config_file, encoding='utf-8') as f:
        config = json.load(f)
    print("  [OK] 配置加载完成\n")

    # 3. 获取/创建 Notebook ID
    print("3. 获取 Notebook ID...")
    notebook_id = get_or_create_notebook_id(config)
    if notebook_id != config.get('notebook_id'):
        config['notebook_id'] = notebook_id
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Notebook ID 已保存到配置\n")

    # 4. 初始化仓库
    print("4. 初始化/更新仓库...")
    has_update, commit = init_or_update_repo(config['repo_url'], config['repo_path'])
    config['last_commit'] = commit
    print()

    # 5. 验证文档结构
    print("5. 验证文档结构...")
    repo_path = SKILL_DIR / config['repo_path']
    try:
        is_valid, message = validate_docs_structure(repo_path)
        print(f"  {message}\n")
    except StructureValidationError as e:
        print(f"\n{e}\n")
        print("同步已终止。")
        sys.exit(1)

    # 6. 解析文档
    print("6. 解析文档结构...")
    docs_json = repo_path / 'docs' / 'docs.json'
    structure = parse_docs_json(docs_json)
    print(f"  [OK] 找到 {len(structure)} 个 Tab\n")

    # 7. 检测源文件变更
    print("7. 检测源文件变更...")
    docs_dir = repo_path / 'docs'
    source_cache_file = SKILL_DIR / 'cache' / 'source_cache.json'

    if source_cache_file.exists():
        with open(source_cache_file, encoding='utf-8') as f:
            source_cache = json.load(f)
    else:
        source_cache = {}

    changes = detect_source_file_changes(structure, docs_dir, source_cache)
    print(f"  新增: {len(changes['added'])} 个文件")
    print(f"  修改: {len(changes['modified'])} 个文件")
    print(f"  删除: {len(changes['deleted'])} 个文件")
    print(f"  未变更: {len(changes['unchanged'])} 个文件\n")

    # 8. 找出受影响的合并文档
    print("8. 分析受影响的合并文档...")
    merge_cache_file = SKILL_DIR / 'cache' / 'merge_cache.json'

    if merge_cache_file.exists():
        with open(merge_cache_file, encoding='utf-8') as f:
            merge_cache = json.load(f)
    else:
        merge_cache = {}

    affected_files = find_affected_merged_docs(changes, merge_cache)
    print(f"  受影响: {len(affected_files)} 个合并文档\n")

    # 9. 增量合并文档
    print("9. 合并文档...")
    if affected_files or not merge_cache:
        merged_docs = process_incremental_merge(
            structure, docs_dir, affected_files, merge_cache, config['group_threshold']
        )
    else:
        print("  没有变更，跳过合并")
        merged_docs = {}
        for filename, doc_info in merge_cache.get('merged_docs', {}).items():
            merged_docs[filename] = {
                "merge_type": doc_info["merge_type"],
                "source_files": doc_info["source_files"],
                "content": "",  # 不需要内容
                "content_hash": doc_info["content_hash"],
                "last_updated": doc_info["last_updated"]
            }
    print(f"  [OK] 生成 {len(merged_docs)} 个合并文档\n")

    # 10. 同步到 NotebookLM
    print("10. 同步到 NotebookLM...")
    sync_cache_file = SKILL_DIR / 'cache' / 'sync_cache.json'

    if sync_cache_file.exists():
        with open(sync_cache_file, encoding='utf-8') as f:
            sync_cache = json.load(f)
    else:
        sync_cache = {}

    sync_cache = sync_to_notebooklm(notebook_id, merged_docs, sync_cache)

    # 11. 更新所有缓存
    print("\n11. 更新配置和缓存...")

    # 更新配置
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    # 更新源文件缓存
    current_files = get_current_source_files(structure, docs_dir)
    source_cache = {
        'source_files': current_files,
        'last_check': datetime.now().isoformat()
    }
    with open(source_cache_file, 'w', encoding='utf-8') as f:
        json.dump(source_cache, f, indent=2, ensure_ascii=False)

    # 更新合并缓存
    merge_cache_data = {
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
    with open(merge_cache_file, 'w', encoding='utf-8') as f:
        json.dump(merge_cache_data, f, indent=2, ensure_ascii=False)

    # 更新同步缓存
    with open(sync_cache_file, 'w', encoding='utf-8') as f:
        json.dump(sync_cache, f, indent=2, ensure_ascii=False)

    print("  [OK] 所有缓存已更新")
    print("\n=== 同步完成 ===")

