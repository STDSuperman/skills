# 元标签与结构参考（V5 更新）

放在 [方括号] 内的元标签可控制 Suno 的结构、人声与制作风格。V5 对标签的遵循更稳定，尤其在 Studio 时间线中。

## V5 提示最佳实践

- **前置控制**：关键标签放在前 3-5 行
- **保持简洁**：1-2 个流派 + 1 个情绪 + 可选乐器
- **音节数**：每行 6-12 个音节更利于对齐
- **Extend 用回调**："continue with same vibe as chorus"
- **负向提示**：在风格提示词中添加排除项（"no guitars"、"no harsh distortion"）

## 结构标签

在歌词栏中使用 `[ ]` 放置标签来控制歌曲结构。

### 基础标签

| 标签 | 作用 |
|-----|------|
| `[Intro]` | 器乐或轻人声开场 |
| `[Verse]` / `[Verse 1]` | 主叙事段 |
| `[Pre-Chorus]` | 副歌前的张力铺垫 |
| `[Chorus]` | 主 Hook、记忆点 |
| `[Post-Chorus]` | 副歌后能量延续 |
| `[Bridge]` | 和声/旋律变化 |
| `[Break]` | 器乐间歇、鼓点 Drop |
| `[Hook]` | 重复的抓耳短句 |
| `[Interlude]` | 段落间器乐过渡 |
| `[Outro]` | 结尾 |
| `[End]` | 明确结束标记 |
| `[Fade Out]` | 渐弱到静音 |

### 器乐标签

| 标签 | 作用 |
|-----|------|
| `[Instrumental]` | 无人声段落 |
| `[Guitar Solo]` | 吉他独奏 |
| `[Piano Solo]` | 钢琴独奏 |
| `[Synth Solo]` | 合成器独奏 |
| `[Drum Break]` | 鼓段落 |
| `[Drop]` | EDM 式低频 Drop |
| `[Build]` | 逐步蓄力段 |

## 控制标签

### 能量与情绪

```
[Mood: Uplifting]
[Mood: Dark]
[Mood: Melancholic]
[Mood: Aggressive]
[Mood: Peaceful]
[Mood: Triumphant]
[Energy: Low]
[Energy: Medium]
[Energy: High]
[Energy: Rising]
[Energy: Maximum]
[Energy: Medium→High]
```

### 情绪化段落标签（V5）

V5 会识别段落的情绪修饰：
```
[angry verse]
[sad verse]
[whimsical verse]
[hopeful chorus]
[melancholic bridge]
```

### 乐器配置

```
[Instrument: Piano]
[Instrument: Acoustic Guitar]
[Instrument: Electric Guitar (Distorted)]
[Instrument: Electric Guitar (Clean)]
[Instrument: Strings (Legato)]
[Instrument: Strings (Staccato)]
[Instrument: Brass]
[Instrument: Synth Pads]
[Instrument: 808 Bass]
[Instrument: Bright Electric Guitars, Live Drums]
```

### 质感与年代标签（V5）

```
[Texture: Tape-Saturated]
[Texture: Vinyl Hiss]
[Texture: Lo-fi]
[Texture: Crisp Digital]
```

### 人声风格

```
[Vocal Style: Whisper]
[Vocal Style: Soft]
[Vocal Style: Power]
[Vocal Style: Raspy]
[Vocal Style: Falsetto]
[Vocal Style: Belt]
[Vocal Style: Spoken Word]
[Vocal Style: Rap]
[Vocal Style: Open, Confident]
```

### V5 Persona（更稳定）

V5 对 Persona 的一致性优于旧版本：
- **Whisper Soul** – lo-fi 亲密感
- **Power Praise** – gospel 赞歌
- **Retro Diva** – synthpop 与 disco
- **Conversational Flow** – 清晰的 hip hop 语感

### 人声效果

```
[Vocal Effect: Reverb]
[Vocal Effect: Delay]
[Vocal Effect: Auto-tune]
[Vocal Effect: Vocoder]
[Vocal Effect: Distortion]
```

### 人声音高调制（V5）

```
[modulate up a key]
[modulate down a key]
```

### 特效（V5）

```
[crowd sings]
[echo effect]
[loop-friendly]
```

