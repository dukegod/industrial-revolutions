# 工业革命与人类发展 - 从四轮工业革命推导人类发展的共通规律，并落到当下的 Agent 平台判断

静态 HTML + Markdown + Python 标准库（无框架、无构建步骤、无第三方依赖）

<directory>
wiki/ - 结论、机制与数据口径的权威来源（11 个 Markdown 条目 + 索引，结论唯一出处）
visualization/ - 自包含静态站点，11 个内容页 + 1 个旧页重定向 + assets/（图全部内联 SVG，媒体在 assets/）
scripts/ - 构建与校验工具（build.py 同步结构、verify.py 十一项校验、figures/ 出图与防漂移）
</directory>

<config>
README.md - 项目说明：目录结构、资源承载约定、站点页面表、版本记录
scripts/build.py - 站点结构登记表：导航分组、页脚顺序、页码前缀、旧文件名（内联声明）
scripts/figures/registry.py - 图形登记表：每张脚本生成的图在哪一页、用哪个生成器、按什么锚点定位
.github/workflows/pages.yml - GitHub Pages 部署：触发路径 visualization/**，发布根 visualization/
.gitignore - 忽略本地临时产物、图生成中间产物、媒体源件
</config>

## 资源承载约定（最高优先级，改动前必读）

站点的**图**一律由 `scripts/figures/` 生成并**内联进页面**，不引用外部位图。这样每张图都能被重新生成、被 `verify_embedded.py` 逐字比对，脚本改了页面没改会被立刻发现。

`visualization/assets/` 是唯一的例外目录，当前只有三类文件：`style.css`（全站唯一样式表）、`industrial-revolutions-720p.mp4`（开篇视频，AI 生成的示意演绎）、`industrial-revolutions-poster.jpg`（上一条的封面帧）。

**新增媒体资源的门槛**：图先进 `scripts/figures/registry.py` 登记；媒体必须明确写出它是例外并在页面中引用它。`scripts/verify.py` 同时检查 `src`/`poster` 可达与**孤儿资源** —— 放进 assets/ 却没人引用的文件会被直接报出来。媒体源件不入库，留在 `.tmp/stash/`。

**已入库的位图即技术债**：位图不可被脚本复现，无法进入防漂移体系，页面一改就与图失配。新增位图前先想清楚为什么它不能做成 SVG。

## 内容纪律

- 结论先落 `wiki/`，页面是表达不是来源。事实改动顺序：`wiki/` → `scripts/build.py` → `scripts/verify.py`
- 每一处数字与年代都要能核到出处；核不到就标「尚未定位」，**不猜**（见 `wiki/08-数据来源与口径.md`）
- 分期口径统一采用中国通行口径：18 世纪 60 年代 / 19 世纪 70 年代 / 20 世纪四五十年代 / 2010s
- 术语用「电子计算机」而非「电脑」
- AI 生成的媒体必须带**显式标识**，不能只靠文件里的隐式 AIGC 标记

Laws: minimal · stable · navigational · exact versions
