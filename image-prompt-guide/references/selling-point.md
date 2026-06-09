# 卖点图 (Selling Point Image)

## 场景说明

基于商品原图生成突出产品核心卖点的营销图片。卖点图的核心是通过 **商品主体 + 细节部位（可选）+ 卖点文案（核心、简短）+ 排版** 的组合方式，让消费者快速理解产品优势。

> **与细节图的区别**：细节图是纯粹的「原图局部放大」，不添加文案和排版；卖点图则是「营销导向」的图片，需要融合文案与视觉排版来传达产品卖点。

## 应用方式：拼接

在用户或 Agent 根据需求生成的卖点描述 prompt **后面**拼接以下固定文案。

## Prompt 模板

### 用户/Agent 生成部分

#### Step 1: 卖点来源判定（用户输入 vs Agent 推断）

| 情况 | 判定条件 | Agent 行为 |
|------|----------|------------|
| **用户已提供具体卖点** | 用户 query 中明确提到了卖点内容（如"突出防水和轻量"、"卖点是40dB降噪和30小时续航"） | **以用户卖点为基础**：用户卖点直接进入候选池，Agent 仅做适配改写（翻译为英文短语、控制词数、去除冗余），不得替换或篡改语义。**无需确认，直接执行** |
| **用户未提供具体卖点** | 用户仅表达"生成卖点图"、"做一张卖点图"等意图，但未说明具体卖点 | **Agent 自主构建候选池**：根据商品主体的品类特征、上传图片中可见的产品特点，按下方"卖点判定五维度"推断卖点候选，完成 Step 2–4 后 → **必须通过 `ask_user` 工具向用户确认**（见下方"卖点确认交互"） |
| **混合场景** | 用户提供了部分卖点但不足以填满层级 | **以用户卖点为 L1（核心卖点）**，Agent 基于五维度补充 L2 / L3 层级 → **补充部分必须通过 `ask_user` 工具向用户确认**（见下方"卖点确认交互"） |

#### 卖点确认交互（ask_user）

当 Agent 需要推断或补充卖点时（即上表中「用户未提供」或「混合场景」），**必须在生图前**通过 `ask_user` 工具将推断结果呈现给用户确认。

**交互规则**：

| 步骤 | Agent 行为 | 用户可选操作 |
|------|-----------|-------------|
| 1. 呈现推断结果 | 使用 `ask_user` 工具，将推断的卖点层级（核心卖点 / 功能亮点 / 可信证明）+ 选定的构图模板以选项形式展示给用户 | — |
| 2. 用户反馈 | 等待用户响应 | **确认**：同意当前卖点方案，Agent 直接执行生图<br>**修改**：Agent 将已规划的全部卖点文案预填到输入框中，用户在此基础上直接编辑（改措辞、删减、替换），提交后 Agent 按「用户已提供具体卖点」逻辑直接执行生图 |
| 3. 执行生图 | 根据最终确认的卖点方案构建 prompt 并调用工具 | — |

**ask_user 呈现格式**：

第一步 — 卖点确认弹窗（卖点内容放在**题目**中，按 markdown 格式分行展示，选项仅保留两项）：

```
问题（题目，markdown 格式，每层级之间必须空一行确保独立成段）：

我根据商品特征为您推断了以下卖点方案，请确认或调整：

**核心卖点**：{核心卖点文案}

**功能亮点**：{功能亮点1}、{功能亮点2}

**可信证明**：{可信证明文案}

构图模板：「{模板名}」

选项（仅两项，纯操作不带卖点内容）：
- 确认生图
- 修改卖点
```

第二步 — 用户点击「修改卖点」后，再次通过 `ask_user` 弹出编辑窗口（题目中**继续保留**完整卖点的 markdown 排版，让用户看着原方案进行编辑）：

```
问题（题目，markdown 格式，每层级之间必须空一行确保独立成段）：

请在以下卖点方案基础上修改（直接在输入框中编辑）：

**核心卖点**：{核心卖点文案}

**功能亮点**：{功能亮点1}、{功能亮点2}

**可信证明**：{可信证明文案}

输入框预填内容（与题目同源，方便用户在原文基础上修改，纯文本一行一条）：

核心卖点：{核心卖点文案}
功能亮点：{功能亮点1}、{功能亮点2}
可信证明：{可信证明文案}
```

