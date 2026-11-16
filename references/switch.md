# 开关 · Switch

立即启停一个独立设置，例如开启通知。需要在整张表单末尾统一确认的多项选择，通常用 checkbox 更清楚。

## 组件契约

`Switch(label, checked, onChange)`。轨道、滑块和可选的滑块图标共同表现开关；稳定标签描述设置本身。

点击或系统支持的拖动改变一个布尔值；触发一次变更。远端保存的结果在设置行反馈，状态与实际生效值保持一致。

## 动效与输入

滑块移动或变形走 fast spatial，轨道颜色走 fast effects。减少动效时直接到终点，位置、图标或文字仍能区别两态。

适配桌面键盘 Space；Web 可用原生 checkbox 结合 switch 语义，读屏报告开/关。整行和控件共享同一次切换，避免标签点击导致二次翻转。

## 取用示例

`Switch(label="桌面通知", checked=settings.notifications, onChange=updateNotifications)`。

[本地规格令牌](../assets/tokens/switch.json) · [官网概览](https://m3.material.io/components/switch/overview) · [规格](https://m3.material.io/components/switch/specs) · [指南](https://m3.material.io/components/switch/guidelines) · [无障碍](https://m3.material.io/components/switch/accessibility)
