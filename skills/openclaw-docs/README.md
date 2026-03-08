# OpenClaw 文档配置大师

从 GitHub 仓库自动同步 OpenClaw 官方英文文档到 NotebookLM 并提供智能查询功能。

## 功能特性

- 🔄 从 GitHub 仓库克隆和更新 OpenClaw 文档
- 📋 解析 docs.json 提取英文文档结构
- 🧩 智能合并文档（Group ≤5 按 Tab 合并，>5 按 Group 合并）
- 📤 自动同步文档到 NotebookLM
- 🔍 通过 NotebookLM 进行智能文档查询
- 💾 本地缓存，避免重复上传
- 🔧 基于内容哈希的增量更新

## 快速开始

### 1. 安装依赖

```bash
cd skills/openclaw-docs
pip install -r requirements.txt
```

### 2. 首次同步

```bash
python scripts/sync_docs.py
```

首次运行时，脚本会：
1. 提示创建或输入 Notebook ID
2. 从 GitHub 克隆 openclaw 仓库
3. 解析并合并英文文档
4. 上传到 NotebookLM

Notebook ID 会自动保存到 `references/config.json`，后续无需再次输入。

## 使用场景

### 场景 1：更新文档

直接运行同步脚本，会自动检测并同步变更：

```bash
python scripts/sync_docs.py
```

脚本会自动：
- 更新 GitHub 仓库
- 检测文档变更（基于内容哈希）
- 只上传变更的文档

### 场景 2：在 Claude Code 中使用

当你在 Claude Code 中询问 OpenClaw 相关问题时，skill 会自动触发：

```
用户: OpenClaw 支持哪些认证方式？
Claude: [自动使用 openclaw-docs skill 查询文档并回答]
```

## 目录结构

```
openclaw-docs/
├── SKILL.md                          # Skill 说明文档
├── README.md                         # 本文件
├── requirements.txt                  # Python 依赖
├── .gitignore                        # Git 忽略文件
├── scripts/
│   ├── init_repo.py                 # 仓库管理器
│   ├── parse_docs.py                # 文档解析器
│   ├── merge_docs.py                # 文档合并器
│   └── sync_docs.py                 # 同步管理器
├── references/
│   ├── config.json                  # 配置文件
│   ├── merge_cache.json             # 合并缓存
│   ├── sync_cache.json              # 同步缓存
│   └── DOCS_JSON_STRUCTURE.md       # docs.json 结构说明
└── repo/                            # 克隆的仓库（被 .gitignore 忽略）
```

## 配置文件说明

### references/config.json

存储 Notebook ID 和仓库配置：

```json
{
  "notebook_id": "your-notebook-id-here",
  "repo_url": "https://github.com/openclaw/openclaw",
  "repo_path": "repo/openclaw",
  "last_commit": "abc123...",
  "group_threshold": 5
}
```

### references/merge_cache.json

缓存合并文档的元数据：

```json
{
  "merged_docs": {
    "Get_started.md": {
      "merge_type": "tab",
      "source_files": ["docs/index.mdx"],
      "content_hash": "abc123...",
      "last_updated": "2024-03-08T10:00:00"
    }
  },
  "last_merge": "2024-03-08T10:00:00"
}
```

### references/sync_cache.json

缓存同步状态：

```json
{
  "synced_docs": {
    "Get_started.md": {
      "content_hash": "abc123...",
      "last_synced": "2024-03-08T10:30:00"
    }
  },
  "last_sync": "2024-03-08T10:30:00"
}
```

## 工作原理

### 架构流程

```
GitHub (openclaw/openclaw)
    ↓ clone/pull (depth=1)
本地仓库 (repo/openclaw/)
    ↓ parse docs.json
英文文档结构
    ↓ 智能合并策略
合并文档 (*.md)
    ↓ 内容哈希检测
变更文档列表
    ↓ sync
NotebookLM
```

### 智能合并策略

- **Tab 合并**：Group 数量 ≤5 时，整个 Tab 合并为一个文件
- **Group 合并**：Group 数量 >5 时，每个 Group 单独合并
- **优势**：减少文档数量，提高查询效率

### 增量更新机制

1. 计算每个合并文档的 SHA256 哈希
2. 对比 sync_cache.json 中的哈希值
3. 只上传哈希值变更的文档
4. 删除不再存在的文档

## 注意事项

1. **Notebook ID 管理**：建议创建专门的 Notebook 用于 OpenClaw 文档
2. **网络要求**：需要能够访问 GitHub
3. **CLI 依赖**：确保 `notebooklm` CLI 可以正常使用
4. **增量更新**：脚本会自动识别新增和更新的文档，避免重复上传
5. **仓库目录**：repo/ 目录已被 .gitignore 忽略

## 故障排除

### NotebookLM CLI 未安装

脚本会自动检测，如果未安装会提示：

```bash
pip install notebooklm-py
```

### 无法访问 GitHub

检查网络连接，确保可以访问 https://github.com/openclaw/openclaw

### Notebook ID 丢失

重新运行 `sync_docs.py`，脚本会提示你输入 Notebook ID

## 开发

### 测试脚本

```bash
# 测试仓库管理
python scripts/init_repo.py

# 测试文档解析
python scripts/parse_docs.py

# 测试文档合并
python scripts/merge_docs.py

# 测试完整同步
python scripts/sync_docs.py
```

## License

MIT
