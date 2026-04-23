---
name: claude-md-best-practices
description: Use this skill whenever the user wants to create, write, generate, review, optimize, slim down, audit, score, or revise a CLAUDE.md (or AGENTS.md / GEMINI.md) file for a project. Trigger on phrases like "帮我写 CLAUDE.md"、"生成 claude.md"、"优化我的 CLAUDE.md"、"CLAUDE.md 太长了"、"review 这份 CLAUDE.md"、"audit CLAUDE.md"、"给 CLAUDE.md 打个分"、"更新 CLAUDE.md"、"项目需要加一份 Claude 配置"、"AGENTS.md 最佳实践"、"帮我维护 CLAUDE.md"、"CLAUDE.md 最佳实践"、session learnings capture、会话学习沉淀 — even when the user does not explicitly name this skill. Also use when the user is setting up a new project's agent instruction file, or when an existing one seems bloated, outdated, or ineffective.
tools: Read, Glob, Grep, Bash, Edit, AskUserQuestion
---

# CLAUDE.md / AGENTS.md 最佳实践

## 第一性原理

CLAUDE.md 有两类合法内容,只保留以下其一:

1. **项目独有的事实**:这个项目独有(不是通用知识 / 不能从代码推断),且 Claude 离开它就会写错代码。
2. **用户主动声明的规范**:团队 / 用户明确要求 Claude 遵守的代码风格、约定、禁令 —— 即使内容看起来通用,也要保留(承载"团队意志",不是知识复述)。见 §0.0 豁免。

其他信息用 `@path` 引用到 `docs/` 下的详细文档,不占默认上下文。

---

## §0 四道硬 Gate(强制闸门)

**任何一条内容在写入 CLAUDE.md 之前,必须依次通过下面 4 道 Gate。任何一道不通过,该条内容禁止写入。**

本章是 §A / §B / §C 的共同前置,不是结尾的"参考原则"。

### §0.0 · 用户意图豁免(User-Asserted Override,最高优先级)

> **用户主动声明的团队规范 / 代码风格 / 项目约定,即使内容看起来"通用",也必须保留。**

CLAUDE.md 不只是"Claude 需要的事实库",也是**团队意志的载体**。当用户 / 团队主动写入一条规范时,它承载的是"**我们团队已就此达成共识,Claude 必须遵守**"的权威信号,不是通用知识的复述。

**触发豁免的信号(任一即可):**
- 用户明确说"保留这条" / "这是团队规范" / "这是我们的代码风格" / "写进 CLAUDE.md"
- 内容位于明显的团队规范段落(Code Style / Team Conventions / Coding Standards / 团队约定 / 代码风格)
- 审查存量文件时,这条内容是**用户手写加入**的(非模型自动生成、非从 README 复制)
- 用户在对话中直接给出的禁令/偏好("不要用 any""组件一律函数式""注释用中文")

**豁免后的处理:**
- **跳过 G1(独特性)和 G2(可推断性)** —— 因为这两道 Gate 是为了拦截"模型脑补的通用套话",用户主动声明的内容天然不适用。
- **仍需过 G3(稳定性)和 G4(错误代价)**:
  - G3:仍然不允许写当前 bug
  - G4:违反会导致代码被 reject(错)才写主文件;只是"不优雅"(次优)移到 `@docs/code-style.md`
- **建议归入 Conventions / Code Style 段**,不要混进 Gotchas。

**判定例子:**
- 用户说"团队规定函数体不超过 50 行" → 豁免通过 → 写入
- 用户说"我们用 2 空格缩进,不用 tab" → 豁免通过 → 写入(或放 `.editorconfig` 机械约束,用 CLAUDE.md 指向)
- 模型自己脑补"函数要短、注释要清晰" → **不豁免**,黑名单拦截

### G1 · 独特性(Uniqueness)

> "这条属于**通用知识 / 工具文档 / 编程常识**吗?换一个项目,这条还会原样成立吗?"

- **属于通用知识,或在任意项目都成立** → **禁止写入**。Claude 的训练数据里已经有了,写进 CLAUDE.md 等于浪费默认上下文。
- **这个项目(团队/架构/业务)独有的决策或约束** → 通过 G1。

