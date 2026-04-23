写好 CLAUDE.md 的核心原则

控制在 200 行以内（生产环境建议 60 行左右）。过长的 CLAUDE.md 会导致 Claude 因 position bias 忽略你的指令，这是社区踩过最多的坑。推荐使用 "WHAT-WHY-HOW" 三段式结构：


# Project: my-app

## WHAT — 技术栈与架构
- TypeScript + React 18 + Tailwind CSS
- 后端 Node.js + PostgreSQL, ORM 用 Drizzle
- Monorepo 结构: apps/web, apps/api, packages/shared

## WHY — 核心约束与目标
- 所有 API 必须有 Zod schema 验证
- 组件必须是函数式 + hooks，禁止 class component
- 测试覆盖率不低于 80%

## HOW — 常用命令
- 运行测试: `bun test`
- 类型检查: `bunx tsc --noEmit`
- lint: `bun run lint`
- 启动开发: `bun dev`
应该写什么，不应该写什么

应该写的内容：Claude 无法从代码中自动推断的信息——技术栈选型理由、测试运行命令、部署约束、团队编码规范、架构决策（如"为什么选了 Drizzle 而不是 Prisma"）。不应该写的内容：Claude 能从代码中推断的内容（函数签名、目录结构等），以及与当前项目无关的通用编程知识。一个好的判断标准是：如果一个新加入的高级工程师需要知道这件事才能高效工作，那就写进去。

使用 @import 拆分

当项目复杂度增长时，用 @import 将大文件拆分为模块化的小文件：


# CLAUDE.md
@api-conventions.md
@testing-patterns.md
@deployment-notes.md
被 import 的文件只在 Claude 需要时才加载，不会浪费上下文窗口。


写进 CLAUDE.md 的内容
只有两类内容应该直接写在 CLAUDE.md 中：

AI 理解项目全貌的必要信息——技术栈、仓库结构、核心模块、分层架构
违反会直接导致问题的硬性规则——编码规约、命名约定、禁止项
不写进去的内容
其他详细信息通过文档链接和引用指向对应的文档：

