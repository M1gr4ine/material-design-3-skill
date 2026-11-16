# 工具提示 · Tooltips

Plain 解释图标或简短操作，rich 补充细节，可含标题、链接或动作。完成任务所必需的信息应能在常规界面获得。

## 组件契约

`Tooltip(anchor, text, variant, actions?, presentation)`。普通提示跟随锚点，空间不足时换侧；临时富提示和显式激活的持续富提示需要不同的关闭方式。

鼠标悬停或键盘聚焦可显示普通提示；触屏长按是补充入口。可交互的富提示支持显式触发、移入和关闭，离开锚点后仍有时间阅读。

## 动效与输入

在锚点附近快速出现/消失，避免弹跳或挡住当前焦点。减少动效用即时显隐。

Web 的 `role=tooltip` 用于非交互说明，通过 `aria-describedby` 关联触发器；含链接/按钮的富提示改用可聚焦的 popover 或非模态对话框。Escape 可关，关闭后可回到锚点。

## 取用示例

`Tooltip(anchor=historyButton, text="查看版本历史", variant=plain)`；引导用户查看帮助文章时可用带链接的 rich 版本。

[本地规格令牌](../assets/tokens/tooltips.json) · [官网概览](https://m3.material.io/components/tooltips/overview) · [规格](https://m3.material.io/components/tooltips/specs) · [指南](https://m3.material.io/components/tooltips/guidelines) · [无障碍](https://m3.material.io/components/tooltips/accessibility)
