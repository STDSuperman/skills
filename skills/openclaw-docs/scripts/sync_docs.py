#!/usr/bin/env python3
"""
同步管理器
负责将合并后的文档同步到 NotebookLM
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
from merge_docs import process_all_tabs


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
            ['notebooklm', 'upload', notebook_id, str(temp_file)],
            capture_output=True,
            text=True,
            timeout=60
        )

        success = result.returncode == 0
        if success:
            print(f"  ✓ 上传成功: {filename}")
        else:
            print(f"  ✗ 上传失败: {filename} - {result.stderr}")

        return success
    except Exception as e:
        print(f"  ✗ 上传失败: {filename} - {e}")
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
            ['notebooklm', 'delete', notebook_id, filename],
            capture_output=True,
            text=True,
            timeout=30
        )

        success = result.returncode == 0
        if success:
            print(f"  ✓ 删除成功: {filename}")
        else:
            print(f"  ✗ 删除失败: {filename} - {result.stderr}")

        return success
    except Exception as e:
        print(f"  ✗ 删除失败: {filename} - {e}")
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
    print("  ✓ CLI 可用\n")

    # 2. 加载配置
    print("2. 加载配置...")
    config_file = SKILL_DIR / 'references' / 'config.json'
    with open(config_file, encoding='utf-8') as f:
        config = json.load(f)
    print("  ✓ 配置加载完成\n")

    # 3. 获取/创建 Notebook ID
    print("3. 获取 Notebook ID...")
    notebook_id = get_or_create_notebook_id(config)
    if notebook_id != config.get('notebook_id'):
        config['notebook_id'] = notebook_id
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Notebook ID 已保存到配置\n")

    # 4. 初始化仓库
    print("4. 初始化/更新仓库...")
    has_update, commit = init_or_update_repo(config['repo_url'], config['repo_path'])
    config['last_commit'] = commit
    print()

    # 5. 解析文档
    print("5. 解析文档结构...")
    repo_path = SKILL_DIR / config['repo_path']
    docs_json = repo_path / 'docs' / 'docs.json'
    structure = parse_docs_json(docs_json)
    print(f"  ✓ 找到 {len(structure)} 个 Tab\n")

    # 6. 合并文档
    print("6. 合并文档...")
    docs_dir = repo_path / 'docs'
    merged_docs = process_all_tabs(structure, docs_dir, config['group_threshold'])
    print(f"  ✓ 生成 {len(merged_docs)} 个合并文档\n")

    # 7. 同步到 NotebookLM
    print("7. 同步到 NotebookLM...")
    sync_cache_file = SKILL_DIR / 'references' / 'sync_cache.json'
    with open(sync_cache_file, encoding='utf-8') as f:
        sync_cache = json.load(f)

    sync_cache = sync_to_notebooklm(notebook_id, merged_docs, sync_cache)

    # 8. 更新配置和缓存
    print("\n8. 更新配置和缓存...")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    with open(sync_cache_file, 'w', encoding='utf-8') as f:
        json.dump(sync_cache, f, indent=2, ensure_ascii=False)

    print("  ✓ 配置和缓存已更新")
    print("\n=== 同步完成 ===")

