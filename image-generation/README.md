# image-generation

中文图片生成与改图 Codex skill。它会在用户提出“生成图片 / 画图 / 做海报 / 做封面 / 改图 / 修图 / 换风格 / 参考这张图生成”等需求时触发，并通过用户自己的 OpenAI-compatible 图片接口创建或编辑图片。

默认模型是 `gpt-image-2`，默认输出目录是当前工作目录下的 `image/`。

## 功能

- 文生图：根据中文提示词生成图片。
- 改图：支持本地图片路径、HTTP(S) 图片 URL、data URL。
- 常用自然语言参数映射：尺寸、比例、质量、透明背景、输出格式、数量等。
- 凭据私有化：不会把 `base_url` 或 `api_key` 写进 skill 文件。
- 输出 JSON，方便 Codex 读取生成结果并把图片路径返回给用户。

## 前置条件

- 已安装支持 skills 的 Codex。
- Python 3.10 或更高版本。
- 一个 OpenAI-compatible 图片接口，需支持：
  - `POST /v1/images/generations`
  - `POST /v1/images/edits`

接口需要返回 `data[].b64_json`，或返回 data URL 格式的 `data[].url`。

## 安装

### Windows PowerShell

```powershell
mkdir $env:USERPROFILE\.codex\skills -Force
git clone https://github.com/<your-name>/image-generation.git $env:USERPROFILE\.codex\skills\image-generation
```

### macOS / Linux

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/<your-name>/image-generation.git ~/.codex/skills/image-generation
```

把上面的仓库地址替换成你自己的 GitHub 仓库地址。安装后重启 Codex，或重新打开会话，让 Codex 重新加载 skills。

## 配置 API 凭据

这个 skill 不内置任何接口地址或 API Key。首次使用前，你需要配置自己的图片接口凭据。

推荐使用私有配置文件：

### Windows PowerShell

```powershell
mkdir $env:USERPROFILE\.codex -Force
notepad $env:USERPROFILE\.codex\image-generation.json
```

写入：

```json
{
  "base_url": "https://你的图片接口域名/v1",
  "api_key": "你的 API Key"
}
```

### macOS / Linux

```bash
mkdir -p ~/.codex
nano ~/.codex/image-generation.json
```

写入：

```json
{
  "base_url": "https://你的图片接口域名/v1",
  "api_key": "你的 API Key"
}
```

也可以使用环境变量：

```bash
export IMAGE_BASE_URL="https://你的图片接口域名/v1"
export IMAGE_API_KEY="你的 API Key"
```

如果你已经配置了 OpenAI-compatible 通用变量，也可以直接复用：

```bash
export OPENAI_BASE_URL="https://你的接口域名/v1"
export OPENAI_API_KEY="你的 API Key"
```

凭据读取优先级：

1. 命令行参数 `--base-url` / `--api-key`
2. 环境变量 `IMAGE_BASE_URL` / `IMAGE_API_KEY`
3. 环境变量 `OPENAI_BASE_URL` / `OPENAI_API_KEY`
4. 私有配置文件 `~/.codex/image-generation.json`

不要把真实 API Key 提交到 GitHub。

## 在 Codex 中使用

安装并配置完成后，直接用中文提出图片需求即可，例如：

```text
帮我生成一张 1:1 的水彩风头像，一只圆滚滚的小猪，透明背景
```

```text
把这张图改成复古海报风，保留主体轮廓
```

```text
生成 3 张 16:9 的产品宣传 banner，高清，png
```

在真正调用图片接口前，skill 会要求 Codex 先向用户确认是否使用本 skill。确认后才会继续生成或改图。

## 直接运行脚本

你也可以绕过 Codex，直接调用脚本测试接口是否可用。

文生图：

```bash
python scripts/gen_images.py --mode generate --prompt "一只圆滚滚的小猪，柔和水彩风格" --size "1024x1024" --quality "high"
```

改图：

```bash
python scripts/gen_images.py --mode edit --image "./input.png" --prompt "改成水彩风，保留主体轮廓" --size "1024x1024"
```

指定输出目录：

```bash
python scripts/gen_images.py --mode generate --prompt "赛博朋克城市夜景" --output-dir "./outputs"
```

成功时脚本会输出类似：

```json
{
  "ok": true,
  "paths": ["C:\\path\\to\\image\\20260604-120000-01.png"],
  "used_params": {
    "model": "gpt-image-2",
    "size": "1024x1024",
    "quality": "high",
    "background": null,
    "output_format": "png",
    "n": 1
  }
}
```

## 常用参数

| 自然语言 | 脚本参数 |
| --- | --- |
| `高清`、`高质量` | `--quality high` |
| `透明背景` | `--background transparent --output-format png` |
| `1:1` | `--size 1024x1024` |
| `3:4` | `--size 1024x1536` |
| `4:3` | `--size 1536x1024` |
| `16:9`、`4k横向` | `--size 3840x2160` |
| `9:16`、`4k竖向` | `--size 2160x3840` |
| `生成3张`、`来3张` | `--n 3` |
| `png`、`jpg`、`jpeg`、`webp` | `--output-format <format>` |

完整字段规则见 [`references/fields.md`](references/fields.md)。

## 文件结构

```text
.
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   └── fields.md
└── scripts/
    └── gen_images.py
```

## 安全提醒

- 不要提交 `~/.codex/image-generation.json`。
- 不要在 README、issue、日志、聊天记录里贴真实 API Key。
- 分享仓库时只分享 skill 代码和说明，不分享本地私有配置。
- 如果临时用命令行参数传入 `--api-key`，注意终端历史记录可能会保存命令。

## 许可证

如果你打算公开分享，建议添加一个许可证文件，例如 MIT License。
