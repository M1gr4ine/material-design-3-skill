# 悬浮操作按钮 · Floating action button / FAB

突出当前页面最重要或最常用的动作，例如在文件库中新增文件。若一个图标无法说明动作，取带文字的 extended FAB。

## 组件契约

`Fab(icon, accessibleName, onActivate, size)`。当前推荐 FAB、medium FAB、large FAB；旧 small FAB 和 surface 配色属于基线选择。让它在滚动时保持可达。

窄窗口常放在底部尾侧，避开底栏及系统区域。宽窗口可移入前侧导航轨，或靠近其作用的内容窗格。预留滚动尾部空间，以便最后一行操作仍可达。

## 动效与输入

同一动作开详细流程可用容器变换。跨页面仅在新页面仍有相应动作时出现。减少动效用就地重点标记或短淡变。

Web/桌面让它进入相关任务的焦点顺序，命名描述动作（如「新建文件」）。拖动窗口或切换布局时保留同一命令。

## 取用示例

`Fab(icon=add, accessibleName="新建文件", onActivate=createFile, size=medium)`。

[本地规格令牌](../assets/tokens/floating-action-button.json) · [官网概览](https://m3.material.io/components/floating-action-button/overview) · [规格](https://m3.material.io/components/floating-action-button/specs) · [指南](https://m3.material.io/components/floating-action-button/guidelines) · [无障碍](https://m3.material.io/components/floating-action-button/accessibility)
