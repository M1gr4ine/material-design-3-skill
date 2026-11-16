# 分裂按钮 · Split button

用户高频执行一个默认动作，又偶尔选择同类变体时使用。例如「发送」旁提供「定时发送」。

## 组件契约

`SplitButton(primaryLabel, onPrimary, options, onChoose)`。前段是带标签的普通按钮，尾段的箭头是独立菜单按钮。两段使用相同高度，可与旁边按钮共享 XS–XL 尺度。

主段直接执行默认命令；尾段只展开或收起菜单。选择菜单项执行该项，是否修改下次默认动作由产品定义。无选择地关闭时焦点回到尾段。

## 动效与输入

尾段箭头随菜单开合旋转，内侧轮廓随之改变。官网为箭头旋转指定 **standard** motion scheme。

两段各可聚焦。辅助名可用「发送」和「更多发送方式」，尾段暴露展开状态；键盘从菜单选择或 Escape 退回。Qt 的带分区菜单的工具按钮也能承担这份契约。

## 取用示例

`SplitButton(primaryLabel="发送", onPrimary=sendNow, options=[定时发送], onChoose=scheduleSend)`。

[本地规格令牌](../assets/tokens/split-button.json) · [官网概览](https://m3.material.io/components/split-button/overview) · [规格](https://m3.material.io/components/split-button/specs) · [指南](https://m3.material.io/components/split-button/guidelines) · [无障碍](https://m3.material.io/components/split-button/accessibility)
