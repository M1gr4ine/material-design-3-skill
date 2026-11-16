# Material Design 3 Skill

给编码助手使用的中文 Material Design 3 技能，覆盖网页、原生桌面和手机 App。它把 Google 的组件规范整理成可以按需读取的 Markdown 和 JSON。模型可以查到搜索栏怎样展开、工具栏怎样收纳命令、动效用哪组弹簧，再用项目已有的语言和控件实现。[组件索引](SKILL.md) · [官方设计指南](https://m3.material.io/)

## 安装

在终端选择对应客户端的命令。以下路径是默认的个人技能目录，适用于 PowerShell、Bash 和 Zsh。

**Codex**

```sh
git clone https://github.com/M1gr4ine/material-design-3-skill.git "$HOME/.codex/skills/material-design-3"
```

**DeepSeek Harness（DSH）**

```sh
git clone https://github.com/M1gr4ine/material-design-3-skill.git "$HOME/.dsh/skills/material-design-3"
```

如果设置了 `CODEX_HOME` 或 `DSH_HOME`，请把技能放在相应目录的 `skills/material-design-3` 下。也可以下载源码 ZIP，将解压后含有 `SKILL.md` 的文件夹改名为 `material-design-3`，放进客户端的 `skills` 目录。其他支持读取文件的助手可以直接从技能入口开始。[下载源码 ZIP](https://github.com/M1gr4ine/material-design-3-skill/archive/refs/heads/main.zip) · [技能入口](SKILL.md)

安装后，在新对话中描述要做的界面和交互。

> 用 `material-design-3` 给项目列表加搜索。桌面端把建议显示在输入框下面，手机端全屏展开。支持方向键、Enter 和 Esc，中文输入法选词时保留 Enter。用户开启减少动态效果时跳过展开动画。

## 看同一个搜索功能怎样落到三个平台

| 平台 | 示例里的交互 | 代码 |
| --- | --- | --- |
| Web | 本地打开 HTML，输入「档」试试。方向键浏览建议，Enter 选择，Esc 收起。 | [HTML 搜索示例](assets/examples/search.html) |
| 原生桌面 | 在 Java Swing 表格中筛选行，工具栏和窗口菜单可以共用同一个 `Action`。 | [Java 组件](assets/examples/DesktopSearchTools.java) · [接入示例](references/platforms.md) |
| 手机与大窗 | 在 Flutter 的 `MaterialApp` 中传入项目名和选择回调。可用宽度小于 600 个逻辑像素时全屏搜索，宽窗中停靠显示。 | [Flutter 组件](assets/examples/project_search.dart) |

使用 Qt/PySide、WPF/WinUI、JavaFX、Compose 或 SwiftUI 时，可按平台对照表把搜索、菜单、焦点和系统动效偏好映射到宿主控件。[平台适配](references/platforms.md)

## 按任务查规格

| 要做的事 | 从哪里开始 |
| --- | --- |
| 选组件、变体、键盘和触屏行为 | 36 个组件专题，含搜索栏、工具栏、按钮、导航、表单和反馈。[全部组件](SKILL.md) · [搜索栏](references/search.md) · [工具栏](references/toolbars.md) |
| 定浅深色、字阶、形状和自适应布局 | 按语义角色取颜色，按可用窗宽决定单栏、双栏和导航方式。[主题](references/foundations.md) · [自适应布局](references/adaptive-layout.md) |
| 加控件反馈、拖动和页面转场 | Standard 与 Expressive 共 12 组弹簧、6 种转场模式，包含减少动态效果的处理。[动效指南](references/motion.md) · [CSS 变量](assets/motion.css) · [可打断弹簧](assets/spring.mjs) |
| 查具体尺寸、颜色或弹簧别名 | 5,091 个去重后的组件令牌按组件分文件存放，每个文件保留官方规格链接。[令牌说明](references/tokens.md) · [JSON 目录](assets/tokens/) |

在技能目录里用 Python 3 即可离线查值，脚本只用标准库。省略组件名会列出所有组件。

```sh
python scripts/component.py
python scripts/component.py 搜索条
python scripts/component.py search --token md.comp.search-bar.container.height
python scripts/component.py toolbars --token md.comp.toolbar.floating.standard.container.color
```

最后两条分别返回搜索栏高度 `56 DIPS` 和浮动工具栏的颜色角色 `md.sys.color.surface-container`。任何语言都可以直接读取同一份 JSON。[搜索栏令牌](assets/tokens/search.json) · [工具栏令牌](assets/tokens/toolbars.json)

## 许可与署名

本项目独立维护。查询工具、动效实现和代码示例采用 Apache-2.0。中文文档及根据 Google Material Design 3 规范整理的设计数据采用 CC BY 4.0。转载或改编时请保留原作者和来源，并标明所做的修改。[Apache-2.0](LICENSE) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) · [来源与改编说明](NOTICE)
