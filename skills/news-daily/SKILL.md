---
name: news-daily
description: 抓取多平台每日资讯并生成美观的 Markdown 日报，按平台分类并自动翻译为中文。自动发布到 GitHub 仓库（需配置）。当用户主动询问"今日资讯"、"今日新闻"、"今日热点"、"获取新闻"、"新闻日报"等表达获取资讯意图时触发。
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

自动抓取多个平台的热点资讯，生成按平台分类的 Markdown 日报，自动翻译为中文。

## 使用方式

### 完整工作流程

1. **抓取新闻数据** - 调用 `scripts/fetch_news.py` 获取多平台新闻
2. **生成 Markdown 报告** - 调用 `scripts/generate_report.py` 生成格式化的日报（自动分类、生成总结）
3. **发布到 GitHub 仓库** - 使用 `scripts/publish_to_repo.py` 推送到仓库

### 步骤 1：抓取新闻数据

运行以下命令获取原始新闻数据：

```bash
cd {baseDir}
python3 scripts/fetch_news.py
```

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

### 步骤 2：生成 Markdown 报告

使用 `generate_report.py` 脚本自动生成日报：

```bash
cd {baseDir}
python3 scripts/generate_report.py
```

该脚本会自动：
- 按平台将新闻分类（知乎、华尔街见闻、虎扑、澎湃新闻、Hacker News、Product Hunt、GitHub、少数派）
- 自动将所有资讯翻译为中文
- 每条新闻使用 Markdown 链接格式 `[翻译后的标题](URL)`
- 自动保存到 `daily-news-YYYYMMDD.md` 文件

### 步骤 3：发布到 GitHub 仓库

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

#### #### 发布日报

使用 `--content` 参数直接传递内容：
```bash
python3 scripts/publish_to_repo.py --content "日报内容"
```

或使用 `--file` 参数读取文件：
```bash
python3 scripts/publish_to_repo.py --file daily-report.md
```

### AI 模型调用指南

当触发此 skill 时，AI 模型应按照以下步骤执行：

1. **生成日报**
    ```bash
    cd skills/news-daily
    python3 scripts/generate_report.py
    ```

2. **读取生成的日报文件**
    ```bash
    cat daily-news-*.md
    ```

3. **发布到 GitHub 仓库**（如果已配置且用户要求推送）
    ```bash
    python3 scripts/publish_to_repo.py --file daily-news-*.md
    ```

4. **返回结果给用户**
    - 显示生成的日报内容（或关键统计信息）
    - 提示是否成功推送到 GitHub 仓库

**重要**：
- 如果 `.env` 中未配置 `GITHUB_REPO_URL`，跳过步骤 5
- 如果用户未要求推送，也可以跳过步骤 5
- 所有文件操作使用 UTF-8 编码

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

按照**来源平台**进行分类：

| 分类 | 说明 |
|------|------|
| 📝 知乎 | 知乎热榜话题 |
| 💰 华尔街见闻 | 财经快讯、新闻流、热门文章 |
| ⚽ 虎扑 | 体育热点 |
| 📰 澎湃新闻 | 新闻热点 |
| 💻 Hacker News | 技术资讯 |
| 🚀 Product Hunt | 科技新品 |
| 🐙 GitHub | 趋势项目 |
| 🎯 少数派 | 科技文章 |

所有内容自动翻译为中文。

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
- **使用翻译后的标题作为链接文本**
- **如果标题为空或过短，使用"查看详情"作为链接文本**

```markdown
✅ 正确格式：
1. [翻译后的标题](https://...)
2. [另一条翻译后的标题](https://...)

❌ 错误格式：
1. 翻译后的标题 https://...
2. [原英文标题](https://...)
```

根据抓取的数据，生成如下格式的 Markdown 报告：

```markdown
# 📅 每日资讯日报

**生成时间**: 2026-02-05 21:50:33
**总新闻数**: 178 条

---

## 🚀 Product Hunt (34 条)

1. [超级滑板](https://example.com/1)
2. [新的v0](https://example.com/2)
3. [希格斯菲尔德振动运动](https://example.com/3)
...

---

## 💰 华尔街见闻 (30 条)

1. 拉加德重申欧洲央行政策声明。
2. 据英国政府声明，英美两国于2月4日在华盛顿特区签署了一份谅解备忘录。...
...

---

## 💻 Hacker News (30 条)

1. [不要租用云，而是拥有云](https://example.com/1)
2. [公司代码](https://example.com/2)
3. [当内部主机名泄露给小丑时](https://example.com/3)
...

---

## 🎯 少数派 (30 条)

1. [新玩意 234｜少数派的编辑们最近买了啥？](https://example.com/1)
   > 内容摘要...
2. [浏览器扩展合集：派友近期推荐的 7 款浏览器扩展](https://example.com/2)
   > 内容摘要...
...

---

## 📰 澎湃新闻 (20 条)

1. [详讯丨习近平同美国总统特朗普通电话](https://example.com/1)
2. [宁波通报小洛熙事件调查结果：一级甲等医疗事故，吊销主刀医师执业证书](https://example.com/2)
...

---

## 🐙 GitHub (11 条)

1. [字节跳动/UI-TARS-桌面](https://example.com/1)
2. [开放/技能](https://example.com/2)
...

---

## 📝 知乎 (3 条)

1. 中美元首 2 月 4 日晚通电话，哪些信息值得关注？
   > 内容摘要...
2. 老人用筷子沾酒喂给 5 月龄宝宝，导致肝损伤，酒精对婴儿的影响有多大？...
...

---

*本日报由 OpenClaw News Daily Skill 自动生成*
```

### 报告内容要求

1. **按平台分类**
   - 每个平台作为一个独立的分类
   - 平台按照新闻数量降序排列
   - 每个平台显示所有抓取的新闻

2. **自动翻译**
   - 所有英文内容自动翻译为中文
   - 如果内容已经是中文，保持原样
   - 链接文本使用翻译后的标题

3. **链接格式**
   - 有 URL 的新闻：`[翻译后的标题](URL)`
   - 没有 URL 的新闻：直接显示翻译后的标题
   - 如果有内容摘要，使用引用块显示 `> 内容摘要...`

## 注意事项

- 所有平台数据均为公开 API 或公开页面，无需登录
- 请求包含标准浏览器 User-Agent，避免被拦截
- 内置重试机制和超时控制
- 数据仅供参考，不代表任何平台观点
