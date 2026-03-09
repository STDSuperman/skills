# OpenClaw Docs Skill - Phase 1 MVP 测试指南

**日期**: 2026-03-08
**版本**: Phase 1 MVP
**状态**: 已完成实现，待测试

## 一、完成工作总结

### 1.1 重构概述

将 openclaw-docs skill 从基于 sitemap 的方案重构为基于 GitHub 仓库的方案。

**核心变更**:
- ✅ 从 GitHub 克隆 openclaw 仓库（浅克隆）
- ✅ 解析 docs.json 提取英文文档结构
- ✅ 智能合并文档（Group ≤5 按 Tab，>5 按 Group）
- ✅ 基于内容哈希的增量更新
- ✅ 完整的缓存机制

### 1.2 实现的模块

| 模块 | 文件 | 代码行数 | 状态 |
|------|------|----------|------|
| 仓库管理器 | init_repo.py | 103 | ✅ 完成 |
| 文档解析器 | parse_docs.py | 152 | ✅ 完成 |
| 文档合并器 | merge_docs.py | 199 | ✅ 完成 |
| 同步管理器 | sync_docs.py | 326 | ✅ 完成 |

**总计**: 780+ 行 Python 代码

### 1.3 Git 提交历史

```
a7f1b2d - docs: 更新文档以反映新实现
c713adf - feat: 实现同步管理器
a1f38dc - feat: 实现文档合并器
a22941a - feat: 实现文档解析器
4efcf70 - feat: 实现仓库管理器
dd45f98 - feat: 更新依赖列表
cb0d5eb - feat: 创建新的目录结构和配置文件
771268a - chore: 清理 openclaw-docs 旧文件
```

## 二、测试前准备

### 2.1 环境要求

- Python 3.8+
- Git
- 网络连接（访问 GitHub）
- NotebookLM CLI（可选，用于完整测试）

### 2.2 安装依赖

```bash
cd skills/openclaw-docs
pip install -r requirements.txt
```

**依赖包**:
- gitpython>=3.1.0
- notebooklm-py>=0.1.0

### 2.3 检查初始状态

```bash
# 检查目录结构
ls -la skills/openclaw-docs/

# 应该看到:
# - scripts/ (包含 4 个 .py 文件)
# - references/ (包含配置和缓存文件)
# - .gitignore
# - README.md
# - SKILL.md
# - requirements.txt
```

## 三、测试步骤

### 3.1 测试 1: 仓库管理器

**目的**: 验证能否成功克隆 openclaw 仓库

```bash
cd skills/openclaw-docs
python scripts/init_repo.py
```

**预期结果**:
```
正在克隆仓库: https://github.com/openclaw/openclaw
目标路径: /path/to/skills/openclaw-docs/repo/openclaw
克隆完成，当前 commit: abc12345

结果:
  有更新: True
  当前 commit: abc12345
```

**验证**:
```bash
# 检查仓库是否存在
ls -la skills/openclaw-docs/repo/openclaw/

# 应该看到 openclaw 仓库的内容
# 包括 docs/ 目录和 docs/docs.json 文件
```

**可能的问题**:
- ❌ 网络连接失败 → 检查网络，确保能访问 GitHub
- ❌ 权限问题 → 检查目录权限

---

### 3.2 测试 2: 文档解析器

**目的**: 验证能否正确解析 docs.json

```bash
python scripts/parse_docs.py
```

**预期结果**:
```
正在解析 docs.json...

找到 X 个 Tab:
  - Get started: Y groups, Z pages
  - API Reference: Y groups, Z pages
  ...

正在解析文档文件...

文档文件统计:
  - Get started: N files
  - API Reference: M files
  ...

总计: XX 个文档文件
```

**验证**:
- ✅ 能够找到多个 Tab
- ✅ 每个 Tab 都有 groups 和 pages
- ✅ 文档文件数量合理（>0）

**可能的问题**:
- ❌ 找不到 docs.json → 检查仓库是否正确克隆
- ❌ 解析失败 → 检查 docs.json 格式是否正确

---

### 3.3 测试 3: 文档合并器

**目的**: 验证智能合并策略是否正常工作

```bash
python scripts/merge_docs.py
```