判定例子:
- `git pull` / `npm install` / `uv pip install` —— 通用,不过 G1
- "Python 3.8+" —— `pyproject.toml` 里已声明,不过 G1
- "禁止引入 Redux,统一用 Zustand" —— 团队独有决策,过 G1
- "业务层必须通过 Repository 访问 ORM" —— 项目架构约束,过 G1

### G2 · 可推断性(Inferability)

> "Claude 第一次进这个仓库,读 `package.json` / `pyproject.toml` / `ls` / `README.md`,能自己得出这条结论吗?"

- **能** → **禁止写入**(浪费默认上下文)。
- **不能** → 通过 G2。

### G3 · 稳定性(Stability)

> "这条描述的是**长期存在的事实**,还是**当前存在的 bug / 临时状态**?"

- **Bug / 临时状态** → **禁止写入**。正确动作是**修复**,不是让未来所有 Claude 会话都绕着它走。把 bug 写进 CLAUDE.md 等于固化技术债。
- **长期事实 / 设计约束** → 通过 G3。

### G4 · 错误代价(Error Cost)

> "Claude 不知道这条,会写出**错代码**,还是只是**次优代码**?"

- **错代码**(运行失败 / 语义错误 / 违反团队硬规) → **写 CLAUDE.md**。
- **次优代码**(风格差、能跑) → **写 `@docs/xxx.md`**,不占默认上下文。

### Gate 执行流程

```
候选条目
  ↓
§0.0 用户主动声明的规范? ── 是 → 跳过 G1/G2,直接进 G3
  ↓ 否
G1 独特? ── 否 → 丢弃
  ↓ 是
G2 可推断? ── 是 → 丢弃
  ↓ 否
G3 稳定? ── 否(bug/临时) → 建议修复,不写入
  ↓ 是
G4 错误代价? ── 次优 → 移到 @docs/,主文件仅保留 `@` 引用
  ↓ 错代码 / 违反团队硬规
✅ 写入 CLAUDE.md
```

---

## §0.5 黑名单(这些内容禁止进 CLAUDE.md)

被 G1/G2/G3 频繁拦下的典型反例。看到候选内容命中黑名单,直接拒绝,不必再走 Gate。

| 反例类别 | 示例 | 应去向 |
|---|---|---|
| Git 基础命令 | `git pull` / `git add -A && git commit` / `git push` | 删除(通用常识) |
| 包管理器照抄文档 | `npm install` / `uv pip install -r requirements.txt`(仅此一行) | 删除;只保留项目级差异,如"依赖在 `scripts/` 不在根目录" |
| OS / Shell 常识 | `ls` / `cd` / `mkdir` / `rm` / `ln -s` | 删除 |
| 一次性 setup 步骤 | 初次克隆后建软链接、初始化数据库 | 移到 `README.md` 或 `@docs/setup.md` |
| 完整 ASCII 目录树 | 列出 `src/`, `apps/`, `packages/` 的嵌套结构 | 移到 `@docs/architecture.md`。主文件只写**非显然的架构决策** |
| 当前存在的 bug | "XX 路径错了需要绕开" / "YY 目前不能用" | **修复它**,不要记录它 |
| 从 README 复制的介绍 | 项目是什么、解决什么问题 | `@README.md` |
| 通用编程最佳实践(模型脑补) | 模型自动加上的"函数要短"、"注释要清晰"、"变量命名要有意义"等套话 | 删除。**但用户主动声明的相同内容走 §0.0 豁免,保留** |
| `.env` / `.gitignore` 已覆盖的事 | "`.env` 不要提交" | 删除(`.gitignore` 已机械约束) |
| 语言 / 框架版本要求 | "Python 3.8+" | 删除(`pyproject.toml` / `engines` 已声明) |

---

## §0.6 Bug vs Constraint 判定(§C 捕获的第一步)

会话沉淀学习时,对每条候选必须先回答:

> "这是**项目天然约束**(Constraint),还是**当前存在的 bug**(Bug)?"

| 判定 | 特征 | 动作 |
|---|---|---|
| **Bug** | 可通过一次修复消除;描述里有"目前""当前""错了""多一层""指向错误" | **建议修复动作**,不写入 CLAUDE.md |
| **Constraint** | 源于技术栈/架构/团队约定,修不掉也不该修 | 继续过 G1–G4 |

这一步能直接拦截"软链接指向错误路径""某文件写错了"这类污染。

