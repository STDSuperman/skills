# OpenClaw Docs Skill 重构设计方案

## 文档信息

- **日期**: 2026-03-08
- **作者**: Claude Sonnet 4.6
- **状态**: 设计完成，待实现

## 1. 概述

### 1.1 背景

当前 openclaw-docs skill 通过 sitemap.xml 拉取文档站的文档，存在以下问题：
- 依赖文档站的 sitemap
- 无法精确控制文档语言
- 文档粒度不可控

### 1.2 新方案目标

- 直接从 GitHub 仓库拉取 docs 目录
- 只处理英文文档，过滤其他语言
- 使用 docs/docs.json 解析文档结构
- 按一级分类（Tab）智能合并文档
- 通过 git change 识别更新
- 继续使用 NotebookLM 进行文档管理和查询

### 1.3 核心变更

| 维度 | 旧方案 | 新方案 |
|------|--------|--------|
| 文档源 | sitemap.xml | GitHub 仓库 docs 目录 |
| 语言过滤 | 无 | 只保留英文文档 |
| 文档结构 | sitemap 列表 | docs.json 解析 |
| 合并策略 | 无合并 | 智能合并（Tab/Group） |
| 更新检测 | lastmod 时间 | git diff |
| 存储方式 | NotebookLM | NotebookLM（新 Notebook） |

## 2. 整体架构

### 2.1 核心流程

```
1. 初始化/更新仓库
   ├─ 首次运行：克隆仓库
   └─ 后续运行：git pull
   ↓
2. 解析 docs.json
   ├─ 提取英文文档路径
   └─ 按 Tab 和 Group 组织
   ↓
3. 智能合并文档
   ├─ Group 数量 <= 5：按 Tab 合并
   └─ Group 数量 > 5：按 Group 合并
   ↓
4. 检测文档变更
   ├─ 对比 last_commit
   ├─ 识别受影响的合并文档
   └─ 计算 content_hash
   ↓
5. 同步到 NotebookLM
   ├─ 删除旧文件（通过 file_id）
   └─ 上传新文件
   ↓
6. 更新本地缓存
   ├─ merge_cache.json
   └─ sync_cache.json
```

### 2.2 目录结构

```
skills/openclaw-docs/
├── .gitignore                  # 忽略 repo/ 目录
├── SKILL.md                    # Skill 说明
├── README.md                   # 使用文档
├── requirements.txt            # Python 依赖
├── scripts/
│   ├── init_repo.py           # 初始化/克隆仓库
│   ├── parse_docs.py          # 解析 docs.json
│   ├── merge_docs.py          # 合并文档
│   ├── sync_docs.py           # 同步到 NotebookLM
│   ├── check_updates.py       # 检查更新
│   └── query_docs.py          # 查询文档
├── references/
│   ├── config.json            # 配置（notebook_id, repo_path）
│   ├── merge_cache.json       # 合并文档缓存
│   ├── sync_cache.json        # 同步缓存
│   └── DOCS_JSON_STRUCTURE.md # docs.json 结构说明（保留）
└── repo/                      # 克隆的仓库（被 .gitignore）
    └── openclaw/              # 实际仓库目录
        └── docs/              # 文档目录
```

## 3. 核心组件设计

### 3.1 仓库管理器（init_repo.py）

**职责**：
- 克隆 GitHub 仓库
- 更新仓库（git pull）
- 记录当前 commit hash

**核心函数**：
```python
def init_or_update_repo(repo_url, repo_path):
    """
    初始化或更新仓库
    返回：(是否有更新, 当前 commit hash)
    """
    if not os.path.exists(repo_path):
        # 克隆仓库
        git.Repo.clone_from(repo_url, repo_path, depth=1)
        return True, get_current_commit(repo_path)
    else:
        # 更新仓库
        repo = git.Repo(repo_path)
        old_commit = repo.head.commit.hexsha
        repo.remotes.origin.pull()
        new_commit = repo.head.commit.hexsha
        return old_commit != new_commit, new_commit

def get_changed_files(repo_path, old_commit, new_commit):
    """
    获取两个 commit 之间变更的文件列表
    只返回 docs/ 目录下的文件
    """
    repo = git.Repo(repo_path)
    diff = repo.git.diff(old_commit, new_commit, name_only=True)
    files = diff.split('\n')
    return [f for f in files if f.startswith('docs/')]
```

### 3.2 文档解析器（parse_docs.py）

**职责**：
- 解析 docs/docs.json
- 提取英文文档路径
- 按 Tab 和 Group 组织

