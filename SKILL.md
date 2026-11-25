---
name: material-design-3
description: >-
  当 Web、原生桌面或手机 App 采用 Google Material Design 3、Material You 或 M3 Expressive，
  需要设计、实现、生成主题或审查界面组件、布局、色彩令牌与弹簧动效时使用。
  Use when designing, building, theming, or auditing Material Design 3 (M3 / MD3),
  Material You, or M3 Expressive UIs across Web (HTML/CSS/React/Vue/Svelte/Angular/Tailwind),
  Android (Jetpack Compose / Views), Flutter, iOS/macOS, or native desktop (WinUI/WPF/Qt/JVM).
license: Apache-2.0 AND CC-BY-4.0
compatibility: >-
  Compatible with Agent Skills standard (Antigravity, Claude Code, Codex, Cursor,
  Gemini CLI, OpenCode, Windsurf, GitHub Copilot, DSH). Optional CLI scripts use
  Python 3.9+ standard library only (no third-party dependencies).
metadata:
  spec_snapshot: "2026-10-13"
  components: "36"
  tokens: "5091"
---

# Material Design 3

按用户要完成的动作选组件。设计稿从组件契约取变体与交互，代码把同一契约接到项目已有的控件、状态和主题。

## 执行流程

1. **先选宿主官方库，再补齐令牌。** Android 用 Jetpack Compose Material 3 / MDC-Android，Flutter 用 `package:flutter/material.dart`，Angular 用 `@angular/material`。通用 Web（HTML/React/Vue/Svelte/Tailwind）或桌面端直接复用本技能的 [CSS 令牌](assets/tokens.css)、[动效变量](assets/motion.css) 与 [平台映射](references/platforms.md)——不要因为名字带 Material 就误装默认仍是 Material 2 风格的 `@mui/material`，也不要假设处于维护模式的 `@material/web` 覆盖了 M3 Expressive。
2. **先定品牌主题，严禁硬编码任意色值。** 已有品牌色时运行 `python scripts/theme.py --seed "#HEX" --format css|tailwind|json|compose|flutter`（默认 `tonal-spot`，另支持 `fidelity` / `expressive` / `vibrant` / `neutral` / `monochrome` 及 `standard` / `medium` / `high` 对比度），并用 `--audit` 校验 WCAG 2.1 对比度；默认基线直接引入 [assets/tokens.css](assets/tokens.css)。
3. **按任务查组件契约与精确令牌。** 从下表读对应组件指南，需要精确高度、圆角、颜色角色或弹簧参数时运行 `python scripts/component.py <组件> --token <关键词> --resolve` 或直接读 `assets/tokens/<组件>.json`。
4. **守住 M3 关键护栏：**
   - **表面阶梯优先于重阴影**：用 `surface-container-lowest` → `low` → `default` → `high` → `highest` 区分层级，只在菜单、浮层、停靠面板等需要脱离背景处叠加海拔阴影。
   - **成对绑定语义色**：前景永远配对应 `on-*` 角色（如 `primary` 配 `on-primary`，`secondary-container` 配 `on-secondary-container`）。
   - **交互状态层与焦点环**：实现 hover（8%）、focus/pressed（10%）、dragged（16%）、disabled（38%）状态层，保留 `3dp` 粗、`2dp` 外偏移的可见键盘焦点环，触屏目标保证 `48×48 dp`。
   - **图标与字体回退**：图标优先采用 Google **Material Symbols**（导航未选中 `FILL 0`、选中 `FILL 1`），字体栈保留中文字体回退（如 `"Roboto", "Noto Sans SC", system-ui, sans-serif`）。
   - **空间与效果分通道动效 + 减少动效**：位置/尺寸/圆角用 spatial 弹簧，颜色/透明度用 effects 弹簧；Web 对 `border-radius` 做弹簧形变时，满圆态须用实际短边一半的精确 `px` 而非 `9999px`（避免过冲闪成直角），且 `:active` 不覆写 `transition` 简写；响应 `prefers-reduced-motion` / 系统减少动效偏好，直接呈现目标状态并保留焦点与业务结果。

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
| 建立产品视觉层级、配浅深色、生成品牌主题或字阶 | [设计原则与主题](references/foundations.md) · [离线 CSS 令牌](assets/tokens.css) · [HCT 主题与对比度脚本](scripts/theme.py) |
| 同一页面要覆盖桌面、网页缩放、平板或手机 | [窗口、输入与布局](references/adaptive-layout.md)。用可用窗宽和任务关系决定单/双窗格，跨断点复用当前对象和命令。 |
| 做弹簧、控件反馈、页面转场、拖动或减少动态效果 | [动效](references/motion.md) · [CSS 变量](assets/motion.css) · [可打断弹簧](assets/spring.mjs) |
| 选用 Google 官方组件库或移植到项目语言与框架 | [平台适配与代码样例](references/platforms.md)。含 Google 官方库现状及 Web、Angular、Compose、Flutter、桌面和 iOS 落点。 |
| 按名称、颜色或精确尺寸查值并展开别名链 | [离线令牌用法](references/tokens.md) · [组件与令牌查询](scripts/component.py) |

组合页面时，搜索范围跟随窗格，工具栏命令作用于当前对象，导航跟随路由，进度取自正在执行的任务。验收自适应工作区时，可以先搜索并选中一个文件，再缩窄窗口，从菜单对它执行同一条命令。

[官方组件目录](https://m3.material.io/components) · [按钮选型总览](https://m3.material.io/components/all-buttons)
