# 离线令牌 · Tokens

组件页是决策入口，JSON 是实现时查的值，[tokens.css](../assets/tokens.css) 是 Web 项目的即用样式表。每个组件有独立文件，例如 [搜索](../assets/tokens/search.json)、[工具栏](../assets/tokens/toolbars.json)。用任何语言的 JSON 读取器读取 `tokens` 字典即可。

## 命令行离线查询（Python 3 标准库）

在技能根目录运行以下命令；省略组件名会列出全部 ID 和中英文名称。支持中英文名称、单复数及常见别名（如 `button`、`menu`、`modal`、`toast`、`搜索条`、`弹窗`）：

```sh
python scripts/component.py                                              # 列出全部 36 个组件
python scripts/component.py 搜索条                                        # 读取组件设计卡
python scripts/component.py search --token search-bar.container.height   # 查原始组件令牌
python scripts/component.py search --token search-bar.container --resolve --theme light
python scripts/component.py --token floating.standard.container.color    # 跨全部 36 个组件全局搜索
python scripts/component.py --sys surface-container                      # 查系统颜色/间距/圆角/字阶/动效
python scripts/component.py --sys fast.spatial --motion expressive       # 查指定动效方案参数
```

自定义品牌主题与 WCAG 2.1 对比度核验（纯标准库实现 Google HCT 色彩空间）：

```sh
python scripts/theme.py --seed "#1A73E8" --format css                    # 生成浅深色 CSS 变量
python scripts/theme.py --seed "#1A73E8" --variant expressive --format tailwind
python scripts/theme.py --seed "#1A73E8" --contrast high --format compose
python scripts/theme.py --seed "#1A73E8" --format flutter
python scripts/theme.py --seed "#1A73E8" --audit                         # 校验 18 组浅深色对比度
python scripts/theme.py --pair "#1d1b20" "#fef7ff"                       # 校验任意双色对比度
```

## 令牌值结构说明

| 读到什么 | 怎么用 |
| --- | --- |
| `"md.comp.search-bar.container.color": "md.sys.color.surface-container-high"` | 字符串是别名。在项目主题按同名系统角色取值；加上 `--resolve` 可直接展开到具体值（浅色 `#ece6f0`、深色 `#2b2930`）。 |
| `"md.comp.search-bar.container.height": {"length":{"value":56,"unit":"DIPS"}}` | `56` 是逻辑长度。Web 按 CSS 逻辑尺寸、桌面按设备无关单位、Android 按 dp 接入，字体单位单独随用户缩放。 |
| `"md.comp.search-bar.contained.motion.spring": "md.sys.motion.spring.fast.spatial"` | 在当前 scheme 的 `schemes[scheme][token]` 查阻尼比、刚度；`web` 字段给出无需中途打断的曲线近似。 |
| `byContext` | 匹配项目的条件组合。例如 switch 的 iOS 深色轨道可按对比度取覆盖值，第三方应用（3P）取 `Audience=3P`，其余上下文使用 `default`。 |
| `type`、`shape`、`opacity` | 复合字体含各属性的角色名，形状含轮廓族和边角，透明度为 0–1。遇到 `md.comp.…` 别名沿组件令牌继续查，或传 `--resolve` 自动递归展开。 |

## 离线系统令牌文件

- [tokens.css](../assets/tokens.css)：从下述 JSON 生成的完整 Web CSS 变量（颜色浅深色 + `[data-theme]` 切换、18 级间距、基线与 Expressive 圆角、0–5 海拔阴影、状态层与焦点环、30 个字阶含中文回退）。
- [baseline-colors.json](../assets/baseline-colors.json)：第三方 Web 产品在默认对比度下的 50 个浅色 + 50 个深色基线，原语色值在 `referenceTones`。
- [type-scale.json](../assets/type-scale.json)：30 个静态基线与强调字阶，prominent 字重在 `weights`。
- [metrics.json](../assets/metrics.json)：间距、形状、海拔和状态层。
- [motion.json](../assets/motion.json)：12 种弹簧及其 Web 近似值，单独引用的刚度或阻尼比按 `scalarSuffixes` 映射。

官方网页使用的文档数据版本为 2026-10-13，于 2026-11-16 对照站点地图。36 个组件专题对应 144 个规范页签。每个规格文件带官方 URL；多个专题可共用按钮或搜索等底层令牌，去重后共 5,091 个组件令牌名。All buttons 是跨组件选型总览。更新时查组件页的 Specs 和更新说明，再比较同名令牌与变体用途。[设计令牌](https://m3.material.io/foundations/design-tokens/overview) · [官方站点地图](https://m3.material.io/sitemap.xml) · [按钮总览](https://m3.material.io/components/all-buttons)
