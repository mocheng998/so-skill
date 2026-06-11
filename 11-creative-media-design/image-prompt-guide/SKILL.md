---
name: image-generation-guide
description: |
  Technical reference for crafting effective prompts when generating or editing images (single or batch).
  **When to Use** (AFTER deciding to generate/edit an image):
    - Simple image generation: "Generate a cute red labubu", "Create an image of...", "Draw a..."
    - Single creative requests: "Make me a logo", "Design a poster", "Generate product mockup"
    - Image editing: "Edit this image to...", "Change the background", "Add text to image"
    - **E-commerce platform product images**: "帮我做 Amazon 主图", "生成一套 Shopify 商品图", "做一组 listing images" (single or multi-image sets)
    - **Specialized image editing scenes**: White background (白底图), watermark removal (去水印), HD upscale (变清晰/提高分辨率), model showcase (模特图), scene image (场景图/换背景), SKU color change (商品换色), image translation (翻译图片文字), image detail (细节图/局部放大), selling point image (卖点图), logo customization (Logo合成到商品)
    - **Advertising creatives**: Logos, branding materials, posters, banners (even for business use)
    - **Categories NOT covered by new-product-development-design**: Food & beverages, books & media, virtual goods/services, industrial equipment/parts
  **DO NOT use for full product development** (in supported categories):
    - "Design a product line for Gen-Z market" → Use new-product-development-design first (if category is apparel, home, beauty, electronics, etc.)
    - "Develop 3 product proposals with cost analysis" → Use new-product-development-design instead
    - Requests involving market research, multi-proposal comparison, or supplier matching
  **Key differentiator**: This skill is for IMAGE GENERATION/EDITING technique, not business product strategy.
enabled: true
---

# Image Generation Guide

An all-in-one AI image creation toolkit covering everything from generating from scratch to fine-grained editing. Supports creative generation, image editing, and e-commerce platform image set creation.

---

## Part 1: Prompt Guide

### Golden Rules

| Rule | Description |
|------|-------------|
| **Edit, Don't Re-roll** | If 80% correct, modify conversationally instead of regenerating |
| **Natural Language** | Use complete sentences, not keyword stacking |
| **Be Specific** | Define subject, environment, lighting, mood explicitly |
| **Provide Context** | Include "why" or "for whom" to guide artistic decisions |
| **Structured Elements** | Treat prompts as design briefs with clear components |
| **Avoid Brand Infringement** | Unless explicitly requested by user, avoid including recognizable brand logos, brand names, or trademarked elements to prevent copyright/trademark issues |

### Prompt Structure Formula (for image generation)

```
[Shot type] of [Subject] in [Setting], [Action/State]. 
[Style], [Composition], [Lighting], [Color], [Quality].
```

### Required Elements

| Element | Description | Examples |
|---------|-------------|----------|
| **Subject** | What to draw (be specific) | "ginger tabby cat", "ergonomic wireless headphones" |
| **Setting** | Where is the subject | "windowsill bathed in afternoon sunlight" |
| **Style** | Overall feeling | "cinematic", "watercolor", "minimalist" |
| **Composition** | Camera placement | "close-up", "wide-angle", "rule-of-thirds" |
| **Lighting** | Light source and mood | "golden hour", "soft diffused", "Rembrandt lighting" |
| **Color** | Color palette | "Morandi palette", "high saturation", "monochromatic" |
| **Quality** | Detail level | "8K", "hyperrealistic", "masterpiece" |

### For Image Generation (No Reference)

Construct comprehensive prompts covering:
- **Core Elements**: Subject or product features
- **Design Philosophy**: Minimalist, luxurious, eco-friendly, futuristic
- **Setting**: Studio lighting, natural environment, lifestyle context
- **Artistic Style**: Modern, vintage, industrial, organic
- **Visual Effects**: Textures, lighting, materials, color schemes
- **Text**: Use quotes for exact text: `"Display 'LIMITED EDITION' in bold serif"`
- **Resolution**: Request 2K/4K for texture-heavy or print materials

**Note on Brand Safety**: When constructing prompts, avoid including recognizable brand logos, brand names, or trademarked visual elements unless the user explicitly requests them.

### For Image Editing (With Reference)

