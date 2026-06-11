# Codex Skills

这是一个用于收集和维护本地 Codex skills 的仓库。每个 skill 使用独立目录存放，目录内包含自己的 `SKILL.md`、脚本、参考文档和可选配置。

当前仓库共整理 127 个 skills，其中包含 Accio 导入的 126 个 skills，以及本仓库原有的 `image-generation` skill。所有 skills 已按主要使用场景分类，避免根目录平铺过乱。

## 分类入口

分类规则见 [`CATEGORY_RULES.md`](CATEGORY_RULES.md)，完整分类索引见 [`SKILL_CATEGORIES.md`](SKILL_CATEGORIES.md)，新增流程见 [`ADD_SKILL_WORKFLOW.md`](ADD_SKILL_WORKFLOW.md)。

| 分类目录 | 中文分类 | 数量 | 规则 |
| --- | --- | ---: | --- |
| [`01-market-research-intelligence/`](01-market-research-intelligence/) | 市场研究与商业情报 | 13 | 用于市场、公司、竞品、趋势、评论、平台数据和商业情报分析的技能。 |
| [`02-product-strategy-merchandising/`](02-product-strategy-merchandising/) | 产品策略与商品规划 | 12 | 用于选品、产品设计、产品规划、商品属性、产品发布和商品化策略的技能。 |
| [`03-sourcing-supply-chain/`](03-sourcing-supply-chain/) | 采购供应链与履约 | 13 | 用于采购、供应商、代发、库存、物流、海关、关税、仓储和履约的技能。 |
| [`04-marketplaces-sales-channels/`](04-marketplaces-sales-channels/) | 平台渠道与店铺运营 | 14 | 用于 Amazon、Shopify、TikTok Shop、Etsy、Google Shopping、社交电商等销售渠道运营的技能。 |
| [`05-marketing-growth-crm/`](05-marketing-growth-crm/) | 营销增长与CRM | 15 | 用于广告营销、邮件/生命周期自动化、会员、推荐、社媒、留存、赢回和增长活动的技能。 |
| [`06-seo-content/`](06-seo-content/) | SEO与内容 | 9 | 用于内容策略、文案、关键词、页面审计、SERP、程序化 SEO 和搜索流量增长的技能。 |
| [`07-conversion-pricing-revenue/`](07-conversion-pricing-revenue/) | 转化定价与收入优化 | 9 | 用于 A/B 测试、结账体验、折扣、促销、动态定价、CRO、加购和收入提升的技能。 |
| [`08-finance-payments-compliance/`](08-finance-payments-compliance/) | 财务支付与合规 | 13 | 用于财务模型、预算、利润、估值、发票、支付、拒付、欺诈、税务、VAT 和合规的技能。 |
| [`09-customer-service-returns/`](09-customer-service-returns/) | 客户服务与售后 | 6 | 用于客服、客户分群、客户声音、退换货、评价邀约和销售谈判的技能。 |
| [`10-storefront-dev-integration/`](10-storefront-dev-integration/) | 建站开发与系统集成 | 4 | 用于网站创建、GraphQL、店铺开发、系统接口和工程集成的技能。 |
| [`11-creative-media-design/`](11-creative-media-design/) | 创意媒体与设计 | 5 | 用于图片生成、提示词、Logo、视频、视觉创意和媒体制作的技能。 |
| [`12-documents-office-productivity/`](12-documents-office-productivity/) | 文档办公与协作 | 7 | 用于 Word、PDF、PPT、Excel、飞书、文档共创和内部沟通的技能。 |
| [`13-codex-mcp-tooling/`](13-codex-mcp-tooling/) | Codex/MCP工具与技能管理 | 6 | 用于 Codex skill 创建、查找、审查、MCP 工具、MCP 迁移和 Accio CLI 的技能。 |
| [`14-personal-development-learning/`](14-personal-development-learning/) | 个人发展与学习 | 1 | 用于自我改进、学习规划、个人成长和非业务型个人效率提升的技能。 |

## Accio Skills

Accio 技能索引：

- 中文分类索引：[`ACCIO_SKILLS.md`](ACCIO_SKILLS.md)
- CSV 索引：[`ACCIO_SKILLS.csv`](ACCIO_SKILLS.csv)
- 纯文本名称列表：[`ACCIO_SKILL_NAMES.txt`](ACCIO_SKILL_NAMES.txt)

