# Skills Project Management

管理多个 Claude Code / Copilot CLI skills 的仓库。每个 skill 是独立的 Python 项目，使用 uv 管理依赖。

## Commands

- **依赖管理**: `uv pip install -r requirements.txt`(在 skill 目录下,禁止 pip)
- **软链接创建**: `cd .claude/skills/ && ln -s ../../skills/<skill-name> <skill-name>`(相对路径,在 .claude/skills/ 目录下执行)
- **软链接验证**: `ls -la .claude/skills/` 确认指向正确

## Architecture

**核心架构决策**:
- **软链接机制**: `.claude/skills/` 软链接指向 `skills/<skill-name>/`,**必须在 .claude/skills/ 目录下执行创建**,使用相对路径 `../../skills/<skill-name>`
- **Skill 唯一源头**: `skills/` 目录是唯一 skill 定义源,禁止修改 `.claude/skills/` 下的软链接内容
- **全局污染禁令**: 未经允许禁止在 `~/.claude/` 等全局目录创建文件

详细目录结构见 `@docs/architecture.md`。

## Skill Management

### 创建新 Skill

1. `mkdir skills/<new-skill>` — 创建目录
2. 创建 `SKILL.md`（必须）— 定义名称、触发条件、内容
3. 创建 `scripts/` 和 `requirements.txt` — 编写脚本和依赖

### 修改存量 Skill

**所有修改必须在 `skills/` 目录下进行**，禁止直接修改 `.claude/skills/` 下的软链接指向的内容。

### 测试 Skill

每个 skill 的测试方式不同，查看 `skills/<skill-name>/SKILL.md` 了解具体用法。通用流程：
```bash
cd skills/<skill-name>
uv pip install -r requirements.txt  # 安装依赖（如有）
# 运行脚本参考该 skill 的 SKILL.md
```

## Python Standards

- **包管理**: 使用 `uv`（禁止 pip 直接安装）
- **依赖安装**: `uv pip install -r requirements.txt`
- **Python 版本**: 3.8+

## Conventions

- **回复风格**: 简体中文,称呼用户为"先森"(项目级约束)

## Gotchas

- **不要用 pip**: 必须用 `uv pip install`,直接 pip 会破坏依赖管理
- **软链接陷阱**: 创建软链接时路径必须正确,否则 skill 无法加载
- **依赖位置不一致**: 部分 skill 在根目录,部分在 scripts/ 下,查看该 skill 的 SKILL.md 确认
- **Skill 使用**: 每个 skill 使用方式不同,查看 `skills/<skill-name>/SKILL.md`

## Verification

- Skills 可运行：进入 skill 目录，安装依赖并运行主脚本
- 依赖正确：`uv pip install -r requirements.txt` 无错误
- 软链接正确：`ls -la .claude/skills/` 检查链接指向
- Skill 已识别：运行 Claude Code，输入 `/<skill-name>` 验证加载