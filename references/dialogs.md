# 对话框 · Dialogs

需要用户就一件事作出决定时使用。Basic 适合短说明或确认；复杂但完整的编辑任务在紧凑窗口可用 full-screen。一般成功提示可交给 snackbar。

## 组件契约

`Dialog(title, body, actions, open, onDismiss)`。基本型可有图标、正文、确认与取消；基线宽度 280–560 dp。全屏型通常在上栏提供退出和完成。

表单对话框区分草稿与已提交值；确认保存，取消保留原值。破坏性动作明确命名，例如「删除文件夹」；默认焦点按风险和内容选择。

## 动效与输入

从触发点或布局中心进入，背景遮罩独立变化。关闭动画不改变确认/取消结果；减少动效可用短淡变。

Web 原生 dialog 的 `showModal()`、桌面模态窗口或手机原生模态均可。提供可访问名称，约束模态焦点，Esc/返回按产品关闭规则执行；返回触发者被删除时移至下一个合理目标。

## 取用示例

`Dialog(title="删除「季度报告」？", body=impactSummary, actions=[cancel,deleteFolder], open=confirming, onDismiss=cancel)`。

[本地规格令牌](../assets/tokens/dialogs.json) · [官网概览](https://m3.material.io/components/dialogs/overview) · [规格](https://m3.material.io/components/dialogs/specs) · [指南](https://m3.material.io/components/dialogs/guidelines) · [无障碍](https://m3.material.io/components/dialogs/accessibility)
