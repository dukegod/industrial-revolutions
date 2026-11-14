# scripts/figures/
> L2 | Parent: ../CLAUDE.md

图形生成与防漂移体系。站点的每张脚本生成图都在这里有唯一出处：改脚本 → 重新生成 → 回写页面 → 逐字比对。页面里嵌的是副本，脚本产出的才是本体。

## 成员清单

`registry.py`: 图形登记表；一张图 = 在哪一页 + 用哪个生成器 + 按什么锚点定位（`attrs` 结构性锚点 / `aria` 前缀）；现有 20 条记录
`build_figures.py`: 按登记表生成全部图到 `out/`；`--splice` 逐张回写页面（一张一张替换，每张替换后重读文件，避免偏移失效）
`verify_embedded.py`: 比对「页面里嵌的」与「生成器输出的」是否逐字一致，防止脚本改了页面没改
`check_svg.py`: 几何检查五项 —— 同基线文本重叠、画布越界、文字溢出色块、SVG 内混入 HTML 标签、id 重复
`svgutil.py`: SVG 定位 / 取出 / 归一化，以及 CJK 文本宽度估算（供 check_svg 判断溢出色块）
`stage_template.py`: 三族放大图共用的渲染模板；保证计算线与连接线两套图结构完全一致
`gen_stages.py`: 三族放大图共 12 张（计算线台阶 / 连接线阶段 / 物理段）
`steps_data.py`: 计算线台阶图的文案与对齐标记（`data-stage` / `data-leaps`）
`stages_data.py`: 连接线阶段图的文案与对齐标记（`data-stage` / `data-events`）
`phys_stages_data.py`: 物理段图的文案与对齐标记（`data-stage` / `data-events`）
`gen_twolines.py`: 03 第三次页的三条线总图
`gen_forks.py`: 03 第三次页的三个岔路图
`gen_roadmap.py`: 04 底层架构页的技术架构路线图；含 `UNDET` 标记，2026→ 前景列无依据的格子一律标「尚未定位」
`gen_cutaway.py`: 04 底层架构页的「同一套抽象结构的两套物理实现」；三列对照 —— 电子管时代实物 / 共用抽象层 / 集成电路时代实物，底带说明稀缺换了位置
`gen_semi.py`: 05 半导体页的缩放方式三次转移、光刻波长演进两张图
`gen_semi3.py`: 05 半导体页的「瓶颈的性质在跃迁 7」图
`gen_energy.py`: 10 能源页的 ERCOT 并网队列漏斗；数据来自 ERCOT 一手原件
`preview_narrow.html`: 窄屏布局验收台；把页面塞进 380 / 520 / 768px 的 iframe，媒体查询按该宽度生效
`README.md`: 改图的标准流程、文件清单、三族放大图、几何检查查什么、窄屏怎么验、写 SVG 的硬约束、手写图清单

## 纪律

- **改文案只动 `*_data.py`，改画法才动 `gen_*.py` / `stage_template.py`**
- 登记表外的手写图脚本不碰，改完必须跑 `check_svg.py`
- 生成器的输出必须能被 `verify_embedded.py` 逐字复现 —— 页面里的 SVG 不要手改
- SVG 内禁止出现 `<b>` `<strong>` `<br>` 等 HTML 标签，浏览器会把内容甩出画布
- 渐变与 marker 的 id 必须全图唯一，否则 `url(#id)` 会串到别的图上

Laws: complete membership · one line per file · parent link · technical terms first
[PROTOCOL]: Update this header on change, then check CLAUDE.md
