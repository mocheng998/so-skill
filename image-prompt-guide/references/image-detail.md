# 细节图 (Image Detail)

## 场景说明

基于商品原图对商品主体的**重点区域进行裁切放大展示**，让用户清晰看到产品局部细节（如材质纹理、工艺细节、功能结构、接缝、Logo 等）。核心原则是**严格保持商品主体一致性**，仅对原图中已有的部分进行裁切放大或聚焦呈现，绝不生成原图中不存在的内容。

> **与卖点图的区别**：细节图是纯粹的「局部放大」，不添加文案、不做排版设计、不添加任何原图中不存在的视觉元素。如需突出商品卖点并配合文案排版，请使用 **卖点图**（`references/selling-point.md`）。

## 应用方式：拼接

在用户或 Agent 根据需求生成的细节描述 prompt **后面**拼接以下固定文案。

## Prompt 模板

### 用户/Agent 生成部分

由用户描述需要放大展示的细节区域，例如："Zoom in on the zipper and stitching details" 或 "放大展示鞋底的纹理和缓震结构"

### 固定拼接文案

```
A detail image is purely a local zoom-in based on the original product image — nothing more. Only crop and enlarge the existing detail area from the original image. Do NOT add any text, captions, typography, or layout design. Do NOT generate, add, or fabricate any visual elements that do not exist in the original image.
```

### 完整 prompt 结构

```
{用户/Agent 的细节描述 prompt} + A detail image is purely a local zoom-in based on the original product image — nothing more. Only crop and enlarge the existing detail area from the original image. Do NOT add any text, captions, typography, or layout design. Do NOT generate, add, or fabricate any visual elements that do not exist in the original image.
```

## 工具调用

- 工具：`image_edit`
- task_type：`simple_generation`

## 注意事项

- **商品主体一致性是核心要求**：生成的细节图必须与原图中的商品主体完全一致，不允许出现形变、颜色偏差或结构改变
- **严禁凭空生成内容**：只能对原图中已存在的细节进行放大展示，不得添加原图中没有的纹理、结构、标签、文字或任何视觉元素
- **⚠️ 遮挡部位禁止推测**：对于原图中被手部、包装、其他物体或商品自身遮挡/隐藏的部位，**严禁推测、还原或想象**被遮挡的内容，仅对原图中**实际可见的区域**进行裁切放大。如用户要求放大被遮挡区域，应主动告知用户原图该区域不可见，建议提供更清晰的角度或重新拍摄。
- **不做排版和文案**：细节图只负责局部放大，不叠加卖点文案、不进行排版设计
- 用户/Agent 负责指定需要放大的细节区域（如拉链、缝线、材质表面、Logo、功能部件等）
- 固定文案用于约束输出严格基于原图，防止 AI 幻觉生成不存在的内容
