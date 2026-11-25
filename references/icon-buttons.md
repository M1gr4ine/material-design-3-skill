# 图标按钮 · Icon buttons

用于可通过熟悉符号识别的短动作。收藏、静音这类二态操作用 toggle；「打印」每次执行一次。图标含义需要解释时，优先加可见文字。

## 组件契约

`IconButton(icon, accessibleName, onActivate)`；切换型再绑定 `selected`。可选 standard、filled、tonal、outlined，五种尺寸、窄/标准/宽容器与圆/方形状按空间选。

选择态可用线框/实心图标加容器变化。无论视觉大小，命中包含整个按钮；触屏的 XS/S 也预留至少 48×48 dp 的目标。Web 若用 `position: absolute` 的 `::before`/`::after` 在 `48×48` 命中区内绘制较小可见背景框、选中容器或状态层，宿主按钮须设 `isolation: isolate` 且背景伪元素设 `z-index: -1`，避免定位伪元素按 CSS 层叠顺序盖住直接字符/图标（不透明容器色会直接遮没文字，半透明底也会拉低对比度）；轻量描边选中态可用 `color`/`border-color: var(--md-sys-color-primary)` 配 `z-index: -1` 的 `background: color-mix(in srgb, var(--md-sys-color-primary) 16%, transparent)` 兼顾高对比度与可读性。

## 动效与输入

图标与容器用状态层反馈按压；可变轮廓用 fast spatial，颜色用 fast effects。图形更新后保持原焦点。Web CSS 做圆/方形变时，满圆态须用按钮实际短边一半的精确 `px`（如 `calc(var(--btn-size) / 2)`）而非 `9999px`（避免过冲闪成直角），并勿在 `:active` 中覆写 `transition` 简写。

键盘聚焦可见；Web/桌面为图标提供操作名和可聚焦时读取的提示，窄触屏保留读屏名称。切换名保持稳定，让读屏单独宣布按下状态。

## 取用示例

`IconButton(icon=bookmark, accessibleName="收藏", selected=item.saved, onSelectedChange=setSaved)`。

[本地规格令牌](../assets/tokens/icon-buttons.json) · [官网概览](https://m3.material.io/components/icon-buttons/overview) · [规格](https://m3.material.io/components/icon-buttons/specs) · [指南](https://m3.material.io/components/icon-buttons/guidelines) · [无障碍](https://m3.material.io/components/icon-buttons/accessibility)
