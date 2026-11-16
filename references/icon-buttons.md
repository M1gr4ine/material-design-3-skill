# 图标按钮 · Icon buttons

用于可通过熟悉符号识别的短动作。收藏、静音这类二态操作用 toggle；「打印」每次执行一次。图标含义需要解释时，优先加可见文字。

## 组件契约

`IconButton(icon, accessibleName, onActivate)`；切换型再绑定 `selected`。可选 standard、filled、tonal、outlined，五种尺寸、窄/标准/宽容器与圆/方形状按空间选。

选择态可用线框/实心图标加容器变化。无论视觉大小，命中包含整个按钮；触屏的 XS/S 也预留至少 48×48 dp 的目标。

## 动效与输入

图标与容器用状态层反馈按压；可变轮廓用 fast spatial，颜色用 fast effects。图形更新后保持原焦点。

键盘聚焦可见；Web/桌面为图标提供操作名和可聚焦时读取的提示，窄触屏保留读屏名称。切换名保持稳定，让读屏单独宣布按下状态。

## 取用示例

`IconButton(icon=bookmark, accessibleName="收藏", selected=item.saved, onSelectedChange=setSaved)`。

[本地规格令牌](../assets/tokens/icon-buttons.json) · [官网概览](https://m3.material.io/components/icon-buttons/overview) · [规格](https://m3.material.io/components/icon-buttons/specs) · [指南](https://m3.material.io/components/icon-buttons/guidelines) · [无障碍](https://m3.material.io/components/icon-buttons/accessibility)
