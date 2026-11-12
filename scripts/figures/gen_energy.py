#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「ERCOT 并网队列漏斗：请求 → 获批 → 运行」SVG。

这张图要说明的是第四轮革命的一个具体事实：
**需求侧画出了 466.5 GW 的饼，供给侧只兑现了 0.84%。**

数据全部来自 ERCOT 一手原件（Large Load Working Group 报告 2026-06-19，
数据截至 2026-06-18），已核到页码，见 wiki「08 数据来源与口径」。

画法上的关键取舍：
**不做等比漏斗。** 3,900 MW 只占 466,497 MW 的 0.84%，等比画出来第三段只有
几像素，等于把「漏斗」这个隐喻自己毁掉。这里改成**三段各自等比 + 段间标注
收敛倍数**，并明确写出「刻度不连续」，不制造等比的错觉。

用法：python3 scripts/figures/gen_energy.py（打印 SVG）
      或由 scripts/figures/build_figures.py 统一生成 / 回写。
"""

# ── 数据（一手，页码见 wiki/08） ──────────────────────────────────
# ERCOT LLWG 报告 p.3：请求总量 466,497 MW
# ERCOT LLWG 报告 p.8：获批通电 8,927 MW；非同时月峰值 3,900 MW
# ERCOT LLWG 报告 p.14：数据中心占请求容量 90.2%（420,812 MW）
REQUESTED = 466497
APPROVED = 8927
OPERATING = 3900
DC_SHARE = 90.2

VIEW_W = 1190
PAD = 14

# ── 画法：两把尺，避免等比把第三段压成一条线 ────────────────────
# 第一段用「全局尺」（相对请求总量），后两段用「段内尺」（各自满量）。
# 两把尺分别标注，不制造等比错觉。
BAR_X = 232          # 条形起点
BAR_MAX = 560        # 一段满量时的长度
SEG_H = 46           # 每段条形高度
SEG_GAP = 34         # 段间距
SEG_Y0 = 150         # 第一段顶部

# 段落定义：(标题, 数值, 长度, 尺说明, 颜色)
SEGMENTS = [
    ('请求总量', REQUESTED, BAR_MAX, '全局尺 · 相对请求总量', '#2f6f5e'),
    ('已获批通电', APPROVED, BAR_MAX * APPROVED / REQUESTED * 12,
     '放大 12 倍 · 相对请求总量', '#c97b3f'),
    ('实际运行', OPERATING, BAR_MAX * OPERATING / REQUESTED * 12,
     '放大 12 倍 · 相对请求总量', '#b0433a'),
]


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def fmt(n):
    """千分位。"""
    return format(n, ',')


def gen():
    o = []
    a = o.append
    height = SEG_Y0 + 3 * SEG_H + 2 * SEG_GAP + 172
    a('<svg class="energyfig" data-funnel="requested|approved|operating" '
      'data-requested="%d" data-approved="%d" data-operating="%d" '
      'viewBox="0 0 %d %d" width="100%%" style="display:block;height:auto" '
      'role="img" aria-label="ERCOT 并网队列漏斗：请求总量 466497 兆瓦，'
      '已获批通电 8927 兆瓦，实际运行 3900 兆瓦，兑现率 0.84%%">'
      % (REQUESTED, APPROVED, OPERATING, VIEW_W, height))
    a('  <g font-family="Outfit, \'PingFang SC\', sans-serif">')

    # ── 标题区 ──
    a('    <text x="%d" y="30" font-size="15" font-weight="600" fill="#14171e">'
      'ERCOT 并网队列：需求侧画了 466.5 GW 的饼，供给侧只兑现了 0.84%%</text>'
      % PAD)
    a('    <text x="%d" y="52" font-size="12.5" fill="#3a4256">'
      '稀缺不在电价上，在「能不能拿到电」上 —— 大型负荷队列请求 466,497 MW，'
      '最终跑起来的只有 3,900 MW。</text>' % PAD)
    a('    <line x1="%d" y1="70" x2="%d" y2="70" stroke="#e9e3d6"/>'
      % (PAD, VIEW_W - PAD))

    # ── 三段漏斗 ──
    y = SEG_Y0
    for i, (title, val, w, scale_note, col) in enumerate(SEGMENTS):
        # 左侧：标题 + 说明
        a('    <text x="%d" y="%d" font-size="13" font-weight="600" fill="#14171e">%s</text>'
          % (PAD, y + 20, esc(title)))
        a('    <text x="%d" y="%d" font-size="10.5" fill="#7c7a72">%s</text>'
          % (PAD, y + 37, esc(scale_note)))

        # 条形（浅底 + 实心）
        a('    <rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s" fill-opacity=".16"/>'
          % (BAR_X, y + 6, w, SEG_H - 12, col))
        a('    <rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s"/>'
          % (BAR_X, y + 6, w, SEG_H - 12, col))

        # 条形右侧：数值 + 单位 + 占请求总量的比例
        a('    <text x="%d" y="%d" font-size="17" font-weight="600" fill="#14171e">%s</text>'
          % (BAR_X + w + 16, y + 27, fmt(val)))
        ux = BAR_X + w + 16 + len(fmt(val)) * 9.8 + 8
        a('    <text x="%d" y="%d" font-size="11" fill="#7c7a72">MW</text>' % (ux, y + 27))
        pct = val / REQUESTED * 100.0
        a('    <text x="%d" y="%d" font-size="11.5" fill="#3a4256">'
          '占请求总量 <tspan font-weight="600" fill="#14171e">%.2f%%</tspan></text>'
          % (ux + 34, y + 27, pct))

        # 段间收敛：箭头 + 相对上一段的倍数
        if i < len(SEGMENTS) - 1:
            nxt = SEGMENTS[i + 1][1]
            ratio = nxt / val * 100.0
            ay = y + SEG_H + 4
            a('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#b3aea2" stroke-width="1.4"/>'
              % (BAR_X + 10, ay, BAR_X + 10, ay + SEG_GAP - 12))
            a('    <path d="M%d %d L%d %d L%d %d Z" fill="#b3aea2"/>'
              % (BAR_X + 5, ay + SEG_GAP - 12, BAR_X + 15, ay + SEG_GAP - 12,
                 BAR_X + 10, ay + SEG_GAP - 4))
            a('    <text x="%d" y="%d" font-size="12" fill="#3a4256">'
              '进入下一段的只剩 <tspan font-weight="600" fill="#14171e">%.1f%%</tspan>'
              '（%s → %s MW）</text>'
              % (BAR_X + 28, ay + SEG_GAP / 2 + 2, ratio, fmt(val), fmt(nxt)))
        y += SEG_H + SEG_GAP

    # ── 兑现率 ──
    rate = OPERATING / REQUESTED * 100.0
    ry = y + 6
    a('    <rect x="%d" y="%d" width="%d" height="46" rx="10" fill="#b0433a" fill-opacity=".07" stroke="#b0433a" stroke-opacity=".2"/>'
      % (PAD, ry, VIEW_W - 2 * PAD))
    a('    <text x="%d" y="%d" font-size="12.5" fill="#3a4256">'
      '兑现率</text>' % (PAD + 16, ry + 29))
    a('    <text x="%d" y="%d" font-size="21" font-weight="600" fill="#b0433a">%.2f%%</text>'
      % (PAD + 72, ry + 30, rate))
    a('    <text x="%d" y="%d" font-size="11.5" fill="#3a4256">'
      '—— 每 100 MW 的并网意向，最终跑起来不到 1 MW。'
      '其中数据中心占请求容量的 90.2%%（420,812 MW）。</text>'
      % (PAD + 148, ry + 29))

    # ── 刻度说明与来源 ──
    fy = ry + 46 + 30
    a('    <text x="%d" y="%d" font-size="11" fill="#7c7a72">'
      '⚠ 条形长度<tspan font-weight="600" fill="#3a4256">刻意不等比</tspan>'
      '：第一段是全局尺（相对请求总量），后两段放大 12 倍才画得出来，'
      '所以段与段之间不可直接比长度；每段右侧标的是它<tspan font-weight="600" fill="#3a4256">占请求总量的真实比例</tspan>。</text>'
      % (PAD, fy))
    a('    <text x="%d" y="%d" font-size="11" fill="#7c7a72">'
      '口径：ERCOT 大型负荷并网队列，数据截至 2026-06-18。'
      '「实际运行」为非同时月峰值（同时月峰值口径为 3,675 MW，两者不可混用）；'
      '数据中心 90.2%% 是请求容量按项目类型的占比。来源见 wiki「08 数据来源与口径」。</text>'
      % (PAD, fy + 20))

    a('  </g>')
    a('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    print(gen())
