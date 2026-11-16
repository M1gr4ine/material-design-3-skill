# 标签页 · Tabs

呈现同一上下文中的同级内容；一级标签分大类，二级标签细分已有类别。数量或翻译长度超出宽度时可横向滚动。

## 组件契约

`Tabs(items, activeId, onSelect, level, layout)`。每项关联唯一面板；primary / secondary 可搭配 fixed / scrollable。指示器和文字都能表现活动项。

固定标签平分合适的宽度；可滚动布局把当前项滚入可见区。切换保留各面板合适的视图状态。若内容延迟明显，键盘移动焦点后用 Enter/Space 激活。

## 动效与输入

同级页签按顺序切换时用 lateral 转场，内容沿一个轴移动，指示器跟随当前项。

Web 的页内面板用 tablist、tab、tabpanel 和配对 ID，方向键切同组焦点，Tab 进入面板。桌面原生 tab 控件保留其键盘行为；移动端滑动只是触发方式之一。

## 取用示例

`Tabs(items=[概览,活动,成员], activeId=panel, onSelect=setPanel, level=primary, layout=scrollable)`。

[本地规格令牌](../assets/tokens/tabs.json) · [官网概览](https://m3.material.io/components/tabs/overview) · [规格](https://m3.material.io/components/tabs/specs) · [指南](https://m3.material.io/components/tabs/guidelines) · [无障碍](https://m3.material.io/components/tabs/accessibility)
