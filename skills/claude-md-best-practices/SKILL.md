---
name: claude-md-best-practices
description: Use this skill whenever the user wants to create, write, generate, review, optimize, slim down, or audit a CLAUDE.md (or AGENTS.md / GEMINI.md) file for a project. Trigger on phrases like "帮我写 CLAUDE.md"、"生成 claude.md"、"优化我的 CLAUDE.md"、"CLAUDE.md 太长了"、"review 这份 CLAUDE.md"、"项目需要加一份 Claude 配置"、"AGENTS.md 最佳实践" — even when the user does not explicitly name this skill. Also use when the user is setting up a new project's agent instruction file, or when an existing one seems bloated, outdated, or ineffective.
---

# CLAUDE.md 编写最佳实践

本 skill 用于产出一份高杠杆、低噪音的 `CLAUDE.md`。核心第一性原理只有一条：

> **只保留"Claude 离开它就一定会犯错"的信息。**

其他信息用 `@path` 引用到 `docs/` 下的详细文档。

---

## 何时用这个 skill

| 场景 | 走哪条流程 |
|------|-----------|
| 项目根目录**没有** `CLAUDE.md` | 走 §A 生成流程 |
| 项目根目录**已有** `CLAUDE.md` | 走 §B 审查/优化流程 |
| 用户明确说"我要重写" | 走 §A，但以现有文件为素材 |

先用 `ls` / `Read` 判断 `./CLAUDE.md` 是否存在，再选择分支。禁止未确认就覆盖已有文件。

---

## 核心原则（两条流程都要遵守）

1. **长度**：控制在 **200 行以内**，理想 60–150 行。如果写超了，先问自己每一行："删掉它 Claude 会犯错吗？" 不会 → 删掉或移到 `docs/`。
2. **结构**：建议 WHAT / WHY / HOW 三段，或 Commands / Architecture / Conventions / Gotchas / Verification 五段，**按项目实际选用**，不要生搬硬套。
3. **应该写**：
   - 精确可复制的命令（测试、lint、typecheck、dev、build）
   - 核心目录结构与分层
   - **与默认值不同**的约定（命名、导出方式、strict 模式等）
   - 非显而易见的坑（Gotchas）
   - 验证方式（跑哪个测试、截图比对等）
4. **不要写**：
   - Claude 能从代码里推断的东西（函数签名、完整目录树）
   - 通用编程常识（"use meaningful names"）
   - 从 README 复制的项目介绍 —— 用 `@README.md` 引用
   - 频繁变化的信息（会迅速漂移）
   - 长段落散文 —— 一律用 bullet
5. **拆分**：复杂项目用 `@docs/xxx.md` 拆分，被 import 的文件按需加载，不占默认上下文。
6. **位置**：
   - `./CLAUDE.md` → 项目级，提交 Git
   - `./CLAUDE.local.md` → 个人笔记，加入 `.gitignore`
   - `~/.claude/CLAUDE.md` → 全局偏好
   - 子目录 `CLAUDE.md` → 该目录范围生效（monorepo 很有用）
7. **强调词的使用**：只在 Claude 多次忽略某条规则时，才升级到 `**IMPORTANT**` / `**YOU MUST**` / `**NEVER**`。一上来就堆 MUST 会稀释效果。
8. **机械约束优先于散文**：如果某条规则可以用 lint / hook / CI 强制，就在 CLAUDE.md 里只写"运行 `npm run lint` 前必须通过"，具体规则交给工具链。

---

## §A 从零生成 CLAUDE.md

### A.1 信息采集（必做）

按顺序收集以下信息，尽量用工具自动探测，**不要问用户已经能从代码推断的问题**：

1. **技术栈**：读 `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` 等
2. **包管理器**：看 lockfile（`pnpm-lock.yaml` → pnpm，`bun.lockb` → bun，`uv.lock` → uv）
3. **脚本命令**：从 `package.json` 的 `scripts`、`Makefile`、`justfile` 里提取
4. **核心目录**：用 `ls` 探测 `src/`, `apps/`, `packages/` 等顶层结构
5. **测试框架**：从依赖推断（vitest / jest / pytest / go test …）
6. **已有文档**：看 `README.md`, `docs/` 里有没有架构说明，有就用 `@` 引用

**只有无法自动探测的信息才问用户**，例如：
- 团队硬性规范（"禁止引入 Redux"、"必须用 Zod 校验"）
- 架构决策的理由（"为什么选 Drizzle 不选 Prisma"）
- 部署约束、敏感的业务坑

一次最多问 3–4 个最关键的问题，用 `AskUserQuestion` 工具。

### A.2 生成文件

按下方模板产出，**根据项目规模选择档位**：

#### 极简档（~30 行，新项目/小工具）

