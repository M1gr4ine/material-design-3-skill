# 滑块 · Sliders

从有界范围中快速调整连续值或步进值。标准型表示单值，centered 以中点为基准，range 选择两个端点。需要精确输入时可并排提供数值框。

## 组件契约

`Slider(min, max, value, step?, onChange, onCommit?)`；范围滑块提供 low/high 各自的名称。支持横/竖方向、五种尺寸、离散刻度、值提示，较厚的轨道可内置图标。

拖动时立即预览值；有成本的操作可在松手确认。range 保持已显示的两端含义与可用范围一致，键盘可分别聚焦两个手柄。

## 动效与输入

拖动中手柄贴住指针，离散吸附在释放时发生；可承接释放速度。减少动效仍保留直接操控与值反馈。

Web 单值优先原生 range，方向键按步进调整，Home/End 到端点；为自定义/双手柄暴露名称、数值和单位。触屏点击或键盘输入均能到达可选值。

## 取用示例

`Slider(min=-12, max=12, step=1, value=gainDb, variant=centered, onChange=previewGain, onCommit=storeGain)`。

[本地规格令牌](../assets/tokens/sliders.json) · [官网概览](https://m3.material.io/components/sliders/overview) · [规格](https://m3.material.io/components/sliders/specs) · [指南](https://m3.material.io/components/sliders/guidelines) · [无障碍](https://m3.material.io/components/sliders/accessibility)
