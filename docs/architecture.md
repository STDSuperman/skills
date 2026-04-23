# Skills Project Architecture

详细目录结构及说明,从 CLAUDE.md 移出以节省默认上下文。

## Directory Tree

```
skills/
  ├── <skill-name>/           — 每个 skill 是独立子项目
  │   ├── SKILL.md            — skill 定义文件(必须)
  │   ├── scripts/            — Python 脚本目录
  │   ├── requirements.txt    — Python 依赖(部分在 scripts/ 下)
  │   ├── references/         — 参考文档(可选)
  │   └── .env.example        — 环境变量示例(可选)
  ├── docs/                   — 项目级文档
  │   ├── TESTING_GUIDE.md    — skill 测试指南
  │   └── claude_md最佳实践参考.md
  └── .claude/                — Claude Code 配置
      ├── settings.json       — 全局权限配置
      └ skills/               — 软链接指向 skills/<skill-name>/
```

## 各目录职责

- `skills/` — Skill 定义唯一源头,所有修改在此进行
- `docs/` — 项目级文档,测试指南,最佳实践参考
- `.claude/skills/` — 软链接目录,不存放实际文件