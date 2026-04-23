---
name: claude-md-best-practices
description: Use this skill whenever the user wants to create, write, generate, review, optimize, slim down, audit, score, or revise a CLAUDE.md (or AGENTS.md / GEMINI.md) file for a project. Trigger on phrases like "帮我写 CLAUDE.md"、"生成 claude.md"、"优化我的 CLAUDE.md"、"CLAUDE.md 太长了"、"review 这份 CLAUDE.md"、"audit CLAUDE.md"、"给 CLAUDE.md 打个分"、"更新 CLAUDE.md"、"项目需要加一份 Claude 配置"、"AGENTS.md 最佳实践"、"帮我维护 CLAUDE.md"、"CLAUDE.md 最佳实践"、session learnings capture、会话学习沉淀 — even when the user does not explicitly name this skill. Also use when the user is setting up a new project's agent instruction file, or when an existing one seems bloated, outdated, or ineffective.
tools: Read, Glob, Grep, Bash, Edit, AskUserQuestion
---

# CLAUDE.md / AGENTS.md 最佳实践

## 第一性原理

> 只保留"Claude 离开它就一定会犯错"的信息。

其他信息用 `@path` 引用到 `docs/` 下的详细文档，不占默认上下文。

---

## 何时用 / 场景路由表

| 场景 | 流程 | 详见 |
|------|------|------|
| 没有 CLAUDE.md | §A 生成 | 本文件 + [references/templates.md](references/templates.md) |
| 有但需审查/评分/优化 | §B 5-Phase 审查 | [references/quality-criteria.md](references/quality-criteria.md) + [references/update-guidelines.md](references/update-guidelines.md) |
| 会话结束沉淀学习 | §C 捕获 | [references/session-capture.md](references/session-capture.md) |

先用 `ls` / `Read` 判断 `./CLAUDE.md` 是否存在，再选分支。禁止未确认就覆盖已有文件。

---

## 通用原则（8 条）

1. **长度**：控制在 200 行以内，理想 60–150 行。超出时逐行问："删掉它 Claude 会犯错吗？"不会 → 删掉或移到 `docs/`。
2. **结构**：建议 Commands / Architecture / Conventions / Gotchas / Verification 五段，或 WHAT / WHY / HOW 三段。按项目实际选用，不生搬硬套。
3. **应该写**：精确可复制的命令、核心目录结构、与默认值不同的约定、非显而易见的坑、验证方式。
4. **不要写**：Claude 能从代码推断的内容、通用编程常识、从 README 复制的项目介绍（用 `@README.md` 引用）、频繁变化的信息、长段落散文（一律改 bullet）。
5. **拆分**：复杂项目用 `@docs/xxx.md` 拆分，被 import 的文件按需加载，不占默认上下文。
6. **文件位置**：
   - `./CLAUDE.md` — 项目级，提交 Git
   - `./CLAUDE.local.md` — 个人笔记，加入 `.gitignore`
   - `~/.claude/CLAUDE.md` — 全局偏好
   - 子目录 `CLAUDE.md` — 该目录范围生效（monorepo 很有用）
   - `./packages/*/CLAUDE.md` — monorepo 子包专用
7. **强调词分级**：只在 Claude 多次忽略某条规则时，才升级到 `MUST` / `NEVER`。一开始就堆强调词会稀释效果。
8. **机械约束优先于散文**：能用 lint / hook / CI 强制的规则，CLAUDE.md 里只写"运行 `npm run lint` 必须通过"，具体规则交给工具链。

---

## §A 从零生成 CLAUDE.md

### A.1 信息采集（必做）

尽量用工具自动探测，不要问用户已能从代码推断的问题：

1. **技术栈**：读 `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml`
2. **包管理器**：看 lockfile（`pnpm-lock.yaml` → pnpm，`bun.lockb` → bun，`uv.lock` → uv）
3. **脚本命令**：从 `package.json` 的 `scripts`、`Makefile`、`justfile` 提取
4. **核心目录**：用 `ls` 探测 `src/`, `apps/`, `packages/` 等顶层结构
5. **测试框架**：从依赖推断（vitest / jest / pytest / go test）
6. **已有文档**：看 `README.md`、`docs/` 里有无架构说明，有就用 `@` 引用

只有无法自动探测的信息才用 `AskUserQuestion` 询问，例如：
- 团队硬性规范（"禁止引入 Redux"）
- 架构决策的理由
- 部署约束、敏感的业务坑

一次最多问 3–4 个最关键的问题。

### A.2 选档位并生成

根据项目规模选择档位，详细模板见 [references/templates.md](references/templates.md)：