## 仓库结构

```text
.
|-- README.md
|-- CATEGORY_RULES.md
|-- ADD_SKILL_WORKFLOW.md
|-- SKILL_CATEGORIES.md
|-- ACCIO_SKILLS.md
|-- ACCIO_SKILLS.csv
|-- ACCIO_SKILL_NAMES.txt
|-- 01-market-research-intelligence/
|   |-- README.md
|   `-- skill-id/
|       `-- SKILL.md
`-- 14-personal-development-learning/
    |-- README.md
    `-- skill-id/
        `-- SKILL.md
```

每个 skill 建议保持以下结构：

```text
skill-id/
|-- SKILL.md
|-- README.md              # 可选
|-- agents/                # 可选，存放 agent/plugin 入口配置
|-- references/            # 可选，存放字段规则、示例、设计说明等
`-- scripts/               # 可选，存放可执行脚本
```

## 安装

### 让 Codex 自动安装

在 Codex 里直接发送下面这段话即可：

```text
请从 https://github.com/mocheng998/so-skill.git 安装 Codex skills。递归查找仓库中所有包含 SKILL.md 的技能目录，并把每个技能目录复制到我的 ~/.codex/skills/{skill-id} 下；如果目标目录已存在，请覆盖更新。安装完成后告诉我安装了哪些 skills。
```

如果只想安装指定 skill，可以指定分类路径，例如：

```text
请从 https://github.com/mocheng998/so-skill.git 安装指定 Codex skill：11-creative-media-design/image-generation。只复制这个技能目录到我的 ~/.codex/skills/image-generation；如果目标目录已存在，请覆盖更新。
```

### Windows PowerShell

安装单个 skill：

```powershell
$repo = "C:\path\to\so-skill"
$skill = Join-Path $repo "11-creative-media-design\image-generation"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force $skill "$env:USERPROFILE\.codex\skills\image-generation"
```

安装仓库里的全部 skills：

```powershell
$repo = "C:\path\to\so-skill"
$target = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force $target | Out-Null
Get-ChildItem -Path $repo -Recurse -Filter SKILL.md | ForEach-Object {
  $skillDir = $_.Directory
  Copy-Item -Recurse -Force $skillDir.FullName (Join-Path $target $skillDir.Name)
}
```

### macOS / Linux

安装单个 skill：

```bash
repo=/path/to/so-skill
mkdir -p ~/.codex/skills
cp -R "$repo/11-creative-media-design/image-generation" ~/.codex/skills/image-generation
```

安装仓库里的全部 skills：

```bash
repo=/path/to/so-skill
mkdir -p ~/.codex/skills
find "$repo" -name SKILL.md -print0 | while IFS= read -r -d '' file; do
  dir=$(dirname "$file")
  cp -R "$dir" "$HOME/.codex/skills/$(basename "$dir")"
done
```

安装完成后，重启 Codex 或重新打开会话，让 Codex 重新加载 skills。

## 新增 Skill 约定

快速新增流程见 [`ADD_SKILL_WORKFLOW.md`](ADD_SKILL_WORKFLOW.md)。新增前先按 [`CATEGORY_RULES.md`](CATEGORY_RULES.md) 判断分类；如果不符合现有分类，创建新的编号分类并同步更新规则和索引。

新增 skill 时：

1. 按 [`CATEGORY_RULES.md`](CATEGORY_RULES.md) 选择分类。
2. 如果不符合任何现有分类，创建新的编号分类目录，并更新分类规则和索引。
3. 使用短横线命名目录，例如 `my-skill`。
4. 在目录根部提供 `SKILL.md`，并确保 frontmatter 中有清晰的 `name` 和 `description`。
5. 脚本放在 `scripts/`，长文档、示例、字段映射放在 `references/`。
6. 不要提交 API Key、账号密码、私有配置、日志、缓存或生成产物。

## Git 忽略规则

仓库会忽略 Python 缓存、虚拟环境、本地配置、日志和生成图片目录。私有配置应放在用户目录，例如 `~/.codex/*.json`，不要放进仓库。