**修改操作的预填规则**：
- 题目（markdown 排版）和输入框（纯文本预填）**同步携带完整卖点方案**，每层级单独一行
- **题目中每层级之间必须用空行分隔**（markdown 段落规则），否则渲染时会合并成一段
- 若某层级不存在则该行省略
- 用户在输入框直接编辑：修改措辞、删除某行、替换为其他卖点
- 用户提交修改后，Agent 将修改后的内容视为「用户已提供具体卖点」，**不再二次确认**，直接进入适配改写 → 构图选择 → 生图流程

**交互约束**：
- **仅限 Agent 推断/补充场景**：用户已明确提供全部卖点时，不触发确认流程，直接执行
- **一轮确认即可**：用户确认或修改提交后立即执行，不做二次追问
- **修改后走「用户已提供」逻辑**：用户修改提交的文案等同于用户主动提供的卖点，Agent 仅做适配改写（词数、英文转换），不得再次推翻用户意图

#### Step 2: 卖点判定（什么算"卖点"）

候选卖点必须落入以下五个维度之一，Agent 推断卖点时也只能从这五类中产出：

| 维度 | 含义 | 示例 |
|------|------|------|
| **利益/体验** | 给买家带来的直接利益或使用体验 | "all-day comfort"、"silent commute"、"effortless cleaning" |
| **可量化优势** | 用数字/参数表达的硬指标 | "40dB ANC"、"24h cold"、"30H Battery"、"IPX8" |
| **场景化能力 / 适用人群** | 明确的使用场景或目标用户 | "通勤静音"、"母婴可用"、"office-friendly"、"travel-ready" |
| **资质 / 认证** | 权威背书与合规性 | "FDA-approved"、"BPA-free"、"CE Certified"、"OEKO-TEX" |
| **痛点解决** | 直接对应消费者抱怨/恐惧的解决方案 | "防滑"、"不漏水"、"no slipping"、"leak-proof" |

> **不属于卖点**：纯主观形容词（"高品质"、"好看"）、品类常识（"可以装水"）、营销套话（"匠心打造"）。一律不得作为卖点输出。

#### Step 3: 卖点分层改写（L1 → L2 → L3）

> **命名说明**：内部 prompt 构建沿用 L1/L2/L3 作为模型层级语义；**面向用户的所有展示**（ask_user 弹窗、Agent 回复话术）统一使用「核心卖点 / 功能亮点 / 可信证明」。

将候选池中的卖点按以下三层结构组织，Agent 需根据卖点丰富度判断输出到第几层：

| 层级（内部代号） | 用户可见名称 | 选取规则 | 文案要求 |
|------|------|----------|----------|
| **L1** | **核心卖点** | 从候选卖点池里挑**最有差异化 / 用户决策权重最高**的 1 个卖点 | 极简（≤4 词），通常对应"利益/体验"或"可量化优势"维度 |
| **L2** | **功能亮点** | 对 L1 的**展开或补充**——可能是场景化解释、参数支撑、或并列的次级卖点，1–2 条 | 简短（≤6 词），通常来自"场景化能力"或"可量化优势" |
| **L3** | **可信证明** | 包含**可验证元素**：数字、认证名、测试条件、用户数 | 短语形式，例如 "FDA-grade silicone"、"Loved by 10k+ moms"，通常来自"资质/认证"或量化数据 |

**输出层级判断规则（结合候选池丰富度自动决定输出几层）**：

| 候选池情况 | 输出层级 | task_type |
|-----------|---------|-----------|
| 候选池仅 1 个差异化卖点，或用户明确要求"极简卖点图" | 仅 L1 | `simple_generation` |
| 候选池有 1 个核心 + 1–2 个补充（典型场景） | L1 + L2 | `simple_generation` |
| 候选池中同时存在差异化卖点、功能补充、可验证证据（认证/数据） | L1 + L2 + L3 | `complex_generation` |

