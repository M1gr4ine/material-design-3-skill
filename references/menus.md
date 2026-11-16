# 菜单 · Menus

显示临时命令或选项。工具栏保留常用命令，余项收进 menu。上下文菜单作用于明确对象，可由右键、长按或可见的更多按钮打开。

## 组件契约

`Menu(anchor, items, open, onChoose, onDismiss)`。当前 vertical menu 可用标准或鲜明配色、分组、选中态和子菜单；旧 baseline 仍可维护。条目可表示命令、单选、多选或下一级。

锚定触发控件，靠近屏幕边缘时调整展开方向；保留被操作的对象。菜单项按命令可用性启停。子菜单返回上级，整个菜单退出时焦点回到入口。

## 动效与输入

从锚点沿可用方向展开；子菜单层级变化保留来源项与父级的空间线索。减少动效时直接定位，焦点仍落到可操作项。

桌面采用原生菜单或完整的 menu 键盘模式（方向键、Enter、Escape、子菜单方向）；Web 普通站点导航使用链接。只用右键触发时，给键盘和触屏提供同一命令入口。

## 取用示例

`Menu(anchor=fileMore, items=[重命名,移动到,删除], open=menuOpen, onChoose=runFileCommand, onDismiss=closeMenu)`。

[本地规格令牌](../assets/tokens/menus.json) · [官网概览](https://m3.material.io/components/menus/overview) · [规格](https://m3.material.io/components/menus/specs) · [指南](https://m3.material.io/components/menus/guidelines) · [无障碍](https://m3.material.io/components/menus/accessibility)
