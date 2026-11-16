# 列表 · Lists

便于浏览、寻找、选择或操作一组同类项目。Standard 连续排列，segmented 通过容器和间距表达组；1–3 行文字可配前置媒体和尾端操作。

## 组件契约

`List(items, key, itemContent, onActivate?, selection?)`。稳定 ID 绑定焦点、选择及展开状态；标题/辅助文字保持层级。按需加入分组、展开收起、排序或滑出操作。

行打开详情和勾选行是两种行为。若尾部有独立操作，让它不会连带激活整行。窄窗用逐层导航；宽窗可在列表旁显示所选项详情，切换宽度保留对象 ID。

## 动效与输入

焦点/选中可改变形状和容器色；展开从所属项起。拖动排序贴手，释放后安放；为滑动/拖动提供更多菜单或移动命令。减少动效时直接更新并说明新位置。

浏览资料映射到原生列表/列表链接，多选才使用多选控件语义。桌面键盘可到达行内动作；虚拟化列表用稳定键以便焦点落到同一数据项。

## 取用示例

`List(items=documents, key=document.id, itemContent=[title,modifiedAt,more], onActivate=openDocument)`。

[本地规格令牌](../assets/tokens/lists.json) · [官网概览](https://m3.material.io/components/lists/overview) · [规格](https://m3.material.io/components/lists/specs) · [指南](https://m3.material.io/components/lists/guidelines) · [无障碍](https://m3.material.io/components/lists/accessibility)
