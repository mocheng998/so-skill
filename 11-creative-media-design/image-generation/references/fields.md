# 字段与交互规则

## 必填字段

文生图需要：

- `prompt`

改图需要：

- `prompt`
- `image`，支持本地路径、HTTP(S) URL、data URL；脚本会以 `multipart/form-data` 上传到编辑接口

缺少 `prompt` 时追问：

`请补充图片提示词，例如你想生成什么画面。`

改图缺少图片来源时追问：

`请提供要编辑的图片来源：1）本地路径 2）图片 URL / data URL`

## 可选字段

- `model`：默认 `gpt-image-2`
- `size`
- `quality`
- `background`
- `output_format`
- `output_compression`
- `partial_images`
- `n`：默认 `1`
- `moderation`
- `input_fidelity`：改图可用
- `mask`：改图可用
- `output_dir`：默认当前工作目录的 `image/`

## 自然语言映射

### size

- `1024x1024`、`1:1` -> `size=1024x1024`
- `1024x1536`、`3:4` -> `size=1024x1536`
- `1536x1024`、`4:3` -> `size=1536x1024`
- `2048x2048` -> `size=2048x2048`
- `3840x2160`、`16:9`、`4k横向` -> `size=3840x2160`
- `2160x3840`、`9:16`、`4k竖向` -> `size=2160x3840`
- `auto` -> `size=auto`

### quality

- `高清`、`高质量`、`高品质` -> `quality=high`
- `中等质量` -> `quality=medium`
- `低质量` -> `quality=low`

### background

- `透明背景` -> `background=transparent`
- `白色背景` -> `background=white`
- `黑色背景` -> `background=black`

### output_format

- `png` -> `output_format=png`
- `jpg` -> `output_format=jpg`
- `jpeg` -> `output_format=jpeg`
- `webp` -> `output_format=webp`

### n

- `生成3张`、`来3张`、`输出3张` -> `n=3`
- 未指定时默认 `n=1`

## timeout 规则

调用脚本前按 `size` 计算超时：

- `size` 匹配 `宽x高` 且 `宽 * 高 >= 8000000` 时，使用 15 分钟。
- 其他情况使用 10 分钟。
- `auto`、缺少 `size` 或无法解析尺寸时，使用 10 分钟。

## 回复规则

成功后报告：

- `图片已生成，图片路径：<路径>`
- `实际使用的关键参数：model=..., size=..., quality=..., output_format=..., n=...`

如果用户没有指定输出目录，确认路径位于当前工作区的 `image/` 目录；目录不存在时脚本会自动创建。

失败后报告：

- `生成失败：<简短错误原因>`
