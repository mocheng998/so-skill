# 场景图 (Scene Image)

## 场景说明

保持商品主体不变，为其生成或替换一个新的场景背景，营造生活化、使用场景化的视觉效果。

## 应用方式：拼接

在用户或 Agent 根据需求生成的场景描述 prompt **后面**拼接以下固定文案。

## Prompt 模板

### 用户/Agent 生成部分

由用户描述期望的场景，例如："Place the product on a modern kitchen countertop with warm morning light"

### 固定拼接文案

```
Keep the main product in the image fully consistent with the original in shape, color, texture, material details, and structural features — do NOT alter, simplify, or reimagine any aspect of the product's appearance. For any parts that are occluded, blocked, or hidden in the original image (covered by hands, packaging, other objects, or the product itself), do NOT infer, reconstruct, or fabricate the hidden content — only render the visible portions actually shown in the original image. Only the surrounding scene/background may change as described.
```

### 完整 prompt 结构

```
{用户/Agent 的场景描述 prompt} + Keep the main product in the image fully consistent with the original in shape, color, texture, material details, and structural features — do NOT alter, simplify, or reimagine any aspect of the product's appearance. For any parts that are occluded, blocked, or hidden in the original image (covered by hands, packaging, other objects, or the product itself), do NOT infer, reconstruct, or fabricate the hidden content — only render the visible portions actually shown in the original image. Only the surrounding scene/background may change as described.
```

## 工具调用

- 工具：`image_edit`
- task_type：根据场景复杂度选择 `simple_generation` 或 `complex_generation`

## 注意事项

- **商品主体一致性是核心要求**：商品的形状、颜色、纹理、材质细节、结构特征及所有可见细节必须与原图完全一致，禁止形变、颜色偏差、材质改写或结构调整
- **⚠️ 遮挡部位禁止推测**：对于原图中被手部、包装、其他物体或商品自身遮挡/隐藏的部位，**严禁推测、还原或想象**被遮挡的内容；只能基于原图**实际可见的部位**进行场景合成。如用户希望在新场景中展示原图被遮挡的角度（如背面、内部），应主动告知该区域不可见，并建议用户提供更清晰的角度图
- **仅替换/补充背景与环境**：场景图只对商品周围的环境、光线、氛围进行替换或重塑，不得修改商品本体
- 用户/Agent 负责描述场景内容（如背景环境、光线、氛围等）
- 固定文案用于约束商品主体不被修改，并防止 AI 对遮挡部位的幻觉补全
