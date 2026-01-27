图片生成支持下新平台：

新平台调用示例代码：

```python
import requests

url = "https://api.jiekou.ai/v3/seedream-4.5"

payload = {
    "size": "<string>",
    "image": [{}],
    "prompt": "<string>",
    "watermark": True,
    "optimize_prompt_options": { "mode": "<string>" },
    "sequential_image_generation": "<string>",
    "sequential_image_generation_options": { "max_images": 123 }
}
headers = {
    "Content-Type": "<content-type>",
    "Authorization": "<authorization>"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
```

详细文档如：https://docs.jiekou.ai/docs/models/reference-seedream-4.5

这里默认关掉水印


加好新平台后在图片生成 skill 的 .env 里加一个开启这个平台的环境变量和新平台的 api key 参数，我会给你填好，你可以等待我填好，填好我会告诉你，你禁止访问这个文件


上面都完成后读取 create/music-create 里的task.md,合成一个带图片画面和音频的视频,字幕暂时不要，只需要对每个小结生成一个图片来合成即可，使用即梦4.5生成，要求每一个生图提示词要是氛围感风格


字幕 + 时间轴的数据如下直接使用，禁止重新调用 asr 转录获取：

```json
{
    "utterances": [
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 19860,
            "start_time": 15400,
            "text": "最后一班地铁 你没回头",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 15760,
                    "start_time": 15400,
                    "text": "最"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 16040,
                    "start_time": 15760,
                    "text": "后"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 16440,
                    "start_time": 16040,
                    "text": "一"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 16480,
                    "start_time": 16440,
                    "text": "班"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 16680,
                    "start_time": 16480,
                    "text": "地"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 17160,
                    "start_time": 16680,
                    "text": "铁"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 17160,
                    "start_time": 17160,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 17560,
                    "start_time": 17240,
                    "text": "你"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 17840,
                    "start_time": 17560,
                    "text": "没"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 18360,
                    "start_time": 17840,
                    "text": "回"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 19860,
                    "start_time": 18360,
                    "text": "头"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 25980,
            "start_time": 20520,
            "text": "我站在原地 数着秒",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 20880,
                    "start_time": 20520,
                    "text": "我"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 21080,
                    "start_time": 20880,
                    "text": "站"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 21520,
                    "start_time": 21080,
                    "text": "在"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 21920,
                    "start_time": 21520,
                    "text": "原"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 22520,
                    "start_time": 21920,
                    "text": "地"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 22520,
                    "start_time": 22520,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 24240,
                    "start_time": 23440,
                    "text": "数"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 25160,
                    "start_time": 24760,
                    "text": "着"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 25980,
                    "start_time": 25160,
                    "text": "秒"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 32800,
            "start_time": 27320,
            "text": "想追想去 可脚步怎么都迈不开",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 27840,
                    "start_time": 27320,
                    "text": "想"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 28200,
                    "start_time": 27840,
                    "text": "追"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 28480,
                    "start_time": 28200,
                    "text": "想"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 29120,
                    "start_time": 28480,
                    "text": "去"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 29120,
                    "start_time": 29120,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 29520,
                    "start_time": 29240,
                    "text": "可"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 29760,
                    "start_time": 29520,
                    "text": "脚"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 29920,
                    "start_time": 29760,
                    "text": "步"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 30200,
                    "start_time": 29920,
                    "text": "怎"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 30360,
                    "start_time": 30200,
                    "text": "么"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 30880,
                    "start_time": 30360,
                    "text": "都"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 31120,
                    "start_time": 30880,
                    "text": "迈"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 31560,
                    "start_time": 31120,
                    "text": "不"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 32800,
                    "start_time": 31560,
                    "text": "开"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 35360,
            "start_time": 32800,
            "text": "月台上的风很冷",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 33120,
                    "start_time": 32800,
                    "text": "月"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 33280,
                    "start_time": 33120,
                    "text": "台"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 33560,
                    "start_time": 33280,
                    "text": "上"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 33800,
                    "start_time": 33560,
                    "text": "的"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 34320,
                    "start_time": 33800,
                    "text": "风"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 34960,
                    "start_time": 34320,
                    "text": "很"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 35360,
                    "start_time": 34960,
                    "text": "冷"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 41620,
            "start_time": 35360,
            "text": "吹散了 你说过 会等我的那些话",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 35800,
                    "start_time": 35360,
                    "text": "吹"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 36160,
                    "start_time": 35800,
                    "text": "散"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 36560,
                    "start_time": 36160,
                    "text": "了"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 36560,
                    "start_time": 36560,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 37120,
                    "start_time": 36840,
                    "text": "你"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 37520,
                    "start_time": 37120,
                    "text": "说"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 37720,
                    "start_time": 37520,
                    "text": "过"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 37720,
                    "start_time": 37720,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 38240,
                    "start_time": 37720,
                    "text": "会"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 38680,
                    "start_time": 38240,
                    "text": "等"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 39200,
                    "start_time": 38680,
                    "text": "我"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 39480,
                    "start_time": 39200,
                    "text": "的"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 39840,
                    "start_time": 39480,
                    "text": "那"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 40240,
                    "start_time": 39840,
                    "text": "些"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 41620,
                    "start_time": 40240,
                    "text": "话"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 46220,
            "start_time": 41920,
            "text": "当一盏盏熄灭",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 42240,
                    "start_time": 41920,
                    "text": "当"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 43000,
                    "start_time": 42240,
                    "text": "一"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 43520,
                    "start_time": 43000,
                    "text": "盏"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 44240,
                    "start_time": 43760,
                    "text": "盏"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 45120,
                    "start_time": 44640,
                    "text": "熄"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 46220,
                    "start_time": 45120,
                    "text": "灭"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 52980,
            "start_time": 48680,
            "text": "我还在这",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 49720,
                    "start_time": 48680,
                    "text": "我"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 50560,
                    "start_time": 49720,
                    "text": "还"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 51880,
                    "start_time": 50560,
                    "text": "在"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 52980,
                    "start_time": 51880,
                    "text": "这"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 57500,
            "start_time": 54200,
            "text": "如果重来",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 54720,
                    "start_time": 54200,
                    "text": "如"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 55240,
                    "start_time": 54720,
                    "text": "果"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 56040,
                    "start_time": 55240,
                    "text": "重"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 57500,
                    "start_time": 56040,
                    "text": "来"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 63340,
            "start_time": 57720,
            "text": "我不会让你一个人 走进车厢",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 58240,
                    "start_time": 57720,
                    "text": "我"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 58680,
                    "start_time": 58240,
                    "text": "不"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 59520,
                    "start_time": 58680,
                    "text": "会"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 59960,
                    "start_time": 59520,
                    "text": "让"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 60280,
                    "start_time": 59960,
                    "text": "你"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 60560,
                    "start_time": 60280,
                    "text": "一"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 60840,
                    "start_time": 60560,
                    "text": "个"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 61200,
                    "start_time": 60840,
                    "text": "人"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 61200,
                    "start_time": 61200,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 61480,
                    "start_time": 61200,
                    "text": "走"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 61960,
                    "start_time": 61480,
                    "text": "进"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 62280,
                    "start_time": 61960,
                    "text": "车"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 63340,
                    "start_time": 62280,
                    "text": "厢"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 71020,
            "start_time": 67720,
            "text": "如果重来",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 68080,
                    "start_time": 67720,
                    "text": "如"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 68760,
                    "start_time": 68080,
                    "text": "果"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 69600,
                    "start_time": 68760,
                    "text": "重"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 71020,
                    "start_time": 69600,
                    "text": "来"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 75360,
            "start_time": 71080,
            "text": "那些沉默的夜晚 我会开口说想你",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 71520,
                    "start_time": 71080,
                    "text": "那"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 71680,
                    "start_time": 71520,
                    "text": "些"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 71800,
                    "start_time": 71680,
                    "text": "沉"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 72160,
                    "start_time": 71800,
                    "text": "默"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 72400,
                    "start_time": 72160,
                    "text": "的"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 72600,
                    "start_time": 72400,
                    "text": "夜"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 72960,
                    "start_time": 72600,
                    "text": "晚"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 72960,
                    "start_time": 72960,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 73280,
                    "start_time": 72960,
                    "text": "我"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 73480,
                    "start_time": 73280,
                    "text": "会"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 73800,
                    "start_time": 73480,
                    "text": "开"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 74080,
                    "start_time": 73800,
                    "text": "口"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 74520,
                    "start_time": 74080,
                    "text": "说"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 74960,
                    "start_time": 74520,
                    "text": "想"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 75360,
                    "start_time": 74960,
                    "text": "你"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 80500,
            "start_time": 75360,
            "text": "可是没没有如果",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 75760,
                    "start_time": 75360,
                    "text": "可"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 76040,
                    "start_time": 75760,
                    "text": "是"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 76440,
                    "start_time": 76040,
                    "text": "没"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 78320,
                    "start_time": 77680,
                    "text": "没"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 79120,
                    "start_time": 78680,
                    "text": "有"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 79160,
                    "start_time": 79120,
                    "text": "如"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 80500,
                    "start_time": 79160,
                    "text": "果"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 87780,
            "start_time": 81400,
            "text": "列车开走后 站太空了",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 81760,
                    "start_time": 81400,
                    "text": "列"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 82280,
                    "start_time": 81800,
                    "text": "车"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 83120,
                    "start_time": 82280,
                    "text": "开"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 83400,
                    "start_time": 83120,
                    "text": "走"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 84480,
                    "start_time": 83400,
                    "text": "后"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 84480,
                    "start_time": 84480,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 85200,
                    "start_time": 84760,
                    "text": "站"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 85720,
                    "start_time": 85200,
                    "text": "太"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 86560,
                    "start_time": 85720,
                    "text": "空"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 87780,
                    "start_time": 86560,
                    "text": "了"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 95180,
            "start_time": 88080,
            "text": "只剩我 和没说出口的对不起",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 88640,
                    "start_time": 88080,
                    "text": "只"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 89080,
                    "start_time": 88640,
                    "text": "剩"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 89880,
                    "start_time": 89080,
                    "text": "我"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 89880,
                    "start_time": 89880,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 90200,
                    "start_time": 89880,
                    "text": "和"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 90680,
                    "start_time": 90200,
                    "text": "没"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 91000,
                    "start_time": 90680,
                    "text": "说"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 91560,
                    "start_time": 91000,
                    "text": "出"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 91880,
                    "start_time": 91560,
                    "text": "口"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 92440,
                    "start_time": 91880,
                    "text": "的"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 92840,
                    "start_time": 92440,
                    "text": "对"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 94120,
                    "start_time": 92840,
                    "text": "不"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 95180,
                    "start_time": 94120,
                    "text": "起"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 107300,
            "start_time": 103160,
            "text": "手机里还存着 你发的 最后一条消息",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 103480,
                    "start_time": 103160,
                    "text": "手"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 103680,
                    "start_time": 103480,
                    "text": "机"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 103880,
                    "start_time": 103680,
                    "text": "里"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 104080,
                    "start_time": 103880,
                    "text": "还"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 104240,
                    "start_time": 104080,
                    "text": "存"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 104560,
                    "start_time": 104240,
                    "text": "着"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 104560,
                    "start_time": 104560,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 104720,
                    "start_time": 104560,
                    "text": "你"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 105000,
                    "start_time": 104720,
                    "text": "发"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 105120,
                    "start_time": 105000,
                    "text": "的"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 105120,
                    "start_time": 105120,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 105360,
                    "start_time": 105120,
                    "text": "最"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 105560,
                    "start_time": 105360,
                    "text": "后"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 105800,
                    "start_time": 105560,
                    "text": "一"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 105920,
                    "start_time": 105800,
                    "text": "条"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 106280,
                    "start_time": 105920,
                    "text": "消"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 107300,
                    "start_time": 106280,
                    "text": "息"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 111840,
            "start_time": 107400,
            "text": "晚安之后 就再也没有然后了",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 107840,
                    "start_time": 107400,
                    "text": "晚"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 108360,
                    "start_time": 107840,
                    "text": "安"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 108920,
                    "start_time": 108680,
                    "text": "之"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 109200,
                    "start_time": 108920,
                    "text": "后"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 109200,
                    "start_time": 109200,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 109400,
                    "start_time": 109200,
                    "text": "就"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 109640,
                    "start_time": 109400,
                    "text": "再"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 109840,
                    "start_time": 109640,
                    "text": "也"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 110160,
                    "start_time": 109840,
                    "text": "没"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 110480,
                    "start_time": 110200,
                    "text": "有"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 110800,
                    "start_time": 110480,
                    "text": "然"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 111240,
                    "start_time": 110800,
                    "text": "后"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 111840,
                    "start_time": 111240,
                    "text": "了"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 115820,
            "start_time": 111840,
            "text": "我试着回播你的后乐",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 112200,
                    "start_time": 111840,
                    "text": "我"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 112720,
                    "start_time": 112200,
                    "text": "试"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 112920,
                    "start_time": 112720,
                    "text": "着"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 113440,
                    "start_time": 112920,
                    "text": "回"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 113840,
                    "start_time": 113440,
                    "text": "播"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 114280,
                    "start_time": 113840,
                    "text": "你"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 114640,
                    "start_time": 114280,
                    "text": "的"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 115080,
                    "start_time": 114640,
                    "text": "后"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 115820,
                    "start_time": 115080,
                    "text": "乐"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 121420,
            "start_time": 116080,
            "text": "总叫独独生",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 116520,
                    "start_time": 116080,
                    "text": "总"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 117120,
                    "start_time": 116640,
                    "text": "叫"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 120040,
                    "start_time": 118960,
                    "text": "独"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 120320,
                    "start_time": 120200,
                    "text": "独"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 121420,
                    "start_time": 120320,
                    "text": "生"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 127620,
            "start_time": 123000,
            "text": "假装你只是暂时不防辩解",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 123320,
                    "start_time": 123000,
                    "text": "假"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 123720,
                    "start_time": 123320,
                    "text": "装"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 124000,
                    "start_time": 123720,
                    "text": "你"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 124560,
                    "start_time": 124000,
                    "text": "只"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 124840,
                    "start_time": 124560,
                    "text": "是"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 125400,
                    "start_time": 124840,
                    "text": "暂"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 125640,
                    "start_time": 125400,
                    "text": "时"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 126160,
                    "start_time": 125640,
                    "text": "不"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 126400,
                    "start_time": 126160,
                    "text": "防"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 126640,
                    "start_time": 126400,
                    "text": "辩"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 127620,
                    "start_time": 126680,
                    "text": "解"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 135640,
            "start_time": 129160,
            "text": "为什么 当时我没能说出那句留下来",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 129480,
                    "start_time": 129160,
                    "text": "为"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 129720,
                    "start_time": 129480,
                    "text": "什"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 130000,
                    "start_time": 129720,
                    "text": "么"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 130000,
                    "start_time": 130000,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 130480,
                    "start_time": 130000,
                    "text": "当"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 130880,
                    "start_time": 130480,
                    "text": "时"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 131320,
                    "start_time": 131080,
                    "text": "我"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 131560,
                    "start_time": 131320,
                    "text": "没"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 131720,
                    "start_time": 131560,
                    "text": "能"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 132120,
                    "start_time": 131720,
                    "text": "说"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 132440,
                    "start_time": 132120,
                    "text": "出"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 133000,
                    "start_time": 132440,
                    "text": "那"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 133400,
                    "start_time": 133000,
                    "text": "句"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 134080,
                    "start_time": 133400,
                    "text": "留"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 134640,
                    "start_time": 134080,
                    "text": "下"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 135640,
                    "start_time": 134640,
                    "text": "来"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 138640,
            "start_time": 135640,
            "text": "现在想说的话 堆积成山",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 135960,
                    "start_time": 135640,
                    "text": "现"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 136160,
                    "start_time": 135960,
                    "text": "在"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 136360,
                    "start_time": 136160,
                    "text": "想"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 136600,
                    "start_time": 136360,
                    "text": "说"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 136840,
                    "start_time": 136600,
                    "text": "的"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 137240,
                    "start_time": 136840,
                    "text": "话"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 137240,
                    "start_time": 137240,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 137520,
                    "start_time": 137240,
                    "text": "堆"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 137800,
                    "start_time": 137520,
                    "text": "积"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 138080,
                    "start_time": 137800,
                    "text": "成"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 138640,
                    "start_time": 138080,
                    "text": "山"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 142420,
            "start_time": 138640,
            "text": "却再也传不到你那边",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 138960,
                    "start_time": 138640,
                    "text": "却"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 139160,
                    "start_time": 138960,
                    "text": "再"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 139400,
                    "start_time": 139160,
                    "text": "也"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 139520,
                    "start_time": 139400,
                    "text": "传"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 139760,
                    "start_time": 139520,
                    "text": "不"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 140040,
                    "start_time": 139760,
                    "text": "到"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 140200,
                    "start_time": 140040,
                    "text": "你"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 140840,
                    "start_time": 140200,
                    "text": "那"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 142420,
                    "start_time": 140840,
                    "text": "边"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 149580,
            "start_time": 143320,
            "text": "时间它不停解释 就这样把我们推远",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 143560,
                    "start_time": 143320,
                    "text": "时"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 143960,
                    "start_time": 143560,
                    "text": "间"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 144240,
                    "start_time": 143960,
                    "text": "它"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 144640,
                    "start_time": 144240,
                    "text": "不"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 145000,
                    "start_time": 144640,
                    "text": "停"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 145400,
                    "start_time": 145000,
                    "text": "解"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 145840,
                    "start_time": 145440,
                    "text": "释"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 145840,
                    "start_time": 145840,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 146560,
                    "start_time": 146280,
                    "text": "就"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 146760,
                    "start_time": 146560,
                    "text": "这"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 146960,
                    "start_time": 146760,
                    "text": "样"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 147400,
                    "start_time": 146960,
                    "text": "把"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 147640,
                    "start_time": 147400,
                    "text": "我"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 148000,
                    "start_time": 147640,
                    "text": "们"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 148400,
                    "start_time": 148000,
                    "text": "推"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 149580,
                    "start_time": 148440,
                    "text": "远"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 154200,
            "start_time": 153400,
            "text": "耶",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 154200,
                    "start_time": 153400,
                    "text": "耶"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 158940,
            "start_time": 155640,
            "text": "如果重来",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 155960,
                    "start_time": 155640,
                    "text": "如"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 156600,
                    "start_time": 155960,
                    "text": "果"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 157200,
                    "start_time": 156600,
                    "text": "重"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 158940,
                    "start_time": 157440,
                    "text": "来"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 164700,
            "start_time": 159040,
            "text": "我不会在车门关上前选择",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 159640,
                    "start_time": 159040,
                    "text": "我"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 160080,
                    "start_time": 159640,
                    "text": "不"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 160880,
                    "start_time": 160080,
                    "text": "会"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 161360,
                    "start_time": 160880,
                    "text": "在"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 161720,
                    "start_time": 161360,
                    "text": "车"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 162120,
                    "start_time": 161720,
                    "text": "门"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 162560,
                    "start_time": 162120,
                    "text": "关"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 162800,
                    "start_time": 162560,
                    "text": "上"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 163360,
                    "start_time": 162800,
                    "text": "前"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 163640,
                    "start_time": 163360,
                    "text": "选"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 164700,
                    "start_time": 163640,
                    "text": "择"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 167900,
            "start_time": 166240,
            "text": "沉默",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 166440,
                    "start_time": 166240,
                    "text": "沉"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 167900,
                    "start_time": 166440,
                    "text": "默"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 172420,
            "start_time": 169360,
            "text": "如果重来",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 169440,
                    "start_time": 169360,
                    "text": "如"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 170120,
                    "start_time": 169440,
                    "text": "果"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 170760,
                    "start_time": 170120,
                    "text": "重"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 172420,
                    "start_time": 170960,
                    "text": "来"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 176520,
            "start_time": 172600,
            "text": "会抓紧你的手 告诉你别走",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 173080,
                    "start_time": 172600,
                    "text": "会"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 173400,
                    "start_time": 173080,
                    "text": "抓"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 173600,
                    "start_time": 173400,
                    "text": "紧"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 173800,
                    "start_time": 173600,
                    "text": "你"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 174000,
                    "start_time": 173800,
                    "text": "的"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 174400,
                    "start_time": 174000,
                    "text": "手"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 174400,
                    "start_time": 174400,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 174520,
                    "start_time": 174400,
                    "text": "告"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 175040,
                    "start_time": 174520,
                    "text": "诉"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 175520,
                    "start_time": 175040,
                    "text": "你"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 176120,
                    "start_time": 175520,
                    "text": "别"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 176520,
                    "start_time": 176120,
                    "text": "走"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 178380,
            "start_time": 176520,
            "text": "可是想念",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 176840,
                    "start_time": 176520,
                    "text": "可"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 177080,
                    "start_time": 176840,
                    "text": "是"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 177400,
                    "start_time": 177080,
                    "text": "想"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 178380,
                    "start_time": 177400,
                    "text": "念"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 181940,
            "start_time": 179840,
            "text": "愿有道再见",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 179880,
                    "start_time": 179840,
                    "text": "愿"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 180240,
                    "start_time": 179880,
                    "text": "有"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 180560,
                    "start_time": 180240,
                    "text": "道"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 180800,
                    "start_time": 180560,
                    "text": "再"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 181940,
                    "start_time": 180800,
                    "text": "见"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 186200,
            "start_time": 182760,
            "text": "列车驶向远方",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 183240,
                    "start_time": 182760,
                    "text": "列"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 183640,
                    "start_time": 183240,
                    "text": "车"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 184160,
                    "start_time": 183640,
                    "text": "驶"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 184960,
                    "start_time": 184480,
                    "text": "向"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 185400,
                    "start_time": 184960,
                    "text": "远"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 186200,
                    "start_time": 185400,
                    "text": "方"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 194740,
            "start_time": 186200,
            "text": "而我困在这个 说不出 再见的站台",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 186600,
                    "start_time": 186200,
                    "text": "而"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 187120,
                    "start_time": 186600,
                    "text": "我"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 187920,
                    "start_time": 187120,
                    "text": "困"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 188320,
                    "start_time": 187920,
                    "text": "在"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 188760,
                    "start_time": 188320,
                    "text": "这"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 189320,
                    "start_time": 188760,
                    "text": "个"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 189320,
                    "start_time": 189320,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 190080,
                    "start_time": 189520,
                    "text": "说"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 190480,
                    "start_time": 190080,
                    "text": "不"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 191280,
                    "start_time": 190480,
                    "text": "出"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 191280,
                    "start_time": 191280,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 191720,
                    "start_time": 191280,
                    "text": "再"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 192160,
                    "start_time": 191720,
                    "text": "见"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 193000,
                    "start_time": 192160,
                    "text": "的"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 193680,
                    "start_time": 193000,
                    "text": "站"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 194740,
                    "start_time": 193800,
                    "text": "台"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 207300,
            "start_time": 204680,
            "text": "月台的灯又亮了",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 204840,
                    "start_time": 204680,
                    "text": "月"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 205120,
                    "start_time": 204840,
                    "text": "台"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 205280,
                    "start_time": 205120,
                    "text": "的"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 205720,
                    "start_time": 205280,
                    "text": "灯"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 205960,
                    "start_time": 205720,
                    "text": "又"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 206360,
                    "start_time": 205960,
                    "text": "亮"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 207300,
                    "start_time": 206360,
                    "text": "了"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 210240,
            "start_time": 207880,
            "text": "下一班列车清晨",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 208280,
                    "start_time": 207880,
                    "text": "下"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 208480,
                    "start_time": 208280,
                    "text": "一"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 208640,
                    "start_time": 208480,
                    "text": "班"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 209000,
                    "start_time": 208640,
                    "text": "列"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 209240,
                    "start_time": 209000,
                    "text": "车"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 209680,
                    "start_time": 209240,
                    "text": "清"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 210240,
                    "start_time": 209680,
                    "text": "晨"
                }
            ]
        },
        {
            "attribute": {
                "event": "singing"
            },
            "end_time": 215980,
            "start_time": 210240,
            "text": "可我知道 上面不会有你",
            "words": [
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 210760,
                    "start_time": 210240,
                    "text": "可"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 211040,
                    "start_time": 210760,
                    "text": "我"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 211120,
                    "start_time": 211040,
                    "text": "知"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 211920,
                    "start_time": 211120,
                    "text": "道"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 211920,
                    "start_time": 211920,
                    "text": " "
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 213560,
                    "start_time": 213160,
                    "text": "上"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 213800,
                    "start_time": 213560,
                    "text": "面"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 214080,
                    "start_time": 213800,
                    "text": "不"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 214440,
                    "start_time": 214080,
                    "text": "会"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 214720,
                    "start_time": 214440,
                    "text": "有"
                },
                {
                    "attribute": {
                        "event": "singing"
                    },
                    "end_time": 215980,
                    "start_time": 214720,
                    "text": "你"
                }
            ]
        }
    ]
}
```