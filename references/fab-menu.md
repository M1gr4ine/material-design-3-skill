# 悬浮操作菜单 · FAB menu

当一个主动作有 2–6 个密切相关的入口，可从一个普通 FAB 展开。适合「新建」的多种内容类型；带文字的 extended FAB 与这个菜单分开选用。

## 组件契约

`FabMenu(trigger, actions, expanded, onChoose)`。一列带图标和标签的动作，打开后原 FAB 变为关闭按钮；同一菜单尺寸可配多种 FAB。主要、次要、第三色系均有对应令牌。

打开首先保留焦点在原位的关闭按钮，随后可依次访问从上到下的菜单项。单次选择执行一个命令；Escape、关闭按钮或平台返回撤收。

## 动效与输入

从主按钮附近展开相关动作，关闭后收回原位。反向操作直接改变当前展开目标。减少动效保留按钮和操作列表的空间关系。

宽屏保证菜单不会完全遮住其他可操作元素的焦点。触屏动作可用点击，读屏能获每项名称以及发起按钮的展开状态。

## 取用示例

`FabMenu(trigger="新建", actions=[文档,表格,文件夹], expanded=isOpen, onChoose=createItem)`。

[本地规格令牌](../assets/tokens/fab-menu.json) · [官网概览](https://m3.material.io/components/fab-menu/overview) · [规格](https://m3.material.io/components/fab-menu/specs) · [指南](https://m3.material.io/components/fab-menu/guidelines) · [无障碍](https://m3.material.io/components/fab-menu/accessibility)