> **改写规范（统一适用于 L1/L2/L3）**：
> - 每条文案不超过 6 个英文词 / 8 个中文字
> - 优先使用数据化表达（"40dB ANC" 优于 "强力降噪"）
> - 保留用户原始措辞的核心信息，不得篡改语义
> - 若用户提供的卖点过长，提炼关键词后告知用户改写结果
> - L1 必须是差异化最强的一条；L2 不得与 L1 语义重复；L3 必须包含可验证元素

#### Step 4: 构图模板选择

根据 L1/L2/L3 输出层级与商品特性，从以下 5 种构图模板中选择最匹配的一种，作为排版指引的基础：

| 构图模板 | 适用场景 | 视觉特征 | 视觉锚点（必备元素） | 与层级匹配 | Prompt 关键词 |
|----------|----------|----------|---------------------|------------|---------------|
| **① 单卖点强调（一图一点）** | 主打一个核心卖点，强调记忆点；候选池只有 1 个差异化卖点；社媒首图/广告头图 | 商品居中或偏侧，**单一大字号**主标题占据画面显眼位置，留白充足 | • **辅助动态线条**烘托卖点：风线 / 弧光 / 弯折轨迹 / 速度线，引导视线指向卖点<br>• **放大局部**：在主商品旁附 1 个圆形或矩形特写突出卖点位置 | 仅 L1 | "single bold headline beside the product, large typography, generous whitespace, dynamic motion lines (wind / light arc / curved trail) emphasizing the selling point, optional circular zoom-in highlighting the key area, one-focal-point composition" |
| **② 多卖点罗列（2×2 / 3 列）** | 需并列展示多个卖点；详情页前几屏；亚马逊 A+ 模块 | 商品居中，卖点以**网格/分栏**方式环绕（2×2 四宫格、3 列横排或竖排），每点配小标题 | • **圆形特写图**：每个卖点配一个**圆形局部特写**展示对应部位<br>• 圆形特写下方/旁边附**短文字标注**（≤6 词）<br>• 圆形之间排列整齐、间距均衡 | L1 + L2（2–4 条卖点并列） | "product centered, surrounded by circular close-up callouts of key feature areas, each circular thumbnail paired with a short text label (≤6 words), arranged in a 2x2 grid or 3-column layout with even spacing" |
| **③ 参数规格图（数据可视化）** | 强调可量化参数；技术品类（电子、家电、户外装备）；规格对比 | 商品作为视觉主体，配**数字徽章 / 标尺 / 引线标注**呈现参数；可附小图标（电池、容量、防水等级） | • **双向箭头 + 引线（必备）**：用于标注尺寸、距离、容量等区间数值<br>• **数字标在引线旁边**，不与商品主体重叠<br>• 必要时配小图标（电池/容量/防水等级） | L1 + L2 偏数值，常含 L3 | "product with technical callouts, double-headed arrows with leader lines indicating dimensions/specs, numeric values placed alongside the leader lines (not overlapping the product), small icons for battery/capacity/IP rating, infographic style, technical visualization" |
| **④ 使用图（场景+标注）** | 强调使用场景与人群；服饰、家居、母婴、户外 | 真实使用情境中的商品，文案以**短引线/标签**指向具体使用部位或场景元素 | • **细引线 + 短文字**：纤细的引线（thin leader lines）指向商品功能部位<br>• 每条引线尾端配 ≤6 词的短标签<br>• 引线避免穿过人物面部或商品主体 | L1（场景化）+ L2（功能标注） | "product in real-life usage scene, thin leader lines connecting short text labels (≤6 words) to specific usage details on the product, lifestyle context, leader lines never crossing faces or main product silhouette" |
| **⑤ 对比竞品图（vs others）** | 凸显差异化优势；行业同质化严重的品类 | 画面**左右分栏 / vs 双列**：左侧 "Others" 弱化呈现痛点，右侧 "Ours" 高亮卖点；中间用 "VS" 或对比图标 | • **每行 ✓/✗ 标记**：左侧每条对比项前置 ✗（红色或灰），右侧前置 ✓（绿色或品牌色）<br>• ✓/✗ 与文字同行对齐，强化情绪与差异感<br>• 两列对比项行数一致<br>• **⚠️ 严禁体现竞品品牌名 / 商标 / Logo / 包装文字**：左侧竞品必须用**灰色方块、轮廓剪影或抽象灰色物体**代替，仅对比关键功能点 | L1（差异点）+ L2（具体对比项） | "split-screen comparison layout, left side labeled 'Others' showing a generic gray silhouette / abstract gray block as the competitor placeholder (NO brand names, NO logos, NO trademarks, NO recognizable packaging) with each pain point prefixed by a red ✗ in muted tones, right side labeled 'Ours' highlighting our product with each selling point prefixed by a green ✓ aligned row by row, bold 'VS' divider in the middle, equal number of items on both sides, comparison focused only on key functional points" |

