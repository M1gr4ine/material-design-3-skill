# Material Design 3 Skill

面向所有主流 AI 编码助手的 **Material Design 3 & M3 Expressive** 跨平台技能（兼容 **Agent Skills** 开放标准），覆盖 Web、原生桌面与手机 App。

它将 Google 官方 `m3.material.io`（`2026-10-13` 快照）的 **36 个组件规范**、**5,091 个去重组件令牌**、**12 组弹簧动效** 与 **零依赖 HCT 动态主题引擎** 整理为按需加载的 Markdown、JSON、CSS 与 Python 工具——无论使用哪个 Agent 或前端/原生框架，都能直接落地正宗的 Material Design 3 界面。[技能入口](SKILL.md) · [官方设计指南](https://m3.material.io/)

## 安装（兼容所有主流 Agent）

### 方式一：一键跨 Agent 安装（推荐）

使用通用 Agent Skills CLI，自动识别并安装到 Antigravity、Claude Code、Codex、Cursor、Gemini CLI、OpenCode、Windsurf、GitHub Copilot 等 30+ 客户端：

```sh
npx skills add M1gr4ine/material-design-3-skill
```

全局安装（所有项目可用）：

```sh
npx skills add M1gr4ine/material-design-3-skill -g
```

### 方式二：按客户端手动克隆（无需 Node.js）

以下路径适用于 PowerShell、Bash 与 Zsh；也可以下载 [源码 ZIP](https://github.com/M1gr4ine/material-design-3-skill/archive/refs/heads/main.zip)，将解压后的目录重命名为 `material-design-3` 放入对应 `skills/` 目录。

| 客户端 / 作用域 | 安装命令 |
| --- | --- |
| **项目级通用目录**（Antigravity / Codex / Cursor / Gemini CLI / OpenCode / Copilot） | `git clone https://github.com/M1gr4ine/material-design-3-skill.git .agents/skills/material-design-3` |
| **Google Antigravity**（全局） | `git clone https://github.com/M1gr4ine/material-design-3-skill.git "$HOME/.gemini/config/skills/material-design-3"` |
| **Claude Code**（全局） | `git clone https://github.com/M1gr4ine/material-design-3-skill.git "$HOME/.claude/skills/material-design-3"` |
| **OpenAI Codex**（全局） | `git clone https://github.com/M1gr4ine/material-design-3-skill.git "$HOME/.codex/skills/material-design-3"` |
| **Cursor**（全局） | `git clone https://github.com/M1gr4ine/material-design-3-skill.git "$HOME/.cursor/skills/material-design-3"` |
| **Gemini CLI**（全局） | `git clone https://github.com/M1gr4ine/material-design-3-skill.git "$HOME/.gemini/skills/material-design-3"` |
| **OpenCode**（全局） | `git clone https://github.com/M1gr4ine/material-design-3-skill.git "$HOME/.config/opencode/skills/material-design-3"` |
| **DeepSeek Harness（DSH）**（全局） | `git clone https://github.com/M1gr4ine/material-design-3-skill.git "$HOME/.dsh/skills/material-design-3"` |

> 如果设置了 `CODEX_HOME` 或 `DSH_HOME`，将技能放入相应目录的 `skills/material-design-3` 下即可。其他支持读取本地文件的助手可以直接从 [SKILL.md](SKILL.md) 开始。

### 开始使用

安装后，在新对话中直接描述界面需求（中英文均可触发）：

> 用 `material-design-3` 给项目列表加搜索，主色 `#1A73E8`，采用 Expressive 风格并支持浅深色切换。桌面端停靠显示建议，手机端全屏展开；支持方向键、Enter、Esc 与中文输入法选词保护，减少动态效果时跳过展开动画。

## 与 Google 官方组件库的关系

Google 在不同平台对 M3 的官方组件库支持程度并不一致，本技能帮你选对官方库并补齐跨平台缺口（详表见 [平台适配](references/platforms.md)）：

- **原生有官方活跃库**：Android（**Jetpack Compose Material 3** / MDC-Android）、**Flutter Material**、Web Angular（**Angular Material**）优先使用官方库，配合本技能查询精确令牌、交互契约与 Expressive 动效。
- **通用 Web 与跨平台桌面**：Google 官方 `@material/web` 目前处于维护模式且未完整覆盖 M3 Expressive；React、Vue、Svelte、Tailwind、Electron/Tauri、WinUI/WPF、Qt、JVM 桌面可直接套用本技能的 [tokens.css](assets/tokens.css)、[motion.css](assets/motion.css)、[spring.mjs](assets/spring.mjs) 与 5,091 条官方离线令牌。
- **动态取色与图标**：静态构建期可用内置零依赖 [theme.py](scripts/theme.py) 按 HCT 空间生成主题并自动校验 WCAG 对比度；运行时动态换肤可接入 Google 官方 `@material/material-color-utilities`，图标配合官方 **Material Symbols** 可变字体。

## 看同一个搜索功能怎样落到多平台

| 平台 | 示例里的交互 | 代码 |
| --- | --- | --- |
| Web | 本地打开 HTML，体验官方 `--md-sys-*` 令牌、浅深色切换与 `color-mix` 状态层；输入「档」测试键盘与 IME。 | [HTML 搜索示例](assets/examples/search.html) |
| 原生桌面 | 在 Java Swing 表格中筛选行，工具栏和窗口菜单共用同一个 `Action`。 | [Java 组件](assets/examples/DesktopSearchTools.java) · [接入示例](references/platforms.md) |
| 手机与大窗 | 在 Flutter 的 `MaterialApp` 中传入项目名和选择回调。可用宽度小于 600 dp 时全屏搜索，宽窗停靠显示。 | [Flutter 组件](assets/examples/project_search.dart) |

使用 React、Vue、Svelte、Tailwind、Angular、Compose、Qt/PySide、WPF/WinUI、JavaFX 或 SwiftUI 时，可按 [平台适配](references/platforms.md) 映射到宿主控件。

## 离线工具与按任务查规格

| 要做的事 | 从哪里开始 |
| --- | --- |
| 选组件、变体、键盘和触屏行为 | 36 个组件专题，含搜索栏、工具栏、分裂按钮、按钮组、导航、表单和反馈。[全部组件](SKILL.md) · [搜索栏](references/search.md) · [工具栏](references/toolbars.md) |
| 定浅深色、表面层级、品牌动态色、字阶与形状 | 按语义角色取色，用 HCT 从任意品牌种子色生成主题并审计对比度。[主题指南](references/foundations.md) · [CSS 令牌](assets/tokens.css) · [主题脚本](scripts/theme.py) |
| 做响应式窗口断点与多窗格骨架 | 按可用窗宽决定单栏、双栏和导航方式。[自适应布局](references/adaptive-layout.md) |
| 加弹簧反馈、手势拖动和页面转场 | Standard 与 Expressive 共 12 组弹簧、6 种转场模式，含减少动效处理。[动效指南](references/motion.md) · [CSS 变量](assets/motion.css) · [可打断弹簧](assets/spring.mjs) |
| 查具体尺寸、颜色或自动展开令牌别名链 | 5,091 个去重后的官方组件令牌，保留官方规格链接。[令牌说明](references/tokens.md) · [JSON 目录](assets/tokens/) |

以下脚本均只依赖 **Python 3 标准库**，可在任意 Agent 沙箱内完全离线运行：

```sh
# 1. 查组件卡、原始令牌、自动展开别名链（--resolve）或全局/系统搜索
python scripts/component.py
python scripts/component.py 搜索条
python scripts/component.py search --token search-bar.container --resolve --theme light
python scripts/component.py --token floating.standard.container.color
python scripts/component.py --sys fast.spatial --motion expressive

# 2. 按 Google HCT 算法从品牌种子色生成 M3 主题（CSS / Tailwind v4 / JSON / Compose / Flutter）
python scripts/theme.py --seed "#1A73E8" --format css
python scripts/theme.py --seed "#1A73E8" --variant expressive --format tailwind
python scripts/theme.py --seed "#1A73E8" --contrast high --format compose
python scripts/theme.py --seed "#1A73E8" --audit
python scripts/theme.py --pair "#1d1b20" "#fef7ff"
```

## 验证测试

```sh
python -m unittest discover -s tests -v
```

## 许可与署名

本项目独立维护。查询工具、HCT 主题生成器、CSS 样式表、动效实现、测试用例和代码示例采用 Apache-2.0。中文文档及根据 Google Material Design 3 规范整理的设计数据采用 CC BY 4.0。转载或改编时请保留原作者和来源，并标明所做的修改。[Apache-2.0](LICENSE) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) · [来源与改编说明](NOTICE)
