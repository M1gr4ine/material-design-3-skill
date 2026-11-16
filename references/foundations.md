# 设计原则与主题

## 从任务建立视觉层级

先写下用户在这一页最想完成的一件事。例如文件库希望用户找回文档，就把可辨认的搜索入口放在文件列表附近，编辑工具留在打开文档的工作区。需要引导注意力时，先调整位置、尺度、分组和文字，再为重点动作分配颜色或形变。Expressive 的颜色、字体、包容形状和动效可以单独采用；高频专业操作更重视稳定的位置与反馈速度。[M3 可用性](https://m3.material.io/foundations/usability/applying-m3-expressive)

比较方案时观察用户能否找到入口、辨别当前选择、理解操作结果。一次删档用清晰的动作名和确认，成功归档用可撤销反馈；两者的严重程度决定组件。品牌风格可由配色、字形和形状表达，表单验证与导航含义贯穿整套主题。[设计可用性](https://m3.material.io/foundations/usability/overview) · [自定义](https://m3.material.io/foundations/customization)

## 从角色生成主题

| 设计决定 | 落地 |
| --- | --- |
| 强调主要操作 | 高强调容器用 `primary` 搭配 `on-primary`；较温和的强调使用对应 container/on-container。一个任务区域内给最重要的动作最高视觉权重。 |
| 组织表面 | 正文用 `surface/on-surface`，不同分组从 surface-container 系列选择。次级正文、轮廓、遮罩和浮层都有各自角色。 |
| 报错与选中 | 将 error 与对应前景配对，给出可操作的文字。选中态同时使用标记、轮廓、位置或语义状态，保留不同色觉下的可辨识性。 |
| 支持亮暗与个性化 | 固定品牌色可从品牌种子生成一对主题；支持系统动态色的平台可用用户或内容来源生成色板。切换时重取全部语义角色。 |
| 对接设计令牌 | 例如 `md.comp.search-bar.container.color → md.sys.color.surface-container-high → 当前主题值`。主题决定品牌色，组件决定用途。 |

离线文件提供 50 个浅色及 50 个深色 Web 基线颜色角色。产品已有品牌主题时继续使用其角色。用实际前/背景色对测对比度；普通文本按 4.5:1、大文本按 3:1，识别控件和状态所需的非文本信息按 3:1 核对。[离线色表](../assets/baseline-colors.json) · [配色角色](https://m3.material.io/styles/color/roles) · [选用配色方案](https://m3.material.io/styles/color/choosing-a-scheme) · [色彩对比](https://m3.material.io/foundations/designing/color-contrast)

## 排版、形状与间距

- **字阶。** 五类角色各有大中小。display 用于高强调短文，headline 是页级题名，title 给工具区/卡片标题，body 给内容，label 给控件。15 个基线字阶对应 15 个 emphasized 样式，适合选中项或关键数字。系统字号、翻译及中文字体回退应保留层级。离线表给出字体、字号、字重、行高、字距。[字阶数据](../assets/type-scale.json) · [字阶规范](https://m3.material.io/styles/typography/type-scale-tokens)
- **间距。** 区分父容器 padding、子项间 gap 与容器外 margin。官方以 `space100 = 8 dp` 表示基本单位，也有 2/4/6 dp 等细分；搜索栏聚焦时改变 margin，图标和文字内部仍有自己的间距。紧凑桌面优先缩短留白，混合输入保留触摸目标。[间距系统](https://m3.material.io/styles/spacing/tokens)
- **形状。** 角色从 0、4、8、12、16、20、28、32、48 dp 到 full；大小与形状可分别选。用同族轮廓提示对象相关性，用轮廓变化表示按下或选中。35 个表达性形状适用于需要突出的位置，例如加载过程中的形变；文字输入的边框以识别和稳定为先。[圆角尺度](https://m3.material.io/styles/shape/corner-radius-scale) · [形变](https://m3.material.io/styles/shape/shape-morph)
- **海拔。** 级别 0–5 对应 0、1、3、6、8、12 dp。用表面色、遮挡关系，必要时配阴影表达层叠。菜单需要与锚点区分，静态分组首先考虑留白与表面色。[海拔](https://m3.material.io/styles/elevation/overview)
- **图标与状态。** 对齐图标的可见边界与实际命中面积，采用一致的符号风格。默认、悬停、聚焦、按下、拖动属于交互反馈；选中、错误、忙碌属于内容或任务状态。按下松手后，数据决定哪项继续显示选中。键盘焦点环要能独立辨识。[图标](https://m3.material.io/styles/icons/applying-icons) · [状态层](https://m3.material.io/foundations/interaction/states/state-layers)
