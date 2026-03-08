# OpenClaw Docs Skill 重构实现计划 - Part 2

> 这是实现计划的第二部分，补充 Task 6-8 的完整步骤

## Task 6 (续): 完成文档合并器

**Step 3: 补充 merge_docs.py 的测试代码和主函数**

在 merge_docs.py 末尾添加：

```python
if __name__ == '__main__':
    import sys
    sys.path.append(str(SCRIPT_DIR))
    from parse_docs import parse_docs_json

    config_file = SKILL_DIR / 'references' / 'config.json'
    with open(config_file) as f:
        config = json.load(f)

    repo_path = SKILL_DIR / config['repo_path']
    docs_json = repo_path / 'docs' / 'docs.json'
    docs_dir = repo_path / 'docs'

    print("正在解析文档结构...")
    structure = parse_docs_json(docs_json)

    print("正在合并文档...")
    merged_docs = process_all_tabs(structure, docs_dir, config['group_threshold'])

    print(f"\n合并结果:")
    print(f"  生成文件数: {len(merged_docs)}")
    for filename, doc_info in merged_docs.items():
        content_size = len(doc_info['content'])
        source_count = len(doc_info['source_files'])
        print(f"  - {filename}: {content_size} bytes, {source_count} source files ({doc_info['merge_type']})")

    # 保存到 merge_cache.json
    cache_file = SKILL_DIR / 'references' / 'merge_cache.json'
    cache_data = {
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

    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, indent=2, ensure_ascii=False)

    print(f"\n缓存已保存到: {cache_file}")
```

**Step 4: 测试文档合并**

```bash
cd skills/openclaw-docs
python scripts/merge_docs.py
```

Expected: 显示合并统计信息，生成 merge_cache.json

**Step 5: 验证合并缓存**

```bash
cat references/merge_cache.json | head -50
```

Expected: 看到合并文档的元数据

**Step 6: Commit**

```bash
git add scripts/merge_docs.py references/merge_cache.json
git commit -m "feat: 实现文档合并器

- 智能合并策略(Group ≤5 按 Tab, >5 按 Group)
- 计算内容哈希用于变更检测
- 保存合并缓存

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 7: 实现同步管理器 (sync_docs.py)

**Files:**
- Create: `skills/openclaw-docs/scripts/sync_docs.py`

**说明:** 由于 sync_docs.py 代码较长，这里提供核心框架。完整代码参考设计文档。

**Step 1: 创建 sync_docs.py 核心函数**

创建包含以下函数的文件：
- `check_notebooklm_cli()` - 检查 CLI 可用性
- `get_or_create_notebook_id()` - 获取或创建 Notebook
- `upload_to_notebooklm()` - 上传文档
- `delete_from_notebooklm()` - 删除文档
- `detect_changes()` - 检测变更
- `sync_to_notebooklm()` - 同步主函数

**Step 2: 创建主执行流程**

```python
if __name__ == '__main__':
    # 1. 检查 CLI
    # 2. 加载配置
    # 3. 获取/创建 Notebook ID
    # 4. 初始化仓库
    # 5. 解析文档
    # 6. 合并文档
    # 7. 同步到 NotebookLM
    # 8. 更新配置
```

**Step 3: 测试同步功能**

```bash
python scripts/sync_docs.py
```

Expected:
- 提示创建或输入 Notebook ID
- 成功同步文档
- 更新 sync_cache.json 和 config.json

**Step 4: Commit**

```bash
git add scripts/sync_docs.py references/sync_cache.json references/config.json
git commit -m "feat: 实现同步管理器

- 支持创建或使用现有 Notebook
- 检测文档变更并同步
- 更新同步缓存

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 8: 更新文档

**Files:**
- Modify: `skills/openclaw-docs/SKILL.md`
- Modify: `skills/openclaw-docs/README.md`

**Step 1: 更新 SKILL.md**

关键更新点：
- 更新描述：说明从 GitHub 仓库拉取
- 更新核心功能：智能合并策略
- 更新使用示例：新的脚本名称

**Step 2: 更新 README.md**

关键更新点：
- 更新功能特性列表
- 更新快速开始步骤
- 更新目录结构
- 更新工作原理说明

**Step 3: Commit**

```bash
git add SKILL.md README.md
git commit -m "docs: 更新文档以反映新实现

- 更新 SKILL.md 说明新工作流程
- 更新 README.md 使用指南
- 说明智能合并策略

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## 验证和测试

**完整流程测试:**

```bash
# 进入 skill 目录
cd skills/openclaw-docs

# 清理环境（如果需要重新测试）
rm -rf repo/
rm -rf temp/

# 重置配置
cat > references/config.json << 'EOF'
{
  "notebook_id": "",
  "repo_url": "https://github.com/openclaw/openclaw",
  "repo_path": "repo/openclaw",
  "last_commit": "",
  "group_threshold": 5
}
EOF

# 运行完整同步
python scripts/sync_docs.py

# 验证结果
echo "=== 仓库状态 ==="
ls -la repo/openclaw/docs/ | head -20

echo "=== 合并缓存 ==="
cat references/merge_cache.json | head -30

echo "=== 同步缓存 ==="
cat references/sync_cache.json | head -30

echo "=== 配置文件 ==="
cat references/config.json
```

Expected: 所有步骤成功，文档已同步到 NotebookLM

---

## 总结

Phase 1 MVP 实现完成后，openclaw-docs skill 将具备：

✅ **核心功能:**
1. 从 GitHub 仓库克隆和更新
2. 解析 docs.json 提取英文文档结构
3. 智能合并文档（Group ≤5 按 Tab，>5 按 Group）
4. 同步到 NotebookLM
5. 缓存机制避免重复上传

✅ **文件结构:**
```
skills/openclaw-docs/
├── .gitignore
├── SKILL.md (已更新)
├── README.md (已更新)
├── requirements.txt (已更新)
├── scripts/
│   ├── init_repo.py
│   ├── parse_docs.py
│   ├── merge_docs.py
│   └── sync_docs.py
├── references/
│   ├── config.json
│   ├── merge_cache.json
│   ├── sync_cache.json
│   └── DOCS_JSON_STRUCTURE.md
└── repo/ (被 .gitignore)
```

✅ **预期提交:**
- 8 个功能提交
- 清晰的提交历史
- 完整的文档更新

**下一步 (Phase 2):**
- 增量更新检测（基于 git diff）
- check_updates.py 脚本
- query_docs.py 脚本
