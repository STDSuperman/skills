---
name: openclaw-docs
description: OpenClaw 文档配置大师，从 GitHub 仓库自动同步 OpenClaw 官方英文文档到 NotebookLM 并提供智能查询功能。当用户需要查询 OpenClaw 文档、同步 OpenClaw 文档、检查文档更新，或询问关于 OpenClaw 配置和使用的问题时使用此 skill。
---

# OpenClaw 文档配置大师

## 概述

此 skill 提供 OpenClaw 官方文档的自动化管理功能，包括：
- 从 GitHub 仓库克隆和更新 OpenClaw 文档
- 验证文档结构（检测框架变更）
- 解析 docs.json 提取英文文档结构
- 智能合并文档（动态调整阈值，确保合并后文档数 < 50）
- 增量检测文档变更（基于文件哈希）
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
3. **验证文档结构**（检测框架是否变更）
4. 解析 docs.json 提取英文文档结构
5. **检测源文件变更**（基于文件哈希）
6. 根据智能策略合并文档：
   - 初始阈值：Group 数量 ≤5 时整个 Tab 合并，>5 时每个 Group 单独合并
   - **动态调整**：如果预估文档数 > 50，自动提高阈值
   - **强制合并**：如果提高阈值仍超过 50，强制所有 Tab 合并为单个文件
   - **增量合并**：只重新合并受影响的文档，未变更的文档复用缓存
7. 检测合并文档变更（基于内容哈希）
8. 同步到 NotebookLM（只上传变更的文档）
9. 更新所有缓存文件

**首次使用：**
首次运行会提示创建或输入 Notebook ID：
```
1. 输入现有 Notebook ID
2. 创建新的 Notebook
```

### 2. 智能合并策略

文档合并遵循以下规则：

**基础策略**：
- **Tab 合并**：当 Tab 下的 Group 数量 ≤ 阈值时，将整个 Tab 的所有文档合并为一个文件
- **Group 合并**：当 Tab 下的 Group 数量 > 阈值时，每个 Group 单独合并为一个文件

**动态调整机制**：
- **初始阈值**：默认为 5（可在 config.json 中配置）
- **自动提高阈值**：如果预估合并后文档数 > 50，自动提高阈值直到文档数 ≤ 50
- **强制合并**：如果提高阈值到 100 仍超过 50 个文档，强制所有 Tab 合并为单个文件
- **硬性限制**：合并后的文档数量必须 < 50

**增量合并优化**：
- 检测原始文档的新增、修改、删除（基于文件哈希）
- 只重新合并受影响的文档
- 未变更的文档直接复用缓存
- 大幅提高同步速度

**优势**：
- 减少 NotebookLM 的文档数量，提高查询效率
- 自动适应文档规模变化
- 增量更新，避免重复处理

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

1. **validate_structure.py** - 文档结构验证器
   - 检测 docs.json 是否存在
   - 验证文档结构是否符合预期
   - 检测框架是否发生根本性变化
   - 如果验证失败，提示需要重新设计解析策略

2. **init_repo.py** - 仓库管理器
   - 克隆 GitHub 仓库（浅克隆，depth=1）
   - 更新仓库到最新版本
   - 获取变更文件列表

3. **parse_docs.py** - 文档解析器
   - 解析 docs.json 提取英文文档结构
   - 支持 .mdx 和 .md 文件
   - 按 Tab 和 Group 组织文档
   - **只处理英文文档**（过滤其他语言）

4. **detect_changes.py** - 文档变更检测器
   - 计算原始文件的 SHA256 哈希
   - 检测文件的新增、修改、删除
   - 找出受影响的合并文档
   - **只检测英文文档**（基于 docs_structure）

5. **merge_docs.py** - 文档合并器
   - 智能合并策略（基于 Group 数量）
   - 动态调整阈值（确保文档数 < 50）
   - 增量合并（只重新合并受影响的文档）
   - 计算内容哈希用于变更检测
   - 生成合并缓存

6. **sync_docs.py** - 同步管理器
   - 协调所有模块的工作流程
   - 检测文档变更
   - 上传/删除文档到 NotebookLM
   - 更新所有缓存

### 缓存机制

所有缓存文件存储在 `cache/` 目录下（已被 .gitignore 忽略）：

**cache/source_cache.json** - 源文件缓存
```json
{
  "source_files": {
    "docs/index.mdx": {
      "file_hash": "abc123...",
      "mtime": 1234567890.0,
      "relative_path": "docs/index.mdx"
    }
  },
  "last_check": "2024-03-08T10:00:00"
}
```

**cache/merge_cache.json** - 合并缓存
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

**cache/sync_cache.json** - 同步缓存
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

### cache/ 目录
缓存文件目录（自动生成，已被 .gitignore 忽略）：
- `cache/source_cache.json` - 源文件元数据缓存
- `cache/merge_cache.json` - 合并文档元数据缓存
- `cache/sync_cache.json` - 同步状态缓存

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
2. **增量更新**：脚本会自动识别新增、修改和删除的文档，避免重复处理
3. **文档结构验证**：每次同步前会验证文档结构，如果检测到框架变更会提示需要重新设计解析策略
4. **动态阈值调整**：合并策略会根据文档数量自动调整，确保最终文档数 < 50
5. **只处理英文文档**：所有模块都只处理英文文档，其他语言文档会被自动过滤
6. **网络要求**：需要能够访问 GitHub
7. **CLI 依赖**：确保 `notebooklm` CLI 可以正常使用
8. **目录说明**：
   - `repo/` - 克隆的仓库目录（已被 .gitignore 忽略）
   - `merged/` - 合并后的文档输出目录（已被 .gitignore 忽略）
   - `cache/` - 缓存文件目录（已被 .gitignore 忽略）
   - 这些目录不会提交到版本控制
