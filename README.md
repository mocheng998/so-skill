# Codex Skills

这是一个用于收集和维护本地 Codex skills 的仓库。每个 skill 使用一个独立目录存放，目录内包含自己的 `SKILL.md`、脚本、参考文档和可选的 agent 配置。

当前仓库只包含一个生图相关 skill，后续可以按同样结构继续添加新的能力。

## Skills

| Skill | 说明 | 路径 |
| --- | --- | --- |
| `image-generation` | 使用用户配置的 OpenAI-compatible 图片接口进行文生图和改图，默认模型为 `gpt-image-2`。 | [`image-generation/`](image-generation/) |

## 仓库结构

```text
.
├── README.md
├── image-generation/
│   ├── SKILL.md
│   ├── README.md
│   ├── agents/
│   ├── references/
│   └── scripts/
└── .gitignore
```

每个 skill 建议保持以下结构：

```text
skill-name/
├── SKILL.md
├── README.md
├── agents/          # 可选，存放 agent/plugin 入口配置
├── references/      # 可选，存放字段规则、示例、设计说明等
└── scripts/         # 可选，存放可执行脚本
```

## 安装

### 让 Codex 自动安装

在 Codex 里直接发送下面这段话即可让 Codex 帮你安装：

```text
请从 https://github.com/mocheng998/so-skill.git 安装 Codex skills。
把仓库中所有包含 SKILL.md 的目录复制到我的 ~/.codex/skills 目录下；
如果目标目录已存在，请覆盖更新。安装完成后告诉我安装了哪些 skills。
```

### Windows PowerShell

安装单个 skill：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\image-generation" "$env:USERPROFILE\.codex\skills\image-generation"
```

安装仓库里的全部 skills：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Get-ChildItem -Directory | Where-Object {
  Test-Path (Join-Path $_.FullName "SKILL.md")
} | ForEach-Object {
  Copy-Item -Recurse -Force $_.FullName "$env:USERPROFILE\.codex\skills\$($_.Name)"
}
```

### macOS / Linux

安装单个 skill：

```bash
mkdir -p ~/.codex/skills
cp -R ./image-generation ~/.codex/skills/image-generation
```

安装仓库里的全部 skills：

```bash
mkdir -p ~/.codex/skills
for dir in */; do
  if [ -f "$dir/SKILL.md" ]; then
    cp -R "$dir" "$HOME/.codex/skills/${dir%/}"
  fi
done
```

安装完成后，重启 Codex 或重新打开会话，让 Codex 重新加载 skills。

## `image-generation`

`image-generation` 用于中文图片生成和改图请求。它通过用户自己的 OpenAI-compatible 图片 API 工作，不在仓库中保存 `base_url` 或 `api_key`。

常见配置方式：

```json
{
  "base_url": "https://你的图片接口域名/v1",
  "api_key": "你的 API Key"
}
```

把配置保存到：

- Windows: `%USERPROFILE%\.codex\image-generation.json`
- macOS / Linux: `~/.codex/image-generation.json`

也可以使用环境变量：

```bash
export IMAGE_BASE_URL="https://你的图片接口域名/v1"
export IMAGE_API_KEY="你的 API Key"
```

具体用法见 [`image-generation/README.md`](image-generation/README.md)。

## 新增 Skill 约定

新增 skill 时建议：

1. 使用短横线命名目录，例如 `my-skill`。
2. 在目录根部提供 `SKILL.md`，并确保 frontmatter 中有清晰的 `name` 和 `description`。
3. 如果有脚本，放在 `scripts/` 下，并在 skill README 中写清楚运行方式。
4. 如果有字段映射、示例或长说明，放在 `references/` 下，避免 `SKILL.md` 过长。
5. 不要把 API Key、账号密码、私有配置或生成产物提交到仓库。
6. 在本 README 的 Skills 表格中新增一行索引。

## Git 忽略规则

仓库会忽略 Python 缓存、虚拟环境、本地配置、日志和生成图片目录。私有配置应放在用户目录，例如 `~/.codex/*.json`，不要放进仓库。