**构图模板选择规则（自动判断）**：

| 触发条件 | 推荐构图 |
|----------|----------|
| 仅 L1，或用户要求"突出一个卖点" | ① 单卖点强调 |
| L1 + L2（2–4 条并列卖点，无明显数据/认证） | ② 多卖点罗列 |
| 含较多可量化指标（如 40dB / 24h / IPX8）或 L3 偏数据，**且用户已主动提供具体参数数值** | ③ 参数规格图 |
| 商品有明确使用场景或目标人群（服饰/家居/户外/母婴） | ④ 使用图 |
| 用户明确要求"对比"、"vs 竞品"、"差异化" | ⑤ 对比竞品图 |

> **⚠️ 参数规格图前置条件**：构图③ 参数规格图仅在**用户已主动给出具体参数数值**（如尺寸、容量、续航时长、防水等级等数字）时才可选用。若用户未提供任何可量化参数，即使商品品类偏技术型，也**禁止 Agent 自行编造数值**，应降级为构图② 多卖点罗列 或构图④ 使用图。

> **构图与 task_type**：
> - 模板 ①、② → 排版相对简单 → `simple_generation`
> - 模板 ③、④、⑤ → 含引线标注/分栏对比/场景元素，排版复杂 → `complex_generation`

#### Prompt 构建要素

| 要素 | 是否必选 | 说明 | 示例 |
|------|----------|------|------|
| **商品主体** | ✅ 必选 | 商品的整体展示，作为画面主角 | "wireless noise-canceling headphones as the main subject" |
| **细节部位** | ⬚ 可选 | 需要重点展示的局部区域，用于辅助说明卖点 | "with a close-up callout on the ear cushion memory foam" |
| **L1 核心卖点** | ✅ 必选 | Step 3 选出的核心卖点，作为视觉最大文字 | `"Display 'All-Day Comfort' as the headline label"` |
| **L2 功能亮点** | ⬚ 可选 | 1–2 条补充卖点，字号次于 L1 | `"with sub-labels '40dB ANC' and '30H Battery'"` |
| **L3 可信证明** | ⬚ 可选 | 认证或数据徽章，置于角落或底部 | `"with a small badge 'FDA-grade silicone'"` |
| **排版指引** | ✅ 必选 | 文案与商品的空间关系、视觉布局，体现 L1/L2/L3 主次 | "headline on top, sub-labels below, badge at bottom-right" |

**Prompt 构建公式**：

```
[商品主体描述], [细节部位聚焦（可选）], [L1 文案 + L2 文案（可选）+ L3 文案（可选）], [Step 4 构图模板的排版关键词]. [风格/背景/配色等附加描述（可选）].
```

**构建示例**：

示例 1 — 仅 L1 + 构图① 单卖点强调（动态线条 + 局部放大）：

```
Wireless noise-canceling headphones as the main subject. Display "Silent Commute" as a single bold headline beside the product on the right, large typography, generous whitespace. Add curved dynamic light arcs flowing around the ear cups to emphasize the silence effect, plus a small circular zoom-in showing the ear cushion detail. One-focal-point composition. Minimalist light gray background, modern tech style.
```

示例 2 — L1 + L2 + 构图② 多卖点罗列（圆形特写 + 文字标注，用户已提供卖点："卖点是40dB降噪和30小时续航"）：

```
Wireless noise-canceling headphones centered as the main subject. Surround the product with four circular close-up callouts in a 2x2 grid: ear cushion close-up paired with "Memory Foam", driver close-up paired with "40dB ANC", battery icon close-up paired with "30H Battery", Bluetooth chip close-up paired with "BT 5.3". Each circular thumbnail with even spacing and short text label below. Headline "All-Day Comfort" on top. Minimalist light gray background, modern tech style.
```

