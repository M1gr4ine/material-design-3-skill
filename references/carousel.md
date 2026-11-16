# 轮播 · Carousel

在同一方向浏览图片、视频等视觉内容。六种布局为 multi-browse、uncontained、uncontained multi-aspect ratio、hero、center-aligned hero、full-screen。需要同时比较多张选 multi-browse，聚焦一张选 hero，保留各原始比例选 multi-aspect。

## 组件契约

`Carousel(items, key, layout, activeId, onActivate)`。容器负责滚动、遮罩或吸附，项目负责媒体、可选标签和动作。可给集合标题配「查看全部」入口。

触摸拖动、滚轮/触控板或键盘都可浏览。用相邻项目的露出提示可继续浏览；宽窗调整可见数量。让焦点项目完整进入视口。

## 动效与输入

随滚动改变裁切与大小，视差只作用于媒体，主要内容仍可读。减少动效时移除视差、形变和装饰性自动滚动，保留手动浏览与选中反馈。

向读屏提供名称和「第几项/共几项」。若产品主动轮换，提供暂停控制并在键盘交互时停止；普通可滑动集合可保持静止。

## 取用示例

`Carousel(items=albums, key=album.id, layout=uncontainedMultiAspectRatio, activeId=current, onActivate=openAlbum)`。

[本地规格令牌](../assets/tokens/carousel.json) · [官网概览](https://m3.material.io/components/carousel/overview) · [规格](https://m3.material.io/components/carousel/specs) · [指南](https://m3.material.io/components/carousel/guidelines) · [无障碍](https://m3.material.io/components/carousel/accessibility)
