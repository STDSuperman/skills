# OpenClaw Docs Skill 重构实现计划 - Phase 1 MVP

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将 openclaw-docs skill 从基于 sitemap 的方案重构为基于 GitHub 仓库的方案，实现更精确的英文文档管理和智能合并。

**Architecture:** 从 GitHub 克隆 openclaw 仓库，解析 docs.json 提取英文文档结构，按智能策略合并文档（Group ≤5 按 Tab 合并，>5 按 Group 合并），同步到新的 NotebookLM Notebook。

**Tech Stack:** Python 3, GitPython, NotebookLM CLI, Markdown

---

## Task 1: 清理旧文件

**Files:**
- Delete: `skills/openclaw-docs/docs/` (整个目录)
- Delete: `skills/openclaw-docs/scripts/*.py` (所有旧脚本)
- Delete: `skills/openclaw-docs/references/config.json`
- Delete: `skills/openclaw-docs/references/notebooklm_cache.json`

**Step 1: 删除旧的 docs 目录**

```bash
cd skills/openclaw-docs
rm -rf docs/
```

Expected: docs/ 目录被删除

**Step 2: 删除旧的脚本文件**

```bash
rm -f scripts/sync_docs.py \
      scripts/check_updates.py \
      scripts/query_docs.py \
      scripts/download_docs.py \
      scripts/check_git_updates.py \
      scripts/clone_and_merge.py \
      scripts/extract_en_docs.py \
      scripts/sync_docs_v2.py
```

Expected: 所有旧脚本被删除

**Step 3: 删除旧的配置和缓存文件**

```bash
rm -f references/config.json \
      references/notebooklm_cache.json
```

Expected: 旧配置文件被删除

**Step 4: 验证清理结果**

```bash
ls -la scripts/
ls -la references/
```

Expected: scripts/ 为空，references/ 只剩 DOCS_JSON_STRUCTURE.md

**Step 5: Commit**

```bash
git add -A
git commit -m "chore: 清理 openclaw-docs 旧文件

- 删除旧的 docs/ 目录
- 删除所有旧脚本
- 删除旧配置和缓存文件

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 2: 创建新的目录结构

**Files:**
- Create: `skills/openclaw-docs/.gitignore`
- Create: `skills/openclaw-docs/references/config.json`
- Create: `skills/openclaw-docs/references/merge_cache.json`
- Create: `skills/openclaw-docs/references/sync_cache.json`

**Step 1: 创建 .gitignore**

```bash
cat > .gitignore << 'EOF'
# 克隆的仓库目录
repo/

# Python
*.pyc
__pycache__/
*.py[cod]
*$py.class