### 回调标签（V5 - 用于 Extend）

用于 Extend 时保持一致性：
```
[Callback: continue with same vibe as chorus]
[Callback: maintain energy from verse]
```

## 演唱表现指示

### 文本格式

| 格式 | 效果 |
|--------|--------|
| `UPPERCASE TEXT` | 叫喊/强调 |
| `(text in parentheses)` | 和声/背唱 |
| Repeated lines | 循环唱法 |
| `~word~` | 拉长音 |
| `word-` | 突然截断 |

### 节奏提示

```
[Slow]
[Fast]
[Half-time]
[Double-time]
[Breakdown]
[Buildup, 8 bars]
[Instrumental, 4 bars]
```

## 完整示例（V5 优化）

注：每行 6-12 音节、标签前置、可回调。

```
[Intro]
[Mood: Uplifting]
[Energy: Medium→High]
[Instrument: Bright Electric Guitars, Live Drums]

[Verse 1]
[Vocal Style: Open, Confident]
Walking through the morning light
Shadows fading out of sight
Every step a new beginning
Feel the world around me spinning

[Pre-Chorus]
[Energy: Rising]
Here it comes, can you feel it now
The moment we've been waiting for

[Chorus]
[Energy: High]
[Vocal Style: Power]
We are RISING, breaking through the sky
Nothing's gonna stop us, born to fly
(Born to fly, born to fly)
This is our time, THIS IS OUR TIME!

[Verse 2]
[Vocal Style: Soft]
Doubt was holding back my dreams
Nothing ever as it seems
Now I see the path before me
Written in the stars, my story

[Pre-Chorus]
[Energy: Rising]
[Callback: continue with same vibe as chorus]
Here it comes, can you feel it now
The moment we've been waiting for

[Chorus]
[Energy: High]
We are RISING, breaking through the sky
Nothing's gonna stop us, born to fly

[Bridge]
[Mood: Triumphant]
[Texture: Tape-Saturated]
[Instrument: Full orchestra]
When they said impossible
We said WATCH US NOW
When they tried to pull us down
We rose above the crowd

[Drop]
[Energy: Maximum]

[Chorus]
[Vocal Style: Belt]
We are RISING, breaking through the sky
NOTHING'S GONNA STOP US!

[Outro]
[Fade Out]
Rising... rising... born to fly...
```

## 结构建议

### 歌曲长度控制
- 段落越多，歌曲越长（V5 支持最长 8 分钟）
- 2 段主歌 + 2 段副歌 ≈ 2-3 分钟
- 加入 Bridge 与 Outro 可达 3-4 分钟
- 用 `[Instrumental, X bars]` 进行补足

### 能量管理
- 以 `[Energy: Medium]` 开始，为后续提升留空间
- 在 Pre-Chorus 使用 `[Energy: Rising]`
- 用 `[Energy: Medium→High]` 做渐变过渡
- 末段副歌冲顶到 `[Energy: High]` 或 `[Maximum]`
- Outro 逐步降低

### 连贯性
- 副歌结构保持一致
- 标签风格统一
- 情绪标签与歌词内容一致
- V5 的持续记忆可保持动机一致

### V5 特别提示
- Extend 时使用回调，避免风格漂移
- 风格栏负向提示："no guitars"、"no harsh distortion"
- 情绪化段落标签表现更好：[sad verse]、[angry chorus]
- "loop-friendly" 可用于无缝循环
- 歌单整体建议 Remaster（Subtle）

### 常见错误
- 连续标签过多（模型难以理解）
- 情绪指令互相矛盾
- 短歌曲使用过于复杂的结构
- 缺少必要段落（Intro/Outro）
- Extend 过多且无回调（造成漂移）
- 单行超过 12 音节（对齐问题）

### 故障排查

| 问题 | 解决方案 |
|---------|----------|
| 提示词过载（标签被忽略） | 简化为 1-2 个流派，情绪更具体 |
| 过度重复 | 加入 "variation/dynamic" 或 Replace section |
| 伪影（嘶声/闪烁） | 先尝试 Remaster Subtle |
| 人声被埋 | 导出分轨重平衡，或更换 Persona |
| Extend 漂移 | 重新注入流派/情绪 + 使用回调措辞 |