**核心函数**：
```python
def parse_docs_json(docs_json_path):
    """
    解析 docs.json，提取英文文档结构
    返回：
    {
        "Get started": {
            "groups": [
                {"group": "Home", "pages": ["index"]},
                {"group": "Overview", "pages": ["start/showcase"]}
            ]
        },
        "Channels": {
            "groups": [...]
        }
    }
    """
    with open(docs_json_path) as f:
        config = json.load(f)

    result = {}
    for lang in config['navigation']['languages']:
        if lang.get('locale') != 'en':
            continue

        for tab in lang.get('tabs', []):
            tab_name = tab.get('tab')
            groups = []

            for group in tab.get('groups', []):
                groups.append({
                    'group': group.get('group'),
                    'pages': group.get('pages', [])
                })

            result[tab_name] = {'groups': groups}

    return result

def resolve_doc_files(docs_dir, pages):
    """
    解析 pages 路径为实际文件路径
    pages: ["index", "start/showcase"]
    返回: ["docs/index.mdx", "docs/start/showcase.mdx"]
    """
    files = []
    for page in pages:
        # 尝试 .mdx 和 .md
        for ext in ['.mdx', '.md']:
            file_path = os.path.join(docs_dir, page + ext)
            if os.path.exists(file_path):
                files.append(file_path)
                break
    return files
```

### 3.3 文档合并器（merge_docs.py）

**职责**：
- 根据智能策略合并文档
- 生成合并后的 Markdown 文件
- 计算文件内容哈希

**智能合并策略**：
```python
def decide_merge_strategy(tab_name, groups):
    """
    决定合并策略
    - 如果 group 数量 <= 5：整个 Tab 合并为一个文件
    - 如果 group 数量 > 5：每个 Group 单独合并

    返回：
    ("tab", [{"name": "Get_started", "groups": [...]}])
    或
    ("group", [
        {"name": "Channels_Discord", "groups": [...]},
        {"name": "Channels_Telegram", "groups": [...]}
    ])
    """
    GROUP_THRESHOLD = 5

    if len(groups) <= GROUP_THRESHOLD:
        return "tab", [{
            "name": sanitize_filename(tab_name),
            "groups": groups
        }]
    else:
        return "group", [
            {
                "name": sanitize_filename(f"{tab_name}_{g['group']}"),
                "groups": [g]
            }
            for g in groups
        ]

def merge_documents(merge_spec, docs_dir):
    """
    合并文档
    merge_spec: {"name": "Get_started", "groups": [...]}
    返回：合并后的 Markdown 内容
    """
    content = f"# {merge_spec['name'].replace('_', ' ')}\n\n"

    for group in merge_spec['groups']:
        content += f"## {group['group']}\n\n"

        for page in group['pages']:
            file_path = resolve_doc_file(docs_dir, page)
            if file_path:
                with open(file_path) as f:
                    page_content = f.read()
                content += f"### {page}\n\n"
                content += page_content + "\n\n"

    return content

def calculate_hash(content):
    """计算内容的 SHA256 哈希"""
    return hashlib.sha256(content.encode()).hexdigest()
```

### 3.4 同步管理器（sync_docs.py）

**职责**：
- 检测合并文档的变更
- 同步到 NotebookLM
- 更新缓存

**核心流程**：
```python
def sync_to_notebooklm(merged_docs, merge_cache, sync_cache, notebook_id):
    """
    同步合并文档到 NotebookLM

    流程：
    1. 对比 merge_cache，识别新增/变更/删除的文档
    2. 对于变更的文档：
       - 从 sync_cache 获取 file_id
       - 删除旧文件
       - 上传新文件
       - 更新 sync_cache
    3. 对于新增的文档：
       - 上传新文件
       - 记录到 sync_cache
    4. 对于删除的文档：
       - 从 NotebookLM 删除
       - 从 sync_cache 移除
    """

    # 识别变更
    changes = detect_changes(merged_docs, merge_cache)

    for change_type, doc_name, doc_info in changes:
        if change_type == 'added' or change_type == 'modified':
            # 如果是修改，先删除旧文件
            if change_type == 'modified':
                old_file_id = sync_cache['synced_docs'][doc_name]['notebooklm_file_id']
                delete_from_notebooklm(notebook_id, old_file_id)

            # 上传新文件
            file_id = upload_to_notebooklm(notebook_id, doc_name, doc_info['content'])

            # 更新 sync_cache
            sync_cache['synced_docs'][doc_name] = {
                'notebooklm_file_id': file_id,
                'content_hash': doc_info['content_hash'],
                'uploaded_at': datetime.now().isoformat()
            }

        elif change_type == 'deleted':
            # 删除文件
            old_file_id = sync_cache['synced_docs'][doc_name]['notebooklm_file_id']
            delete_from_notebooklm(notebook_id, old_file_id)
            del sync_cache['synced_docs'][doc_name]

    sync_cache['last_sync'] = datetime.now().isoformat()
    save_cache(sync_cache, 'references/sync_cache.json')

def detect_changes(merged_docs, merge_cache):
    """
    检测文档变更
    返回：[(change_type, doc_name, doc_info), ...]
    change_type: 'added', 'modified', 'deleted'
    """
    changes = []

    # 检测新增和修改
    for doc_name, doc_info in merged_docs.items():
        if doc_name not in merge_cache['merged_docs']:
            changes.append(('added', doc_name, doc_info))
        elif doc_info['content_hash'] != merge_cache['merged_docs'][doc_name]['content_hash']:
            changes.append(('modified', doc_name, doc_info))

    # 检测删除
    for doc_name in merge_cache['merged_docs']:
        if doc_name not in merged_docs:
            changes.append(('deleted', doc_name, None))

    return changes
```

