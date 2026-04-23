# 会话学习捕获指南

本指南对应 SKILL.md 的 §C，用于在会话结束时将有价值的发现沉淀到 CLAUDE.md。

---

## 5 步流程

### Step 1：回顾本次会话

在会话结束前，回顾以下 5 类信号，判断哪些值得写入 CLAUDE.md：

| 信号类型 | 示例 |
|----------|------|
| Bash 命令 | 发现了没有记录的构建/测试命令 |
| 代码风格 | 遵守了某个与默认不同的项目约定 |
| 测试方法 | 找到了有效的测试夹具或 mock 模式 |
| 环境/配置 | 踩到了环境变量或配置项的坑 |
| Gotchas | 遇到了非显而易见的依赖顺序或限制 |

**关键问题**：如果下一个 Claude 会话没有这条信息，它会犯错吗？
- 会犯错 → 值得写入
- 只是"没那么好" → 考虑放 docs/，用 `@` 引用
- 能从代码推断 → 不写

### Step 2：找到目标文件

```bash
find . -name "CLAUDE.md" -o -name ".claude.local.md" 2>/dev/null | head -20
```

根据信息性质决定写入位置：

- `./CLAUDE.md` — 团队共享，应提交 Git
- `./.claude.local.md` — 个人/本地，加入 `.gitignore`，不分享给团队
- `~/.claude/CLAUDE.md` — 跨项目的全局个人偏好

对于 monorepo，还要考虑写入子包的 `CLAUDE.md` 而非根文件。

### Step 3：起草新增内容

格式：每条一行，简洁明了。

```
<command or pattern> - <brief description>
```

**避免**：
- 啰嗦的解释（一行搞定的不写两行）
- 显而易见的信息（代码已经说明的不重复）
- 一次性修复（不会复现的问题不记录）

**通过"第一性原理删除测试"**：逐条问自己——删掉这条，下一个 Claude 会话会犯错吗？
不会 → 删掉或不写。

### Step 4：以 Diff 格式展示建议

使用 [update-guidelines.md](update-guidelines.md) 中的三段式格式展示每个建议：

```
File: ./CLAUDE.md
Section: Gotchas（新增到现有 Gotchas 之后）

diff:
+- Tests must run sequentially (`--runInBand`) due to shared DB state

Why: Without this, parallel test runs cause flaky failures that waste
     debugging time.
```

对每条修改都给出明确的"为什么"说明。

### Step 5：等用户确认后再改

展示所有建议后，询问用户是否同意应用。

**只有用户明确确认后，才使用 Edit 工具修改文件。**

---

## 使用技巧

**`#` 快捷键**：在 Claude Code 会话中按 `#`，Claude 会自动触发会话学习捕获流程，
无需手动输入指令。

**`.claude.local.md` 的用途**：
- 个人偏好（比如"我喜欢看详细的步骤说明"）
- 本机特有的路径或环境变量
- 试验性的规则，还不确定是否推广给团队

记得把 `.claude.local.md` 加入 `.gitignore`，避免个人配置污染团队仓库。
