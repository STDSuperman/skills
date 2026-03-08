---
name: openclaw-docs
description: OpenClaw 文档配置大师，从 GitHub 仓库自动同步 OpenClaw 官方英文文档到 NotebookLM 并提供智能查询功能。当用户需要查询 OpenClaw 文档、同步 OpenClaw 文档、检查文档更新，或询问关于 OpenClaw 配置和使用的问题时使用此 skill。
---

# OpenClaw 文档配置大师

## 概述

此 skill 提供 OpenClaw 官方文档的自动化管理功能，包括：
- 从 GitHub 仓库克隆和更新 OpenClaw 文档
- 解析 docs.json 提取英文文档结构
- 智能合并文档（Group ≤5 按 Tab 合并，>5 按 Group 合并）
- 自动同步文档到 NotebookLM
- 通过 NotebookLM 进行文档查询

## 核心功能

### 1. 同步文档

使用 `sync_docs.py` 脚本同步 OpenClaw 文档到 NotebookLM：

```bash
python scripts/sync_docs.py
```

**工作流程：**
1. 检查 notebooklm CLI 是否可用
2. 从 GitHub 克隆或更新 openclaw 仓库
3. 解析 docs.json 提取英文文档结构
4. 根据智能策略合并文档：
   - Group 数量 ≤5：整个 Tab 合并为一个文件
   - Group 数量 >5：每个 Group 单独合并
5. 检测文档变更（基于内容哈希）
6. 同步到 NotebookLM（只上传变更的文档）
7. 更新缓存文件

**首次使用：**
首次运行会提示创建或输入 Notebook ID：
```
1. 输入现有 Notebook ID
2. 创建新的 Notebook
```

### 2. 智能合并策略

文档合并遵循以下规则：
- **Tab 合并**：当 Tab 下的 Group 数量 ≤5 时，将整个 Tab 的所有文档合并为一个文件
- **Group 合并**：当 Tab 下的 Group 数量 >5 时，每个 Group 单独合并为一个文件
- **优势**：减少 NotebookLM 的文档数量，提高查询效率

## 工作原理

### 架构设计

```
GitHub Repo (openclaw/openclaw)
    ↓ clone/pull
本地仓库 (repo/openclaw/)
    ↓ parse
docs.json 解析
    ↓ merge
智能合并文档
    ↓ sync
NotebookLM
```

### 核心模块

1. **init_repo.py** - 仓库管理器
   - 克隆 GitHub 仓库（浅克隆，depth=1）
   - 更新仓库到最新版本
   - 获取变更文件列表

2. **parse_docs.py** - 文档解析器
   - 解析 docs.json 提取英文文档结构
   - 支持 .mdx 和 .md 文件
   - 按 Tab 和 Group 组织文档

3. **merge_docs.py** - 文档合并器
   - 智能合并策略（基于 Group 数量）
   - 计算内容哈希用于变更检测
   - 生成合并缓存

4. **sync_docs.py** - 同步管理器
   - 检测文档变更
   - 上传/删除文档到 NotebookLM
   - 更新同步缓存

### 缓存机制

**merge_cache.json** - 合并缓存
```json
{
  "merged_docs": {
    "Get_started.md": {
      "merge_type": "tab",
      "source_files": ["docs/index.mdx", "docs/start/showcase.mdx"],
      "content_hash": "abc123...",
      "last_updated": "2024-03-08T10:00:00"
    }
  },
  "last_merge": "2024-03-08T10:00:00"
}
```

**sync_cache.json** - 同步缓存
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

## 配置文件

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
缓存合并文档的元数据（自动生成）

### references/sync_cache.json
缓存同步状态（自动生成）

## 依赖安装

```bash
pip install -r requirements.txt
```

主要依赖：
- `gitpython`: 管理 Git 仓库
- `notebooklm-py`: NotebookLM CLI 工具

## 使用示例

**示例 1：首次同步**
```bash
# 运行同步脚本
python scripts/sync_docs.py

# 脚本会提示创建或输入 Notebook ID
# 输入后会自动保存，后续无需再次输入
```

**示例 2：更新文档**
```bash
# 直接运行同步脚本
python scripts/sync_docs.py

# 脚本会自动：
# 1. 更新 GitHub 仓库
# 2. 检测文档变更
# 3. 只上传变更的文档
```

## 注意事项

1. **Notebook ID 管理**：首次运行会要求输入 Notebook ID，建议创建专门的 Notebook 用于 OpenClaw 文档
2. **增量更新**：脚本会自动识别新增和更新的文档，避免重复上传
3. **网络要求**：需要能够访问 GitHub
4. **CLI 依赖**：确保 `notebooklm` CLI 可以正常使用
5. **仓库目录**：repo/ 目录已被 .gitignore 忽略，不会提交到版本控制
