# 维护脚本

保证 `visualization/` 下九个页面的结构一致性。只用 Python 标准库，无依赖。

---

## build.py —— 站点构建

同步四类结构，避免手工改九个文件时出错：

| 同步项 | 说明 |
|---|---|
| **树形导航** | 按工业革命分期生成 `<details>/<summary>` 分组，当前页所在分组带 `has-active` 标记，面板内当前页高亮 |
| **页脚** | 统一站点名 + 按树形层级排序的主线链接串；保留原缩进风格 |
| **编号** | 校验「文件名 / kicker / title」三者编号一致 |
| **内部链接** | 同步 `href` 与正文中的页码前缀引用 |

### 用法

```bash
python3 scripts/build.py            # 构建
python3 scripts/build.py --check    # 只检查，退出码 1 = 有待构建内容
```

**幂等**：连续执行两次，第二次应报告「0 个页面有更新」。

### 改站点结构时改哪里

页面树定义在 `build.py` 顶部的 `TREE` 常量：

```python
TREE = [
    ('核心沉淀', None),
    ('第一次工业革命', [
        ('01-first.html', '第一次', '蒸汽动力 · 工厂制度 · 1833 工厂法'),
    ]),
    ...
]
```

每项为 `(分组名, [(文件名, 短名, 副标题)])`；`None` 表示该组是单个直达链接。
**改完必须同步** `PREFIX_MAP`（正文页码前缀）与 `LEGACY_PREFIX`（旧编号 → 新编号）。

---

## verify.py —— 全站校验

九项检查：

1. 链接可达性（无断链）
2. HTML 标签配平（19 类标签）
3. 树形导航结构一致（分组数、当前项标记、面板高亮）
4. 文件名 / kicker / title 编号一致
5. 旧文件名无残留
6. 页脚链接顺序与树形层级一致
7. 术语表分组计数自洽（declared == actual）
8. 关键数字口径跨页一致（15 项）
9. `wiki/` 与 `visualization/` 口径一致（链接可达、标签与目标对得上、关键数字已沉淀）

### 用法

```bash
python3 scripts/verify.py
```

退出码 `0` = 全部通过，`1` = 存在问题（问题逐条列出）。

### 什么时候必须跑

- 改了 `wiki/` 并同步页面后
- 增删页面或调整分组后
- 提交前

### 新增关键数字时

在 `verify.py` 的 `KEY_FIGURES` 列表里加一项——它会检查该数字是否跨页一致（存在且未丢失）。**改动统计口径时，这个列表要同步更新。**
若该数字也应进 wiki，再加进 `WIKI_FIGURES`（页面里有则 wiki 必须有）。

---

## test_verify.py —— 校验逻辑自测

`verify.py` 第 9 项（链接标签与目标是否对得上）判据较复杂，改动 `verify.py` 后必须跑它确认没有失效：

```bash
python3 scripts/test_verify.py
```

14 条用例，含真实踩过的坑（「底层架构」曾误指向第四次页——编号对得上、名称对不上，只有比名称才抓得住）。退出码 `0` = 判据仍然有效。

---

## test_alignment.py —— 三条线的逐项对齐校验
第三次革命有三条线，段号一一对应，每段覆盖同一批跃迁：

| 线 | 段 | 位置 |
|---|---|---|
| **计算线** | 四段台阶（八次架构跃迁） | `04-architecture.html`，`class="stepfig"` |
| **连接与接入线** | 四个阶段（互联网与移动设备） | `03-third.html`，`class="stagefig"` |
| **物理基础线** | 四个物理段（半导体·通信·能源） | `03-third.html`，`class="physfig"` |

```bash
python3 scripts/test_alignment.py
```

八项检查：

1. 三条线各自的阶段号 1–4 无缺无重
2. 计算线的跃迁区间合并后**正好覆盖八次跃迁**，不重叠、不遗漏
3. 同阶段号的三张图，跃迁区间完全一致
4. 每张图 `data-events` 里的每个名称都必须出现在该图的实际文本里（标记不能与画出来的内容脱节）
5. `wiki/03-第三次工业革命.md` 的**两张**对齐表逐行与三张图的数据一致

**外加三个岔路的检查**（`check_forks()`）：物理层前方有三条岔路（散热形态 / 芯片形态 / 堆叠形态），已查证到判定条件。脚本验三处说同一件事：

- 岔路图（`class="forkfig"`）上的三个名称与 `wiki/03` 岔路表逐行一致
- 岔路表的每行「已定型的现状 / 判定条件 / 仍然不确定」三栏**都非空** —— 不允许留「？」占位（诚实性约束）
- 路线图 2026→ 列里三个岔路关键词带 `data-forkkey` 精确标记，且**几何上落在整张图最右一列**（只写「关键词出现在图里」是不够的：实测过它会漏判）

**数据从哪来**：三套图的 `<svg>` 上带 `data-stage` / `data-leaps` / `data-events`（连接与接入线另有 `data-peers`），岔路图带 `data-forknames`，路线图带 `data-forkkeys`，路线图里被标记的文本带 `data-forkkey`。脚本读这些属性与 wiki 表比对。**改图时必须同步改这些属性**，否则脚本会报错——这是有意的：宁可报错，也不要静默错位。

---

## figures/ —— 图的生成与校验

页面上的 18 张 SVG 由 `scripts/figures/` 下的生成器产出：生成器是本体，页面里嵌的是它的产物。另有 8 处手写图没有生成器。

```bash
python3 scripts/figures/build_figures.py            # 生成到 out/
python3 scripts/figures/build_figures.py --splice    # 生成并回写进页面
python3 scripts/figures/verify_embedded.py           # 页面与生成器是否逐字一致（防漂移）
python3 scripts/figures/check_svg.py                 # 全站所有图的几何检查
```

**改图的标准流程**：改 `scripts/figures/` 里的生成器 → `build_figures.py --splice` 回写 → `verify_embedded.py` + `check_svg.py` 双校验。

`verify_embedded.py` 挡的是「脚本改了、页面没改」：这种漂移页面照旧显示旧图，
下一次回写会把页面整体改掉，肉眼很难发现。
`check_svg.py` 查同基线文本重叠、画布越界、文字溢出所属色块、SVG 内混入 HTML 标签、id 重复 —— 全部是肉眼看不出来的那一类。

细节见 [`figures/README.md`](figures/README.md)。

---

## 约定

- **脚本只保证结构，不生成内容。** 内容以 `wiki/` 为准，页面是它的呈现。
- **不改脚本的路径常量。** `build.py` / `verify.py` 用 `Path(__file__).parent.parent` 定位项目根，可整体移动。
- **历史迭代版不进仓库。** 本目录只保留当前有效的最终形态。
- **临时脚本不进仓库，也不留在 workspace。** 需要长期维护的脚本一律放进本目录对应位置。
