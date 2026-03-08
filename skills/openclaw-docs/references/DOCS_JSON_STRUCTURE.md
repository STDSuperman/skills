# OpenClaw docs.json 结构说明

## 文件位置
- 仓库：https://github.com/openclaw/openclaw
- 路径：`docs/docs.json`

## 整体结构

```json
{
  "$schema": "https://mintlify.com/docs.json",
  "name": "OpenClaw",
  "description": "...",
  "navigation": {
    "languages": [
      {
        "locale": "en",
        "tabs": [...]
      },
      {
        "locale": "zh-CN",
        "tabs": [...]
      },
      {
        "locale": "ja-JP",
        "tabs": [...]
      }
    ]
  }
}
```

## 关键路径

### 1. 语言配置
- 路径：`navigation.languages`
- 类型：数组
- 每个元素包含：
  - `locale`: 语言代码（"en", "zh-CN", "ja-JP"）
  - `tabs`: 该语言的文档导航结构

### 2. Tab 结构
每个 language 下的 `tabs` 数组：
```json
{
  "tab": "Get started",
  "groups": [
    {
      "group": "Home",
      "pages": ["index"]
    },
    {
      "group": "Overview",
      "pages": ["start/showcase"]
    }
  ]
}
```

### 3. 文档路径规则

**英文文档**：
- locale: "en"
- pages 路径：无语言前缀
- 示例：`"index"`, `"start/showcase"`, `"channels/discord"`
- 实际文件：`docs/index.mdx`, `docs/start/showcase.mdx`

**中文文档**：
- locale: "zh-CN"
- pages 路径：有 `zh-CN/` 前缀
- 示例：`"zh-CN/index"`, `"zh-CN/start/showcase"`
- 实际文件：`docs/zh-CN/index.mdx`

**日文文档**：
- locale: "ja-JP"
- pages 路径：有 `ja-JP/` 前缀
- 示例：`"ja-JP/index"`
- 实际文件：`docs/ja-JP/index.mdx`

## 提取英文文档的逻辑

```python
# 1. 读取 docs.json
config = json.load(f)

# 2. 遍历 languages
for lang in config['navigation']['languages']:
    locale = lang.get('locale', 'en')

    # 3. 只处理英文
    if locale != 'en':
        continue

    # 4. 遍历 tabs
    for tab in lang.get('tabs', []):
        tab_name = tab.get('tab')

        # 5. 遍历 groups
        for group in tab.get('groups', []):

            # 6. 收集 pages
            for page in group.get('pages', []):
                # page 就是文档路径
                # 实际文件：docs/{page}.mdx 或 docs/{page}.md
                pass
```

## Tab 分类（英文版）

根据实际解析，英文文档包含以下 tabs：
1. Get started - 快速开始
2. Install - 安装方法
3. Channels - 消息渠道（Discord, Telegram, WhatsApp 等）
4. Agents - AI 代理配置
5. Tools - 工具集成
6. Models - AI 模型提供商
7. Platforms - 平台支持（macOS, Linux, Windows 等）
8. Gateway & Ops - 网关和运维
9. Reference - 参考文档
10. Help - 帮助文档

## 文档合并策略

### 按 Tab 合并
- 每个 tab 生成一个合并文件
- 文件名：`{tab_name}.md`（空格替换为下划线）
- 优点：文档数量少（约 10 个）
- 缺点：单个文件可能较大

### 按 Group 合并（备选）
- 每个 group 生成一个合并文件
- 文件名：`{tab_name}_{group_name}.md`
- 优点：文件更小，更精细
- 缺点：文档数量多（约 50+ 个）

## 文件扩展名

文档文件可能是：
- `.mdx` (Mintlify 默认)
- `.md` (标准 Markdown)

提取时需要同时检查两种扩展名。

## 注意事项

1. **多语言处理**：确保只提取 `locale == "en"` 的文档
2. **路径前缀**：英文文档的 pages 路径没有语言前缀
3. **文件存在性**：并非所有 pages 都有对应文件，需要检查文件是否存在
4. **重定向**：docs.json 中有 `redirects` 配置，但不影响文档提取

## 示例输出

提取后的结构示例：
```json
{
  "Get started": [
    "index",
    "start/showcase",
    "concepts/features",
    "start/getting-started"
  ],
  "Channels": [
    "channels/index",
    "channels/discord",
    "channels/telegram",
    "channels/whatsapp"
  ]
}
```