#### General Editing

Use **semantic instructions**—describe changes naturally:

| Action Type | Examples |
|-------------|----------|
| **Core** | Add, Change, Remove, Replace, Make |
| **Creative** | Restore, Colorize, Illustrate as, Retexture |
| **Compositional** | Combine, Isolate, Zoom out, Blur, Overlay |
| **Dimensional** | Convert 2D to 3D, Convert sketch to render |

#### Scene Router (Priority-Based)

When the user's request matches a specialized scenario, follow the **priority order** below. Higher-priority matches take precedence — do NOT fall through to lower-priority routes.

**Priority 1 — Platform Product Image (Composite Scenario)**

| Trigger Condition | Reference | Action |
|-------------------|-----------|--------|
| User mentions a specific e-commerce platform (Amazon, eBay, Walmart, Shopify, Etsy, AliExpress, TikTok Shop, Shopee, Lazada, Alibaba.com, 1688) AND requests main image / image set / listing images | `references/platform-product-guidelines.md` | Load platform specs first, then decompose into sub-tasks and route each sub-task to the appropriate scene below |

> **Key**: Platform Product Image is a composite workflow — it consults platform requirements first, then delegates to White Background, Scene Image, Model Showcase, etc. as sub-tasks. If the user explicitly mentions a platform, this takes priority over all individual scenes below.

**Priority 2 — Single-Purpose Scenes (Exact Match)**

These scenes use dedicated tool task_types that cannot be combined with other edits:

| Scenario | Trigger Keywords | Reference | Apply Method | task_type |
|----------|-----------------|-----------|--------------|-----------|
| **White Background** | 白底图、纯白背景、white background、换白底 | `references/white-background.md` | Direct Apply | `white_background` |
| **Watermark Removal** | 去水印、消除水印、remove watermark、去除水印 | `references/remove-watermark.md` | Direct Apply (2 variants) | `watermark_removal` |
| **HD Upscale** | 高清、超清、清晰度增强、upscale、enhance resolution、变清晰 | N/A | Tool-Only (no prompt needed) | `hd_upscale` |

**Priority 3 — Specialized Editing Scenes (Prompt-Driven)**

| Scenario | Trigger Keywords | Reference | Apply Method | task_type |
|----------|-----------------|-----------|--------------|-----------|
| **Scene Image** | 场景图、换场景背景、lifestyle shot、放到...场景 | `references/scene-image.md` | Concatenate | `simple_generation` or `complex_generation` |
| **SKU Color Change** | 商品换色、SKU换色、产品改颜色、recolor product | `references/sku-color-change.md` | Concatenate | `simple_generation` or `complex_generation` |
| **Logo Customization** | Logo定制、logo合成、print logo on product | `references/logo-customization.md` | Concatenate | `simple_generation` |
| **Model Showcase** | 模特图、模特展示、model photo | `references/model-showcase.md` | Direct Apply (3 variants) | `simple_generation` |
| **Image Detail** | 细节图、局部放大、detail shot、zoom in detail | `references/image-detail.md` | Concatenate | `simple_generation` |
| **Selling Point Image** | 卖点图、产品卖点、selling point image、卖点展示 | `references/selling-point.md` | Concatenate | `simple_generation` / `complex_generation`（用户上传原图，走 `image_edit`）<br>或 `simple` / `complex`（纯文字描述，走 `image_generate`） |
| **Image Translation** | 文字翻译、翻译图片文字、translate text in image | `references/image-translation.md` | Direct Apply (variable substitution) | `simple_generation` |

> **⚠️ Image Translation 强制规则**：匹配到图片翻译场景时，必须调用 `image_edit` 工具生成翻译后的图片。严禁仅以文本形式输出翻译结果，严禁跳过工具调用直接回复译文。

**Priority 4 — General Editing (Fallback)**

If no specialized scene matches, use semantic instructions with `simple_generation` or `complex_generation` based on complexity.

#### Disambiguation Rules

To resolve potential routing conflicts:

> **总则（Selling Point Image 优先原则）**：当用户请求**同时包含「卖点 / 文案 / 排版 / 标注 / 对比 / 卖点图」等营销表达**与其他场景关键词（如「细节」「场景」「模特」等）时，统一路由到 **Selling Point Image**。原因：只有卖点图场景能同时输出文案 + 排版 + 视觉锚点，其他场景均不输出文案。

