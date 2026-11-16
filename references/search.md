# 搜索栏 · Search / Search bar

先确定搜索范围。查当前列表，把 search bar 放在该窗格附近；全产品搜索是主任务时用 search app bar；偶尔使用的搜索可以从图标进入。

## 组件契约

`Search(query, suggestions, results, onQueryChange, onSubmit, onChoose, onDismiss)`。入口、可编辑查询、清除/返回、建议与结果各有独立职责。聚焦时可取 contained 或基线 divided 样式，二者都可全屏或停靠。

空输入可显示历史；输入后显示与当前查询对应的建议或结果。提交可进入结果页，清除保留编辑焦点。异步搜索若先发的请求后返回，按查询身份丢弃过期结果。中文输入法选词期间的 Enter 交给 IME。

## 动效与输入

Contained 栏高 56 dp，聚焦时外边距从 24 dp 缩至 12 dp。宽度变化用 spatial，内容显隐用 effects。

紧凑窗口用全屏搜索，宽窗用输入框下方的 docked 面板；关闭覆盖层时回到触发点。Web 的值建议用 combobox + listbox，输入持有焦点，上下键预览、Enter 接受、Esc 收起。可导航的搜索结果用链接列表；桌面支持鼠标、键盘和窗口内缩放。

## 取用示例

`Search(query=state.query, suggestions=recentProjects, results=matchingProjects, onSubmit=runSearch, onChoose=openProject)`。仅需本地列表过滤时，可直接在列表上方放带标签的搜索框并展示匹配数。

[本地规格令牌](../assets/tokens/search.json) · [官网概览](https://m3.material.io/components/search/overview) · [规格](https://m3.material.io/components/search/specs) · [指南](https://m3.material.io/components/search/guidelines) · [无障碍](https://m3.material.io/components/search/accessibility)
