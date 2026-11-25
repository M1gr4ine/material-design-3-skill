# 平台适配与代码样例

## Google 官方组件库与生态现状

能用 Google 官方维护的原生 M3 组件库时优先使用；缺失或处于维护模式的平台，使用本技能的离线令牌、主题生成器与宿主原生控件补齐。[M3 开发入口](https://m3.material.io/develop)

| 官方包 / 生态工具 | 适用平台 | 状态与 M3 Expressive 支持 | 使用建议 |
| --- | --- | --- | --- |
| **Jetpack Compose Material 3** (`androidx.compose.material3`) | Android / Compose Multiplatform | 活跃维护，**官方首发 M3 + M3 Expressive**（含 `MotionScheme`、分裂按钮、浮动工具栏、形变加载器） | Android 首选；按项目依赖版本查阅公开 API。 |
| **MDC-Android** (`com.google.android.material:material`) | Android Views (Kotlin/Java) | 活跃维护，支持 M3 与 Expressive 组件 | 现有 View 体系项目使用。 |
| **Flutter Material** (`package:flutter/material.dart`) | 手机、桌面、Web | 活跃维护，默认启用基线 M3（`useMaterial3: true`） | Expressive 新增样式和弹簧按本地 SDK 能力用本技能令牌补齐。 |
| **Angular Material** (`@angular/material`) | Web (Angular) | 活跃维护，内置官方 M3 主题系统（`mat.theme`）与组件令牌 | Angular 项目首选；Expressive 动效可叠加 `assets/motion.css`。 |
| **Material Web** (`@material/web`) | Web Components (Lit) | **处于维护模式**，未完整覆盖 M3 Expressive | 不建议新项目重度绑定；改用原生 HTML / 宿主框架 + 本技能 [tokens.css](../assets/tokens.css) 与 [motion.css](../assets/motion.css)。 |
| **Material Color Utilities** (`@material/material-color-utilities`) | TS/JS、Dart、Kotlin、Java、Swift、Python、C++ | 活跃维护，Google 官方 HCT 动态取色算法库 | 运行时根据图片/用户壁纸动态换肤时接入；静态构建期可直接用 [theme.py](../scripts/theme.py)。 |
| **Material Symbols** | 全平台（Variable Font / SVG） | 活跃维护，Google 官方可变图标集（`FILL` / `wght` / `GRAD` / `opsz`） | 替代旧 Material Icons，选中导航项切换 `FILL 0 → 1`。 |

## 各框架与平台落点

| 目标与语言 | 适配入口 |
| --- | --- |
| Web：HTML/CSS/JS/TS、React、Vue、Svelte、Tailwind CSS v4，及 Electron/Tauri | 直接引入 [tokens.css](../assets/tokens.css) + [motion.css](../assets/motion.css)（或用 `python scripts/theme.py --seed "#HEX" --format css\|tailwind` 生成品牌主题）。状态层用 `color-mix(in srgb, currentColor calc(var(--md-sys-state-hover-state-layer-opacity) * 100%), transparent)` 实现；若用 `position: absolute` 伪元素绘制较小可见底框（如 `48×48` 命中区内的按钮容器）、选中态背景或状态层，宿主须设 `isolation: isolate` 且背景伪元素设 `z-index: -1`，防止按 CSS 层叠顺序盖住直接文本/图标。需要混合胶囊与小圆角或对 `border-radius` 做 Expressive 弹簧过渡时，用元素实际短边一半的精确 `px`（如 `20px`）代替 `9999px`（且避免 `%` 与 `px` 混用），防止 CSS 重叠圆角缩放坍缩和过冲闪成直角；基础态声明完整 `transition`，`:active` 不覆写 `transition` 简写。控件交互遵循 WAI-ARIA APG 模式（如建议输入框用 combobox + listbox）。**注意**：`@mui/material` 默认样式仍偏向 Material Design 2，不要为了 M3 盲目引入它。[WAI-ARIA 组件模式](https://www.w3.org/WAI/ARIA/apg/patterns/) |
| Angular (TypeScript) | 使用官方 `@angular/material` 的 M3 Sass API（`mat.theme(...)` 与系统变量 `--mat-sys-*`），配合 `BreakpointObserver` 映射 M3 窗口断点；Expressive 专属组件（如 Split button、Floating toolbar）按组件契约组合实现。[Angular Material 主题](https://material.angular.dev/guide/theming) |
| Windows，C# / C++ / XAML | WinUI 可用 `AutoSuggestBox`、`CommandBar`、`NavigationView`、`ContentDialog`。WPF 使用 `TextBox`、`ToolBar`、命令绑定、`AutomationProperties`；用 `ResourceDictionary` 映射颜色和尺寸。窄窗用既有 overflow，菜单、快捷键、工具栏共享同一命令及可用状态。[WinUI 输入](https://learn.microsoft.com/en-us/windows/apps/develop/input/keyboard-interactions) · [WPF ToolBar](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/toolbar) |
| Qt，C++ / Python (PySide/PyQt) | Qt Widgets 的 `QLineEdit` + `QCompleter` 对应编辑与建议，`QAction` 可同时接 `QToolBar` 和菜单；Qt Quick Controls 可用平台样式和语义控件。保留 Qt 的焦点、输入法、逻辑坐标与辅助技术树。Qt 自带 Material 风格的版本能力按所用 Qt 核对。[QLineEdit](https://doc.qt.io/qt-6/qlineedit.html) · [Qt 无障碍](https://doc.qt.io/qt-6/accessible.html) |
| JVM 桌面，Java / Kotlin | Swing 可把搜索挂在表格的 `TableRowSorter`，把共享 `Action` 放入 `JToolBar`；JavaFX 可分别使用 `TextField`、`FilteredList`、`ToolBar`。主题适配沿用 Look and Feel 或 JavaFX CSS。列表变更时保存数据对象身份。[Swing 共用动作](https://docs.oracle.com/javase/tutorial/uiswing/misc/action.html) · [JavaFX ToolBar](https://openjfx.io/javadoc/21/javafx.controls/javafx/scene/control/ToolBar.html) |
| Android，Kotlin / Java | Compose Material 3 通过 `MaterialTheme` 绑定颜色、字阶、形状与 `motionScheme`（可用 `scripts/theme.py --format compose` 生成色板）；Java/View 项目查 MDC-Android。键盘、读屏、系统返回和预测返回接宿主导航。[Compose Material 3](https://developer.android.com/develop/ui/compose/designsystems/material3) · [Android Views](https://m3.material.io/develop/android/mdc-android) |
| iOS / macOS，Swift / SwiftUI | 用 `searchable`、`toolbar`、`sheet`、系统焦点与无障碍值承载行为。视觉角色映射到颜色资产、字体与形状，保留平台导航手势和窗口命令。用户启用 Reduce Motion 时调整自定义动画。[SwiftUI Search](https://developer.apple.com/documentation/swiftui/search) · [Reduce Motion](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion) |
| Flutter，Dart，手机、桌面和 Web | `ThemeData` / `ColorScheme` 管主题（可用 `scripts/theme.py --format flutter` 或 `ColorScheme.fromSeed`），`SearchAnchor`、`NavigationRail`、`MenuAnchor` 等承载行为。`LayoutBuilder` / `MediaQuery` 看实际可用宽度。[M3 的 Flutter 说明](https://m3.material.io/develop/flutter) · [Flutter 自适应设计](https://docs.flutter.dev/ui/adaptive-responsive) |
| 其他 GUI 语言或自绘控件 | 把状态留在业务模型，将令牌接入主题。自绘控件向辅助技术暴露名称、角色、值和动作，并加入宿主的焦点遍历。手势和键盘调用同一命令。 |

## 可直接取用的适配示例

**Web 的建议搜索。** [search.html](../assets/examples/search.html) 可本地直接打开，已接入 [tokens.css](../assets/tokens.css) 与 [motion.css](../assets/motion.css)，演示 `--md-sys-color-*`、`color-mix` 状态层、浅深色切换、上下键/Enter/Esc 与中文 IME 选词保护。接远程数据时，按查询身份丢弃过期响应。[W3C Combobox](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/)

**原生 PC 的表格搜索与工具栏。** 在 Swing 事件派发线程调用 [DesktopSearchTools.java](../assets/examples/DesktopSearchTools.java)（Java 11+）。搜索框过滤表格，工具栏与窗口的「文件」菜单共用 `Action`。缩窄窗口后，菜单仍提供完整命令。依赖当前文件的 `Action` 从表格取所选行，经 `convertRowIndexToModel` 找到过滤、排序后的原对象。未选文件时禁用该命令。

```java
var sorter = new TableRowSorter<>(table.getModel());
table.setRowSorter(sorter);
List<Action> commands = List.of(openAction, exportAction);
commands.forEach(fileMenu::add);
var header = DesktopSearchTools.create(
    "搜索文件", "文件操作", sorter, commands, surfaceContainer, onSurface);
window.add(header, BorderLayout.PAGE_START);
```

**手机与大窗的搜索选择（Flutter）。** [project_search.dart](../assets/examples/project_search.dart) 接收项目名称和 `onChoose`。可用宽度小于 600 时全屏，较宽时停靠。搜索视图使用 Flutter 自带的控制器。[SearchAnchor](https://api.flutter.dev/flutter/material/SearchAnchor/searchController.html)

**Android 原生主题接入（Jetpack Compose Material 3）。** 用 `python scripts/theme.py --seed "#1A73E8" --variant expressive --format compose` 生成 `LightColorScheme` / `DarkColorScheme` 后，直接接入 `MaterialTheme`：

```kotlin
MaterialTheme(
    colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme,
    motionScheme = MotionScheme.expressive(), // 需要高频工具稳定反馈时改用 MotionScheme.standard()
    content = content,
)
```

同一份 PDF 编辑器可以在窄屏使用全屏搜索和底部浮动工具栏，在宽屏使用停靠搜索、侧边工具栏和属性窗格。查询、选中页、撤销栈由文档会话持有；改变布局只更换承载控件。
