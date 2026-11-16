# 窗口、输入与布局

## 选择当前窗口的布局

按应用实际可用宽度选择布局。手机分屏、桌面窄窗、网页放大后都可能进入 compact。M3 的范围以逻辑 dp 表达；Web 用 CSS 布局视口或特定容器的逻辑尺寸，桌面取客户区的设备无关单位。窗格控件可单独按自身可用宽度调整。下表的页面组合是适配示例。[窗口规范](https://m3.material.io/foundations/layout/breakpoints/overview) · [自适应布局](https://m3.material.io/foundations/layout/layout-overview/adaptive-design)

| 窗口宽度 | 示例 |
| --- | --- |
| Compact，< 600 | 一次呈现列表或详情。3–5 个顶级目的地可用底部导航；搜索全屏，编辑命令靠近工作区。 |
| Medium，600–<840 | 根据业务给正文或辅助内容更多空间。可将搜索停靠，在导航栏与导航轨之间衡量目的地数量和剩余内容宽度。 |
| Expanded，840–<1200 | 导航轨、列表与详情可并排。编辑属性可用 standard side sheet，短浮动工具栏靠近所选对象。 |
| Large，1200–<1600 | 可展开导航轨，并固定一个工具或检查器窗格。正文和编辑画布各自限定可读宽度。 |
| Extra large，≥1600 | 高信息密度工作区可保留三个协作区域；表单与阅读内容继续使用适合其任务的行长。 |

## 选页面骨架

- **列表–详情。** 适合邮箱、文档和订单。将 `selectedId`、查询、筛选存放在页面状态；窄窗选择项后进入详情，宽窗更新相邻详情。宽窗缩回窄窗时保留当前任务和返回落点。[List-detail](https://m3.material.io/foundations/layout/canonical-examples/list-detail)
- **辅助窗格。** 文件属性、评论或图例只对当前对象有意义。宽窗放在主内容旁，窄窗可放在下方，或使用可关闭的面板。编辑草稿归属于对象，切换面板形态继续使用同一值。[Supporting pane](https://m3.material.io/foundations/layout/canonical-examples/supporting-pane)
- **信息流。** 图文集合可随容器宽度增加列数或重点卡片。保持阅读顺序与键盘顺序一致；图片按固有比例预留空间，减少加载跳动。[Feed](https://m3.material.io/foundations/layout/canonical-examples/feed)

## 输入与平台惯例

| 情境 | 实施决定 |
| --- | --- |
| 触屏/手写笔 | 触屏以约 48×48 dp 的可触区域为常用目标，视觉图标可更小。长按、拖动、滑出操作另提供可点按的入口。避开系统返回手势和软键盘。 |
| 鼠标与键盘 | 提供可见焦点、指针命中与键盘等价动作。右键菜单和快捷键复用同一命令。复合控件用方向键，Tab 在任务区域之间移动，文本框保留编辑键。 |
| 触控笔记本/外接键盘 | 输入能力与窗口宽度分别判定。同一宽度下，鼠标可见 hover、手指有足够触控面积，外接键盘可独立完成操作。 |
| 浏览器 | 地址和历史承载可导航目的地。缩放与文本重排后仍能访问主操作；用弹层时处理 Escape、滚动及焦点归还。 |
| 原生 PC 窗口 | 保留系统标题栏、窗口控制、命令菜单和原生文本编辑。首选贴近文档的搜索和工具栏，压缩窗口时把次要命令收入溢出区域。 |
| RTL / 大字 / 辅助技术 | 用 start/end 布局并只镜像有方向语义的图标。系统字号变大允许行高增长。模态层有名字并管理焦点，状态改变可通过辅助技术感知。 |

Web 的 WCAG 2.2 AA 目标大小准则是 24×24 CSS px 或满足其间距等例外；M3 的触摸建议属于另一项设计尺度。检查界面时分别使用目标平台的单位和输入方式。[M3 无障碍](https://m3.material.io/foundations/designing/overview) · [WCAG 目标尺寸](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) · [双向布局](https://m3.material.io/foundations/layout/bidirectionality-rtl)
