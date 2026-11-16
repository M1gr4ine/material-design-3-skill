# 底部面板 · Bottom sheets

紧凑或中等窗口的补充内容与短任务。Standard 允许操作原页面，modal 通过遮罩集中处理面板中的任务。

## 组件契约

`BottomSheet(content, modality, detents, position, onDismiss)`。上方可有拖动把手；模态有遮罩。官网给出的最大宽度为 640 dp，更宽的产品可评估改为侧面板。

拖动在允许的高度间移动；点击把手或单独按钮也能循环可用高度。模态支持关闭按钮/返回或适用的遮罩关闭；将内层滚动和面板拖动分别处理。

## 动效与输入

面板沿底边移动，拖动中与指针同步，松手后用速度和位置决定停靠点。面板空间与遮罩透明度使用独立通道；减少动效时可直接停靠。

模态中约束焦点并在关闭后回到入口；非模态可以继续访问正文。为调节把手命名并提供 48 dp 命中区域，桌面用键盘也可展开或收起。

## 取用示例

`BottomSheet(content=shareActions, modality=modal, detents=[partial,full], position=sheetPosition, onDismiss=returnToFile)`。

[本地规格令牌](../assets/tokens/bottom-sheets.json) · [官网概览](https://m3.material.io/components/bottom-sheets/overview) · [规格](https://m3.material.io/components/bottom-sheets/specs) · [指南](https://m3.material.io/components/bottom-sheets/guidelines) · [无障碍](https://m3.material.io/components/bottom-sheets/accessibility)
