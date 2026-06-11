# 新增 Skill 快速流程

这个流程用于后续把新 skill 快速、稳定地加入本仓库。核心原则：先分类，再放目录，再更新索引，最后校验。

## 1. 准备信息

新增前先确认 4 件事：

| 项目 | 要求 | 示例 |
| --- | --- | --- |
| Skill ID | 小写短横线命名，不使用空格 | `amazon-review-exporter` |
| 中文名 | 用于索引展示 | `亚马逊评论导出器` |
| 主要用途 | 用一句话说明它解决什么问题 | `导出并分析 Amazon 产品评论` |
| 来源 | Accio、本仓库自建、第三方仓库等 | `Accio` |

每个 skill 目录必须包含：

```text
skill-id/
|-- SKILL.md
|-- README.md              # 可选
|-- agents/                # 可选
|-- references/            # 可选
`-- scripts/               # 可选
```

## 2. 选择分类

先打开 [`CATEGORY_RULES.md`](CATEGORY_RULES.md)，按“主要使用场景”选择分类。

| 场景 | 放入分类 |
| --- | --- |
| 市场、公司、竞品、趋势、评论情报 | `01-market-research-intelligence` |
| 选品、产品设计、产品规划、商品属性 | `02-product-strategy-merchandising` |
| 采购、供应商、库存、物流、关税、履约 | `03-sourcing-supply-chain` |
| Amazon、Shopify、TikTok Shop、Etsy、Google Shopping | `04-marketplaces-sales-channels` |
| 广告、会员、邮件、生命周期、留存、增长活动 | `05-marketing-growth-crm` |
| SEO、内容、关键词、SERP、文案 | `06-seo-content` |
| A/B 测试、CRO、结账、折扣、定价、收入优化 | `07-conversion-pricing-revenue` |
| 财务、支付、税务、VAT、合规、发票、估值 | `08-finance-payments-compliance` |
| 客服、售后、退换货、客户声音、销售谈判 | `09-customer-service-returns` |
| 建站、GraphQL、店铺开发、工程集成 | `10-storefront-dev-integration` |
| 图片、视频、Logo、提示词、创意媒体 | `11-creative-media-design` |
| Word、PDF、PPT、Excel、飞书、文档协作 | `12-documents-office-productivity` |
| Codex skill、MCP、CLI、技能治理 | `13-codex-mcp-tooling` |
| 自我改进、学习、个人成长 | `14-personal-development-learning` |

如果新 skill 不符合任何现有分类，执行第 5 节“新增分类流程”。

## 3. 放入目录

把 skill 放到：

```text
分类目录/skill-id/
```

PowerShell 示例：

```powershell
$repo = "C:\Users\ycwh\ai\skill"
$source = "C:\path\to\new-skill"
$category = "04-marketplaces-sales-channels"
$skillId = "amazon-review-exporter"

Copy-Item -Recurse -Force $source (Join-Path $repo "$category\$skillId")
```

如果是移动仓库内已有目录，优先使用 `git mv`：

```powershell
git -C C:\Users\ycwh\ai\skill mv old-skill 04-marketplaces-sales-channels/amazon-review-exporter
```

## 4. 更新索引

新增或移动 skill 后，按来源更新对应索引。

所有 skill 都要更新：

1. [`SKILL_CATEGORIES.md`](SKILL_CATEGORIES.md)
2. 对应分类目录下的 `README.md`
3. 根目录 [`README.md`](README.md) 中的分类数量

如果是 Accio skill，还要更新：

1. [`ACCIO_SKILLS.md`](ACCIO_SKILLS.md)
2. [`ACCIO_SKILLS.csv`](ACCIO_SKILLS.csv)
3. [`ACCIO_SKILL_NAMES.txt`](ACCIO_SKILL_NAMES.txt)

新增条目时保持同一分类内按 `skill_id` 字母顺序排列。

## 5. 新增分类流程

只有当新 skill 不符合任何现有分类时，才创建新分类。

1. 取下一个编号，例如当前最大是 `14-...`，新分类用 `15-new-category-name`。
2. 分类目录名使用英文小写短横线，语义清楚。
3. 创建分类目录和分类 README。
4. 更新 [`CATEGORY_RULES.md`](CATEGORY_RULES.md)，写清楚新分类的适用范围。
5. 更新 [`SKILL_CATEGORIES.md`](SKILL_CATEGORIES.md) 和根目录 [`README.md`](README.md)。
6. 如果新 skill 来自 Accio，同步更新 Accio 三个索引文件。

新分类 README 模板：

```markdown
# 中文分类名

一句话说明这个分类收纳什么类型的 skills。

| Skill | 中文名 |
| --- | --- |
| [`skill-id/`](skill-id/) | 中文名 |
```

## 6. 校验

新增完成后运行：

```powershell
$repo = "C:\Users\ycwh\ai\skill"

$skills = Get-ChildItem -Path $repo -Recurse -Filter SKILL.md |
  Where-Object { $_.FullName -notmatch "\\.git\\" }

"skills_with_SKILL_md=$($skills.Count)"

$rootLevel = $skills | Where-Object { $_.Directory.Parent.FullName -eq $repo }
"root_level_skill_dirs=$($rootLevel.Count)"
```

期望结果：

```text
root_level_skill_dirs=0
```

如果更新了 `ACCIO_SKILLS.csv`，再校验 CSV 路径：

```powershell
@'
from pathlib import Path
import csv

root = Path(r"C:\Users\ycwh\ai\skill")
missing = []

with (root / "ACCIO_SKILLS.csv").open("r", encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        skill_dir = root / row["path"]
        if not (skill_dir / "SKILL.md").exists():
            missing.append(row["path"])

print("missing_csv_paths", len(missing))
for path in missing:
    print(path)
'@ | python -
```

期望结果：

```text
missing_csv_paths 0
```

## 7. Git 提交

确认只提交本次新增 skill 和索引更新：

```powershell
git -C C:\Users\ycwh\ai\skill status --short
git -C C:\Users\ycwh\ai\skill add <本次新增或更新的文件>
git -C C:\Users\ycwh\ai\skill commit -m "Add <skill-id> skill"
```

如果工作区里有无关未跟踪文件，不要一起提交。

## 8. 给 Codex 的快捷指令

以后可以直接对 Codex 说：

```text
请按照 C:\Users\ycwh\ai\skill\ADD_SKILL_WORKFLOW.md 的流程，把这个 skill 加入 C:\Users\ycwh\ai\skill。
先判断分类；如果不符合现有分类，创建新分类并更新分类规则和索引。
完成后运行校验，但不要提交，除非我明确要求提交。
```
