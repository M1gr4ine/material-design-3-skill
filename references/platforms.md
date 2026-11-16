# 平台适配与代码样例

下表把 M3 契约映射到常见 GUI 框架。具体 Expressive 变体以项目所用组件库的版本为准。[M3 开发入口](https://m3.material.io/develop)

| 目标与语言 | 适配入口 |
| --- | --- |
| Web，HTML/CSS/JS/TS、React、Vue、Svelte，及 Electron/Tauri 渲染层 | 保留宿主框架，使用原生 HTML 控件、已有组件库和 CSS 变量。建议输入框对接 combobox 模式，真正的结果是链接或列表。官方 `@material/web` 处于维护模式，官网未把它列为完整 Expressive 实现。[Material Web](https://material-web.dev/) · [WAI-ARIA 组件模式](https://www.w3.org/WAI/ARIA/apg/patterns/) |
| Windows，C# / C++ / XAML | WinUI 可用 AutoSuggestBox、CommandBar、NavigationView、ContentDialog。WPF 使用 TextBox、ToolBar、命令绑定、AutomationProperties；用 ResourceDictionary 映射颜色和尺寸。窄窗用既有 overflow，菜单、快捷键、工具栏共享同一命令及可用状态。[WinUI 输入](https://learn.microsoft.com/en-us/windows/apps/develop/input/keyboard-interactions) · [WPF ToolBar](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/toolbar) |
| Qt，C++ / Python (PySide/PyQt) | Qt Widgets 的 QLineEdit + QCompleter 对应编辑与建议，QAction 可同时接 QToolBar 和菜单；Qt Quick Controls 可用平台样式和语义控件。保留 Qt 的焦点、输入法、逻辑坐标与辅助技术树。Qt 自带 Material 风格的版本能力按所用 Qt 核对。[QLineEdit](https://doc.qt.io/qt-6/qlineedit.html) · [Qt 无障碍](https://doc.qt.io/qt-6/accessible.html) |
| JVM 桌面，Java / Kotlin | Swing 可把搜索挂在表格的 TableRowSorter，把共享 Action 放入 JToolBar；JavaFX 可分别使用 TextField、FilteredList、ToolBar。主题适配沿用 Look and Feel 或 JavaFX CSS。列表变更时保存数据对象身份。[Swing 共用动作](https://docs.oracle.com/javase/tutorial/uiswing/misc/action.html) · [JavaFX ToolBar](https://openjfx.io/javadoc/21/javafx.controls/javafx/scene/control/ToolBar.html) |
| Android，Kotlin / Java | Compose Material 3 通过 MaterialTheme 绑定角色；SearchBar、页面 scaffold、弹层、动效优先取当前依赖版本的公开 API。Java/View 项目查 MDC-Android 现有组件。键盘、读屏、系统返回和预测返回接宿主导航。[Compose](https://developer.android.com/develop/ui/compose/designsystems/material3) · [Android Views](https://m3.material.io/develop/android/mdc-android) |
| iOS / macOS，Swift / SwiftUI | 用 searchable、toolbar、sheet、系统焦点与无障碍值承载行为。视觉角色映射到颜色资产、字体与形状，保留平台导航手势和窗口命令。用户启用 Reduce Motion 时调整自定义动画。[SwiftUI Search](https://developer.apple.com/documentation/swiftui/search) · [Reduce Motion](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion) |
| Flutter，Dart，手机、桌面和 Web | ThemeData/ColorScheme 管主题，SearchAnchor、NavigationRail、MenuAnchor 等承载行为。LayoutBuilder/MediaQuery 看实际可用宽度。官网列出 Flutter 的基线 M3 支持；Expressive 的选择、样式和弹簧可依本地 SDK 按需补齐。[M3 的 Flutter 说明](https://m3.material.io/develop/flutter) · [Flutter 自适应设计](https://docs.flutter.dev/ui/adaptive-responsive) |
| 其他 GUI 语言或自绘控件 | 把状态留在业务模型，将令牌接入主题。自绘控件向辅助技术暴露名称、角色、值和动作，并加入宿主的焦点遍历。手势和键盘调用同一命令。 |

## 三个可以取走的适配示例

**Web 的建议搜索。** [search.html](../assets/examples/search.html) 可本地直接打开。它区分输入建议和提交后的结果，支持上下键、Enter、Esc、鼠标与输入法组合过程。复制该文件与相邻目录中的 motion.css 即可复用示例；接远程数据时，把当前查询与返回结果对应起来。[W3C Combobox](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/)

**原生 PC 的表格搜索与工具栏。** 在 Swing 事件派发线程调用 [DesktopSearchTools.java](../assets/examples/DesktopSearchTools.java)（Java 11+）。搜索框过滤表格，工具栏与窗口的「文件」菜单共用 Action。缩窄窗口后，菜单仍提供完整命令。依赖当前文件的 Action 从表格取所选行，经 `convertRowIndexToModel` 找到过滤、排序后的原对象。未选文件时禁用该命令。

```java
var sorter = new TableRowSorter<>(table.getModel());
table.setRowSorter(sorter);
List<Action> commands = List.of(openAction, exportAction);
commands.forEach(fileMenu::add);
var header = DesktopSearchTools.create(
    "搜索文件", "文件操作", sorter, commands, surfaceContainer, onSurface);
window.add(header, BorderLayout.PAGE_START);
```

**手机与大窗的搜索选择。** [project_search.dart](../assets/examples/project_search.dart) 接收项目名称和 `onChoose`。可用宽度小于 600 时全屏，较宽时停靠。搜索视图使用 Flutter 自带的控制器。[SearchAnchor](https://api.flutter.dev/flutter/material/SearchAnchor/searchController.html)

同一份 PDF 编辑器可以在窄屏使用全屏搜索和底部浮动工具栏，在宽屏使用停靠搜索、侧边工具栏和属性窗格。查询、选中页、撤销栈由文档会话持有；改变布局只更换承载控件。