- **极简档**（约 30 行）— 新项目、小工具、Demo
- **标准档**（约 100–150 行）— 绝大多数业务项目
- **企业级档**（根文件精简 + `docs/standards/` 拆分）— 多人协作、有完整工程规范
- **Package 模板** — monorepo 内的单个包
- **Monorepo 根模板** — monorepo 根目录

### A.3 自检清单

交付前逐项确认：

- [ ] 行数 ≤ 200
- [ ] 每条规则都通过"删掉会不会犯错"测试
- [ ] 命令全部可复制，无 `<your-token>` 占位符
- [ ] 用 bullet，不用大段落
- [ ] 没有复制 README 内容
- [ ] 频繁变动的内容已用 `@` 引用
- [ ] 创建了 `.local.md` 的话，已提醒加入 `.gitignore`

---

## §B 审查/优化（5-Phase）

### Phase 1：Discovery

找到仓库中所有 CLAUDE.md 文件：

```bash
find . -name "CLAUDE.md" -o -name ".claude.md" -o -name ".claude.local.md" 2>/dev/null | head -50
```

文件类型速查：

| 类型 | 位置 | 用途 |
|------|------|------|
| 项目根 | `./CLAUDE.md` | 主要项目上下文，提交 Git |
| 本地覆盖 | `./.claude.local.md` | 个人/本地设置，gitignore |
| 全局默认 | `~/.claude/CLAUDE.md` | 跨项目的用户全局默认 |
| 子包专用 | `./packages/*/CLAUDE.md` | monorepo 模块级上下文 |
| 子目录 | 任意嵌套位置 | 功能/领域专用上下文 |

### Phase 2：Quality Assessment

对每个 CLAUDE.md 按 6 个维度打分（满分 100）。
详细评分标准见 [references/quality-criteria.md](references/quality-criteria.md)。

评分时必须对 build / test / lint 等关键命令**实际运行验证**，不能只靠目测判断。

### Phase 3：Quality Report

必须在任何修改之前输出完整的质量报告，格式如下：

```
## CLAUDE.md Quality Report

### Summary
- Files found: X
- Average score: X/100
- Files needing update: X

### File-by-File Assessment

#### 1. ./CLAUDE.md (Project Root)
**Score: XX/100 (Grade: X)**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Commands/workflows | X/20 | ... |
| Architecture clarity | X/20 | ... |
| Non-obvious patterns | X/15 | ... |
| Conciseness | X/15 | ... |
| Currency | X/15 | ... |
| Actionability | X/15 | ... |

**Issues:**
- [具体问题列表，标注行号]

**Recommended additions:**
- [建议新增的内容]
```

### Phase 4：Propose Diffs

报告输出后，等用户确认，再提出具体修改建议。
使用 [references/update-guidelines.md](references/update-guidelines.md) 规定的三段式 diff 格式（File → Diff → Why）。

重点关注：
- 真正有用的命令和工作流
- 已验证的 Gotchas 和非显而易见的模式
- 包依赖关系和架构知识

避免：
- 重述代码已有的信息
- 通用最佳实践
- 一次性修复记录

### Phase 5：Apply with Approval

用户明确确认后，使用 `Edit` 工具精确替换，保留原有文件结构。
改完后再跑一次 §A.3 自检清单。

---

## §C 会话学习捕获

详见 [references/session-capture.md](references/session-capture.md)。

简要流程：
1. **Reflect** — 回顾本次会话的 5 类信号（命令/风格/测试/环境/Gotchas）
2. **Find** — `find . -name "CLAUDE.md" -o -name ".claude.local.md"`，决定写入哪一层
3. **Draft** — 每条一行，格式 `<cmd or pattern> — <brief>`
4. **Show** — 用三段式 diff 格式展示建议
5. **Apply** — 用户同意后才改

写入前必须通过"第一性原理删除测试"：删掉这条，下一个 Claude 会话会犯错吗？

---

## 交付 Tips（告诉用户的 5 条）

1. **`#` 快捷键**：会话中按 `#` 可触发 Claude 自动沉淀学习到 CLAUDE.md
2. **`.local.md` 隔离**：个人偏好写 `CLAUDE.local.md`，加入 `.gitignore`
3. **全局偏好**：跨项目的个人设置写到 `~/.claude/CLAUDE.md`
4. **命令精度**：所有命令必须可直接复制，不留 `<placeholder>`
5. **简洁 > 冗长**：CLAUDE.md 是提示词的一部分，冗长会稀释重要信息

---

## 最终裁决

判断一条内容是否放入 CLAUDE.md：

- 不知道它 → 写出**错误**代码 → **放 CLAUDE.md**
- 不知道它 → 写出**不够好**的代码 → 放 `docs/`，CLAUDE.md 用 `@` 引用
- 能从代码推断出来 → **不写**

把这一条作为执行 §A / §B / §C 时的最终裁决依据。
