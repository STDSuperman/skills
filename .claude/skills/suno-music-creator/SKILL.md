---
name: suno-music-creator
description: 使用 Suno AI V5 与 Suno Studio 的专业音乐创作流程。当用户想创作歌曲、歌单、企业 anthem、jingle、健身音乐、氛围音景或任何 AI 生成音乐时使用此 skill。触发条件包括提到 Suno、音乐创作、歌单生成、歌曲创作，或诸如“create a track”“make a playlist”“compose music for”“corporate anthem”“workout mix”等具体音乐项目需求。
license: MIT
metadata:
  author: Schwepps
  version: "1.0.0"
  category: music
  tags: music, suno, ai-music, music-creation, song-creation, audio-generation
---

# Suno 音乐创作

使用 Suno AI V5 与 Suno Studio 创作高质量音乐的专业流程。

## 快速索引

| 主题 | 参考文件 |
|-------|----------------|
| 按风格的提示词 | [references/style-library.md](references/style-library.md) |
| 按使用场景的 BPM 指南 | [references/bpm-guide.md](references/bpm-guide.md) |
| 结构与元标签 | [references/metatags.md](references/metatags.md) |
| 项目模板 | [references/project-types.md](references/project-types.md) |

## 核心流程

### 1. 项目设定

需求收集：
- **类型**：单曲 / 歌单 / 专辑
- **用途**：个人 / 客户 / 商业发行
- **风格**：流派、情绪、能量水平
- **声线**：男声 / 女声 / 混合 / 纯器乐
- **语言**：歌词目标语言
- **时长**：单曲长度或歌单总时长（每次生成最多 8 分钟）
- **限制**：内容限制、品牌规范

### 2. 提示词构建

**风格提示词公式：**
```
[Genre], [BPM] BPM, [Mood], [Key instruments], [Vocal type], [Production style]
```

**负向提示（V5）：** 直接写出排除项：
```
Upbeat pop, 120 BPM, no guitars, no harsh distortion, clean mix
```

**歌词结构：** 在歌词栏放置元标签（比风格提示更有效）：
```
[Section Tag]
[Mood/Energy instruction]
Lyrics content (6-12 syllables per line for best alignment)
```

按流派的测试提示词参见 [references/style-library.md](references/style-library.md)。
结构标签与人声控制参见 [references/metatags.md](references/metatags.md)。

### 3. 生成流程

1. 每首生成 2-4 个版本（V5 速度提升约 10 倍）
2. 根据以下标准挑选最佳版本：
   - BPM 准确度（关键场景可用外部工具验证）
   - 人声清晰度与情绪表现（V5 人声更自然）
   - 混音质量与乐器分离度
   - 与提示词的匹配度
3. 后期处理：
   - **Extend**：补充段落、修复突兀结尾（用回调："continue with same vibe"）
   - **Remaster**：Subtle（均匀）/ Medium / Wide（更有变化）
   - **Crop**：去除不需要的前奏/尾奏
   - **Cover**：切换风格或声线
   - **Replace Section**：重生成特定片段（Studio）

### 4. 质量检查清单

- [ ] BPM 接近目标（±5 BPM 可接受）
- [ ] 人声清晰、有表现力
- [ ] 无明显音频伪影（V5 频率分离更好）
- [ ] 结构完整（前奏 → 主歌 → 副歌 → 结尾）
- [ ] 能量水平符合用途
- [ ] 歌词可听清且正确
- [ ] 音乐记忆一致（主题动机在 8 分钟内能正确复现）

### 5. 导出与交付

- **母带/成品**：WAV 16-bit/44.1kHz
- **预览/草稿**：MP3 320kbps
- **分轨**：人声、鼓、贝斯、吉他、合成器等
- **MIDI**：支持导出

## Suno Studio

Suno Studio 是一种生成式音频工作站（GAW），将 DAW 编辑与 AI 生成结合。

### 关键功能

| 功能 | 说明 |
|---------|-------------|
| **多轨时间线** | 精准编排、叠加与编辑 |
| **分轨分离** | 自动拆分成人声、鼓、贝斯等 |
| **Take Lanes** | 对比多版本生成结果 |
| **Comping** | 组合不同版本的最佳片段 |
| **Replace Section** | 平滑交叉淡入淡出地重生成任意片段 |
| **BPM/音高控制** | 按轨调整速度与音高 |
| **录音** | 直接在时间线录制 |
| **Sample to Song** | 上传短片段扩展成完整作品 |
| **MIDI 导出** | 便于外部 DAW 编辑 |
| **自动保存** | 项目自动保存 |

### Studio 工作流

1. 在 Studio 中创建或导入歌曲
2. 在 Details 面板查看分轨 → Insert All 到时间线
3. 用 Take Lanes 试听不同版本
4. 将最佳片段 Comp 到主轨
5. 添加/替换乐器或人声
6. 导出：整首、选区或多轨

## V5 特性概览

| 特性 | 价值 |
|---------|---------|
| **持续记忆** | 主题动机在 8 分钟内保持一致 |
| **负向提示** | 排除元素：“no vocals”“no guitars” |
| **更好的人声** | 更自然的发音与情绪 |
| **更干净的混音** | 更好的频率分离，减少“浑浊” |
| **更快生成** | 速度提升约 10 倍 |
| **智能编曲** | 自动生成主歌/副歌/桥段结构 |
| **Hoooks** | 生成可分享的短片段用于推广 |

## 按项目类型的流程

### 单曲

1. 明确风格、情绪与目标时长（最多 8 分钟）
2. 用元标签写结构化歌词（每行 6-12 音节）
3. 生成并选择最佳版本
4. 需要时 Extend（用回调保持一致）
5. Remaster（Subtle）做精修

### 歌单创作

1. 明确主题、总时长、曲目数
2. 设计能量曲线（参见 [references/bpm-guide.md](references/bpm-guide.md)）
3. 建立统一风格模板或保存 Persona
4. 按进程生成曲目
5. 全部曲目 Remaster（Subtle）以统一质感
6. 校验总时长与衔接过渡

### 企业/客户项目

1. 调研背景（公司、品牌、价值观）
2. 明确关键信息与语气
3. 在歌词中融入品牌元素
4. 用合适的专业风格生成
5. 需要时使用 Studio（Premier）精修
6. 准备多个版本供客户审阅
7. 记录流程以便迭代

## 最佳实践

### 建议
- 为节奏关键项目指定精确 BPM
- 编写原创歌词（增强版权主张）
- 使用年代参考（"80s synths"、"90s boom bap"）
- 提示词保持聚焦：1-2 个流派 + 1 种情绪 + 乐器
- 重要标签前置到开头几行
- Extend 时用回调："continue with same vibe as chorus"
- 用负向提示排除不需要的元素
- 保存成功的提示词与 Persona 便于复用
- 每行歌词保持 6-12 音节以获得更好对齐

### 避免
- 指名具体艺人（版权风险）
- 在提示词中塞入相互冲突的描述
- 使用模糊描述（"cool song"）
- 为歌单跳过 Remaster 步骤
- 忽视面向受众的内容限制
- 在没有回调的情况下连续 Extend 太多次（会跑偏）
