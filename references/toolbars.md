# 工具栏 · Toolbars / Bottom app bar

常驻通用命令取 docked，随所选对象或编辑场景变化的命令取 floating。导航栏切换目的地；工具栏操作当前内容。旧 bottom app bar 可映射到 docked toolbar。

## 组件契约

`Toolbar(actions, placement, orientation, emphasis, overflow)`。槽位可放图标按钮、菜单、输入、文字或一项高优先级动作。颜色可用 standard / vibrant；状态绑定到各条命令，例如撤销可用性、加粗选中态。

窄屏停靠工具栏通常在底部占满宽度，避免与底部导航争同一位置。宽屏可在文档边缘放水平或垂直浮动工具栏；与导航轨并存时优先占相对两侧。常用项保持可见，其余进入带标签的溢出菜单。

## 动效与输入

子控件各自响应按压。滚动时可固定工具栏、滑出或只保留主要操作。键盘焦点还在工具栏内时，让当前命令保持可见。

触屏确保各项命中面积。桌面原生命令可同时接到菜单、工具栏、快捷键。Web 使用命名的 toolbar 时，Tab 进出、沿主轴方向键移动；含文本输入时为编辑光标保留左右键。

## 取用示例

`Toolbar(actions=[undo,redo,highlight,more], placement=floating, orientation=wideWindow ? vertical : horizontal, emphasis=standard)`。

[本地规格令牌](../assets/tokens/toolbars.json) · [官网概览](https://m3.material.io/components/toolbars/overview) · [规格](https://m3.material.io/components/toolbars/specs) · [指南](https://m3.material.io/components/toolbars/guidelines) · [无障碍](https://m3.material.io/components/toolbars/accessibility)