```markdown
# <ProjectName>

<一句话技术栈描述>

## Commands
- `<cmd>` — <作用>
- ...

## Structure
- `src/xxx/` — <作用>

## Rules
- <与默认不同的硬性约束>
```

#### 标准档（~100–150 行，绝大多数项目）

```markdown
# Project: <Name>

<1–2 句项目定位 + 主要技术栈>

## Commands
- `<dev/test/lint/typecheck/build>` — <作用>
- 提交前必须运行: `<combined command>`

## Architecture
- `src/xxx/` — <作用>
- ...

## Conventions
- <只写与默认不同的约定>

## State / Data / Testing / Git
- <按需分节，每节 3–6 条>

## Do NOT
- <最容易踩坑的禁止项，3–5 条>
```

#### 企业级档（根文件精简 + `docs/standards/` 拆分）

根文件只放命令 + 引用：

```markdown
# Coding Agent Standards

## Commands
- ...

## Code Standards
Follow the standards in `docs/standards/`:
- `code-quality.md`
- `testing.md`
- `security.md`

## Critical Rules (always apply)
- <5–8 条不可违反的底线>
```

### A.3 自检清单

交付前对生成的 CLAUDE.md 逐条确认：

- [ ] 行数 ≤ 200
- [ ] 每条规则都通过"删掉会不会犯错"测试
- [ ] 命令全部是可复制的（没有 `<your-token>` 这种占位符）
- [ ] 用 bullet，不用大段落
- [ ] 没有复制 README 内容
- [ ] 对频繁变动的内容用了 `@` 引用
- [ ] 把 `.local.md` 写进了 `.gitignore`（如果创建了）

---

## §B 审查/优化已有 CLAUDE.md

### B.1 诊断

读取现有文件，按下表给出问题清单：

| 反模式 | 识别信号 | 修复动作 |
|--------|----------|----------|
| 内容过载 | > 200 行，缺乏重点 | 拆到 `docs/*.md`，用 `@` 引用 |
| 信息重复 | 复制了 README / package.json 内容 | 删除，改用 `@README.md` |
| 过度规范 | 规定每行代码怎么写 | 删除通用内容，只保留项目特有 |
| 文档漂移 | 命令/目录与当前代码不一致 | 按实际代码校准 |
| 缺少验证 | 有"必须通过测试"但未指明具体命令 | 补 Verification 节 |
| 散文体过多 | 出现 3 行以上段落 | 改成 bullet |
| 强调词滥用 | 全文大量 MUST/NEVER | 降级为陈述句，仅保留真正的底线规则 |
| 作用域错配 | 个人偏好写在项目 CLAUDE.md 里 | 迁移到 `CLAUDE.local.md` 或 `~/.claude/CLAUDE.md` |

### B.2 输出格式

给用户交付一份审查报告，结构为：

```
## 整体评估
<一句话结论 + 当前行数 / 目标行数>

## 发现的问题
1. [行号区间] <问题类型>: <具体说明>
   建议: <具体修复>

## 建议拆分
- 原 `XX` 节 → 迁移到 `docs/xxx.md`，用 `@docs/xxx.md` 引用

## 建议新增
- <项目明显缺失但应该有的内容>

## 修订后示例
<直接给出优化后的 CLAUDE.md 全文 或 diff>
```

### B.3 动手修改前

- 先给报告，**等用户确认**再改文件
- 改文件时用 `Edit` 工具精确替换，不要全量 `Write` 覆盖，除非是大规模重写
- 修订后再跑一次 §A.3 自检清单

---

## 常见交付细节

1. **语言**：CLAUDE.md **本身建议用英文写**（社区惯例，模型遵从更稳），但与用户对话仍用简体中文。如果用户明确要求中文 CLAUDE.md，照办即可。
2. **命令精度**：写死具体命令，例如 `pnpm test -- --run src/components/Button.test.tsx` 而不是"跑某个文件的测试"。
3. **引用语法**：`@path/to/file` 且路径必须存在；产出前验证这些文件真的存在。
4. **.local.md**：生成 `CLAUDE.local.md` 时主动提醒把它加进 `.gitignore`。
5. **Monorepo**：顶层 `CLAUDE.md` 写公共约定，子包单独放 `apps/xxx/CLAUDE.md` 写该包特有内容，避免父文件膨胀。

---

## 判断标准（再强调一次）

判断一条内容放不放 CLAUDE.md：

- 不知道它 → 写出**错误**代码 ⇒ **放 CLAUDE.md**
- 不知道它 → 写出**不够好**的代码 ⇒ 放 `docs/`，CLAUDE.md 用 `@` 引用
- 从代码就能推断出来 ⇒ **不写**

把这一条作为执行任何 §A / §B 工作时的最终裁决依据。