**预期结果**:
```
正在解析文档结构...
正在合并文档...

合并结果:
  生成文件数: X
  - Get_started.md: XXXXX bytes, Y source files (tab)
  - API_Reference_Authentication.md: XXXXX bytes, Z source files (group)
  ...

缓存已保存到: /path/to/merge_cache.json
```

**验证**:
```bash
# 检查缓存文件
cat skills/openclaw-docs/references/merge_cache.json

# 应该看到:
# - merged_docs 对象
# - 每个文档的 merge_type, source_files, content_hash
# - last_merge 时间戳
```

**智能合并策略验证**:
- ✅ Group ≤5 的 Tab → merge_type 为 "tab"
- ✅ Group >5 的 Tab → merge_type 为 "group"
- ✅ 每个文档都有 content_hash

**可能的问题**:
- ❌ 生成文件数为 0 → 检查文档解析是否成功
- ❌ 缓存文件格式错误 → 检查 JSON 格式

---

### 3.4 测试 4: 同步管理器（模拟模式）

**目的**: 验证完整流程（不实际上传到 NotebookLM）

**注意**: 此测试需要 NotebookLM CLI，如果未安装会提示错误，这是正常的。

```bash
python scripts/sync_docs.py
```

**预期结果（如果 CLI 未安装）**:
```
=== OpenClaw Docs 同步管理器 ===

1. 检查 notebooklm CLI...
错误: notebooklm CLI 不可用
请先安装: pip install notebooklm-py
```

**预期结果（如果 CLI 已安装）**:
```
=== OpenClaw Docs 同步管理器 ===

1. 检查 notebooklm CLI...
  ✓ CLI 可用

2. 加载配置...
  ✓ 配置加载完成

3. 获取 Notebook ID...
未找到 Notebook ID。
1. 输入现有 Notebook ID
2. 创建新的 Notebook
请选择 (1/2):
```

**验证**:
- ✅ 能够检测 CLI 状态
- ✅ 能够加载配置文件
- ✅ 能够提示用户输入 Notebook ID

---

### 3.5 测试 5: 增量更新机制

**目的**: 验证第二次运行时只上传变更的文档

**步骤**:
1. 第一次运行 sync_docs.py（如果有 CLI）
2. 不做任何修改，第二次运行
3. 观察输出

**预期结果**:
```
变更检测:
  需要上传: 0 个文件
  需要删除: 0 个文件
  未变更: X 个文件
```

**验证**:
- ✅ 第二次运行时，未变更文件数 = 第一次上传的文件数
- ✅ 不会重复上传相同内容的文档

---

## 四、完整测试流程（端到端）

### 4.1 前提条件

- ✅ 已安装 notebooklm-py
- ✅ 有 NotebookLM 账号
- ✅ 网络连接正常

### 4.2 完整流程

```bash
# 1. 清理旧数据（可选）
rm -rf skills/openclaw-docs/repo/
rm -f skills/openclaw-docs/references/merge_cache.json
rm -f skills/openclaw-docs/references/sync_cache.json

# 2. 运行完整同步
cd skills/openclaw-docs
python scripts/sync_docs.py

# 3. 按提示操作
# - 选择创建新 Notebook 或输入现有 ID
# - 等待克隆、解析、合并、上传完成

# 4. 验证结果
# - 检查 NotebookLM 中是否有文档
# - 检查缓存文件是否更新
```

### 4.3 预期完整输出

```
=== OpenClaw Docs 同步管理器 ===

1. 检查 notebooklm CLI...
  ✓ CLI 可用

2. 加载配置...
  ✓ 配置加载完成

3. 获取 Notebook ID...
未找到 Notebook ID。
1. 输入现有 Notebook ID
2. 创建新的 Notebook
请选择 (1/2): 2
请输入 Notebook 名称 (默认: OpenClaw Docs):

正在创建 Notebook: OpenClaw Docs
Notebook 创建成功: nb_abc123
  ✓ Notebook ID 已保存到配置

4. 初始化/更新仓库...
正在克隆仓库: https://github.com/openclaw/openclaw
目标路径: /path/to/repo/openclaw
克隆完成，当前 commit: abc12345

5. 解析文档结构...
  ✓ 找到 X 个 Tab

6. 合并文档...
  ✓ 生成 Y 个合并文档

7. 同步到 NotebookLM...

变更检测:
  需要上传: Y 个文件
  需要删除: 0 个文件
  未变更: 0 个文件

正在上传 Y 个文档...
  ✓ 上传成功: Get_started.md
  ✓ 上传成功: API_Reference_Authentication.md
  ...

8. 更新配置和缓存...
  ✓ 配置和缓存已更新

=== 同步完成 ===
```

