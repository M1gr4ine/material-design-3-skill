# 导航栏 · Navigation bar

在紧凑或部分中等窗口提供 3–5 个同级、跨页面稳定的主要目的地。给「新建」这种命令单独的操作入口。

## 组件契约

`NavigationBar(destinations, currentId, onNavigate)`，每项包含 ID、图标、短标签，可带 badge。Expressive 的 flexible 版本支持垂直和水平图文排列；旧 baseline 版本保留供已有界面使用。

选中项与实际路由同步，返回或深链接也更新活动指示。变宽后可切换为 rail，继续使用同一组目的地、地址和当前项。

## 动效与输入

指示形状跟随选中项；不同顶级目的地用 top-level 淡出再淡入。减少动效用静态指示标出当前页。

Web 使用命名的 nav 和链接，并以 `aria-current="page"` 标出当前位置，可复制地址、后退或新开标签页。触屏在系统安全区上方留出目标区域。

## 取用示例

`NavigationBar(destinations=[首页,项目,我的], currentId=route.section, onNavigate=goToSection)`。

[本地规格令牌](../assets/tokens/navigation-bar.json) · [官网概览](https://m3.material.io/components/navigation-bar/overview) · [规格](https://m3.material.io/components/navigation-bar/specs) · [指南](https://m3.material.io/components/navigation-bar/guidelines) · [无障碍](https://m3.material.io/components/navigation-bar/accessibility)
