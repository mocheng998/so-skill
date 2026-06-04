---
name: image-generation
description: 中文图片生成与改图 skill。用户只要表达生成图片、画图、帮我画一个、帮我画张图、帮我做张图、帮我出图、出一张图、出图、文生图、做配图、生成配图、做封面图、做头图、做海报、做 banner、做主图、做头像、做插图、来一张图、来几张图、整一张图、弄一张图、给我画、给我生成一张、生成一张某某风格的图、把这张图改一下、帮我修图、帮我改图、改一下这张图、重绘这张图、局部重绘、图片风格化、换个风格、以图生图、垫图生成、参考这张图生成，就优先触发。前文如果刚生成、展示、上传、引用过一张图片，后续用户继续说帮我改一下、优化一下、调整一下、微调一下、换个风格、重做一下、再来一版、基于这张图修改、保留主体改一下、在刚才那张图上修改、按这个图继续改，也优先触发。使用 scripts/gen_images.py，支持文生图和改图，默认输出到当前工作目录的 image/ 目录。
---

# 图片生成

使用用户提供的 OpenAI-compatible 图片接口创建或编辑位图图片。默认模型为 `gpt-image-2`，输出保存到当前工作目录的 `image/`，目录不存在时脚本会自动创建。

## 核心原则

- 不要把 `base_url` 或 `api_key` 写进 `SKILL.md`、引用文档、日志或最终回复。
- 在真正调用本 skill 或执行图片接口前，先询问用户是否确认使用本 skill；得到明确同意后再继续。
- 优先从环境变量读取凭据：`IMAGE_BASE_URL` 和 `IMAGE_API_KEY`。
- 也支持 `OPENAI_BASE_URL` / `OPENAI_API_KEY`，以及私有配置 `~/.codex/image-generation.json`。
- 如果用户在对话里直接提供 key，只在本次命令环境里临时使用，不要复述完整 key。
- 缺少凭据时，先给用户首次配置提示，不要盲目调用接口。
- 缺少图片任务必填信息时先追问，例如 `prompt` 或改图的图片来源。

## 首次安装后配置

这个 skill 不内置任何 `base_url` 或 `api_key`。用户第一次安装后，必须自己配置图片接口凭据才能使用。

优先建议用户创建私有配置文件 `~/.codex/image-generation.json`：

```bash
mkdir -p ~/.codex
```

然后在 `~/.codex/image-generation.json` 中写入自己的接口地址和 Key：

```json
{
  "base_url": "https://你的图片接口域名/v1",
  "api_key": "你的 API Key"
}
```

也可以只在当前终端会话中临时配置环境变量：

```bash
export IMAGE_BASE_URL="https://你的图片接口域名/v1"
export IMAGE_API_KEY="你的 API Key"
```

如果用户已经有 OpenAI-compatible 通用变量，也可以使用：

```bash
export OPENAI_BASE_URL="https://你的接口域名/v1"
export OPENAI_API_KEY="你的 API Key"
```

分享 skill 给别人时，只分享 skill 目录；不要分享自己的 `~/.codex/image-generation.json`，也不要把真实 Key 写进仓库、压缩包、聊天记录或日志。

## 工作流

1. 判断任务类型：没有明确图片来源时按文生图 `generate`；有本地路径、URL 或 data URL 且语义是修改时按改图 `edit`。
2. 在调用本 skill 的实际生成或改图能力前，先询问用户是否确认使用本 skill；只有在用户明确同意后再继续。
3. 提取 `prompt`、图片来源、尺寸、质量、背景、格式、数量等字段。字段规则见 `references/fields.md`。
4. 如果缺少凭据，提示用户完成首次配置：创建 `~/.codex/image-generation.json`，或设置 `IMAGE_BASE_URL` / `IMAGE_API_KEY` 环境变量。
5. 调用 `scripts/gen_images.py`，不要重写一次性图片 API 脚本；文生图走 JSON，请求改图走 `multipart/form-data` 上传图片。
6. 根据脚本输出检查是否成功，并向用户报告图片路径和关键参数。

## 凭据来源

脚本按以下顺序读取配置：

1. 命令行参数 `--base-url` 与 `--api-key`，仅在用户明确要求或临时测试时使用。
2. 环境变量 `IMAGE_BASE_URL` 和 `IMAGE_API_KEY`。
3. 环境变量 `OPENAI_BASE_URL` 和 `OPENAI_API_KEY`。
4. 私有 JSON 配置 `~/.codex/image-generation.json`：

```json
{
  "base_url": "https://example.com/v1",
  "api_key": "sk-..."
}
```

不要自动创建这个配置文件，除非用户明确要求保存凭据。

## 调用方式

文生图：

```bash
python3 "<skill-dir>/scripts/gen_images.py" --mode generate --prompt "一只圆滚滚的小猪，柔和水彩风格" --size "1024x1024" --quality "high"
```

改图：

```bash
python3 "<skill-dir>/scripts/gen_images.py" --mode edit --image "./input.png" --prompt "改成水彩风，保留主体轮廓" --size "1024x1024"
```

输出目录默认是当前工作目录下的 `image/`。如果用户明确要求其他目录，使用 `--output-dir <目录>`；相对路径按当前工作目录解析。

按 `references/fields.md` 计算超时：普通图片 10 分钟，约 4K 或 800 万像素以上 15 分钟。

## 参数映射

- `高清`、`高质量` -> `--quality high`
- `透明背景` -> `--background transparent --output-format png`
- `1:1` -> `--size 1024x1024`
- `3:4` -> `--size 1024x1536`
- `4:3` -> `--size 1536x1024`
- `16:9`、`4k横向` -> `--size 3840x2160`
- `9:16`、`4k竖向` -> `--size 2160x3840`
- `生成3张`、`来3张` -> `--n 3`
- `png`、`jpg`、`jpeg`、`webp` -> `--output-format <format>`

## 输出处理

脚本成功时输出 JSON，`paths` 应位于当前工作区的 `image/` 目录，除非用户明确指定了其他输出目录：

```json
{"ok": true, "paths": ["..."], "used_params": {"model": "gpt-image-2", "size": "1024x1024", "quality": "high", "output_format": "png", "n": 1}}
```

最终回复用户时使用中文，包含：

- `图片已生成，图片路径：<路径>`
- `实际使用的关键参数：model=..., size=..., quality=..., output_format=..., n=...`

失败时简短说明：

- `生成失败：<错误原因>`
