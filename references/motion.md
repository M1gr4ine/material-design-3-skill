# 动效 · Motion

## 选机制、通道和速度

指针拖动期间由手势直接控制位置。松手或中途改变目标时，用能接收当前位置和速度的弹簧。普通按压、颜色或短暂显隐可直接使用组件的内建动效。网页上无需连续打断的变化，可以用官网给出的 CSS 曲线近似。页面转场另有六种模式，官网当前仍以 easing/duration 描述。[物理动效](https://m3.material.io/styles/motion/overview/how-it-works) · [弹簧与 Web 换算](https://m3.material.io/styles/motion/overview/specs) · [转场](https://m3.material.io/styles/motion/transitions/transition-patterns)

在产品主题上选 **expressive** 或 **standard**。前者的空间弹簧有较明显的回弹，后者适合高频工具与工作界面。通道和速度仍由具体属性决定。组件有专用令牌或明确行为时沿用它，例如 split button 的菜单箭头使用 standard。

| 场景 | 空间属性 spatial | 效果属性 effects |
| --- | --- | --- |
| fast，小范围反馈 | 开关滑块、按钮圆角、图标旋转 | 按压层、开关着色 |
| default，局部视区 | 面板位置、导航轨展开 | 面板内容或遮罩透明度 |
| slow，大面积变化 | 全屏容器尺寸或位置 | 全屏内容刷新 |

空间弹簧处理位置、尺寸、旋转、圆角。效果弹簧处理有边界的透明度或颜色；输出保持在合法范围。程序传入当前手势的初速度，静止启动时速度为零。对使用质量、刚度、阻尼系数的 API，取质量 `m=1`，从阻尼比 ζ 和刚度 k 换算 `c = 2ζ√(km)`。以秒计算速度；输入是 px/ms 时乘以 1000。Compose 一类 API 直接收阻尼比。[Android MotionScheme](https://developer.android.com/reference/kotlin/androidx/compose/material3/MotionScheme) · [Flutter SpringDescription](https://api.flutter.dev/flutter/physics/SpringDescription/SpringDescription.withDampingRatio.html)

| 方案 | fast spatial (ζ, k) | default spatial | slow spatial | fast / default / slow effects (ζ, k) |
| --- | --- | --- | --- | --- |
| expressive | 0.6, 800 | 0.8, 380 | 0.8, 200 | 1, 3800 / 1, 1600 / 1, 800 |
| standard | 0.9, 1400 | 0.9, 700 | 0.9, 300 | 1, 3800 / 1, 1600 / 1, 800 |

两套方案共 12 组数值，JSON 同时给出每组的官方 Web 近似曲线与时长。以上是本次官网数据中的通用弹簧；目标组件库已有相应 token 时，由库选择该设备的值。[动效数据](../assets/motion.json) · [Expressive 实现](https://github.com/androidx/androidx/blob/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/tokens/ExpressiveMotionTokens.kt) · [Standard 实现](https://github.com/androidx/androidx/blob/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/tokens/StandardMotionTokens.kt)

## 六种转场按关系选择

| 情境 | 模式与实施 |
| --- | --- |
| 点击卡片、图片或搜索框查看详情 | **Container transform**。共享同一对象的容器或主图，起点和终点明确。关闭时回原对象；原对象在列表外时可用简单退出。 |
| 进入下一层，再返回上一层 | **Forward / backward**。符合平台返回手势，方向与层级一致。桌面列表与详情已经并排时，更新详情区域即可。 |
| 标签页、相册等有顺序的同级内容 | **Lateral**。同组沿一个轴移动并支持反向操作。布局方向与实际内容顺序一致。 |
| 切换顶级目的地 | **Top level**。原内容先淡出，再淡入新目的地。导航选中态和地址随路由更新。 |
| 菜单、提示、面板出现或关闭 | **Enter / exit**。菜单从锚点展开，sheet 从所属边缘进入。空间与遮罩分别处理，允许在退出前再次展开。 |
| 等待版面结构可预知的数据 | **Skeleton loaders**。骨架预留与最终内容相近的区域，完成时内容原位出现。减少动效时静态占位，仍可获知加载中或错误。 |

基线 easing/duration 按路程和出入场选。短时长序列为 50/100/150/200 ms，中为 250/300/350/400 ms，长为 450/500/550/600 ms，特长为 700/800/900/1000 ms。Emphasized decelerate 适合入场，accelerate 适合离场；普通工具的短变化也可用 standard。大范围高频转场保留简单的主方向。[基线曲线与时长](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs) · [转场应用与减少动效](https://m3.material.io/styles/motion/transitions/applying-transitions)

## 取用代码

**Web 的非手势变化。** 引入 [motion.css](../assets/motion.css)，容器可设 `data-m3-motion="standard"`。例如改变说明文字的透明度；这套变量会响应系统的减少动效设置。

```css
.supporting-text {
  transition: opacity var(--m3-fast-effects-duration) var(--m3-fast-effects-curve);
}
```

**可打断的空间变化。** [spring.mjs](../assets/spring.mjs) 可以驱动面板偏移。拖动时调用 `slide.jump(offset)`，松手时调用 `slide.to(snapPoint, velocity)`，速度单位为 px/s。改用 `slide.to(newTarget)` 会承接当前速度。系统启用减少动效时直接定位，卸载面板时调用 `slide.dispose()`。

```js
import { createSpring } from "./spring.mjs";

const spec = motionTokens.schemes.standard["md.sys.motion.spring.default.spatial"];
const slide = createSpring(initialOffset, spec, offset => {
  sheet.style.transform = `translateY(${offset}px)`;
});
```

**原生框架。** Compose 从 `MaterialTheme.motionScheme` 取 `fastSpatialSpec()` 等槽位，手势用可承接速度的 Animatable。Flutter 自定义运动可用 `SpringDescription.withDampingRatio` 和 `SpringSimulation`。SwiftUI 读取 `accessibilityReduceMotion`；Windows 查看系统动画设置；Web 使用 `prefers-reduced-motion`。减少动效时移除视差、明显缩放、循环轮廓，保留静态状态、真实进度或短淡变；提交、关闭、焦点转移的业务结果独立于动画是否播放。[SwiftUI](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion) · [Flutter 动效偏好](https://api.flutter.dev/flutter/widgets/MediaQueryData/disableAnimations.html) · [Flutter 的 Reduce Motion](https://api.flutter.dev/flutter/widgets/MediaQueryData/reduceMotion.html)
