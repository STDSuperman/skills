## 目标
基于 mp3 链接帮我生成带字幕 + 关键帧 + 每一帧上下平移的视频，使用.claude下的skills来做，相邻帧平移方向相反，平移时间等于这一个片段的展示时间。
同时要求转录出来的没个字幕不应该是多个字符分隔的一整句，一整句应该拆成独立的一个字幕来合成视频

## 资源结构
- 资源目录：./resource
- suno生成参数文档：./resource/suno-params.md，里面有 suno 生成歌曲的歌词和风格参数。
- 目标mp3链接：https://cdn1.suno.ai/36182814-3400-445f-ae1e-e8c6726f8ea6.mp3
- 歌词字幕应该从mp3转录出来，然后跟suno的歌词去做校准，把每句字幕歌词时间轴对上。

## 输出说明
- 所有输出产物需要放到跟本文档同级的当前目录下的./output里。

## 语音转录配置
- 默认使用 **FunASR** 模型进行语音转录（通过阿里云 DashScope API）
-模型：使用 `fun-asr`
- API 配置：需要在 `.claude/skills/video-composer/.env` 文件中设置 `DASHSCOPE_API_KEY`(已设置)