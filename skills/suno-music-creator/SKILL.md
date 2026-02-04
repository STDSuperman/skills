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

# Suno AI 音乐生成参数助手

这个 skill 会帮你生成可直接粘贴到 Suno AI 的格式化参数，简化音乐创作流程。

## 工作流程

### 第 1 步：收集需求

我会询问你关于音乐的需求，包括：
- **音乐类型/风格**：流派、情绪、氛围
- **歌词内容**：自定义歌词 / AI 生成 / 纯器乐
- **节奏速度**：BPM 或描述（轻快/中等/缓慢）
- **乐器偏好**：主要乐器或不需要的乐器
- **声线性别**：男声 / 女声 / 无人声
- **特殊要求**：其他个性化需求

### 第 2 步：生成 Suno AI 参数

基于你的需求，我会生成以下格式的输出：

```
═══════════════════════════════════════
📋 SUNO AI 生成参数
═══════════════════════════════════════

【Lyrics 歌词】
[Intro]
[Atmospheric opening]

[Verse 1]
歌词内容...
（每行 6-12 音节效果最佳）

[Chorus]
副歌内容...

[Verse 2]
第二段主歌...

[Bridge]
过渡段...

[Outro]
[Fade out]

-------------------------------------------

【Styles 风格标签】
120bpm, upbeat pop, synthesizer, electric guitar, energetic, modern production

-------------------------------------------

【Advanced Options 高级选项】
✓ Vocal Gender: Female
✓ Lyrics Mode: Manual
✓ Weirdness: 30%
✓ Style Influence: 50%

═══════════════════════════════════════
```

### 第 3 步：直接复制粘贴

你只需将生成的内容复制粘贴到 Suno AI 对应的输入框即可：
1. 复制「Lyrics 歌词」→ 粘贴到 Lyrics 输入框
2. 复制「Styles 风格标签」→ 粘贴到 Styles 输入框
3. 根据「Advanced Options」设置高级选项滑块和开关

## 参数说明

### Lyrics 歌词部分
- 使用 `[标签]` 定义歌曲结构：`[Intro]` `[Verse]` `[Chorus]` `[Bridge]` `[Outro]`
- 可添加情绪/能量指令：`[Soft]` `[Build up]` `[Energetic]` `[Calm]`
- 每行歌词保持 6-12 音节可获得更好的节奏对齐
- 留空表示生成纯器乐音乐

### Styles 风格标签
**推荐格式：**
```
[BPM]bpm, [流派], [情绪], [主要乐器], [人声风格], [制作风格]
```

**示例：**
- `120bpm, upbeat pop, piano, guitar, cheerful, clean production`
- `90bpm, lofi hip hop, jazz piano, vinyl crackle, chill, no vocals`
- `140bpm, edm, synthesizer, bass drop, energetic, no guitars`

**负向提示（排除元素）：**
- 在标签中直接写 `no [元素]`，如：`no vocals`, `no drums`, `no guitars`

### Advanced Options 高级选项

| 选项 | 说明 | 建议值 |
|------|------|--------|
| **Vocal Gender** | 声线性别 | Male / Female（纯器乐则不影响） |
| **Lyrics Mode** | 歌词模式 | Manual（自定义歌词）/ Auto（AI 生成） |
| **Weirdness** | 怪诞度 | 0-30%（常规）/ 50%（平衡）/ 70-100%（实验性） |
| **Style Influence** | 风格影响强度 | 30-50%（平衡）/ 70-100%（严格遵循风格） |

## 快速参考

### 常用 BPM 指南
- **60-80 BPM**：抒情慢歌、冥想、环境音乐
- **90-100 BPM**：Lofi、Chill、R&B
- **110-130 BPM**：流行、摇滚、Hip-Hop
- **130-150 BPM**：House、Techno、舞曲
- **150+ BPM**：Drum & Bass、硬核电子

### 常用结构标签
- `[Intro]` - 前奏
- `[Verse]` / `[Verse 1]` - 主歌
- `[Pre-Chorus]` - 前副歌
- `[Chorus]` - 副歌
- `[Bridge]` - 过渡段/桥段
- `[Solo]` - 独奏段
- `[Outro]` - 尾奏
- `[Instrumental Break]` - 间奏

### 情绪/能量标签
- `[Soft]` - 柔和
- `[Build up]` - 渐强
- `[Energetic]` - 充满活力
- `[Calm]` - 平静
- `[Intense]` - 激烈
- `[Fade out]` - 淡出

### 流派参考
详见 [references/style-library.md](references/style-library.md)

## 使用技巧

### ✅ 建议
- 风格标签保持简洁：1-2 个流派 + 关键乐器 + 情绪
- 为特定用途指定精确 BPM（如健身音乐、视频配乐）
- 使用年代参考增加复古感：`80s synths`, `90s grunge`, `2000s emo`
- 重要关键词放在风格标签的前面
- 原创歌词有助于版权保护

### ❌ 避免
- 不要提及具体艺人名字（版权风险）
- 避免风格标签过长或相互冲突
- 不要使用模糊描述如 "好听的歌"
- 避免在同一首歌中混合过多流派

## 进阶功能参考

如需了解 Suno V5 高级特性、Studio 编辑功能、歌单创作等进阶内容，请查阅：
- [风格库](references/style-library.md) - 各流派提示词模板
- [BPM 指南](references/bpm-guide.md) - 详细的节奏速度应用场景
- [元标签参考](references/metatags.md) - 完整的结构标签列表
- [项目类型](references/project-types.md) - 不同类型音乐项目的最佳实践
