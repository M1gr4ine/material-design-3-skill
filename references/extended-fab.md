# 扩展悬浮操作按钮 · Extended FAB

当主操作需要简短动词才能辨认时，直接显示标签。宽窗口导航轨头部的「写邮件」是典型位置。

## 组件契约

`ExtendedFab(label, icon?, expanded, onActivate)`。当前款式 small / medium / large，高度分别为 56 / 80 / 96 dp。原基线 extended FAB 在新设计中对应 small extended FAB。

展开态保留短标签，具备清晰图标时可随滚动收缩成 FAB。收缩和展开共享同一命令、可访问名称和焦点；纯文字入口应保留可识别内容。

## 动效与输入

轮廓与宽度用 spatial，文字显隐用 effects。反向滚动时从当前位置转向新目标。

触屏给按钮预留安全边距；桌面/键盘用户在按钮有焦点时仍能操作。多语言版本根据标签宽度和窗格空间选择尺寸。

## 取用示例

`ExtendedFab(label="写邮件", icon=edit, expanded=railExpanded, onActivate=composeMessage)`。

[本地规格令牌](../assets/tokens/extended-fab.json) · [官网概览](https://m3.material.io/components/extended-fab/overview) · [规格](https://m3.material.io/components/extended-fab/specs) · [指南](https://m3.material.io/components/extended-fab/guidelines) · [无障碍](https://m3.material.io/components/extended-fab/accessibility)
