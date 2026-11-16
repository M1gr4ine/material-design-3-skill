# 徽标 · Badges

在已有图标旁标出新内容、计数或状态。Small 是圆点，large 显示短数字或标签；可见计数连同加号最多四个字符。

## 组件契约

`Badge(anchor, countOrStatus, variant)`。锚在图标包围盒的上方尾侧。数字过大时显示如 999+；实际数值与业务对象关联。

更新徽标时保留宿主的点击区域。已读计数归零时按产品含义隐藏；徽标本身通常不单独接收点击。

## 动效与输入

更新数字或显隐可用快速 effects。频繁变化的计数直接更新，读屏聚焦宿主时能得到最新值。

宿主名称或描述合并状态，例如「收件箱，12 条未读」，避免重复朗读装饰点；RTL 镜像徽标的锚点。

## 取用示例

`Badge(anchor=inboxLink, countOrStatus=unreadCount, variant=unreadCount > 0 ? large : hidden)`。

[本地规格令牌](../assets/tokens/badges.json) · [官网概览](https://m3.material.io/components/badges/overview) · [规格](https://m3.material.io/components/badges/specs) · [指南](https://m3.material.io/components/badges/guidelines) · [无障碍](https://m3.material.io/components/badges/accessibility)
