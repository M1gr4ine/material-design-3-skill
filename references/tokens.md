# 离线令牌 · Tokens

组件页是决策入口，JSON 是实现时查的值。每个组件有独立文件，例如 [搜索](../assets/tokens/search.json)、[工具栏](../assets/tokens/toolbars.json)。用任何语言的 JSON 读取器读取 `tokens` 字典即可。需要从命令行查找时，在技能根目录运行以下命令；省略组件名会列出全部 ID 和中英文名称。

```text
python scripts/component.py 搜索条
python scripts/component.py search --token md.comp.search-bar.container.height
python scripts/component.py toolbars --token md.comp.toolbar.floating.standard.container.color
python scripts/component.py switch --token selected.track.color
```

| 读到什么 | 怎么用 |
| --- | --- |
| `"md.comp.search-bar.container.color": "md.sys.color.surface-container-high"` | 字符串是别名。在项目主题按同名系统角色取值；离线 Web 基线的该角色为浅色 `#ece6f0`、深色 `#2b2930`。 |
| `"md.comp.search-bar.container.height": {"length":{"value":56,"unit":"DIPS"}}` | 56 是逻辑长度。Web 按 CSS 逻辑尺寸、桌面按设备无关单位、Android 按 dp 接入，字体单位单独随用户缩放。 |
| `"md.comp.search-bar.contained.motion.spring": "md.sys.motion.spring.fast.spatial"` | 在当前 scheme 的 `schemes[scheme][token]` 查阻尼比、刚度；`web` 字段给出无需中途打断的曲线近似。 |
| `byContext` | 匹配项目的条件组合。例如 switch 的 iOS 深色轨道可按对比度取覆盖值，其余上下文使用 `default`。 |
| `type`、`shape`、`opacity` | 复合字体含各属性的角色名，形状含轮廓族和边角，透明度为 0–1。遇到 `md.comp.…` 别名沿组件令牌继续查。 |

[颜色](../assets/baseline-colors.json) 提供第三方 Web 产品在默认对比度下的浅色与深色基线，原语色值在 `referenceTones`。[字体](../assets/type-scale.json) 提供 30 个静态基线与强调字阶，prominent 字重在 `weights`。[度量](../assets/metrics.json) 包含间距、形状、海拔和状态层。[动效](../assets/motion.json) 提供 12 种弹簧及其 Web 近似值，单独引用的刚度或阻尼比按 `scalarSuffixes` 映射。

官方网页使用的文档数据版本为 2026-10-13，于 2026-11-16 对照站点地图。36 个组件专题对应 144 个规范页签。每个规格文件带官方 URL；多个专题可共用按钮或搜索等底层令牌，去重后共 5,091 个组件令牌名。All buttons 是跨组件选型总览。更新时查组件页的 Specs 和更新说明，再比较同名令牌与变体用途。[设计令牌](https://m3.material.io/foundations/design-tokens/overview) · [官方站点地图](https://m3.material.io/sitemap.xml) · [按钮总览](https://m3.material.io/components/all-buttons)
