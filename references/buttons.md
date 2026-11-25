# 按钮 · Buttons

流程末尾的「保存」可用 filled。次要操作可用 tonal 或 outlined，辅助操作用 text；背景花纹影响按钮辨识时可用 elevated。普通按钮执行命令，toggle 按钮记录可切换的选择。

## 组件契约

`Button(label, onActivate)`；切换型绑定 `selected` 与 `onSelectedChange`。可选前置图标。五种大小 XS / S / M / L / XL，搭配圆形端头或方圆角。用项目主题对应的容器、前景、字阶和状态层角色。

默认、悬停、键盘聚焦、按下分别表现；切换型松开后仍显示选中。根据本页动作层级分配强调色，按钮宽度容纳翻译后的完整动词。

## 动效与输入

Expressive 可随按压改变轮廓，切换后用形状和颜色表明选择。轮廓用 fast spatial，着色用 fast effects。Web CSS 做圆角形变时，满圆态须用实际短边一半的精确 `px`（如 40 px 高取 `20px`）而非 `9999px`（避免 `fast spatial` 过冲钳制为 `0px` 直角），且 `:active` 只改目标属性、不覆写 `transition` 简写。

Web 的普通动作使用原生 button，表单提交才用 submit；切换按钮暴露 `aria-pressed`。若用 `position: absolute` 伪元素绘制按钮底框、选中容器或状态层，宿主须设 `isolation: isolate`、背景伪元素设 `z-index: -1`，防止盖住按钮内的直接文本或图标。桌面命令和触屏点击接入同一动作，图标随标签一起命中。

## 取用示例

`Button(label="导出", style=filled, onActivate=exportSelection)`；同一行的「取消」可用 text。

[本地规格令牌](../assets/tokens/buttons.json) · [官网概览](https://m3.material.io/components/buttons/overview) · [规格](https://m3.material.io/components/buttons/specs) · [指南](https://m3.material.io/components/buttons/guidelines) · [无障碍](https://m3.material.io/components/buttons/accessibility)
