#!/usr/bin/env python3
"""
仓库管理器
负责克隆和更新 OpenClaw GitHub 仓库
"""

import os
import sys
from pathlib import Path
import git

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent


def init_or_update_repo(repo_url: str, repo_path: str) -> tuple[bool, str]:
    """
    初始化或更新仓库

    Args:
        repo_url: 仓库 URL
        repo_path: 本地仓库路径

    Returns:
        (是否有更新, 当前 commit hash)
    """
    repo_full_path = SKILL_DIR / repo_path

    if not repo_full_path.exists():
        # 克隆仓库
        print(f"正在克隆仓库: {repo_url}")
        print(f"目标路径: {repo_full_path}")

        repo_full_path.parent.mkdir(parents=True, exist_ok=True)
        git.Repo.clone_from(repo_url, repo_full_path, depth=1)

        repo = git.Repo(repo_full_path)
        current_commit = repo.head.commit.hexsha
        print(f"克隆完成，当前 commit: {current_commit[:8]}")

        return True, current_commit
    else:
        # 更新仓库
        print(f"正在更新仓库: {repo_full_path}")

        repo = git.Repo(repo_full_path)
        old_commit = repo.head.commit.hexsha

        origin = repo.remotes.origin
        origin.pull()

        new_commit = repo.head.commit.hexsha
        has_update = old_commit != new_commit

        if has_update:
            print(f"仓库已更新: {old_commit[:8]} -> {new_commit[:8]}")
        else:
            print(f"仓库已是最新，commit: {new_commit[:8]}")

        return has_update, new_commit


def get_changed_files(repo_path: str, old_commit: str, new_commit: str) -> list[str]:
    """
    获取两个 commit 之间变更的文件列表
    只返回 docs/ 目录下的文件

    Args:
        repo_path: 本地仓库路径
        old_commit: 旧 commit hash
        new_commit: 新 commit hash

    Returns:
        变更文件列表
    """
    repo_full_path = SKILL_DIR / repo_path
    repo = git.Repo(repo_full_path)

    diff = repo.git.diff(old_commit, new_commit, name_only=True)
    files = diff.split('\n') if diff else []

    # 只返回 docs/ 目录下的文件
    docs_files = [f for f in files if f.startswith('docs/')]

    return docs_files


if __name__ == '__main__':
    # 测试代码
    import json

    config_file = SKILL_DIR / 'references' / 'config.json'
    with open(config_file) as f:
        config = json.load(f)

    has_update, commit = init_or_update_repo(
        config['repo_url'],
        config['repo_path']
    )

    print(f"\n结果:")
    print(f"  有更新: {has_update}")
    print(f"  当前 commit: {commit[:8]}")
