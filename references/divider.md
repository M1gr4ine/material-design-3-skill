# 分隔线 · Divider

当留白或标题不足以说明分组时使用。全宽分开主要区域，inset 与行内标题对齐，垂直线区分并排的命令组。

## 组件契约

`Divider(orientation, insetStart?, insetEnd?)`。绑定分隔线颜色/厚度令牌，基线厚度 1 dp。缩进使用逻辑起止方向。

把线画在组边界；相邻列表行已有容器或间距时可省略。纯分隔线不持有交互状态或输入焦点。

## 动效与输入

分隔线静态呈现，面板开合时随面板移动。

表达重要内容分段时，Web 可用 hr 或带方向的 separator。装饰线对读屏隐藏。可拖动改变两窗格大小的 splitter 需要自己的控件与键盘契约。

## 取用示例

`Divider(orientation=vertical)` 放在工具栏的「撤销/重做」组与「文字格式」组之间。

[本地规格令牌](../assets/tokens/divider.json) · [官网概览](https://m3.material.io/components/divider/overview) · [规格](https://m3.material.io/components/divider/specs) · [指南](https://m3.material.io/components/divider/guidelines) · [无障碍](https://m3.material.io/components/divider/accessibility)