---

## 何时用 / 场景路由表

| 场景 | 流程 | 详见 |
|------|------|------|
| 没有 CLAUDE.md | §A 生成 | 本文件 + [references/templates.md](references/templates.md) |
| 有但需审查/评分/优化 | §B 5-Phase 审查 | [references/quality-criteria.md](references/quality-criteria.md) + [references/update-guidelines.md](references/update-guidelines.md) |
| 会话结束沉淀学习 | §C 捕获 | [references/session-capture.md](references/session-capture.md) |

先用 `ls` / `Read` 判断 `./CLAUDE.md` 是否存在,再选分支。禁止未确认就覆盖已有文件。

---

## 通用原则(7 条)

1. **长度**:控制在 150 行以内,理想 40–100 行。超出时逐行过四道 Gate。
2. **结构**:推荐 Commands / Conventions / Gotchas / Verification 四段。**Architecture 段默认不写目录树**,只写"非显然的架构决策";目录树用 `@docs/architecture.md` 引用。
3. **应该写**:**项目独有的**命令(来自 `package.json scripts` / `Makefile`,而非 git/npm/uv 本身)、与默认值不同的团队约定、非显而易见的坑、验证方式。
4. **不要写**:见 §0.5 黑名单。
5. **拆分**:复杂项目用 `@docs/xxx.md`,被 import 的文件按需加载,不占默认上下文。
6. **文件位置**:
   - `./CLAUDE.md` — 项目级,提交 Git
   - `./CLAUDE.local.md` — 个人笔记,加入 `.gitignore`
   - `~/.claude/CLAUDE.md` — 全局偏好
   - 子目录 / `./packages/*/CLAUDE.md` — 作用域级
7. **机械约束优先于散文**:能用 lint / hook / CI / `.gitignore` 强制的规则,CLAUDE.md 里不要重复。

---

## Architecture 段:写什么、不写什么

这是最容易写错的段。**目录结构 ≠ 架构决策。**

| 写入 CLAUDE.md(非显然的架构决策) | 移到 `@docs/architecture.md`(架构说明) |
|---|---|
| "业务层禁止直接引用 ORM,必须经 Repository" | 完整的 ASCII 目录树 |
| "状态管理统一用 Zustand,禁止引入 Redux" | 每个目录的职责说明 |
| "跨 package 引用只能通过 `@scope/shared`,禁止相对路径" | 组件层级图 |
| "为什么选 A 不选 B" 的关键决策 | 文件命名约定(IDE/lint 已覆盖时) |

**判定问法**:"新人读这条,会少写错一个 import / 少走一次弯路吗?" 会 → 写;不会 → `@docs/`。

---

## §A 从零生成 CLAUDE.md

### A.1 信息采集(必做)

尽量用工具自动探测,不要问用户已能从代码推断的问题:

1. **技术栈**:读 `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml`
2. **包管理器**:看 lockfile(`pnpm-lock.yaml` → pnpm,`bun.lockb` → bun,`uv.lock` → uv)
3. **项目独有命令**:只提取 `scripts` / `Makefile` / `justfile` 里**项目自定义**的条目(过 G1,过滤掉 `npm install` 这种通用项)
4. **测试框架**:从依赖推断
5. **已有文档**:看 `README.md` / `docs/` 有无架构说明,有就用 `@` 引用,**不要复制内容过来**

**禁止**:用 `ls` 把目录树抄进 CLAUDE.md(违反 G2)。

只有无法自动探测的信息才用 `AskUserQuestion` 询问(团队硬规、架构决策理由、非显然的业务坑),一次最多 3–4 个。

### A.2 选档位并生成

根据项目规模选择档位,详细模板见 [references/templates.md](references/templates.md):

- **极简档**(约 30 行)— 新项目、小工具、Demo
- **标准档**(约 60–100 行)— 绝大多数业务项目
- **企业级档**(根文件精简 + `docs/standards/` 拆分)— 多人协作
- **Package / Monorepo 根模板**

### A.3 自检清单(必须逐条过 Gate)

交付前逐条过一遍,不是"大致看看":