### 3.5 查询接口（query_docs.py）

**职责**：
- 通过 NotebookLM 查询文档

**实现**：
```python
def query_docs(notebook_id, query):
    """
    查询 NotebookLM
    """
    result = subprocess.run(
        ['notebooklm', 'query', notebook_id, query],
        capture_output=True,
        text=True
    )
    return result.stdout
```

## 4. 数据结构设计

### 4.1 config.json

```json
{
  "notebook_id": "notebook_xxx",
  "repo_url": "https://github.com/openclaw/openclaw",
  "repo_path": "repo/openclaw",
  "last_commit": "abc123def456...",
  "group_threshold": 5
}
```

### 4.2 merge_cache.json

```json
{
  "merged_docs": {
    "Get_started.md": {
      "merge_type": "tab",
      "source_files": [
        "docs/index.mdx",
        "docs/start/showcase.mdx",
        "docs/concepts/features.mdx"
      ],
      "content_hash": "sha256_hash_here",
      "last_updated": "2026-03-08T10:00:00Z"
    },
    "Channels_Discord.md": {
      "merge_type": "group",
      "source_files": [
        "docs/channels/discord.mdx"
      ],
      "content_hash": "sha256_hash_here",
      "last_updated": "2026-03-08T10:00:00Z"
    }
  },
  "last_merge": "2026-03-08T10:00:00Z"
}
```

### 4.3 sync_cache.json

```json
{
  "synced_docs": {
    "Get_started.md": {
      "notebooklm_file_id": "file_xxx",
      "content_hash": "sha256_hash_here",
      "uploaded_at": "2026-03-08T10:30:00Z"
    },
    "Channels_Discord.md": {
      "notebooklm_file_id": "file_yyy",
      "content_hash": "sha256_hash_here",
      "uploaded_at": "2026-03-08T10:30:00Z"
    }
  },
  "last_sync": "2026-03-08T10:30:00Z"
}
```

## 5. 更新检测机制

### 5.1 检测流程

```
1. git pull 更新仓库
   ↓
2. 获取 old_commit 和 new_commit
   ↓
3. git diff 获取变更文件列表（只关注 docs/ 目录）
   ↓
4. 遍历 merge_cache，找出受影响的合并文档
   ↓
5. 重新合并受影响的文档
   ↓
6. 对比 content_hash，识别真正变更的文档
   ↓
7. 同步到 NotebookLM
```

### 5.2 影响判断

```python
def find_affected_merged_docs(changed_files, merge_cache):
    """
    找出受影响的合并文档

    changed_files: ["docs/channels/discord.mdx", "docs/index.mdx"]
    merge_cache: {...}

    返回：需要重新合并的文档名称列表
    """
    affected = set()

    for doc_name, doc_info in merge_cache['merged_docs'].items():
        for source_file in doc_info['source_files']:
            if source_file in changed_files:
                affected.add(doc_name)
                break

    return list(affected)
```

## 6. 错误处理

### 6.1 网络错误

- Git 克隆/拉取失败：重试 3 次，失败后提示用户
- NotebookLM 上传失败：记录失败的文档，下次同步时重试

### 6.2 文件错误

- docs.json 解析失败：提示用户检查文件格式
- 文档文件不存在：跳过该文件，记录警告日志

### 6.3 缓存错误

- 缓存文件损坏：重新初始化缓存
- 缓存与实际状态不一致：提供 `--force-sync` 选项强制全量同步

## 7. 使用流程

### 7.1 首次使用

```bash
# 1. 安装依赖
cd skills/openclaw-docs
uv pip install -r requirements.txt

# 2. 创建 NotebookLM Notebook
notebooklm create --title 'OpenClaw Documentation v2'
# 记录返回的 notebook_id

# 3. 初始化并同步
python scripts/sync_docs.py --notebook-id <notebook_id>
```

### 7.2 定期更新

