# 加载指示器 · Loading indicator

用于估计较短、无法计量的真实工作，官网以约五秒内为典型。Default 可直接置于表面，contained 适合复杂背景和下拉刷新。若稍后会有百分比，取可切换模式的 progress indicator。

## 组件契约

`LoadingIndicator(busy, accessibleLabel, contained)`。活动形状可在七种轮廓间循环；默认整体 48 dp、形状容器 38 dp。显示周期绑定请求或任务生命周期。

下拉刷新越过阈值并释放才开始，反向退回阈值内可取消手势。下载完成、失败或取消后让指示结束，并展示对应结果。

## 动效与输入

加载期间可循环形变，并随刷新手势产生直接反馈。减少动效改用静态图形和「正在刷新」状态；读屏只在工作状态改变时播报。

网页和桌面为同一操作提供刷新按钮；为忙碌内容标记 busy 或相应原生状态。已有数字进度时让用户看到真实数值。

## 取用示例

`LoadingIndicator(busy=refresh.inFlight, accessibleLabel="正在刷新项目列表", contained=true)`。

[本地规格令牌](../assets/tokens/loading-indicator.json) · [官网概览](https://m3.material.io/components/loading-indicator/overview) · [规格](https://m3.material.io/components/loading-indicator/specs) · [指南](https://m3.material.io/components/loading-indicator/guidelines) · [无障碍](https://m3.material.io/components/loading-indicator/accessibility)