| Ambiguous Request | Correct Route | Reasoning |
|-------------------|---------------|-----------|
| "把背景换成白色" / "白色背景" | **White Background** | Target is pure white (RGB 255,255,255), use dedicated `white_background` task_type |
| "把背景换成厨房场景" / "换个户外背景" | **Scene Image** | Target is a non-white scene environment |
| "change the background color to blue" | **Scene Image** | Background color change ≠ SKU body recolor |
| "把商品颜色改成蓝色" / "recolor the product" | **SKU Color Change** | Explicitly targeting product body color |
| "帮我做一张 Amazon 白底主图" | **Platform Product Image** → sub-task: White Background | Platform mentioned → Priority 1 takes over |
| "放大看一下拉链细节" / "zoom in on the stitching" | **Image Detail** | 局部放大，不需要文案和排版 |
| "做一张突出防水卖点的图" / "highlight the selling points" | **Selling Point Image** | 需要卖点文案 + 排版设计 |
| "做一张细节卖点图" / "放大某细节并标注卖点" | **Selling Point Image**（构图② 多卖点罗列 / 构图④ 使用图） | 既要放大又要文案/标注 → 走卖点图，借助构图模板的圆形特写或引线标注实现"放大+卖点"双重表达 |
| "做一张户外场景的卖点图" / "lifestyle 卖点图" | **Selling Point Image**（构图④ 使用图） | 含场景但核心是卖点文案与标注 → 走卖点图，scene 仅作为构图骨架；纯换背景无文案才走 Scene Image |
| "模特展示防水卖点" / "model 卖点图" | **Selling Point Image**（构图④ 使用图） | 含模特但核心是卖点文案 → 走卖点图，模特作为使用情境元素；纯模特展示无文案才走 Model Showcase |
| "图片变清晰" / "提高分辨率" | **HD Upscale** | Resolution/sharpness enhancement |

#### Apply Method Explanation

- **Direct Apply**: Use the reference prompt template as-is (or with variable substitution). Do NOT add or modify the prompt content.
- **Concatenate**: The user/Agent generates a descriptive prompt first, then appends the fixed text from the reference document to constrain the output quality.
- **Tool-Only**: No prompt required. Pass the image directly to the tool, which handles processing automatically.

#### HD Upscale (High Definition Enhancement)

When the user requests higher resolution or sharper image quality, directly use `image_edit` with `hd_upscale` task_type.

- **Tool**: `image_edit`
- **task_type**: `hd_upscale`
- **Prompt**: Not required (the tool automatically enhances resolution and sharpness)

#### Single-Purpose task_type Fallback Rule

The three single-purpose task_types (`white_background`, `hd_upscale`, `watermark_removal`) can ONLY perform their designated function. When the user expresses dissatisfaction or requests further edits after using these task_types:

1. **If the follow-up is a simple adjustment** (e.g., "再亮一点", "去掉那个角落的东西") → switch to `simple_generation`
2. **If the follow-up is a complex task** (e.g., "加个模特", "合成 Logo", "换个场景") → switch to `simple_generation` or route to the matching specialized scene
3. **判断标准**: single edit point + localized change = simple; multi-region + multi-step + high-fidelity requirement = complex

#### Simple vs Complex task_type Selection Criteria

For scenes that support both `simple_generation` and `complex_generation`, use this criteria:

| Criteria | `simple_generation` | `complex_generation` |
|----------|--------------------|--------------------|
| Edit scope | Single region, localized change | Multi-region or full-image transformation |
| Element count | ≤2 elements modified | ≥3 elements or major composition change |
| Fidelity requirement | Standard quality acceptable | High-fidelity, photorealistic required |
| Reference images | 0–1 reference image | ≥2 reference images (e.g., Logo + product) |
| Typical scenarios | Basic background swap, single-color recolor, simple crop/adjust, Logo customization, model showcase, image translation | Complex scene with multiple props, multi-region gradient recolor, full-image style transformation |

#### Platform Product Image Workflow

When the user requests generating product images for a specific e-commerce platform (main image, image set, listing images), follow this workflow:

1. **Identify target platform**: Determine which platform the user is targeting (Amazon, eBay, Walmart, Shopify, Etsy, AliExpress, TikTok Shop, Shopee, Lazada, Alibaba.com, 1688).
2. **Load platform guidelines**: Read `references/platform-product-guidelines.md` and extract the relevant platform's requirements:
   - White background requirement (mandatory or optional)
   - Recommended dimensions and aspect ratio
   - Product-to-frame ratio
   - Prohibited elements
   - Category-specific rules
3. **Decompose into sub-tasks**: Based on platform requirements, break down into executable sub-tasks:
   - Main image (white background required?) → route to White Background scene (`references/white-background.md`)
   - Additional angles (front, side, back) → route to `image_generate` or `image_edit`
   - Detail images (局部放大) → route to Image Detail scene (`references/image-detail.md`)
   - Selling-point images (卖点展示) → route to Selling Point Image scene (`references/selling-point.md`)
   - Lifestyle/scene images → route to Scene Image scene (`references/scene-image.md`)
   - Model images (if applicable) → route to Model Showcase scene (`references/model-showcase.md`)
   - SKU color variants (if applicable) → route to SKU Color Change scene (`references/sku-color-change.md`)
4. **Route sub-task to specialized scene first** (image editing scenes take priority):
   - For each sub-task, first check whether it matches a specialized editing scene in Priority 2–3 (White Background, Watermark Removal, HD Upscale, Scene Image, SKU Color Change, Logo Customization, Model Showcase, Image Detail, Selling Point Image, Image Translation).
   - If matched → use `image_edit` with the scene's designated task_type and prompt construction rules from its reference document.
   - If no specialized scene matches (e.g., additional angles, pure product shots) → fall through to step 5.
5. **Select tool for unmatched sub-tasks**:
   - **⚠️ 强制规则：当用户上传了商品图片时，所有子任务必须使用 `image_edit`**（使用 `simple_generation` 或 `complex_generation`），严禁使用 `image_generate`。
   - 仅当用户未提供任何图片（纯文字描述生成需求）时 → 使用 `image_generate` with `simple` or `complex` task_type
6. **Execute each sub-task**: Apply the corresponding scene's prompt construction rules and tool task_types.
   - **⚠️ 子任务交互约束（套图场景专属）**：在 Platform Product Image 套图生成流程中，**仅 Selling Point Image（卖点图）子任务**在 Agent 推断/补充卖点时需要通过 `ask_user` 工具向用户确认（参见 `references/selling-point.md` 中的「卖点确认交互（ask_user）」）。**其他所有子任务**（White Background、Image Detail、Scene Image、Model Showcase、SKU Color Change、Logo Customization、Image Translation、Additional Angles 等）**严禁触发 ask_user 交互**，直接按各自 reference 文档的规则执行生图，避免在套图流程中产生过多确认弹窗打断用户。
   - **卖点图确认时机**：卖点图子任务的 ask_user 确认需在该子任务实际执行前触发，确认/修改完成后再进入生图，不影响其他子任务的并行/顺序执行。
7. **Validate compliance**: Verify each output against platform's prohibited elements and dimension requirements.
8. **Official docs fallback**: Only consult the platform's official documentation (URLs listed in the guidelines) when the user has a special requirement NOT covered by the listed specifications.

### Anti-Patterns

| Avoid | Why | Better |
|-------|-----|--------|
| "beautiful design" | Too vague | Describe specific elements |
| "high quality" | Non-visual | Describe textures, materials, lighting |
| "professional look" | Subjective | Reference specific brands or contexts |
| "make it pop" | Meaningless | Specify contrast, saturation, or focal emphasis |
| Tag stacking | Model understands intent | Use natural sentences |
| Including brand logos/names without user request | Copyright/trademark risk | Use generic descriptions or style references |

### Advanced References

For detailed prompt enhancement:
- Design aesthetics enhancement → See `## Design Aesthetics` below
- Material & texture precision → See `## Materials` below
- Brand/style anchoring → See `## Brand References` below

---

## Part 2: Tool Invocation

### image_generate (Image Generation)

Use this tool when generating images from scratch (no reference image).