```bash
# 检查更新
python scripts/check_updates.py

# 同步更新
python scripts/sync_docs.py
```

### 7.3 查询文档

```bash
python scripts/query_docs.py "如何配置 Discord 频道？"
```

## 8. 实现优先级

### Phase 1：核心功能（MVP）
1. init_repo.py - 仓库管理
2. parse_docs.py - 文档解析
3. merge_docs.py - 文档合并
4. sync_docs.py - 基础同步（不含更新检测）

### Phase 2：增量更新
5. 完善 sync_docs.py - 添加更新检测
6. check_updates.py - 检查更新

### Phase 3：查询和优化
7. query_docs.py - 查询接口
8. 错误处理和日志
9. 性能优化

## 9. 依赖清单

```txt
# requirements.txt
gitpython>=3.1.0
notebooklm-py>=0.1.0
```

## 10. 测试计划

### 10.1 单元测试

- 测试 docs.json 解析
- 测试智能合并策略
- 测试哈希计算
- 测试变更检测

### 10.2 集成测试

- 测试完整的同步流程
- 测试更新检测流程
- 测试 NotebookLM 交互

### 10.3 边界测试

- 空仓库
- docs.json 格式错误
- 网络异常
- NotebookLM 服务异常

## 11. 迁移计划

### 11.1 清理旧代码

**删除以下目录：**
- `docs/` - 整个目录（包含所有旧的 HTML 文件）

**删除以下脚本文件：**
- `scripts/sync_docs.py` - 旧版同步脚本
- `scripts/check_updates.py` - 旧版检查更新脚本
- `scripts/query_docs.py` - 旧版查询脚本
- `scripts/download_docs.py` - 下载文档脚本
- `scripts/check_git_updates.py` - Git 更新检查脚本
- `scripts/clone_and_merge.py` - 克隆合并脚本
- `scripts/extract_en_docs.py` - 提取英文文档脚本
- `scripts/sync_docs_v2.py` - 同步脚本 v2

**删除以下配置/缓存文件：**
- `references/config.json` - 旧配置文件
- `references/notebooklm_cache.json` - 旧缓存文件

**保留以下文件：**
- `references/DOCS_JSON_STRUCTURE.md` - docs.json 结构说明文档
- `SKILL.md` - Skill 说明（需要更新）
- `README.md` - 使用文档（需要更新）
- `requirements.txt` - 依赖清单（需要更新）
- `.gitignore` - Git 忽略配置（已创建）

**清理命令：**
```bash
# 进入 skill 目录
cd skills/openclaw-docs

# 删除旧的 docs 目录
rm -rf docs/

# 删除旧的脚本文件
rm -f scripts/sync_docs.py \
      scripts/check_updates.py \
      scripts/query_docs.py \
      scripts/download_docs.py \
      scripts/check_git_updates.py \
      scripts/clone_and_merge.py \
      scripts/extract_en_docs.py \
      scripts/sync_docs_v2.py

# 删除旧的配置和缓存
rm -f references/config.json \
      references/notebooklm_cache.json
```

### 11.2 创建 .gitignore

```
# .gitignore
repo/
*.pyc
__pycache__/
.DS_Store
```

### 11.3 更新文档

- 更新 SKILL.md
- 更新 README.md

## 12. 风险和注意事项

### 12.1 风险

1. **NotebookLM 文件数量限制**：需要确认 NotebookLM 单个 Notebook 的文件数量限制
2. **文件大小限制**：合并后的文件可能较大，需要确认 NotebookLM 的文件大小限制
3. **Git 仓库大小**：克隆完整仓库可能较大，考虑使用 `--depth=1` 浅克隆

### 12.2 注意事项

1. **repo/ 目录必须被 ignore**：避免提交到版本控制
2. **缓存文件的一致性**：确保 merge_cache 和 sync_cache 保持同步
3. **NotebookLM 文件 ID 管理**：文件 ID 是更新的关键，必须妥善保存

## 13. 未来优化方向

1. **并行处理**：合并和上传可以并行处理，提升性能
2. **增量合并**：只重新合并受影响的文档，而不是全部重新合并
3. **本地预览**：提供本地预览合并后的文档
4. **多语言支持**：未来可以扩展支持其他语言
5. **自动化定时任务**：提供 cron 配置示例

## 14. 总结

本设计方案通过以下核心改进，实现了更灵活、可控的文档管理：

1. **直接从源头获取**：从 GitHub 仓库拉取，不依赖文档站
2. **精确语言控制**：只处理英文文档
3. **智能合并策略**：根据文档结构动态决定合并粒度
4. **精确更新检测**：通过 git diff 精确识别变更
5. **完整的缓存机制**：支持增量更新，避免重复上传

该方案已经过充分设计，可以直接进入实现阶段。