示例 3 — L1 + L2 + L3 + 构图③ 参数规格图（双向箭头 + 引线 + 数字）：

```
A stainless steel vacuum flask as the main subject in technical visualization style. Add double-headed arrows with thin leader lines indicating dimensions: "500ml" labeled along a vertical double-arrow next to the body, "24h" labeled beside a thermometer icon, "316 Stainless Steel" labeled near the wall cross-section. Numeric values are placed alongside the leader lines and never overlap the product. Headline "24h Cold & Hot" on the left, small badge "FDA-Approved" at the bottom-right. Infographic style. Simple white background.
```

示例 4 — 用户未提供卖点 + 构图④ 使用图（细引线 + 短文字，Agent 按五维度推断 L1+L2+L3，需 ask_user 确认）：

> **Agent 第一步通过 `ask_user` 弹出确认窗口**（卖点放题目，选项仅两项）：
> 
> 题目（markdown 格式）：
> 
> > 我根据商品特征为您推断了以下卖点方案，请确认或调整：
> > 
> > **核心卖点**：Travel-Ready Hydration
> > 
> > **功能亮点**：Double-Wall Insulation、Leak-Proof Lid
> > 
> > **可信证明**：BPA-Free
> > 
> > 构图模板：「使用图（场景+标注）」
> 
> 选项：
> - 确认生图
> - 修改卖点
> 
> **若用户点击「修改卖点」**，Agent 第二步通过 `ask_user` 弹出编辑窗口（题目中保留 markdown 排版的方案，输入框同步预填纯文本）：
> 
> 题目（markdown 格式）：
> 
> > 请在以下卖点方案基础上修改：
> > 
> > **核心卖点**：Travel-Ready Hydration
> > 
> > **功能亮点**：Double-Wall Insulation、Leak-Proof Lid
> > 
> > **可信证明**：BPA-Free
> 
> 输入框预填：
> ```
> 核心卖点：Travel-Ready Hydration
> 功能亮点：Double-Wall Insulation、Leak-Proof Lid
> 可信证明：BPA-Free
> ```

用户确认后，Agent 构建 prompt：

```
A stainless steel vacuum flask placed on a hiking backpack in an outdoor mountain scene. Use thin leader lines connecting short text labels (≤6 words) to specific parts of the flask: "Double-Wall Insulation" pointing to the body, "Leak-Proof Lid" pointing to the cap. Headline "Travel-Ready Hydration" displayed in the upper-left, small badge "BPA-Free" at the bottom-right. Leader lines never cross the main product silhouette. Lifestyle context, natural daylight.
```
> Agent 回复时应说明："已根据商品特征构建三层卖点：核心卖点『Travel-Ready Hydration』、功能亮点『Double-Wall Insulation / Leak-Proof Lid』、可信证明『BPA-Free』，构图采用「使用图（场景+标注）」，如需调整请告知。"

示例 5 — 构图⑤ 对比竞品图（每行 ✓/✗ + 灰色方块代替竞品，无品牌/商标）：

```
Split-screen comparison layout. Left side labeled "Others" showing an abstract gray silhouette / generic gray block as the competitor placeholder — NO brand names, NO logos, NO trademarks, NO recognizable packaging — with three rows each prefixed by a red ✗: "✗ Leaks easily", "✗ Loses heat in 6h", "✗ Plastic odor". Right side labeled "Ours" highlighting our stainless steel vacuum flask with three rows each prefixed by a green ✓: "✓ Leak-Proof", "✓ 24h Cold & Hot", "✓ BPA-Free". ✓/✗ aligned row by row with the text, equal number of items on both sides, comparison focused only on key functional points. Bold "VS" divider in the middle. Clean white background, professional e-commerce style.
```

### 固定拼接文案

```
Create a selling-point product image that clearly highlights the product's key advantages. The product subject must be prominently displayed as the visual focus and must remain fully consistent with the original image in shape, color, texture, material details, and structural features — do NOT alter, simplify, or reimagine any aspect of the product's appearance. For any parts that are occluded, blocked, or hidden in the original image (covered by hands, packaging, other objects, or the product itself), do NOT infer, reconstruct, or fabricate the hidden content — only highlight selling points based on the visible portions actually shown in the original image. Selling-point text labels must be short (max 6 words each), legible, and well-positioned without overlapping the product. Maintain a clean, professional e-commerce layout with balanced whitespace. Do NOT add any text or elements not specified in the prompt.
```

