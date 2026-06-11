# Skill 分类规则

本仓库采用“主要使用场景优先”的分类方式。每个 skill 只能放在一个主分类中；如果一个 skill 横跨多个领域，优先放到用户最可能寻找它的分类。

完整操作流程见 [`ADD_SKILL_WORKFLOW.md`](ADD_SKILL_WORKFLOW.md)。本文件只维护分类判断规则；具体新增、索引更新、校验和提交步骤以流程文档为准。

## 新增 skill 时的处理流程

1. 先阅读新 skill 的 `SKILL.md`，确认它解决的主要问题、目标用户和典型触发场景。
2. 对照下方分类规则，选择最贴近“主要使用场景”的分类目录。
3. 将 skill 放入对应分类目录：`分类目录/skill-id/`。目录名使用小写短横线，例如 `my-new-skill`。
4. 如果新 skill 不符合任何现有分类，不要硬塞进旧分类；创建新的编号分类目录，并在本文件、`SKILL_CATEGORIES.md`、`README.md` 和相关索引中同步更新规则。
5. 每个 skill 目录根部必须包含 `SKILL.md`。脚本放入 `scripts/`，长文档、示例、字段规则放入 `references/`。
6. 不提交 API Key、账号密码、本地私有配置、日志、缓存或生成产物。

## 分类判定优先级

当一个 skill 同时命中多个分类时，按下面顺序判断：

1. 平台强绑定技能优先放入“平台渠道与店铺运营”，例如 Amazon、Shopify、TikTok Shop、Etsy、Google Shopping。
2. 支付、财务、税务、合规、发票、估值相关技能优先放入“财务支付与合规”。
3. 供应商、采购、库存、海关、仓储和履约相关技能优先放入“采购供应链与履约”。
4. 内容、文案、关键词、SERP、页面 SEO 相关技能优先放入“SEO与内容”。
5. A/B 测试、CRO、结账、折扣、促销、动态定价和收入优化相关技能优先放入“转化定价与收入优化”。
6. Codex skill、MCP、CLI、工具迁移和技能治理相关技能优先放入“Codex/MCP工具与技能管理”。
7. 仍然冲突时，以用户搜索时最可能使用的业务词为准，并在分类 README 中保持解释一致。

## 现有分类

### 01-market-research-intelligence - 市场研究与商业情报

规则：用于市场、公司、竞品、趋势、评论、平台数据和商业情报分析的技能。

当前数量：13

### 02-product-strategy-merchandising - 产品策略与商品规划

规则：用于选品、产品设计、产品规划、商品属性、产品发布和商品化策略的技能。

当前数量：12

### 03-sourcing-supply-chain - 采购供应链与履约

规则：用于采购、供应商、代发、库存、物流、海关、关税、仓储和履约的技能。

当前数量：13

### 04-marketplaces-sales-channels - 平台渠道与店铺运营

规则：用于 Amazon、Shopify、TikTok Shop、Etsy、Google Shopping、社交电商等销售渠道运营的技能。

当前数量：14

### 05-marketing-growth-crm - 营销增长与CRM

规则：用于广告营销、邮件/生命周期自动化、会员、推荐、社媒、留存、赢回和增长活动的技能。

当前数量：15

### 06-seo-content - SEO与内容

规则：用于内容策略、文案、关键词、页面审计、SERP、程序化 SEO 和搜索流量增长的技能。

当前数量：9

### 07-conversion-pricing-revenue - 转化定价与收入优化

规则：用于 A/B 测试、结账体验、折扣、促销、动态定价、CRO、加购和收入提升的技能。

当前数量：9

### 08-finance-payments-compliance - 财务支付与合规

规则：用于财务模型、预算、利润、估值、发票、支付、拒付、欺诈、税务、VAT 和合规的技能。

当前数量：13

### 09-customer-service-returns - 客户服务与售后

规则：用于客服、客户分群、客户声音、退换货、评价邀约和销售谈判的技能。

当前数量：6

### 10-storefront-dev-integration - 建站开发与系统集成

规则：用于网站创建、GraphQL、店铺开发、系统接口和工程集成的技能。

当前数量：4

### 11-creative-media-design - 创意媒体与设计

规则：用于图片生成、提示词、Logo、视频、视觉创意和媒体制作的技能。

当前数量：5

### 12-documents-office-productivity - 文档办公与协作

规则：用于 Word、PDF、PPT、Excel、飞书、文档共创和内部沟通的技能。

当前数量：7

### 13-codex-mcp-tooling - Codex/MCP工具与技能管理

规则：用于 Codex skill 创建、查找、审查、MCP 工具、MCP 迁移和 Accio CLI 的技能。

当前数量：6

### 14-personal-development-learning - 个人发展与学习

规则：用于自我改进、学习规划、个人成长和非业务型个人效率提升的技能。

当前数量：1