- [ ] **每一行**都通过 G1(独特)+ G2(不可推断)+ G3(稳定)+ G4(错代价)
- [ ] 无黑名单条目(见 §0.5)
- [ ] Architecture 段无完整目录树(有则移到 `@docs/`)
- [ ] 无"当前 bug"描述(有则建议修复,不写入)
- [ ] 行数 ≤ 150
- [ ] 命令全部可复制,无 `<your-token>` 占位符
- [ ] 用 bullet,不用大段落
- [ ] 没有复制 README 内容(用 `@README.md` 引用)
- [ ] 创建了 `.local.md` 的话,已提醒加入 `.gitignore`

---

## §B 审查/优化(5-Phase)

### Phase 1:Discovery

```bash
find . -name "CLAUDE.md" -o -name ".claude.md" -o -name ".claude.local.md" 2>/dev/null | head -50
```

### Phase 2:Quality Assessment

对每个 CLAUDE.md 按 6 个维度打分(满分 100),详见 [references/quality-criteria.md](references/quality-criteria.md)。

**评分时对每一条内容逐条过四道 Gate**,并统计:
- Gate 失败条目数(G1/G2/G3/G4 各自拦下多少条)
- 黑名单命中条目数

这两个数字直接影响 Conciseness / Actionability 维度得分。

### Phase 3:Quality Report

必须在任何修改之前输出完整报告:

```
## CLAUDE.md Quality Report

### Summary
- Files found: X
- Average score: X/100
- Gate failures: G1=X G2=X G3=X G4=X
- Blacklist hits: X

### File-by-File Assessment

#### 1. ./CLAUDE.md
**Score: XX/100**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Commands/workflows | X/20 | ... |
| Architecture clarity | X/20 | ... |
| Non-obvious patterns | X/15 | ... |
| Conciseness | X/15 | ... |
| Currency | X/15 | ... |
| Actionability | X/15 | ... |

**Gate-failed items:**
- L12 `git pull` → G1 通用命令,建议删除
- L34-48 ASCII 目录树 → G2 可 `ls` 推断,建议移到 `@docs/architecture.md`
- L76 "软链接指向错误路径" → G3 bug 而非约束,建议修复路径
```

### Phase 4:Propose Diffs

用户确认后,用 [references/update-guidelines.md](references/update-guidelines.md) 的三段式 diff(File → Diff → Why)。

每条 Why 必须引用对应 Gate 或黑名单条目。

### Phase 5:Apply with Approval

用户确认后用 `Edit` 工具精确替换。改完再跑一次 §A.3 自检。

---

## §C 会话学习捕获

详见 [references/session-capture.md](references/session-capture.md)。

**流程(顺序不可调):**
1. **Reflect** — 回顾本次会话的 5 类信号(命令/风格/测试/环境/Gotchas)
2. **Bug vs Constraint 判定** — 见 §0.6。Bug 一律建议修复,不入 CLAUDE.md
3. **过四道 Gate** — 逐条过 G1–G4
4. **Find** — `find . -name "CLAUDE.md"`,决定写入哪一层
5. **Draft** — 每条一行,`<cmd or pattern> — <brief>`
6. **Show** — 三段式 diff,每条标注通过了哪些 Gate
7. **Apply** — 用户同意后才改

---

## 交付 Tips(告诉用户的 5 条)

1. **`#` 快捷键**:会话中按 `#` 可触发 Claude 自动沉淀学习到 CLAUDE.md
2. **`.local.md` 隔离**:个人偏好写 `CLAUDE.local.md`,加入 `.gitignore`
3. **全局偏好**:跨项目的个人设置写到 `~/.claude/CLAUDE.md`
4. **命令精度**:所有命令必须可直接复制,不留 `<placeholder>`
5. **简洁 > 冗长**:CLAUDE.md 是提示词的一部分,每一行都要"用默认上下文换 Claude 少犯一类错"

---

## 最终裁决(Gate 的一句话总结)

一条内容是否放入 CLAUDE.md,按优先级问:

1. **是用户主动声明的团队规范 / 代码风格吗?** 是 → 走 §0.0 豁免,只过 G3+G4 → 保留
2. **否则:这条是项目独有决策/约束(非通用知识、不能从代码推断),且 Claude 不知道会写错代码吗?**
   - 两个都成立 → 写 CLAUDE.md
   - 只成立一个(次优而非错) → 写 `@docs/`,主文件用 `@` 引用
   - 都不成立 → **不写**(属于常识、可推断、或 bug)