| task_type | Description | When to Use |
|-----------|-------------|-------------|
| `simple` | Single product or simple scene, lower cost | Simple objects, single subjects, basic backgrounds |
| `complex` | Sets, posters, models, 3D-style or high-detail scenes | Multi-element compositions, detailed posters, 3D renders, model photos |

Agent should judge task complexity and select the appropriate task_type.

### image_edit (Image Editing)

Use this tool when editing an existing image.

| task_type | Description | When to Use |
|-----------|-------------|-------------|
| `white_background` | Product on pure white background (single-purpose) | White background scene |
| `hd_upscale` | Resolution / sharpness enhancement (single-purpose) | User requests higher resolution or sharper image |
| `watermark_removal` | Remove watermarks, website/branding text, contact details, QR codes (single-purpose) | Watermark removal scene |
| `simple_generation` | Straightforward edits (default) | Simple scene edits, basic SKU color change |
| `complex_generation` | Heavy edits, multi-region, or high fidelity | Complex scene edits, complex SKU color change, multi-region transformations |

### Scene-to-Tool Routing Table

| Scenario | Tool | task_type | Priority |
|----------|------|-----------|----------|
| Platform product image (main/set) | `image_generate` / `image_edit` | Decompose into sub-tasks per platform specs | P1 |
| White background | `image_edit` | `white_background` | P2 |
| Watermark removal | `image_edit` | `watermark_removal` | P2 |
| HD upscale | `image_edit` | `hd_upscale` | P2 |
| Scene image (single region, simple bg) | `image_edit` | `simple_generation` | P3 |
| Scene image (multi-element, complex) | `image_edit` | `complex_generation` | P3 |
| SKU color change (single color change) | `image_edit` | `simple_generation` | P3 |
| SKU color change (multi-region/gradient) | `image_edit` | `complex_generation` | P3 |
| Logo customization | `image_edit` | `simple_generation` | P3 |
| Model showcase | `image_edit` | `simple_generation` | P3 |
| Image detail (zoom/crop) | `image_edit` | `simple_generation` | P3 |
| Selling point image (simple, with reference image) | `image_edit` | `simple_generation` | P3 |
| Selling point image (complex, with reference image) | `image_edit` | `complex_generation` | P3 |
| Selling point image (text-only, no reference image, simple) | `image_generate` | `simple` | P3 |
| Selling point image (text-only, no reference image, complex) | `image_generate` | `complex` | P3 |
| Image translation | `image_edit` | `simple_generation` | P3 |
| Free-form image generation (simple) | `image_generate` | `simple` | P4 |
| Free-form image generation (complex) | `image_generate` | `complex` | P4 |
| General editing (simple) | `image_edit` | `simple_generation` | P4 |
| General editing (complex) | `image_edit` | `complex_generation` | P4 |

### Aspect Ratio (aspect_ratio) 参数

生成或编辑图像时需确定输出图像的宽高比。

#### 支持的比例

```
1:1 | 2:3 | 3:2 | 3:4 | 4:3 | 4:5 | 5:4 | 9:16 | 16:9 | 21:9
```

#### 适用范围

| 场景 | 是否需要 aspect_ratio |
|------|----------------------|
| White Background (`white_background`) | ⚠️ 仅支持 1:1，若用户要求其他比例需告知不支持 |
| HD Upscale (`hd_upscale`) | ⚠️ 仅支持 1:1，若用户要求其他比例需告知不支持 |
| Watermark Removal (`watermark_removal`) | ⚠️ 仅支持 1:1，若用户要求其他比例需告知不支持 |
| 其他所有场景（Scene Image、SKU Color Change、Logo Customization、Model Showcase、Image Detail、Selling Point Image、Image Translation、Free-form Generation、General Editing、Platform Product Image 子任务等） | ✅ 需要判断 |

#### 判断规则

