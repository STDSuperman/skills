---
name: news-daily
description: 抓取多平台每日资讯并生成美观的 Markdown 日报，支持 AI、财经、技术等分类。当用户主动询问"今日资讯"、"今日新闻"、"今日热点"、"获取新闻"、"新闻日报"等表达获取资讯意图时触发。
metadata:
  {
    "openclaw":
      {
        "emoji": "📰",
        "requires": { "bins": ["python3"] },
      },
  }
---

# News Daily - 每日资讯聚合

自动抓取多个平台的热点资讯，生成分类清晰的 Markdown 日报。

## 使用方式

### 1. 抓取新闻数据

运行以下命令获取原始新闻数据：

```bash
cd {baseDir}
python3 scripts/fetch_news.py
```

### 2. 发布日报到 GitHub 仓库（可选）

如果需要将日报自动发布到 GitHub 仓库，按照以下步骤配置：

#### 配置环境变量

1. 复制配置模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填写必要配置：
```bash
# GitHub 仓库 URL（必须）
GITHUB_REPO_URL=https://github.com/username/repo.git

# 其他配置可选，留空则使用默认值
# REPO_TYPE=
# REPO_TARGET_DIR=
# FILENAME_FORMAT=daily-news-%Y%m%d.md
```

**重要提示**：
- 请确保本地已配置好 `git` 用户信息和认证方式（SSH 密钥或 HTTPS Token）
- 脚本会使用本地 git 配置进行操作，不会要求输入用户名密码

#### 发布日报

使用 `--content` 参数直接传递内容：
```bash
python3 scripts/publish_to_repo.py --content "日报内容"
```

或使用 `--file` 参数读取文件：
```bash
python3 scripts/publish_to_repo.py --file daily-report.md
```

#### 仓库类型支持

| 类型 | 说明 | 目标目录 |
|------|------|---------|
| `vuepress` | VuePress 博客 | `docs/` |
| `generic` | 通用仓库 | 仓库根目录 |
| `custom` | 自定义目录 | 由 `REPO_TARGET_DIR` 指定 |

**自动检测规则**：
- 如果配置了 `REPO_TYPE`，直接使用配置值
- 如果仓库存在 `docs/` 或 `.vuepress/` 目录，自动识别为 `vuepress`
- 其他情况默认为 `generic`

**输出格式** (JSON)：
```json
{
  "total": 180,
  "items": [
    {
      "title": "新闻标题",
      "url": "https://...",
      "platform": "zhihu",
      "platform_icon": "📝",
      "content": "内容摘要..."
    }
  ]
}
```

## 支持的平台

| 平台 | 类型 | 内容 |
|------|------|------|
| 知乎 | API | 热榜话题 |
| 华尔街见闻 | API | 财经快讯、新闻流、热门文章 |
| 虎扑 | HTML | 体育热点 |
| 澎湃新闻 | API | 新闻热点 |
| Hacker News | HTML | 技术资讯 |
| Product Hunt | HTML | 科技新品 |
| GitHub | HTML | 趋势项目 |
| 少数派 | API | 科技文章 |

## 数据字段说明

每条新闻包含以下字段：

- `title`: 新闻标题
- `url`: 链接（可能为空）
- `platform`: 平台标识
- `platform_icon`: 平台图标
- `content`: 内容摘要（可选，可能为空）

## 分类规则

根据新闻的**内容主题**进行分类（由调用方根据以下规则自动判断）：

| 分类 | 说明 |
|------|------|
| 🤖 AI | 人工智能相关的资讯，包括GPT、大模型、机器学习、深度学习等AI技术 |
| 💰 财经 | 金融投资相关资讯，包括股票、基金、经济、市场、投资等 |
| 💻 技术 | 编程开发相关资讯，包括代码、开源、框架、编程语言、开发工具等 |
| 🎬 娱乐 | 娱乐文化相关资讯，包括电影、音乐、明星、综艺、剧集、游戏等 |
| 📱 科技 | 科技创新相关资讯，包括手机、芯片、产品、新品、发布等科技新闻 |
| ⚽ 体育 | 体育赛事相关资讯，包括NBA、足球、篮球、奥运、世界杯等体育新闻 |

**重要**：即使某新闻来自"虎扑"（通常体育为主），如果内容讨论的是"AI技术"，也应该归类为"AI"而不是"体育"。分类应该基于**内容主题**而非来源平台。

## 过滤规则

处理数据时建议过滤以下内容：

1. **广告内容**：标题或内容包含"广告"、"推广"等关键词
2. **重复内容**：相同标题和URL的条目
3. **空内容**：标题为空或长度少于3个字符
4. **广告标记**：特定平台的广告标记（如 ads_word）

## 报告生成示例

### 链接格式规范（重要）

- **所有外链必须使用 Markdown 链接格式**：`[显示文本](URL)`
- **禁止直接输出原始 URL**（如 `https://example.com`）
- **优先使用新闻标题作为链接文本**
- **如果标题为空或过短，使用"查看详情"作为链接文本**

```markdown
✅ 正确格式：
- [📝 知乎] [OpenAI 发布新模型](https://...)
- [💰 华尔街见闻] [美股大涨 2%](https://...)

❌ 错误格式：
- [📝 知乎] OpenAI 发布新模型 https://...
- [💰 华尔街见闻] 美股大涨 - https://example.com/news
```

根据抓取的数据和上述分类、过滤规则，生成如下格式的 Markdown 报告：

```markdown
# 📅 每日资讯日报

**生成时间**: 2026-02-04 16:30:00
**数据来源**: 知乎 | 华尔街见闻 | 虎扑 | 澎湃新闻 | Hacker News | Product Hunt | GitHub | 少数派

---

## 📊 今日统计

| 指标 | 数值 |
|------|------|
| 📰 总新闻数 | 180 |
| 🏷️ 分类数 | 5 |

### 📈 分类分布
| 分类 | 数量 | 占比 |
|------|------|------|
| 💰 财经 | 50 | 27.8% |
| 🤖 AI | 35 | 19.4% |
| 💻 技术 | 30 | 16.7% |
...

### 📺 平台分布
| 平台 | 数量 |
|------|------|
| producthunt | 37 |
| wallstreetcn | 30 |
...

---

## 📋 分类资讯详情

### 🤖 AI (35 条)
- [📝 知乎] [OpenAI 发布新模型](https://example.com/1)
- [🐙 GitHub] [awesome-ml: 机器学习资源集合](https://example.com/2)
...

### 💰 财经 (50 条)
- [💰 华尔街见闻] [美股大涨 2%，创历史新高](https://example.com/3)
- [💰 华尔街见闻] [美联储宣布维持利率不变](https://example.com/4)
...

---

*本日报由 OpenClaw News Daily Skill 自动生成*
```

## 注意事项

- 所有平台数据均为公开 API 或公开页面，无需登录
- 请求包含标准浏览器 User-Agent，避免被拦截
- 内置重试机制和超时控制
- 数据仅供参考，不代表任何平台观点
