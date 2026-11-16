# 卡片 · Cards

聚合描述同一对象的标题、媒体、摘要和动作。Filled 靠表面色分组，outlined 用边界，elevated 在复杂背景上用层级区分；连续均质资料常用列表更易扫读。

## 组件契约

`Card(content, variant, primaryAction?, secondaryActions?)`。整卡进入详情时提供一个主操作；独立按钮保留各自命中区。内容随本地化和系统字号增长，集合可用列表、网格或轮播。

若卡片仅展示数据，保留静态语义。可点击区域和独立操作分开布置，例如标题进入详情、尾部按钮收藏。卡片的强调程度与内容层级相符。

## 动效与输入

单张展开可用 container transform，共享卡片或主图的身份；若详情显示在另一窗格，只更新详情区。减少动效时保留所选卡片标记。

Web 用 article/标题链接配相邻按钮，避免在链接或按钮内部再嵌按钮；桌面点击和 Enter 进入同一详情。触屏保留各动作的目标间距。

## 取用示例

`Card(variant=outlined, content=projectSummary, primaryAction=openProject, secondaryActions=[pinProject])`。

[本地规格令牌](../assets/tokens/cards.json) · [官网概览](https://m3.material.io/components/cards/overview) · [规格](https://m3.material.io/components/cards/specs) · [指南](https://m3.material.io/components/cards/guidelines) · [无障碍](https://m3.material.io/components/cards/accessibility)
