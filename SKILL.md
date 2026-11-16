---
name: material-design-3
description: 当 Web、原生桌面或手机 App 采用 Google Material Design 3、Material You 或 M3 Expressive，需要设计、实现或审查界面组件、布局、主题或动效时使用。
---

# Material Design 3

按用户要完成的动作选组件。设计稿从组件契约取变体与交互，代码把同一契约接到项目已有的控件、状态和主题。

## 按任务取组件

每个条目附交互说明、语言无关的调用示例和离线规格。

| 用户要做什么 | 取用条目 |
| --- | --- |
| 在当前页或全产品找内容、了解所处位置 | [搜索栏 Search](references/search.md) · [应用栏 App bars](references/app-bars.md) |
| 对当前文档执行常用或临时命令 | [工具栏 Toolbars／底部应用栏](references/toolbars.md) · [菜单 Menus／右键菜单](references/menus.md) |
| 提交、切换、在相关操作间选择 | [按钮 Buttons](references/buttons.md) · [图标按钮 Icon buttons](references/icon-buttons.md) · [按钮组 Button groups](references/button-groups.md) · [分裂按钮 Split button](references/split-button.md) · [基线分段按钮 Segmented buttons](references/segmented-buttons.md) |
| 突出当前页面的主动作 | [悬浮按钮 FAB](references/floating-action-button.md) · [带文字的 Extended FAB](references/extended-fab.md) · [悬浮操作菜单 FAB menu](references/fab-menu.md) |
| 切换顶级目的地或页内同级内容 | [导航栏 Navigation bar](references/navigation-bar.md) · [导航轨 Navigation rail](references/navigation-rail.md) · [基线导航抽屉 Navigation drawer](references/navigation-drawer.md) · [页签 Tabs](references/tabs.md) |
| 浏览对象、分组与组织内容 | [列表 Lists](references/lists.md) · [卡片 Cards](references/cards.md) · [轮播 Carousel](references/carousel.md) · [分隔线 Divider](references/divider.md) |
| 在上下文中显示详情、筛选器或必答决策 | [底部面板 Bottom sheets](references/bottom-sheets.md) · [侧面板 Side sheets](references/side-sheets.md) · [对话框 Dialogs](references/dialogs.md) |
| 输入文本、日期或时间 | [文本框 Text fields](references/text-fields.md) · [日期选择器 Date pickers](references/date-pickers.md) · [时间选择器 Time pickers](references/time-pickers.md) |
| 多选、单选、启停或调值 | [复选框 Checkbox](references/checkbox.md) · [单选 Radio button](references/radio-button.md) · [开关 Switch](references/switch.md) · [滑块 Sliders](references/sliders.md) · [标签 Chips](references/chips.md) |
| 提示未读、操作结果或额外说明 | [徽标 Badges](references/badges.md) · [短消息 Snackbar](references/snackbar.md) · [工具提示 Tooltips](references/tooltips.md) |
| 表示工作正在进行或完成比例 | [加载指示器 Loading indicator](references/loading-indicator.md) · [进度指示器 Progress indicators](references/progress-indicators.md) |

## 按设计问题取资料

| 情境 | 读取与使用 |
| --- | --- |
| 建立产品视觉层级、配浅深色、字阶或高密度样式 | [设计原则与主题](references/foundations.md)。把颜色绑定到成对角色，再套具体组件令牌。 |
| 同一页面要覆盖桌面、网页缩放、平板或手机 | [窗口、输入与布局](references/adaptive-layout.md)。用可用窗宽和任务关系决定单/双窗格，跨断点复用当前对象和命令。 |
| 做弹簧、控件反馈、页面转场、拖动或减少动态效果 | [动效](references/motion.md)。组件先取自身规格，空间属性与颜色/透明度分别驱动。 |
| 将组件移植到项目使用的编程语言或框架 | [平台适配与代码样例](references/platforms.md)。Web、Windows、跨平台桌面、Android、iOS 和 Flutter 各有落点。 |
| 按名称、颜色或精确尺寸查值 | [离线令牌用法](references/tokens.md)。直接读 JSON，也可运行 [组件查询](scripts/component.py)。 |

组合页面时，搜索范围跟随窗格，工具栏命令作用于当前对象，导航跟随路由，进度取自正在执行的任务。用户启用减少动态效果时，可直接呈现目标状态，保留操作结果、焦点与进度反馈。

验收自适应工作区时，可以先搜索并选中一个文件，再缩窄窗口，从菜单对它执行同一条命令。

[官方组件目录](https://m3.material.io/components) · [按钮选型总览](https://m3.material.io/components/all-buttons)