# 系统文件
.DS_Store
Thumbs.db
EOF
```

Expected: .gitignore 文件创建成功

**Step 2: 创建初始配置文件**

```bash
cat > references/config.json << 'EOF'
{
  "notebook_id": "",
  "repo_url": "https://github.com/openclaw/openclaw",
  "repo_path": "repo/openclaw",
  "last_commit": "",
  "group_threshold": 5
}
EOF
```

Expected: config.json 创建成功

**Step 3: 创建合并缓存文件**

```bash
cat > references/merge_cache.json << 'EOF'
{
  "merged_docs": {},
  "last_merge": ""
}
EOF
```

Expected: merge_cache.json 创建成功

**Step 4: 创建同步缓存文件**

```bash
cat > references/sync_cache.json << 'EOF'
{
  "synced_docs": {},
  "last_sync": ""
}
EOF
```

Expected: sync_cache.json 创建成功

**Step 5: Commit**

```bash
git add .gitignore references/*.json
git commit -m "feat: 创建新的目录结构和配置文件

- 添加 .gitignore 忽略 repo/ 目录
- 创建新的配置文件结构
- 初始化缓存文件

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 3: 更新 requirements.txt

**Files:**
- Modify: `skills/openclaw-docs/requirements.txt`

**Step 1: 更新依赖列表**

```bash
cat > requirements.txt << 'EOF'
gitpython>=3.1.0
notebooklm-py>=0.1.0
EOF
```

Expected: requirements.txt 更新成功

**Step 2: Commit**

```bash
git add requirements.txt
git commit -m "feat: 更新依赖列表

- 添加 gitpython 用于仓库管理
- 保留 notebooklm-py 用于文档同步

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 4: 实现仓库管理器 (init_repo.py)

**Files:**
- Create: `skills/openclaw-docs/scripts/init_repo.py`

**Step 1: 创建仓库管理器基础结构**

```python
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
```

Expected: init_repo.py 创建成功

**Step 2: 测试仓库克隆功能**

```bash
cd skills/openclaw-docs
python scripts/init_repo.py
```

Expected: 成功克隆仓库到 repo/openclaw/

**Step 3: 验证仓库结构**

```bash
ls -la repo/openclaw/docs/
```

Expected: 看到 docs.json 和文档文件

**Step 4: Commit**

```bash
git add scripts/init_repo.py
git commit -m "feat: 实现仓库管理器

- 支持克隆和更新 GitHub 仓库
- 使用浅克隆(depth=1)节省空间
- 支持获取变更文件列表

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 5: 实现文档解析器 (parse_docs.py)

**Files:**
- Create: `skills/openclaw-docs/scripts/parse_docs.py`

**Step 1: 创建文档解析器**

```python
#!/usr/bin/env python3
"""
文档解析器
解析 docs.json，提取英文文档结构
"""

import json
import os
from pathlib import Path
from typing import Dict, List

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent


def parse_docs_json(docs_json_path: str) -> Dict[str, Dict]:
    """
    解析 docs.json，提取英文文档结构

    Args:
        docs_json_path: docs.json 文件路径

    Returns:
        {
            "Get started": {
                "groups": [
                    {"group": "Home", "pages": ["index"]},
                    {"group": "Overview", "pages": ["start/showcase"]}
                ]
            },
            ...
        }
    """
    with open(docs_json_path, encoding='utf-8') as f:
        config = json.load(f)

    result = {}

    # 遍历语言配置
    for lang in config.get('navigation', {}).get('languages', []):
        locale = lang.get('locale', 'en')

        # 只处理英文
        if locale != 'en':
            continue

        # 遍历 tabs
        for tab in lang.get('tabs', []):
            tab_name = tab.get('tab')
            if not tab_name:
                continue

            groups = []

            # 遍历 groups
            for group in tab.get('groups', []):
                group_name = group.get('group')
                pages = group.get('pages', [])

                if group_name and pages:
                    groups.append({
                        'group': group_name,
                        'pages': pages
                    })

            if groups:
                result[tab_name] = {'groups': groups}

    return result


def resolve_doc_files(docs_dir: str, pages: List[str]) -> List[str]:
    """
    解析 pages 路径为实际文件路径

    Args:
        docs_dir: docs 目录路径
        pages: 页面路径列表，如 ["index", "start/showcase"]

    Returns:
        实际文件路径列表，如 ["docs/index.mdx", "docs/start/showcase.mdx"]
    """
    files = []
    docs_path = Path(docs_dir)

    for page in pages:
        # 尝试 .mdx 和 .md 扩展名
        for ext in ['.mdx', '.md']:
            file_path = docs_path / f"{page}{ext}"
            if file_path.exists():
                files.append(str(file_path))
                break

    return files


def get_all_doc_files(docs_structure: Dict[str, Dict], docs_dir: str) -> Dict[str, List[str]]:
    """
    获取所有文档文件路径

    Args:
        docs_structure: parse_docs_json 返回的结构
        docs_dir: docs 目录路径

    Returns:
        {
            "Get started": ["docs/index.mdx", "docs/start/showcase.mdx"],
            ...
        }
    """
    result = {}

    for tab_name, tab_data in docs_structure.items():
        all_pages = []

        for group in tab_data['groups']:
            all_pages.extend(group['pages'])

        files = resolve_doc_files(docs_dir, all_pages)
        result[tab_name] = files

    return result


if __name__ == '__main__':
    # 测试代码
    config_file = SKILL_DIR / 'references' / 'config.json'
    with open(config_file) as f:
        config = json.load(f)

    repo_path = SKILL_DIR / config['repo_path']
    docs_json = repo_path / 'docs' / 'docs.json'

    print("正在解析 docs.json...")
    structure = parse_docs_json(docs_json)

    print(f"\n找到 {len(structure)} 个 Tab:")
    for tab_name, tab_data in structure.items():
        group_count = len(tab_data['groups'])
        page_count = sum(len(g['pages']) for g in tab_data['groups'])
        print(f"  - {tab_name}: {group_count} groups, {page_count} pages")

    print("\n正在解析文档文件...")
    docs_dir = repo_path / 'docs'
    doc_files = get_all_doc_files(structure, docs_dir)

    print(f"\n文档文件统计:")
    total_files = 0
    for tab_name, files in doc_files.items():
        print(f"  - {tab_name}: {len(files)} files")
        total_files += len(files)
    print(f"\n总计: {total_files} 个文档文件")
```

Expected: parse_docs.py 创建成功

**Step 2: 测试文档解析功能**

```bash
python scripts/parse_docs.py
```

Expected: 成功解析 docs.json 并显示统计信息

**Step 3: Commit**

```bash
git add scripts/parse_docs.py
git commit -m "feat: 实现文档解析器

- 解析 docs.json 提取英文文档结构
- 支持 .mdx 和 .md 文件
- 按 Tab 和 Group 组织文档

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 6: 实现文档合并器 (merge_docs.py)

**Files:**
- Create: `skills/openclaw-docs/scripts/merge_docs.py`

**Step 1: 创建文档合并器（第一部分）**

```python
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
```

Expected: merge_docs.py 第一部分创建成功

**Step 2: 创建文档合并器（第二部分）**


继续 merge_docs.py 的第二部分:

```python
def process_all_tabs(docs_structure, docs_dir, threshold=5):
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
```

完整实现计划已保存。
