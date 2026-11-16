# 应用栏 · App bars / Top app bar

说明当前页面的位置和标题，容纳返回或导航入口及 1–2 个重要动作。需要大量编辑命令时把它们放进工具栏。

## 组件契约

`AppBar(title, navigationAction?, actions, variant, subtitle?)`。四种当前变体为 search app bar、small、medium flexible、large flexible。Flexible 可容纳副标题、多行或自定义内容；旧 medium/large 对应 flexible，中心对齐属于可选配置。

用返回箭头退出子层级，用菜单打开导航，全局搜索才占用 search app bar。根据可读宽度把低频动作移入菜单；滚动后可切换容器色以区分内容。

## 动效与输入

根据页面选择固定或随滚动折叠/重新出现；与内容滚动共用同一进度。减少动效时保持可读标题及返回入口。

网页把标题放入标题层级，文档工具窗口保留系统标题栏与窗口按钮。紧凑界面尊重系统状态栏安全区；图标按钮均有动作名称。

## 取用示例

`AppBar(title="收件箱", variant=small, navigationAction=openFolders, actions=[search,more])`。

[本地规格令牌](../assets/tokens/app-bars.json) · [官网概览](https://m3.material.io/components/app-bars/overview) · [规格](https://m3.material.io/components/app-bars/specs) · [指南](https://m3.material.io/components/app-bars/guidelines) · [无障碍](https://m3.material.io/components/app-bars/accessibility)
