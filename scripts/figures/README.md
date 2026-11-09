# 图的生成与校验

页面上的 SVG 有两种来路：

- **由脚本生成**（18 张）—— 本目录管它们。生成器是本体，页面里嵌的是它的产物。
- **手写图**（8 处）—— 本目录不管它们，但几何检查照样覆盖（见下）。

**改图必须在本目录改脚本，不要在 workspace 里维护临时脚本。**

---

## 改一张图的标准流程

```bash
# 1. 改生成器（gen_*.py / *_data.py）
python3 scripts/figures/build_figures.py            # 生成到 out/，先看一眼

# 2. 回写页面（一张一张替换，每张替换后重新读文件）
python3 scripts/figures/build_figures.py --splice

# 3. 校验（两条都要跑）
python3 scripts/figures/verify_embedded.py           # 页面与生成器是否逐字一致
python3 scripts/figures/check_svg.py                 # 全站所有图的几何检查
```

第 3 步的 `verify_embedded.py` 是防漂移的关键：**脚本改了、页面没改**时，
页面照旧显示旧图，脚本却以为已经更新 —— 下一次 `--splice` 会把页面整体改掉，
这种差异肉眼看不出来。

---

## 文件清单

| 文件 | 作用 |
|---|---|
| `registry.py` | **图的登记表**：一张图 = 在哪一页 + 用哪个生成器 + 在页面上靠什么定位它。`build_figures.py` 与 `verify_embedded.py` 都按它工作 |
| `build_figures.py` | 生成全部登记在册的图到 `out/`；`--splice` 回写进页面 |
| `verify_embedded.py` | 比对「页面里嵌的」与「生成器输出的」是否逐字一致 |
| `check_svg.py` | 几何检查（见下），可查全站页面、单个页面或单个 svg 文件 |
| `svgutil.py` | 页面内 SVG 的定位 / 取出 / 归一化，以及文本宽度估算 |
| `stage_template.py` | 三族放大图共用的渲染模板 |
| `gen_stages.py` | 三族放大图共 12 张（计算线台阶 / 连接线阶段 / 物理段） |
| `gen_semi.py` / `gen_semi3.py` | 05 半导体页的三张图 |
| `gen_twolines.py` / `gen_forks.py` | 03 第三次页的三条线总图与三个岔路图 |
| `gen_roadmap.py` | 04 底层架构页的技术架构路线图 |
| `steps_data.py` / `stages_data.py` / `phys_stages_data.py` | 三族放大图的文案与对齐标记（`data-stage` / `data-leaps` / `data-events`） |

**改文案只动 `*_data.py`，改画法才动 `gen_*.py` / `stage_template.py`。**

---

## 三族放大图

| 族 | 类名 | 页面 | 列头 | 渐变 id 前缀 |
|---|---|---|---|---|
| 计算线四段台阶 | `stepfig` | 04-architecture.html | 跃迁 · 名称 | `gup1` / `gdn1` |
| 连接与接入线四阶段 | `stagefig` | 03-third.html | 节点 · 名称 | `gup101` / `gdn101` |
| 物理基础线四物理段 | `physfig` | 03-third.html | 节点 · 名称 | `gup201` / `gdn201` |

三族在 03-third.html **同页共存**，渐变 id 必须互不相同，否则 `url(#gup1)` 会
串到第一张图上。分隔线的右端点也分族：计算线台阶图用 898，另两族用 876。

页面上 `<svg>` 的 `data-stage` / `data-leaps` / `data-events` 是
`scripts/test_alignment.py` 的对齐校验依据，**改图时必须同步改这些属性**——
脚本里的 `*_META` 就是它们的来源。

---

## 几何检查查什么

`check_svg.py` 查五类「肉眼看不出来」的事：

1. **同基线文本重叠** —— 同一行基线上两段文本横向相交或贴得过近（间隙 < 4px）。
2. **画布越界** —— 文本横向超出 viewBox。
3. **文字溢出所属色块** —— 文字所在的最小矩形装不下它。*检测器只查画布边界时查不出
   这一类*；上一轮据此在半导体图 1 上抓到 6 处并修短。
4. **SVG 内混入 HTML 标签** —— `<b>` / `<strong>` / `<br>` 等，浏览器把它们当未知
   元素，内容会被甩出画布，必须用 `<tspan>`。
5. **id 重复** —— 同一张图里渐变 / marker 的 id 必须唯一。

跑法：

```bash
python3 scripts/figures/check_svg.py                 # 全站页面里的所有图
python3 scripts/figures/check_svg.py 03-third.html   # 只查某页
python3 scripts/figures/check_svg.py out/05-fig3.svg # 只查单张
```

退出码 `0` = 全过。

---

## 写 SVG 的硬约束

- **`<text>` 里禁用 HTML 标签**（`<b>` / `<strong>` / `<br>`）—— 用 `<tspan>`。
- **inline SVG 不写 `xmlns`**（HTML 解析器自动放进 SVG 命名空间）；独立预览
  文件必须写。
- **批量替换已入库 HTML 的匹配区段必须逆序**（`sorted(matches, reverse=True)`），
  否则前一次替换改变字符串长度，后续偏移全部失效，产出 `<figure<svg` 这类坏 HTML。
  `build_figures.py --splice` 采取「一张一张替换、每张替换后重新读文件」来规避。
- 文本宽度估算：CJK 按 1.0em，其余按 0.58em。SVG 默认会折叠空白，**估算前必须
  先折叠**（`svgutil.texts_of` 已做）—— 不折叠会把源码缩进算进宽度，凭空报越界。

---

## 手写图（没有生成器）

以下图是早期手写的，**没有生成器**，本目录不碰它们；几何检查仍覆盖它们：

| 页面 | 图 |
|---|---|
| 02-second.html | 中央传动布局与单元驱动布局的对比，以及兑现时滞 |
| 04-architecture.html | 计算机系统七层抽象栈与瓶颈下沉路径 |
| 04-architecture.html | 从物理约束到目标与责任的金字塔（稀缺下沉 · 能力上浮） |
| 04-architecture.html | 三条技术主线的演进方向 |
| 09-logic.html | 技术兑现时间轴 |
| index.html | 四轮工业革命的替代对象、核心机制、组织变革与新稀缺迁移对照图 |
| index.html | 三条铁律构成的闭环 |
| index.html | 三条技术主线的演进方向（与 04 页同一张） |

要改这些图，只能直接改页面里的 SVG —— 改完**必须跑 `check_svg.py`**。
