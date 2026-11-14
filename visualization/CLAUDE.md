# visualization/
> L2 | Parent: ../CLAUDE.md

自包含静态站点：11 个内容页 + 1 个旧页重定向。全部图形内联 SVG（由 `scripts/figures/` 生成后回写），媒体在 `assets/`。无构建步骤、无外部依赖，Pages 直接发布本目录。

## 成员清单

`index.html`: 核心沉淀首页；开篇片、主线地图、三条铁律闭环、当下定位、对 Agent 平台的 5 条推论、术语速查
`01-first.html`: 蒸汽动力、工厂制度、1833 工厂法、为何发生在英国、这一轮的账
`02-second.html`: 单元驱动与布局重排、贝塞麦/泰勒制/流水线、共享增长的确立
`03-third.html`: 可编程与零边际复制；内部章：电子计算机八次架构跃迁 + 互联网与移动设备线 + 物理基础线
`04-architecture.html`: 七层抽象栈、同一套抽象结构的两套物理实现、金字塔总图、技术架构路线、四段台阶放大、逐层传递矩阵、十个维度的影响对照
`05-semiconductor.html`: 独立主题：缩放方式的三次转移、光刻波长与制程节点年表、存储与封装、产业分工、中国的位置
`06-fourth.html`: 自主执行、2026 普及数据、组织端为何没动、新稀缺预告
`07-current.html`: 2026 三个硬约束完整数据、2026–2028 路线图、全部来源与不确定项
`08-glossary.html`: 106 条分组词条 + 按角色的阅读路径
`09-logic.html`: 四条铁律的完整推导、兑现时滞时间轴、推论完整版
`10-energy.html`: 能源的四种角色、ERCOT 并网队列漏斗、IEA/CSO 一手数据、能源解释不了什么
`computer-architecture-evolution.html`: 旧入口的重定向页（meta refresh → index.html），不在导航与页脚中，校验脚本对其特判
`assets/`: 全站唯一的外部资源目录，见 assets/CLAUDE.md

## 页面纪律

- 图一律内联 `<svg>`，不引用外部位图；需要脚本生成的图先进 `scripts/figures/registry.py` 登记再回写
- 每张 SVG 必须带 `role="img"` 与 `aria-label`，必须带 `viewBox`，用 `width="100%" style="display:block;height:auto"` 响应式缩放
- 图注编号（「图 N ·」）手工维护，插入新图需同步重编号并检查正文交叉引用
- 正文引用统一用 `href`，媒体引用用 `src`/`poster` —— 两条通道由 `scripts/verify.py` 分别检查

Laws: complete membership · one line per file · parent link · technical terms first
[PROTOCOL]: Update this header on change, then check CLAUDE.md
