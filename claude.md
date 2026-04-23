# Skills Project Management

管理多个 Claude Code / Copilot CLI skills 的仓库。每个 skill 是独立的 Python 项目，使用 uv 管理依赖。

## Commands

- `uv pip install -r requirements.txt` — 安装某个 skill 的依赖（在 skill 目录下运行）
- `python scripts/<script>.py` — 运行某个 skill 的脚本（在 skill 目录下运行）
- `git pull` — 同步远程更新
- `git add -A && git commit -m "<message>"` — 提交所有变更

## Architecture

```
skills/
  ├── <skill-name>/          — 每个 skill 是独立子项目
  │   ├── SKILL.md           — skill 定义文件（必须）
  │   ├── scripts/           — Python 脚本目录
  │   ├── references/        — 参考文档、配置文件
  │   ├── requirements.txt   — Python 依赖
  │   └── .env.example       — 环境变量示例（如有）
  ├── docs/                  — 项目级文档（规划、测试指南等）
  └── .claude/               — Claude Code 配置
      ├── settings.json      — 全局权限配置
      └── skills/            — 软链接到实际 skills（可选）
```

**软链接机制**: 如果需要 `.claude/skills/` 目录识别，可在该目录创建软链接指向 `skills/<skill-name>/`，但禁止未经允许在全局目录创建文件。

## Skill Management

### 创建新 Skill

1. 在 `skills/` 下创建新目录：`mkdir skills/<new-skill>`
2. 创建 `SKILL.md`（必须，定义 skill 名称、触发条件、内容）
3. 创建 `scripts/` 目录，编写 Python 脚本
4. 创建 `requirements.txt`，列出依赖
5. 如需参考文档，创建 `references/` 目录

### 修改存量 Skill

**所有修改必须在 `skills/` 目录下进行**，禁止直接修改 `.claude/skills/` 下的软链接指向的内容。

### 测试 Skill

```bash
cd skills/<skill-name>
uv pip install -r requirements.txt  # 安装依赖
python scripts/<main-script>.py      # 运行主脚本
```

## Python Standards

- **包管理**: 使用 `uv`（禁止 pip 直接安装）
- **依赖安装**: `uv pip install -r requirements.txt`
- **Python 版本**: 3.8+

## Conventions

- **回复风格**: 简体中文，称呼用户为"先森"（项目级约束）
- **Skill 唯一源头**: `skills/` 目录是唯一的 skill 来源
- **禁止全局污染**: 未经允许禁止在 `~/.claude/` 等全局目录创建文件

## Gotchas

- **不要用 pip**: 必须用 `uv pip install`，直接 pip 会破坏依赖管理
- **软链接陷阱**: 创建软链接时路径必须正确，否则 skill 无法加载
- **.env 文件**: 每个 skill 的 `.env` 文件不要提交 Git（已在 `.gitignore`）

## Verification

- Skills 可运行：进入 skill 目录，安装依赖并运行主脚本
- 依赖正确：`uv pip install -r requirements.txt` 无错误