1. **用户明确指定了比例**（如"生成 16:9 的图"、"竖版 9:16"）→ 使用用户指定的比例
2. **用户指定的比例不在支持列表中**（如"5:3"、"2:1"）→ 告知用户当前支持的比例列表，请用户选择一个合适的比例
3. **用户在白底图/高清/去水印场景中要求非 1:1 比例** → 告知用户当前这三个能力仅支持 1:1 比例，不支持其他比例
4. **用户未指定比例** → 按以下分支处理：
   - **白底图 / 高清 / 去水印场景** → 默认使用 `1:1`
   - **其他所有场景**（Scene Image、SKU Color Change、Logo Customization、Model Showcase、Image Detail、Selling Point Image、Image Translation、Free-form Generation、General Editing、Platform Product Image 子任务等）：
     - **若用户上传了原图** → 先读取原图的宽高尺寸，计算其实际宽高比，从支持列表中选择**最接近**的候选比例作为默认输出比例（参见下方"原图比例匹配规则"）
     - **若用户未上传原图**（纯文字生成需求）→ 默认使用 `1:1`

#### 原图比例匹配规则

当需要根据上传原图自动选择默认 `aspect_ratio` 时，按以下步骤执行：

1. **获取原图尺寸**：读取原图的实际宽度（W）和高度（H），计算比值 `R = W / H`。
2. **计算候选比例与原图比值的差距**：将每个支持的比例（1:1、2:3、3:2、3:4、4:3、4:5、5:4、9:16、16:9、21:9）转换为浮点数 `R_candidate`，计算 `|log(R / R_candidate)|`（使用对数距离能更公平地处理横/竖向比例差异）。
3. **选择距离最小的候选比例**作为默认 `aspect_ratio`。
4. **平局处理**：若多个候选并列最接近，优先选择更"标准"的比例（优先级：`1:1` > `4:3` / `3:4` > `16:9` / `9:16` > `3:2` / `2:3` > `5:4` / `4:5` > `21:9`）。
5. **明显裁切风险提示**：若所选候选比例与原图比值差距过大（`|log(R / R_candidate)| > 0.1`，约对应 10% 以上偏差），可在生成前简短告知用户："已根据原图尺寸选择最接近的 X:Y 比例，可能产生轻微裁切，如需精确控制请指定比例。"

---

## Part 3: Output Examples

### Image Generation Output

After successfully generating an image, always append the following guidance message:

```
已根据您的要求生成图像，点击图像可以进入画布编辑。
```

### Image Editing Output

After successfully editing an image, always append the following guidance message:

```
已根据您的要求完成图像编辑，点击图像可以进入画布继续调整。
```

---

## Design Aesthetics

### Atmosphere & Mood Keywords
serene, contemplative, ethereal, intimate, bold, sophisticated, melancholic, uplifting, mysterious, tranquil, wistful, inviting, dramatic, peaceful, energetic, nostalgic, whimsical, elegant, cozy, minimalist

### Composition Principles

| Principle | Prompt Keywords |
|-----------|----------------|
| Negative Space | "generous negative space", "breathing room around subject" |
| Rule of Thirds | "subject positioned at rule-of-thirds intersection" |
| Visual Hierarchy | "clear visual hierarchy with X as focal point" |
| Leading Lines | "leading lines drawing eye toward subject" |

### Lighting Quality

| Basic | Professional |
|-------|-------------|
| "bright light" | "diffused golden hour light with soft rim lighting" |
| "dark background" | "deep shadows with subtle gradient falloff" |
| "natural light" | "north-facing window light, soft and directional" |

## Materials

| Generic | Precise |
|---------|---------|
| "metal finish" | "brushed titanium with subtle anodized reflections" |
| "glass bottle" | "frosted borosilicate glass with soft-touch matte coating" |
| "leather" | "vegetable-tanned full-grain leather with natural patina" |
| "wood" | "live-edge walnut with hand-rubbed oil finish" |

## Brand References

| Category | Reference Brands |
|----------|-----------------|
| Beauty/Skincare | SK-II, Aesop, La Mer |
| Tech/Electronics | Apple, Bang & Olufsen, Nothing Phone |
| Lifestyle | Kinfolk magazine, Cereal magazine, Monocle |
| Luxury/Fashion | Hermès, Bottega Veneta, Muji |

**Usage**: "Overall aesthetic inspired by [Brand] advertising style"

**Note**: When referencing brand styles, focus on describing aesthetic qualities (minimalist, luxurious, etc.) rather than including actual brand logos, brand names, or trademarked elements. Only include recognizable brand elements if the user explicitly requests them.