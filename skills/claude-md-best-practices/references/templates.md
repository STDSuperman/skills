# CLAUDE.md 模板库

## 核心原则

- **Concise**：内容密集，每行一个概念；能一行说清就不用两行
- **Actionable**：命令可直接复制粘贴，无占位符
- **Project-specific**：只记录项目特有的模式，不写通用建议
- **Current**：所有信息必须与当前代码库保持同步

---

## 选型决策树

根据以下 3 个问题选择合适的模板档位：

**Q1. 项目规模？**
- 小工具 / Demo / 新项目 → 极简档
- 绝大多数业务项目 → 标准档
- 有 docs/standards/ 目录、多人协作 → 企业级档

**Q2. 是否为 Monorepo？**
- 是 → 根目录用 Monorepo 模板 + 各包用 Package 模板
- 否 → 按 Q1 结果选单项目模板

**Q3. 是否为独立库/模块？**
- 是（在 monorepo 内部） → Package / Module 模板
- 否 → 按 Q1 结果

---

## 推荐章节指南

以下 8 个章节按需选用，不必全部包含。

### Commands 章节

记录构建、测试、开发、发布等关键命令。

```markdown
## Commands

| Command | Description |
|---------|-------------|
| `<install command>` | Install dependencies |
| `<dev command>` | Start development server |
| `<build command>` | Production build |
| `<test command>` | Run tests |
| `<lint command>` | Lint/format code |
```

说明：命令必须是当前实际可用的，不要写已废弃的命令。

### Architecture 章节

说明代码库结构，让 Claude 知道去哪里找什么。

```markdown
## Architecture

```
<root>/
  <dir>/    # <purpose>
  <dir>/    # <purpose>
  <dir>/    # <purpose>
```
```

说明：只需列出顶层和关键目录，不需要完整树形图。

### Key Files 章节

列出 Claude 必须了解的重要文件。

```markdown
## Key Files

- `<path>` - <purpose>
- `<path>` - <purpose>
```

说明：入口文件、配置文件、公共类型定义等优先列出。

### Code Style 章节

记录项目特有的编码约定，只写与默认不同的部分。

```markdown
## Code Style

- <convention>
- <preference over default>
```

说明：不要写"use meaningful names"这类通用建议。

### Environment 章节

说明必需的环境变量和初始化步骤。

```markdown
## Environment

Required:
- `<VAR_NAME>` - <purpose>
- `<VAR_NAME>` - <purpose>

Setup:
- <setup step>
```

### Testing 章节

记录测试命令和测试约定。

```markdown
## Testing

- `<test command>` - <what it covers>
- <testing pattern or convention>
```

说明：如果有特殊的测试夹具或工厂函数，在此说明位置。

### Gotchas 章节

记录非显而易见的陷阱、依赖顺序、常见错误。

```markdown
## Gotchas

- <non-obvious thing that causes issues>
- <ordering dependency or prerequisite>
- <common mistake to avoid>
```

说明：这是 CLAUDE.md 中价值最高的章节之一，每条 Gotcha 都应有真实背景。

### Workflow 章节

记录开发工作流，说明"何时做什么"。

```markdown
## Workflow

- <when to do X>
- <preferred approach for Y>
```

---

## 模板一：极简档（约 30 行）

适用于新项目、小工具、Demo。

```markdown
# <ProjectName>

<One-line tech stack description>

## Commands

- `<cmd>` - <purpose>
- `<cmd>` - <purpose>

## Structure

- `src/xxx/` - <purpose>

## Rules

- <hard constraint that differs from default>
- <hard constraint that differs from default>
```

---

## 模板二：标准档（约 100–150 行）

适用于绝大多数项目。

```markdown
# Project: <Name>

<1-2 sentences: project purpose + primary tech stack>

## Commands

| Command | Description |
|---------|-------------|
| `<dev command>` | Start development server |
| `<test command>` | Run tests |
| `<lint command>` | Lint and format |
| `<build command>` | Production build |
| `<typecheck command>` | Type checking |

Pre-commit: `<combined command>`

## Architecture

```
<root>/
  <dir>/        # <purpose>
  <dir>/        # <purpose>
  <dir>/        # <purpose>
```

## Conventions

- <naming convention that differs from default>
- <export pattern>
- <import alias rules>

## Gotchas

- <non-obvious issue>
- <ordering dependency>
- <common mistake>

## Testing

- `<test command>` - <scope>
- <test pattern or helper location>

## Do NOT

- <most likely pitfall 1>
- <most likely pitfall 2>
- <most likely pitfall 3>
```

---

## 模板三：企业级档（根文件精简 + docs/standards/ 拆分）

适用于有完整工程规范、多人协作的项目。根文件只保留命令和关键引用。

```markdown
# Coding Agent Standards

## Commands

| Command | Description |
|---------|-------------|
| `<command>` | <description> |

## Architecture

```
<root>/
  <dir>/    # <purpose>
```

## Code Standards

Follow the standards in `docs/standards/`:
@docs/standards/code-quality.md
@docs/standards/testing.md
@docs/standards/security.md

## Critical Rules (always apply)

- NEVER <bottom-line rule 1>
- NEVER <bottom-line rule 2>
- Always run `<command>` before committing
- <3-5 non-negotiable constraints>
```

说明：`NEVER` 只用于真正不可违反的底线；docs/standards/ 内的文件用 `@` 引用按需加载。

---

## 模板四：Package / Module 模板

适用于 monorepo 内的单个包或独立模块。

```markdown
# <Package Name>

<Purpose of this package in one sentence>

## Usage

```
<import/usage example>
```

## Key Exports

- `<export>` - <purpose>
- `<export>` - <purpose>

## Dependencies

- `<dependency>` - <why needed, especially non-obvious ones>

## Notes

- <important note about this package's constraints>
- <build order dependency if any>
```

---

## 模板五：Monorepo 根模板

适用于 monorepo 根目录，协调多个子包。

```markdown
# <Monorepo Name>

<One-line description>

## Packages

| Package | Description | Path |
|---------|-------------|------|
| `<name>` | <purpose> | `<path>` |
| `<name>` | <purpose> | `<path>` |

## Commands

| Command | Description |
|---------|-------------|
| `<workspace install>` | Install all dependencies |
| `<build all>` | Build all packages |
| `<test all>` | Run all tests |
| `<single package test>` | Test specific package |

## Cross-Package Patterns

- <shared pattern all packages follow>
- <code generation or sync pattern>
- <shared config location>

## Gotchas

- <monorepo-specific dependency gotcha>
- <build order dependency>
```

---

## 更新原则

修改任何 CLAUDE.md 时：

1. **具体**：使用真实的文件路径和实际命令，不要使用通用模板占位符
2. **最新**：修改前对照实际代码库验证所有信息
3. **简短**：每个概念尽量一行表达
4. **有用**：每一行都要能回答"新会话的 Claude 需要这条信息吗？"
