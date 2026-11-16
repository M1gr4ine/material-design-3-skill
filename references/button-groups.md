# 按钮组 · Button groups

一组密切相关的命令可用 standard；互有关联的选项可用 connected。将任务中的「执行命令」「单选」「多选」与视觉形状分别确定。新 Expressive 产品的分段选择可取 connected。

## 组件契约

`ButtonGroup(items, layout, selectionMode, value, onChange)`。项目可用文字、图标按钮；每项有稳定 ID。按业务设单选是否必须有值，按钮组也可持有互相独立的命令。

组内共享尺寸。标准组保留项目之间的间隔，连接组使用连续外轮廓与内部小间隔。宽度不足时确保标签可读，使用产品所需的溢出入口。

## 动效与输入

标准组按压会改变当前项及邻项宽度；连接组按压主要改变当前项形状。用 fast spatial，并让整个组的外部布局稳定。减少动效时直接显示选中项。

单选可取原生 radio group，多选可用分别命名的切换按钮。读屏可获组名和选中值，键盘行为遵从所选控件语义。

## 取用示例

`ButtonGroup(items=[步行,骑行,驾车], layout=connected, selectionMode=singleRequired, value=routeMode, onChange=setRouteMode)`。

[本地规格令牌](../assets/tokens/button-groups.json) · [官网概览](https://m3.material.io/components/button-groups/overview) · [规格](https://m3.material.io/components/button-groups/specs) · [指南](https://m3.material.io/components/button-groups/guidelines) · [无障碍](https://m3.material.io/components/button-groups/accessibility)