### 完整 prompt 结构

```
{用户/Agent 的卖点描述 prompt} + Create a selling-point product image that clearly highlights the product's key advantages. The product subject must be prominently displayed as the visual focus and must remain fully consistent with the original image in shape, color, texture, material details, and structural features — do NOT alter, simplify, or reimagine any aspect of the product's appearance. For any parts that are occluded, blocked, or hidden in the original image (covered by hands, packaging, other objects, or the product itself), do NOT infer, reconstruct, or fabricate the hidden content — only highlight selling points based on the visible portions actually shown in the original image. Selling-point text labels must be short (max 6 words each), legible, and well-positioned without overlapping the product. Maintain a clean, professional e-commerce layout with balanced whitespace. Do NOT add any text or elements not specified in the prompt.
```

## 工具调用

- 工具：`image_edit`（用户上传了商品图时）/ `image_generate`（纯文字描述时）
- task_type：`simple_generation`（单卖点、简单排版） / `complex_generation`（多卖点、复杂排版或含细节局部放大）

### 选择标准

| 条件 | task_type |
|------|-----------|
| 仅 L1，或 L1 + L2（典型场景）；构图采用 ① 单卖点强调 / ② 多卖点罗列 | `simple_generation` |
| L1 + L2 + L3（含认证/数据徽章）；或构图采用 ③ 参数规格图 / ④ 使用图 / ⑤ 对比竞品图（含引线/分栏/场景）；或需要细节局部放大 callout | `complex_generation` |

## 注意事项

- **商品主体必须突出**：商品是画面的视觉核心，文案不能喧宾夺主
- **卖点必须落入五维度**：利益/体验、可量化优势、场景化能力、资质/认证、痛点解决；主观形容词、品类常识、营销套话不得作为卖点
- **L1/L2/L3 层级清晰**：视觉上主次分明，L1 字号最大，L3 通常以小徽章形式置于角落
- **构图模板单选**：从 5 种构图模板中选择**最匹配**的一种，不得混用多种构图骨架
- **视觉锚点必备**：每种构图模板的视觉锚点必须出现在 prompt 中——① 动态线条/局部放大；② 圆形特写+文字；③ 双向箭头+引线+数字（必备）；④ 细引线+短文字；⑤ 每行 ✓/✗ 标记。缺失锚点会导致构图骨架失效
- **⚠️ 竞品对比合规约束**：构图⑤ 对比竞品图严禁体现任何竞品的品牌名、商标、Logo、可识别的包装文字或外观特征；左侧竞品必须用**灰色方块 / 轮廓剪影 / 抽象灰色物体**代替，仅对比关键功能点（如"Leaks easily"、"Loses heat"），避免商标侵权与法律风险
- **⚠️ 遮挡部位禁止推测**：对于原图中被手部、包装、其他物体或商品自身遮挡/隐藏的部位，**严禁推测、还原或想象**被遮挡的内容；只能基于原图**实际可见的部位**生成卖点文案、引线标注或圆形特写。如用户希望对被遮挡部位（如背面 Logo、内部结构）做卖点，应主动告知该区域不可见，并建议用户提供更清晰的角度图或换为基于可见部位的卖点。
- **每条文案务必简短**：L1 ≤4 词，L2/L3 ≤6 个英文词（中文不超过 8 个字）
- **排版清晰专业**：文案位置不遮挡商品主体，保持足够留白，整体布局平衡
- **用户卖点优先**：用户已提供具体卖点时，直接进入候选池作为 L1 核心卖点 / L2 功能亮点 基础，仅做适配改写，无需确认直接执行；Agent 推断/补充卖点时，**必须通过 `ask_user` 工具向用户确认后才能生图**——用户可选择确认（直接生图）或修改（预填文案供用户编辑，提交后按「用户已提供」逻辑执行）
- **遵循平台套图强制规则**：当在平台套图工作流中被调用时，若用户上传了商品图片，必须使用 `image_edit`