CLAUDE.md（地图）
  → docs/architecture.md          分层架构详细说明
  → docs/development.md           开发环境搭建
  → docs/design-docs/ref-*.md     参考项目架构说明
  → docs/design-docs/*-patterns.md 组件使用模式
判断一条信息该放 CLAUDE.md 还是放详细文档，有一个简单的标准：如果 AI 不知道这条信息就会写出错误的代码，放 CLAUDE.md；如果只是写出不够好的代码，放详细文档，CLAUDE.md 里放链接。


# CLAUDE.md 编写最佳实践深度调研

> 调研范围：Anthropic 官方文档、OpenAI Harness Engineering、Augment Code 研究、Claude Code 核心团队（Boris Cherny、Thariq Shihipar）以及社区高质量开源项目（ClaudeForge、harness-engineering 等）。已主动过滤 CSDN 及低质量水文内容。

---

## 一、核心原则：为什么 CLAUDE.md 不是越长越好

CLAUDE.md 的根本约束是**上下文窗口（context window）**。Anthropic 官方明确指出："Claude's context window fills up fast, and performance degrades as it fills." 当上下文填满时，Claude 会开始"遗忘"早期指令，犯错率上升。

因此，编写 CLAUDE.md 的第一性原理是：**只保留 Claude 离开它就一定会犯错的信息**。这一原则被多个高质量来源反复强调：

- **OpenAI Harness Engineering**："Give Codex a map, not a 1,000-page manual." AGENTS.md 应该只有约 100 行，作为目录（table of contents）而非百科全书。
- **Augment Code**（基于 ETH Zurich 的研究）：过多的上下文文件实际上会降低任务成功率，同时增加 20% 以上的成本。Vercel 将 40KB 的文档压缩成 8KB 的索引文件后，build/lint/test 通过率达到了 100%。
- **Boris Cherny**（Claude Code 创造者）：Anthropic 内部使用的 CLAUDE.md 大约只有 ~2.5k tokens。
- **Simon Willison**："As few instructions as possible."

**检验标准**：对每一行内容，问自己——"如果删掉这一句，Claude 会犯错吗？"如果不会，就删掉。

---

## 二、文件位置与加载机制

CLAUDE.md 支持多层级的放置策略，Claude Code 会自动合并所有发现的文件，越具体的文件优先级越高：

| 位置 | 作用域 | 用途 |
|------|--------|------|
| `~/.claude/CLAUDE.md` | 全局 | 个人偏好，适用于所有项目 |
| `./CLAUDE.md` | 项目根目录 | 项目级规范，应提交到 Git 与团队共享 |
| `./CLAUDE.local.md` | 项目根目录 | 个人项目笔记，加入 `.gitignore` |
| 父目录 | 单仓库多包 | Monorepo 场景，`root/CLAUDE.md` 和 `root/foo/CLAUDE.md` 会自动合并 |
| 子目录 | 模块级 | `src/backend/CLAUDE.md` 等，工作到对应目录时按需加载 |

**导入语法**：CLAUDE.md 支持用 `@path/to/file` 引用其他文件，避免内容膨胀：

```markdown
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

---

## 三、应该包含什么（高杠杆内容）

根据 Anthropic 官方文档及社区高质量实践，以下内容是真正的"高杠杆"信息——即 Claude 无法从代码中自行推断、离开它就会犯错的内容：

### 3.1 命令（Commands）
**这是最高优先级的部分。** Claude 会直接执行你写的命令，因此必须提供精确的、可复制的命令：

```markdown
## Commands
- `pnpm test` — run tests with Vitest
- `pnpm test -- --run src/components/Button.test.tsx` — run a single test file
- `pnpm lint` — ESLint + Prettier check
- `pnpm dev` — start dev server

Always run `pnpm typecheck && pnpm lint` before committing.
```

### 3.2 项目结构与架构（Architecture）
告诉 Claude 文件放在哪里，避免它搜索整个代码库：

```markdown
## Architecture
- `src/routes/` — API route handlers
- `src/models/` — database models (Sequelize)
- `src/middleware/` — Express middleware
- `tests/` — test files mirroring src/ structure
```

### 3.3 代码规范（Conventions）
只写**与默认值不同**的规范：

```markdown
## Conventions
- Use ES modules (import/export), not CommonJS (require)
- Use named exports, not default exports
- TypeScript strict mode — no `any`
- All API responses use the format: `{ data, error, status }`
```

### 3.4 常见陷阱（Gotchas）
项目中非显而易见的坑：

```markdown
## Critical Gotchas
- `SKILL.md` is the skill: Claude reads the file as the skill prompt. Changes directly change behavior.
- Scripts run in target projects, not this repo. They must work standalone.
- No package.json at root: Tests run via direct node/jest/bash invocation.
```

### 3.5 验证方式（Verification）
**这是 Boris Cherny 提到的"最高杠杆的事情"：** 给 Claude 一种验证自己工作的方式，测试、截图或预期输出都可以：

```markdown
## Verification
- Run tests after every implementation change
- Use `npm run lint` to verify formatting
- For UI changes: take a screenshot and compare to the design
```

---

## 四、绝对不要包含什么（噪音来源）

以下内容会浪费上下文窗口，甚至被高质量来源明确反对：

| 不要包含 | 原因 |
|----------|------|
| 完整的目录树或文件列表 | 变化频繁，Claude 可以用工具自行读取 |
| 标准语言惯例 | Claude 已经知道 "write clean code" 或 JavaScript 的基础语法 |
| 详细的 API 文档 | 提供链接即可，不要复制粘贴 |
| 频繁变化的信息 | 会导致 CLAUDE.md 与代码不同步 |
| 长段落解释或教程 | 用 bullet points 代替 |
| 从 README 复制的项目介绍 | 用 `@README.md` 引用 |
| "显而易见"的最佳实践 | 如 "use meaningful variable names" |

**Andrej Karpathy 的观察**：即使他作为 "context engineering" 概念的提出者，也发现代理"不听从 AGENTS.md 中的指令"——它们会膨胀抽象、复制粘贴代码块、忽略风格指导。这说明**机械约束（hooks、linters）比散文式指令更可靠**。

---

## 五、长度控制：具体的数字建议

多个来源对长度给出了明确建议：

- **Anthropic 官方**：保持简短（short and human-readable）。如果 Claude 反复违反某条规则，说明文件可能太长，规则被淹没了。
- **OpenAI**：AGENTS.md 应控制在 ~100 行，作为目录/地图。
- **harness-engineering**：两级系统——全局 200-300 行 + 项目级 200-500 行。
- **claude.md-boilerplate**：根文件仅 ~75 行，详细规范放在按需加载的 pillar 文件中。
- **claude-code-best-practices**：建议控制在 200 行以内。

**推荐的层级结构（Progressive Disclosure）**：

| 层级 | 内容 | 加载时机 |
|------|------|----------|
| Tier 1：CLAUDE.md | 命令、架构、关键规范、常见陷阱 | 每次会话启动 |
| Tier 2：docs/*.md | 详细的领域规范（安全、测试、API 设计等） | 按需引用 |
| Tier 3：docs/plans/*.md | 具体的功能规格、设计文档 | 执行特定任务时 |

---

## 六、结构模板

### 6.1 极简模板（20-30 行，推荐起步）

基于 claude-code-best-practices 的 minimal example：

```markdown
# MyApp

Node.js/Express backend with PostgreSQL.

## Commands
- `npm test` — run tests (Jest)
- `npm test -- --testPathPattern=users` — run tests matching "users"
- `npm run lint` — ESLint check
- `npm run dev` — start dev server

## Structure
- `src/routes/` — API route handlers
- `src/models/` — database models (Sequelize)
- `src/middleware/` — Express middleware
- `tests/` — test files mirroring src/ structure

## Rules
- TypeScript strict mode — no `any`
- All API responses use the format: `{ data, error, status }`
- Use the existing logger (`src/utils/logger.ts`), not console.log
```

### 6.2 标准模板（100-150 行，适合大多数项目）

```markdown
# Project: Acme Dashboard

React 19 + TypeScript 5.x single-page application. Vite build system.

## Commands
- `npm run dev` — start dev server (port 3000)
- `npm run build` — production build
- `npm run test` — run all tests with Vitest
- `npm run test -- --run src/components/Button.test.tsx` — run a single test file
- `npm run lint` — ESLint + Prettier check
- `npm run lint:fix` — auto-fix lint issues
- `npm run typecheck` — tsc --noEmit

Always run `npm run typecheck && npm run lint` before committing.

## Architecture
- `src/components/` — reusable UI components
- `src/features/` — feature modules (auth, dashboard, settings)
- `src/hooks/` — shared custom hooks
- `src/api/` — API client and typed request/response definitions
- `src/types/` — shared TypeScript types and interfaces
- `src/utils/` — pure utility functions

## Conventions
- Functional components only — no class components
- Use named exports, not default exports
- Co-locate tests: `Button.tsx` → `Button.test.tsx` in the same directory
- Props interface named `{Component}Props`
- TypeScript strict mode — do not use `any` unless absolutely necessary with a comment

## State Management
- Local state: useState/useReducer
- Server state: TanStack Query — never store API data in local state
- Global app state: Zustand stores in `src/stores/`
- No Redux — do not introduce Redux or Redux Toolkit

## Testing
- Use Vitest + React Testing Library
- Test behavior, not implementation
- Mock API calls with MSW (Mock Service Worker), not jest.mock

## Git
- Conventional commits: feat:, fix:, chore:, docs:, test:
- Branch naming: feature/, fix/, chore/
- Always create a PR — never push directly to main

## Do NOT
- Do not use `any` without a justifying comment
- Do not add new dependencies without discussing first
- Do not use default exports
```

### 6.3 高级模板（企业级，配合 enforcement 层）

参考 harness-engineering 和 claude.md-boilerplate 的设计，根文件保持精简，详细规范拆分到 `docs/standards/`：

```markdown
# Coding Agent Standards

These rules apply to all coding work across the project.

## Commands
- `pytest` — run all tests
- `pytest tests/test_items.py::test_create_item -v` — run a single test
- `ruff check .` — lint
- `ruff format .` — format code
- `mypy src/` — type checking

Run `ruff check . && ruff format --check . && mypy src/ && pytest` before committing.

## Code Standards
Follow the standards in `docs/standards/`. Key files:
- `code-quality.md` — structure, naming, dependencies
- `testing.md` — test coverage requirements
- `security.md` — input validation, auth, TLS
- `error-handling.md` — logging and error patterns

Do not deviate from these standards without explicit user approval.

## Critical Rules (always apply)
- Never hardcode secrets, tokens, keys, or connection strings
- Parameterised queries only. No string concatenation for SQL
- Input validation at every boundary. Allowlists over denylists
- No feature code merged without tests
- No swallowed exceptions. Every catch block must handle, log, or re-throw
- Propose test cases before writing implementation
- Prefer small, reviewable changesets over large monolithic changes
- Touch only what the task requires. Do not refactor adjacent code
```

---

## 七、Mechanical Enforcement：当指令不够时

Andrej Karpathy 的观察引发了社区共识：**代理会忽略散文式指令**。因此高质量实践普遍采用"三层约束"架构：

| 层级 | 机制 | 作用 |
|------|------|------|
| 第一层：机械约束 | Git hooks、linters、CI | 在代码提交前物理性拦截违规 |
| 第二层：路径级规则 | `.claude/rules/*.md` | 针对特定目录的 advisory 上下文 |
| 第三层：全局原则 | `CLAUDE.md` | 设定高层原则和命令 |

**优先级永远是：自动化检查 > 规则文件 > 散文指令。**

harness-engineering 推荐的 pre-commit hooks 检查项：
- **Secret 扫描**：拦截 API keys、tokens、private keys
- **文件大小限制**：单文件不超过 300 行
- **测试同位**：每个 `src/` 文件需有同位置的测试文件
- **文档漂移检测**：源代码变更后提醒更新 CLAUDE.md
- **Lint + Format**：自动运行

---

## 八、维护与演进

CLAUDE.md 不是写一次就完事的文档，需要像代码一样维护：

### 8.1 有机生长
不要一开始就写一份"完美"的 CLAUDE.md。**从极简版本开始**，只有当 Claude 反复犯错时才添加规则。这样得到的 CLAUDE.md 比 speculative 写出来的更有用。

### 8.2 定期修剪
Boris Cherny 建议：如果 Claude 持续做你不希望它做的事，即使已有规则禁止，说明文件可能太长，规则被淹没了。**定期问自己对每一行：删掉它 Claude 会犯错吗？**

### 8.3 自动化维护
- **ClaudeForge**：提供 Guardian Agent，自动检测代码库变更并同步更新 CLAUDE.md
- **harness-engineering**：提供 `generate-docs.js`，通过 `<!-- AUTO:tree -->` 和 `<!-- AUTO:modules -->` 标记自动生成目录结构
- **Drift Detection**：`validate-docs.js` 在提交前检查文档是否过期

### 8.4 版本控制
CLAUDE.md 应该提交到 Git。团队可以共同维护，其价值随时间复利增长。

---

## 九、常见反模式

| 反模式 | 表现 | 修复 |
|--------|------|------|
| **厨房水槽式文件** | 什么都往里塞，超过 500 行 | 按 Progressive Disclosure 拆分到 docs/ |
| **重复造轮子** | 复制 README 或标准文档内容 | 用 `@` 引用外部文件 |
| **过度规范** | 规定每一行代码怎么写 | 只规定 Claude 会犯错的地方 |
| **一成不变** | 项目演进后 CLAUDE.md 还是旧的 | 建立 drift detection 或定期审查 |
| **信任但不验证** | 只给指令不给验证方式 | 每条任务都配套测试或检查命令 |
| **散文体** | 用长段落解释 | 用 bullet points，一条一个动作 |

---

## 十、进阶技巧

### 10.1 强调关键词提高遵从率
如果某条规则 Claude 经常忽略，尝试增加强调：

```markdown
- **IMPORTANT**: Always run tests before committing.
- **YOU MUST**: Use named exports only.
- **NEVER**: Hardcode secrets in source code.
```

### 10.2 使用 Skills 处理领域知识
对于不适用于每次会话的专门知识，使用 `.claude/skills/` 目录创建 `SKILL.md` 文件。Claude 会在相关时自动加载，不会膨胀每次会话的上下文。

### 10.3 Subagent 隔离复杂任务
当任务需要大量文件探索时，让 Claude 使用 subagent 在独立上下文中执行，避免污染主会话的上下文窗口。

### 10.4 配合 Prompt Caching 设计
Thariq Shihipar（Anthropic Claude Code 团队）强调："You fundamentally have to design agents for prompt caching first." 静态内容（CLAUDE.md）先加载，动态内容（对话）后加载，不要混排。

---

## 来源

本调研综合以下高质量来源，已排除 CSDN 及低质量转载内容：

1. [Anthropic Official: Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices) — 官方最佳实践
2. [Anthropic Official: Claude Code Overview / CLAUDE.md](https://code.claude.com/docs/en/overview) — CLAUDE.md 机制说明
3. [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/) — 零手写代码构建产品的经验
4. [Augment Code: Your Agent's Context Is a Junk Drawer](https://www.augmentcode.com/blog/your-agents-context-is-a-junk-drawer) — ETH Zurich 研究-backed 的上下文分析
5. [Boris Cherny (Claude Code Creator) - Pragmatic Engineer Interview](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny) — 创造者视角
6. [Andrej Karpathy on Context Engineering](https://x.com/karpathy/status/1937902205765607626) / [Agents don't listen](https://x.com/karpathy/status/2035173492447224237) — 行业顶尖研究者的反思
7. [Simon Willison: Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/) — 实用主义视角
8. [ClaudeForge](https://github.com/alirezarezvani/ClaudeForge) (353 stars) — CLAUDE.md 自动生成与维护工具
9. [harness-engineering](https://github.com/jrenaldi79/harness-engineering) (56 stars) — 上下文工程与机械约束参考实现
10. [claude.md-boilerplate](https://github.com/leighstillard/claude.md-boilerplate) (6 stars) — 企业级工程标准模板
11. [claude-code-best-practices](https://github.com/MuhammadUsmanGM/claude-code-best-practices) (5 stars) — 社区综合最佳实践 wiki
