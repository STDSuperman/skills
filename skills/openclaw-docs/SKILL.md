---
name: openclaw-docs
description: OpenClaw 文档配置大师，自动同步 OpenClaw 官方文档到 NotebookLM 并提供智能查询功能。当用户需要查询 OpenClaw 文档、同步 OpenClaw 文档、检查文档更新，或询问关于 OpenClaw 配置和使用的问题时使用此 skill。
---

# OpenClaw 文档配置大师

## 概述

此 skill 提供 OpenClaw 官方文档的自动化管理功能，包括：
- 从 https://docs.openclaw.ai 自动获取文档列表
- 智能检测文档更新（基于 sitemap.xml 的 lastmod 时间）
- 自动同步文档到 NotebookLM
- 通过 NotebookLM 进行文档查询

## 核心功能

### 1. 同步文档

使用 `sync_docs.py` 脚本同步 OpenClaw 文档到 NotebookLM：

```bash
python scripts/sync_docs.py
```

**功能说明：**
- 自动检测 `notebooklm-py` CLI 是否安装，未安装则自动安装
- 首次运行时会提示输入或创建 Notebook ID，之后会保存在 `references/config.json` 中
- 解析 sitemap.xml 获取所有文档链接
- 对比本地缓存，只上传新增或更新的文档
- 更新缓存文件 `references/notebooklm_cache.json`

**首次使用：**
如果没有 Notebook ID，脚本会提示你创建或指定：
```bash
# 创建新的 Notebook
notebooklm create --title 'OpenClaw Documentation'

# 或列出现有的 Notebooks
notebooklm list
```

### 2. 检查更新

使用 `check_updates.py` 快速检查是否有文档更新：

```bash
python scripts/check_updates.py
```

**输出信息：**
- 文档总数
- 已缓存文档数
- 新增文档数量和列表
- 更新文档数量和列表
- 上次同步时间

### 3. 查询文档

使用 `query_docs.py` 通过 NotebookLM 查询文档：

```bash
python scripts/query_docs.py "如何配置 OpenClaw 的认证？"
```

**功能说明：**
- 使用已保存的 Notebook ID 进行查询
- 支持自然语言查询
- 返回 NotebookLM 的智能回答

## 工作流程

### 定时同步工作流

1. **设置定时任务**（用户自行配置）：
   ```bash
   # Linux/Mac (crontab)
   0 */6 * * * cd /path/to/skill && python scripts/sync_docs.py

   # Windows (Task Scheduler)
   # 创建计划任务，每 6 小时运行一次 sync_docs.py
   ```

2. **手动检查更新**：
   ```bash
   python scripts/check_updates.py
   ```

3. **按需同步**：
   ```bash
   python scripts/sync_docs.py
   ```

### 查询工作流

当用户询问 OpenClaw 相关问题时：

1. 使用 `query_docs.py` 查询文档
2. 根据返回结果回答用户问题
3. 如果需要更详细的信息，可以提供文档链接

## 配置文件

### references/config.json
存储 Notebook ID：
```json
{
  "notebook_id": "your-notebook-id-here"
}
```

### references/notebooklm_cache.json
缓存已上传文档的元数据：
```json
{
  "documents": {
    "https://docs.openclaw.ai/page1": {
      "lastmod": "2024-03-08T10:00:00Z",
      "uploaded_at": "2024-03-08T10:30:00Z"
    }
  },
  "last_sync": "2024-03-08T10:30:00Z"
}
```

## 依赖安装

```bash
pip install -r requirements.txt
```

主要依赖：
- `requests`: 获取 sitemap.xml
- `notebooklm-py`: NotebookLM CLI 工具

## 使用示例

**示例 1：首次同步**
```bash
# 运行同步脚本
python scripts/sync_docs.py

# 脚本会提示创建或输入 Notebook ID
# 输入后会自动保存，后续无需再次输入
```

**示例 2：定期检查更新**
```bash
# 检查是否有新文档或更新
python scripts/check_updates.py

# 如果有更新，运行同步
python scripts/sync_docs.py
```

**示例 3：查询文档**
```bash
# 查询 OpenClaw 配置相关问题
python scripts/query_docs.py "OpenClaw 支持哪些认证方式？"

# 查询 API 使用方法
python scripts/query_docs.py "如何使用 OpenClaw API 创建任务？"
```

## 注意事项

1. **Notebook ID 管理**：首次运行会要求输入 Notebook ID，建议创建专门的 Notebook 用于 OpenClaw 文档
2. **增量更新**：脚本会自动识别新增和更新的文档，避免重复上传
3. **网络要求**：需要能够访问 https://docs.openclaw.ai
4. **CLI 依赖**：确保 `notebooklm` CLI 可以正常使用