## 五、验证清单

### 5.1 功能验证

- [ ] 能够克隆 openclaw 仓库
- [ ] 能够解析 docs.json
- [ ] 能够智能合并文档
- [ ] 能够检测文档变更
- [ ] 能够上传到 NotebookLM（如果有 CLI）
- [ ] 能够保存和更新缓存

### 5.2 文件验证

```bash
# 检查生成的文件
ls -la skills/openclaw-docs/repo/openclaw/
ls -la skills/openclaw-docs/references/

# 应该看到:
# - repo/openclaw/ (克隆的仓库)
# - references/config.json (更新了 last_commit)
# - references/merge_cache.json (合并缓存)
# - references/sync_cache.json (同步缓存)
```

### 5.3 缓存验证

```bash
# 检查 config.json
cat skills/openclaw-docs/references/config.json
# 应该包含: notebook_id, repo_url, repo_path, last_commit, group_threshold

# 检查 merge_cache.json
cat skills/openclaw-docs/references/merge_cache.json
# 应该包含: merged_docs, last_merge

# 检查 sync_cache.json
cat skills/openclaw-docs/references/sync_cache.json
# 应该包含: synced_docs, last_sync
```

## 六、常见问题

### 6.1 网络问题

**问题**: 无法克隆 GitHub 仓库

**解决方案**:
```bash
# 检查网络连接
ping github.com

# 检查 Git 配置
git config --global http.proxy
git config --global https.proxy

# 手动克隆测试
git clone --depth 1 https://github.com/openclaw/openclaw test-clone
```

### 6.2 依赖问题

**问题**: ImportError: No module named 'git'

**解决方案**:
```bash
pip install gitpython
```

**问题**: notebooklm CLI 不可用

**解决方案**:
```bash
pip install notebooklm-py
notebooklm --version
```

### 6.3 权限问题

**问题**: Permission denied

**解决方案**:
```bash
# 检查目录权限
ls -la skills/openclaw-docs/

# 修复权限
chmod -R u+w skills/openclaw-docs/
```

## 七、性能指标

### 7.1 预期性能

| 操作 | 预期时间 | 说明 |
|------|----------|------|
| 克隆仓库 | 10-30秒 | 取决于网络速度 |
| 解析文档 | <1秒 | 本地操作 |
| 合并文档 | 1-5秒 | 取决于文档数量 |
| 上传文档 | 30-120秒 | 取决于文档数量和网络 |
| 总计（首次） | 1-3分钟 | 完整流程 |
| 总计（增量） | 10-30秒 | 无变更时 |

### 7.2 资源使用

- **磁盘空间**: ~50MB（克隆的仓库）
- **内存**: <100MB
- **网络**: ~10-20MB（首次克隆）

## 八、下一步

### 8.1 如果测试成功

1. ✅ 标记 Phase 1 MVP 为完成
2. 📝 记录测试结果
3. 🚀 准备 Phase 2 功能（查询功能）

### 8.2 如果测试失败

1. 📋 记录失败的测试用例
2. 🐛 定位问题原因
3. 🔧 修复并重新测试

## 九、测试报告模板

```markdown
## 测试报告

**测试日期**: YYYY-MM-DD
**测试人员**: [姓名]
**环境**: [操作系统, Python 版本]

### 测试结果

| 测试项 | 状态 | 备注 |
|--------|------|------|
| 仓库管理器 | ✅/❌ | |
| 文档解析器 | ✅/❌ | |
| 文档合并器 | ✅/❌ | |
| 同步管理器 | ✅/❌ | |
| 增量更新 | ✅/❌ | |

### 问题记录

1. [问题描述]
   - 复现步骤: ...
   - 错误信息: ...
   - 解决方案: ...

### 总结

[测试总结]
```

## 十、联系方式

如有问题，请：
1. 检查本测试指南
2. 查看 README.md 和 SKILL.md
3. 检查 Git 提交历史
4. 创建 Issue 或联系开发者
