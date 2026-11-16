# 复选框 · Checkbox

为可分别选中的项目或要随表单一起提交的选项提供勾选框。树节点或「全选」可显示部分选中。

## 组件契约

`Checkbox(label, checked, onChange)`；父级状态可为 `unchecked / mixed / checked`。统计可选子项生成父级显示值，用户点父级时对这一组执行产品定义的全选动作。

点控件或相邻关联标签均切换一次。选中用勾，部分选中用横线；必选协议或出错项目就近呈现说明。

## 动效与输入

用 fast effects 过渡勾号、横线和填充色。

Web 使用命名的 checkbox，原生 input 的 `indeterminate` 是独立显示属性；提交值由实际选中数据决定。桌面和外接键盘用 Space 切换当前项。

## 取用示例

`Checkbox(label="全选当前页", checked=selectionState(visibleRows), onChange=selectVisibleRows)`。

[本地规格令牌](../assets/tokens/checkbox.json) · [官网概览](https://m3.material.io/components/checkbox/overview) · [规格](https://m3.material.io/components/checkbox/specs) · [指南](https://m3.material.io/components/checkbox/guidelines) · [无障碍](https://m3.material.io/components/checkbox/accessibility)
