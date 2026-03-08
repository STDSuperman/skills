# OpenClaw 文档配置大师

自动同步 OpenClaw 官方文档到 NotebookLM 并提供智能查询功能。

## 功能特性

- 🔄 自动从 https://docs.openclaw.ai 获取文档列表
- 🧠 智能检测文档更新（基于 sitemap.xml 的 lastmod 时间）
- 📤 自动同步文档到 NotebookLM
- 🔍 通过 NotebookLM 进行智能文档查询
- 💾 本地缓存，避免重复上传
- 🔧 自动检测并安装 NotebookLM CLI

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

首次运行时，脚本会提示你创建或输入 Notebook ID：

```bash
# 创建新的 Notebook
notebooklm create --title 'OpenClaw Documentation'

# 或列出现有的 Notebooks
notebooklm list
```

输入 Notebook ID 后，会自动保存到 `references/config.json`，后续无需再次输入。

### 3. 查询文档

```bash
python scripts/query_docs.py "如何配置 OpenClaw 的认证？"
```

## 使用场景

### 场景 1：定期同步文档

设置定时任务自动同步文档：

**Linux/Mac (crontab):**
```bash
0 */6 * * * cd /path/to/skills/openclaw-docs && python scripts/sync_docs.py
```

**Windows (Task Scheduler):**
创建计划任务，每 6 小时运行一次 `sync_docs.py`

### 场景 2：检查文档更新

在同步前快速检查是否有更新：

```bash
python scripts/check_updates.py
```

输出示例：
```
正在检查 OpenClaw 文档更新...

============================================================
文档总数: 45
已缓存: 40
新增文档: 3
更新文档: 2
上次同步: 2024-03-08T10:30:00Z

新增文档:
  - https://docs.openclaw.ai/new-feature
  - https://docs.openclaw.ai/api-v2
  - https://docs.openclaw.ai/migration-guide

更新文档:
  - https://docs.openclaw.ai/getting-started
  - https://docs.openclaw.ai/authentication
============================================================

💡 运行 sync_docs.py 进行同步
```

### 场景 3：在 Claude Code 中使用

当你在 Claude Code 中询问 OpenClaw 相关问题时，skill 会自动触发：

```
用户: OpenClaw 支持哪些认证方式？
Claude: [自动使用 openclaw-docs skill 查询文档并回答]
```

## 目录结构

```
openclaw-docs/
├── SKILL.md                          # Skill 说明文档
├── requirements.txt                  # Python 依赖
├── scripts/
│   ├── sync_docs.py                 # 文档同步脚本
│   ├── check_updates.py             # 检查更新脚本
│   └── query_docs.py                # 文档查询脚本
└── references/
    ├── config.json                  # 配置文件（存储 Notebook ID）
    └── notebooklm_cache.json        # 缓存文件（存储已上传文档）
```

## 配置文件说明

### references/config.json

存储 NotebookLM Notebook ID：

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

## 工作原理

1. **获取文档列表**：从 https://docs.openclaw.ai/sitemap.xml 解析所有文档 URL
2. **检查更新**：对比 sitemap 中的 `lastmod` 时间与本地缓存
3. **增量同步**：只上传新增或更新的文档到 NotebookLM
4. **更新缓存**：记录上传时间和文档元数据
5. **智能查询**：通过 NotebookLM CLI 查询文档内容

## 注意事项

1. **Notebook ID 管理**：建议创建专门的 Notebook 用于 OpenClaw 文档
2. **网络要求**：需要能够访问 https://docs.openclaw.ai
3. **CLI 依赖**：确保 `notebooklm` CLI 可以正常使用
4. **增量更新**：脚本会自动识别新增和更新的文档，避免重复上传

## 故障排除

### NotebookLM CLI 未安装

脚本会自动检测并安装，如果失败可以手动安装：

```bash
pip install notebooklm-py
```

### 无法访问 sitemap.xml

检查网络连接，确保可以访问 https://docs.openclaw.ai/sitemap.xml

### Notebook ID 丢失

重新运行 `sync_docs.py`，脚本会提示你输入 Notebook ID

## 开发

### 测试脚本

```bash
# 测试同步脚本
python scripts/sync_docs.py

# 测试检查更新
python scripts/check_updates.py

# 测试查询功能
python scripts/query_docs.py "test query"
```

## License

MIT
