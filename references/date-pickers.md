# 日期选择器 · Date pickers

点日历选日期、起止区间或直接录入已知日期。Docked 贴近触发字段；模态日历适合集中选择；modal input 用文本输入，适合熟知目标日期的用户。

## 组件契约

`DatePicker(value, mode, minDate?, maxDate?, onConfirm, onDismiss)`。区分今天、焦点日、选中日以及区间端点。用项目的本地日期类型保存无时刻的日历日。

模态打开时从已确认值建本次草稿；翻月、改年、切换输入方式都保留草稿。确认写回，取消保留旧值。解析按显示地区格式，清楚标明可选范围与禁选日。

## 动效与输入

选择日的填充、月份切换用轻量反馈；弹层从锚点或视口进入。减少动效时同步更新月份名称、焦点日期和选中标记。

宽窗可停靠，紧凑窗用模态或全屏范围选择。Web 原生 date 有平台外观；自制日历应支持箭头逐日/周移动、键盘确定以及弹窗焦点返回。

## 取用示例

`DatePicker(mode=range, value=report.period, onConfirm=applyReportPeriod, onDismiss=closePicker)`。

[本地规格令牌](../assets/tokens/date-pickers.json) · [官网概览](https://m3.material.io/components/date-pickers/overview) · [规格](https://m3.material.io/components/date-pickers/specs) · [指南](https://m3.material.io/components/date-pickers/guidelines) · [无障碍](https://m3.material.io/components/date-pickers/accessibility)
