# 导航抽屉 · Navigation drawer

适合维护已有基线 M3 产品。新 Expressive 产品优先选 expanded navigation rail；已有抽屉的路由、分组和历史可以沿用。

## 组件契约

`NavigationDrawer(groups, currentId, open, modality, onSelect)`。标准抽屉与正文并排，模态抽屉覆盖正文并带 scrim；常用目的地居前，分组可用标题和分隔线。

宽窗可常驻；窄窗由菜单按钮开启。选择后更新路由，模态抽屉同时关闭；用返回键关闭抽屉时保留当前页面。

## 动效与输入

从逻辑起始边滑入，遮罩单独处理透明度。减少动效可直接呈现面板；顶级页面切换仍依据实际路由。

只有模态形式将背景置为不可交互，并把焦点局限在抽屉、关闭后送回入口。常驻导航使用可识别的区域名，便于跳到主内容。

## 取用示例

`NavigationDrawer(groups=[工作区,归档], currentId=route.id, open=menuOpen, modality=modal, onSelect=openSection)`。

[本地规格令牌](../assets/tokens/navigation-drawer.json) · [官网概览](https://m3.material.io/components/navigation-drawer/overview) · [规格](https://m3.material.io/components/navigation-drawer/specs) · [指南](https://m3.material.io/components/navigation-drawer/guidelines) · [无障碍](https://m3.material.io/components/navigation-drawer/accessibility)
