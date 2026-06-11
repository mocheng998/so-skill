# 水印消除 (Remove Watermark)

## 场景说明

去除图片中的水印、网站信息、联系方式、二维码等非商品内容，同时保留商品本身可见的文字信息。

## 应用方式：直接应用

Agent 需先观察图片左上角是否有品牌商标，据此选择对应的 prompt 变体。若无法确定，默认使用变体 A（更安全，不会误保留水印）。

## Prompt 模板

### 变体 A：左上角无商标

```
Remove the watermark, website information, contact details, or QR code from the image. Preserve product-related text that is visibly present in the ORIGINAL image.
```

### 变体 B：左上角有商标

```
Remove the watermark, website information, contact details, or QR code from the image. Preserve product-related text and the top-left brand logo that is visibly present in the ORIGINAL image.
```

## 工具调用

- 工具：`image_edit`
- task_type：`watermark_removal`

## 注意事项

- Agent 通过视觉观察判断图片左上角是否存在品牌商标；若无法确定，默认使用变体 A
- 商品相关文字（如产品名称、规格等）必须保留
- 仅移除水印、网址、联系方式、二维码等非商品信息
