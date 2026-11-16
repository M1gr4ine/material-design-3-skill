# 短消息提示 · Snackbar

用于操作后与当前任务有关的简短反馈，例如完成归档并允许撤销。需立即决定或阻止继续的情况用 dialog 或就近错误。

## 组件契约

`Snackbar(message, action?, onAction?, onDismiss)`。通常位于窗口底部，避让 FAB、导航与系统区。显示一条，可用下一条替换已过时的状态。

含「撤销」等动作时保持直到操作或关闭。无动作消息可依平台自行消失，官网给出常见 4–10 秒；Web 采用自动消失时，在原操作附近同步保留结果。

## 动效与输入

靠近底边进入和退出，较新的提示沿用同一位置。减少动效可直接显示或短淡变；显示不抢走编辑焦点。

采用温和的状态播报，给操作和关闭提供键盘入口。将可撤销的业务动作绑定到对应数据项，以免先后多次归档时撤销错误对象。

## 取用示例

`Snackbar(message="已归档《报价单》", action="撤销", onAction=undoThisArchive, onDismiss=closeNotice)`。

[本地规格令牌](../assets/tokens/snackbar.json) · [官网概览](https://m3.material.io/components/snackbar/overview) · [规格](https://m3.material.io/components/snackbar/specs) · [指南](https://m3.material.io/components/snackbar/guidelines) · [无障碍](https://m3.material.io/components/snackbar/accessibility)
