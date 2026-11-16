# 时间选择器 · Time pickers

输入小时、分钟与适用时的 AM/PM。Dial 适合触摸选时，input 适合键盘精确输入；二者可在同一模态任务内切换。

## 组件契约

`TimePicker(localTime, clockFormat, entryMode, onConfirm, onDismiss)`。提供小时、分钟、制式、取消和确认。内部保存时间值，界面按偏好使用 12 / 24 小时制。

表盘先选时、再选分。模式切换保留同一草稿，确认只提交一次，取消还原。把当前选中的单位标清；间隔、跨时区预约由调用方处理。

## 动效与输入

表针跟随直接选择，输入面板更换时保留时分关系。减少动效直接更新指示与数值。

桌面默认可达的数字输入，允许 Tab 走完时、分和确认。触屏表盘给出足够大的目标，并提供输入替代；读屏能听到所选小时或分钟。

## 取用示例

`TimePicker(localTime=alarm.time, clockFormat=userClock, entryMode=keyboardPreferred ? input : dial, onConfirm=setAlarmTime, onDismiss=close)`。

[本地规格令牌](../assets/tokens/time-pickers.json) · [官网概览](https://m3.material.io/components/time-pickers/overview) · [规格](https://m3.material.io/components/time-pickers/specs) · [指南](https://m3.material.io/components/time-pickers/guidelines) · [无障碍](https://m3.material.io/components/time-pickers/accessibility)
