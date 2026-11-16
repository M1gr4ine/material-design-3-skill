# 单选按钮 · Radio button

从一组互斥选项中选一个，适合显示各项文字并进行比较。若是一个设置的开或关，取 switch。

## 组件契约

`RadioGroup(label, options, value, onChange)`；每项含 ID 和可见文字。组持有一个已选 ID；初始选择取业务已有值，允许未作答的表单可保留空选择。

改变选项同步撤销旧项；关联标签扩大可点击区域。若选择需要提交，将草稿保存在表单，并通过确认动作保存。

## 动效与输入

指示点与颜色由选中值驱动，用 fast effects 或静态切换。相邻项不因指示点变化而位移。

Web 用同 name 的原生 radio，组名用 fieldset/legend。Tab 进出组，方向键在选项间移动选择。桌面和手机读屏可获组名、项目名与选中状态。

## 取用示例

`RadioGroup(label="导出格式", options=[PDF,CSV,JSON], value=draft.format, onChange=setDraftFormat)`。

[本地规格令牌](../assets/tokens/radio-button.json) · [官网概览](https://m3.material.io/components/radio-button/overview) · [规格](https://m3.material.io/components/radio-button/specs) · [指南](https://m3.material.io/components/radio-button/guidelines) · [无障碍](https://m3.material.io/components/radio-button/accessibility)
