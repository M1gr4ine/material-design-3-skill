# 导航轨 · Navigation rail

中等及更宽窗口在起始侧使用导航轨。折叠轨常容纳 3–7 个主要目的地和可选 FAB。展开轨可显示分组、标签和更多目的地；Expressive 用它承接旧抽屉。

## 组件契约

`NavigationRail(destinations, currentId, expanded, modality, onNavigate)`。collapsed / expanded 是展示状态，路由是独立状态。展开可用 standard 与正文并排，或 modal 覆盖正文。

常驻轨保留位置；菜单按钮切换宽度。可用宽度不足以并排时，从菜单打开模态展开轨，选择后回到内容。跨断点保留路由和列表滚动位置。

## 动效与输入

活动指示胶囊（折叠态垂直项 `56×32 dp`，`secondary-container`，精确半高 `16px` 圆角）切换时按与导航栏一致的水平中心展开过渡：入场 `scaleX(0.35) → 1` 用 fast spatial、`opacity` 用 fast effects，离场双通道均用 fast effects 干脆收起，指示层与状态层分层实现（示范代码见 [动效](motion.md)）。展开宽度与内容用 default spatial / effects 协调，关闭可从中途反向；顶级目的地切换采用 top-level，减少动态效果时直接更换轨宽和选中指示。

非模态轨允许在导航和正文间跳转；模态展开要管理焦点和返回。桌面可通过键盘直接选择链接，触屏的图标项仍带明确名称。

## 取用示例

`NavigationRail(destinations=sections, currentId=route.section, expanded=showLabels, modality=roomForBoth ? standard : modal, onNavigate=go)`。

[本地规格令牌](../assets/tokens/navigation-rail.json) · [官网概览](https://m3.material.io/components/navigation-rail/overview) · [规格](https://m3.material.io/components/navigation-rail/specs) · [指南](https://m3.material.io/components/navigation-rail/guidelines) · [无障碍](https://m3.material.io/components/navigation-rail/accessibility)
