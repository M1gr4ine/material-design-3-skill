# 标签控件 · Chips

Assist 执行上下文动作；filter 切换筛选；input 表示已输入的实体（例如收件人）；suggestion 提供下一步建议。先选语义再决定胶囊外形。

## 组件契约

`Chip(label, kind, onActivate?, selected?, onRemove?)`。可有前置符号或头像、输入标签的移除入口、筛选选中标记。默认低层级，背景复杂时可提升分离度。

筛选改变条件并保持选择，建议被接受后交给对应流程，删除 input chip 只移除该实体。同类筛选使用可读组名，标签溢出时提供滚动或换行。

## 动效与输入

选择着色和标记走 fast effects；删除或插入引发布局变化时可用局部 spatial。减少动效保持阅读与焦点顺序。

Web 筛选可用切换按钮或原生选择语义；普通建议用按钮。可删除实体的移除操作独立命名，例如「移除王林」，删除后焦点去相邻实体或输入框。

## 取用示例

`Chip(kind=filter, label="仅看我负责的", selected=filters.mine, onActivate=toggleMine)`。

[本地规格令牌](../assets/tokens/chips.json) · [官网概览](https://m3.material.io/components/chips/overview) · [规格](https://m3.material.io/components/chips/specs) · [指南](https://m3.material.io/components/chips/guidelines) · [无障碍](https://m3.material.io/components/chips/accessibility)
