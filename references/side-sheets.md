# 侧边面板 · Side sheets

在正文旁提供所选对象的属性、筛选或预览。Standard 与主任务并行，modal 在空间不足或需要集中操作时覆盖正文。侧面板承载上下文信息，导航轨承载目的地。

## 组件契约

`SideSheet(title, content, modality, open, onClose)`。通常从尾侧出现，带标题和可操作的关闭入口；内部有下层内容时可提供面板内返回。标准面板可与正文并排或按布局覆盖。

空间充足时修改属性可同时观察正文；空间收窄可转为模态或底部面板。保留选择对象、筛选草稿和必要的滚动位置。

## 动效与输入

面板从所属边缘进入。并排布局随面板宽度调整正文，模态布局让遮罩独立淡入。

非模态用命名区域，允许 Tab 返回正文；模态面板可用具名 dialog 管理背景、焦点与 Escape。RTL 跟随布局语义，避免覆盖起始侧导航入口。

## 取用示例

`SideSheet(title="文件属性", content=details(selectedFile), modality=twoPane ? standard : modal, open=showDetails, onClose=hideDetails)`。

[本地规格令牌](../assets/tokens/side-sheets.json) · [官网概览](https://m3.material.io/components/side-sheets/overview) · [规格](https://m3.material.io/components/side-sheets/specs) · [指南](https://m3.material.io/components/side-sheets/guidelines) · [无障碍](https://m3.material.io/components/side-sheets/accessibility)
