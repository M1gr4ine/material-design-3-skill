# 分段按钮 · Segmented buttons

用于已有基线 M3 产品，提供 2–5 个简短的单选或多选选项。Expressive 新设计用 connected button group，迁移时沿用原选择模型。

## 组件契约

`SegmentedButtons(items, selectionMode, selectedIds, onChange)`。一条外边框包住相邻分段，每段有文字、图标或两者。单选与多选对外分别暴露一个值或集合。

点击切换选项，选中项有指示和容器层级。以单选日历视图为例，点已选项保持该视图；多选筛选的各项可以独立取消。

## 动效与输入

用快速着色或选中图标过渡，选中结果立即可见。保留外轮廓与焦点位置，减少动效时显示最终选中标记。

键盘单选用 radio-group 语义，多选用 toggle/checkbox 语义。标签长度使内容换行时可改用筛选 chips 或完整选择列表。

## 取用示例

`SegmentedButtons(items=[天,周,月], selectionMode=single, selectedIds=view, onChange=setView)`。

[本地规格令牌](../assets/tokens/segmented-buttons.json) · [官网概览](https://m3.material.io/components/segmented-buttons/overview) · [规格](https://m3.material.io/components/segmented-buttons/specs) · [指南](https://m3.material.io/components/segmented-buttons/guidelines) · [无障碍](https://m3.material.io/components/segmented-buttons/accessibility)
