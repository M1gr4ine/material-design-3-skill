# 进度指示器 · Progress indicators

线形或圆形均可表示 determinate / indeterminate。已知工作量就展示真实比例，未知且之后会转为有进度时，从同一组件的不定模式过渡。轨道可选直线或波形。

## 组件契约

`ProgressIndicator(shape, mode, value?, label)`。当前值与总量来自任务；线形可显示终点标记。影响整页时放在相关内容边缘，局部任务放在对应项或按钮附近。

总量已知后将工作量映射为比例。成功、失败、取消各自结束忙状态；界面状态与后台结果一致。一个任务在转换模式时保持位置和名称。

## 动效与输入

有量进度跟随实际数值，不能用无限循环伪装百分比；不定进度可循环。减少动效去掉波浪和旋转，保留数字或明确状态文字。

Web 原生 progress 省略 value 表示不定；有量时提供 max/value 和可访问标签。桌面/移动端暴露等价范围语义，读屏按阶段或有意义的增量提示。

## 取用示例

`ProgressIndicator(shape=linear, mode=totalKnown ? determinate : indeterminate, value=uploadedFraction, label="正在上传报告")`。

[本地规格令牌](../assets/tokens/progress-indicators.json) · [官网概览](https://m3.material.io/components/progress-indicators/overview) · [规格](https://m3.material.io/components/progress-indicators/specs) · [指南](https://m3.material.io/components/progress-indicators/guidelines) · [无障碍](https://m3.material.io/components/progress-indicators/accessibility)
