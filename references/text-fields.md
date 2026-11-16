# 文本字段 · Text fields

收集可编辑文字。Filled 利于扫读一组输入，outlined 适用于需要明确字段边界的界面。持久标签说明字段含义，示例或占位文字提示格式。

## 组件契约

`TextField(label, value, onChange, supportingText?, error?, readOnly?)`。支持单/多行、前后缀、图标、计数。空值、输入、聚焦、只读、禁用和错误按实际状态呈现。

输入中保留光标、选区和组合文字。验证在负责该字段的边界进行；错误就近说明怎样修正，并保留原输入。只读内容仍可被选取、复制。

## 动效与输入

标签浮动和边框/指示线随焦点改变；颜色和透明度用 effects。减少动效时直接更新，不用晃动作为唯一报错方式。

Web 关联 label、说明和错误（如 `aria-describedby` 与 `aria-invalid`）。桌面保留复制粘贴、撤销和 IME；移动端按数据类型选择输入键盘。

## 取用示例

`TextField(label="工作邮箱", value=draft.email, onChange=setEmail, error=emailError, supportingText="用于接收审批通知")`。

[本地规格令牌](../assets/tokens/text-fields.json) · [官网概览](https://m3.material.io/components/text-fields/overview) · [规格](https://m3.material.io/components/text-fields/specs) · [指南](https://m3.material.io/components/text-fields/guidelines) · [无障碍](https://m3.material.io/components/text-fields/accessibility)
