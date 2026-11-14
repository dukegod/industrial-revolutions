#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「半导体的发展进程」主题的两张图。

图 1 · 缩放方式的三次转移
图 2 · 光刻波长演进与制程节点年表

用法：python3 scripts/figures/gen_semi.py（打印 SVG）
      或由 scripts/figures/build_figures.py 统一生成 / 回写。

[INPUT]: depends on wiki/09-半导体的发展进程.md
[OUTPUT]: exports the two semiconductor figures: the three shifts of scaling, and the lithography wavelength evolution
[POS]: the producer of the two figures on the semiconductor page
[PROTOCOL]: Update this header on change, then check CLAUDE.md
"""
import json
from pathlib import Path

INK, INK2, MUTED, LINE, ACCENT, RUST = '#14171e', '#3a4256', '#7c7a72', '#e9e3d6', '#2f6f5e', '#c97b3f'

# ── 图 1 ─────────────────────────────────────────────────────────
SCALES = [
    {
        'name': '几何缩放', 'span': '1965–2010',
        'head': '把平面上的线做得更细',
        'items': [
            '摩尔定律（1965）：每年晶体管数翻倍',
            '登纳德缩放（1974）：电压电流随之下降',
            '平面工艺（1959）· 集成电路 · 微处理器（1971）',
            'VLSI · 光刻 g 线 / i 线 → 193nm ArF',
            '90nm（2004）· 45nm（2008）· 32nm（2009）',
        ],
        'fixed': '算力持续翻倍、单位能耗持续下降 —— 第三次革命的地基',
        'hit': [
            '2005 年前后尺寸缩放放缓',
            '互连延迟与漏电先撞墙（不是逻辑，是线）',
            'DUV 单次曝光逼近波长极限',
        ],
    },
    {
        'name': '三维缩放', 'span': '2011–2022',
        'head': '把电路从平面立起来',
        'items': [
            'FinFET（2011–2016）：鳍式沟道 + 三维栅控',
            'EUV 首量产（2019）：13.5nm 反射式光刻',
            'GAA nanosheet（2022）：环绕栅极',
            '背面供电（BSPDN）· 高 k / 低 k 材料',
            '尺寸仍在缩小，但代价从面积转向工艺',
        ],
        'fixed': '把平面缩放放弃的电压与漏电拿回来，换来继续缩小的许可',
        'hit': [
            '工艺步骤与成本指数上升，良率承压',
            'EUV 设备单点集中，产能即瓶颈',
            '3nm 以下只剩 GAA 一条路',
        ],
    },
    {
        'name': '封装缩放', 'span': '2017–→',
        'head': '不再追求一颗大芯片，改为一堆小芯片',
        'items': [
            'CoWoS（2017）：2.5D 中介层把算力与 HBM 贴在一起',
            'Chiplet（2017）：不同模块用各自最优工艺',
            'HBM（2016→2026）：16 层 / 2048-bit',
            '混合键合（SoIC 6μm，逻辑侧已量产）',
            'CPO（2026 首批量产）：光进封装',
        ],
        'fixed': '绕开 reticle 上限与良率乘积 —— 拆成小芯片再拼装',
        'hit': [
            'CoWoS 产能缺口 10–20%，新增产能要到 2027–2028',
            '键合良率、翘曲与测试成本上升',
            '热与电力成为新的天花板',
        ],
    },
]

FIG1_W, FIG1_H = 1160, 596


def fig1():
    o = []
    a = o.append
    a('<svg viewBox="0 0 %d %d" width="100%%" style="display:block;height:auto" role="img" aria-label="缩放方式的三次转移：几何缩放、三维缩放、封装缩放，每一段列出代表工艺、解决了什么、撞上了什么">'
      % (FIG1_W, FIG1_H))
    a('  <defs>')
    a('    <marker id="f1Arrow" markerWidth="9" markerHeight="9" refX="7" refY="3.2" orient="auto">')
    a('      <path d="M0,0 L7,3.2 L0,6.4 Z" fill="%s"/>' % ACCENT)
    a('    </marker>')
    a('  </defs>')
    a('  <g font-family="Outfit, \'PingFang SC\', sans-serif">')

    bw, gap = 348, 48
    for i, s in enumerate(SCALES):
        x = 20 + i * (bw + gap)
        a('    <rect x="%d" y="46" width="%d" height="452" rx="14" fill="#fff" stroke="%s"/>' % (x, bw, LINE))
        a('    <rect x="%d" y="46" width="%d" height="60" rx="14" fill="%s" fill-opacity=".07"/>' % (x, bw, ACCENT))
        a('    <rect x="%d" y="90" width="%d" height="16" fill="%s" fill-opacity=".07"/>' % (x, bw, ACCENT))
        a('    <text x="%d" y="76" font-size="16" font-weight="600" fill="%s">%s</text>' % (x + 16, INK, s['name']))
        a('    <text x="%d" y="94" font-size="11" font-family="JetBrains Mono, monospace" fill="%s">%s</text>' % (x + 150, MUTED, s['span']))
        a('    <text x="%d" y="132" font-size="12" fill="%s">%s</text>' % (x + 16, INK2, s['head']))
        a('    <text x="%d" y="162" font-size="10.5" font-family="JetBrains Mono, monospace" fill="%s">代表工艺与节点</text>' % (x + 16, ACCENT))
        yy = 186
        for it in s['items']:
            a('    <text x="%d" y="%d" font-size="11.5" fill="%s">· %s</text>' % (x + 16, yy, INK2, it))
            yy += 20
        a('    <line x1="%d" y1="306" x2="%d" y2="306" stroke="%s"/>' % (x + 16, x + bw - 16, LINE))
        a('    <text x="%d" y="330" font-size="10.5" font-family="JetBrains Mono, monospace" fill="%s">解决了什么</text>' % (x + 16, ACCENT))
        a('    <text x="%d" y="352" font-size="11.5" fill="%s">%s</text>' % (x + 16, INK2, s['fixed']))
        a('    <line x1="%d" y1="376" x2="%d" y2="376" stroke="%s"/>' % (x + 16, x + bw - 16, LINE))
        a('    <text x="%d" y="400" font-size="10.5" font-family="JetBrains Mono, monospace" fill="%s">撞上了什么</text>' % (x + 16, RUST))
        yy = 422
        for it in s['hit']:
            a('    <text x="%d" y="%d" font-size="11.5" fill="%s">· %s</text>' % (x + 16, yy, INK2, it))
            yy += 20
        if i < 2:
            a('    <line x1="%d" y1="270" x2="%d" y2="270" stroke="%s" stroke-width="2" marker-end="url(#f1Arrow)"/>'
              % (x + bw + 8, x + bw + gap - 8, ACCENT))
    a('    <text x="20" y="530" font-size="12" fill="%s">三次转移的共同点：<tspan font-weight="600" fill="%s">每次都不是「造出更快的芯片」，而是「换一种方式把同样多的晶体管堆起来」</tspan> —— 缩放的载体从平面搬到垂直，再从芯片搬到封装。</text>' % (INK2, INK))
    a('    <text x="20" y="556" font-size="11.5" fill="%s">摩尔定律并没有「失效」，它只是不再是靠缩小单个器件实现的 —— 晶体管数仍在涨，只是改由三维结构与异构集成贡献。</text>' % MUTED)
    a('  </g>')
    a('</svg>')
    return '\n'.join(o)


# ── 图 2 ─────────────────────────────────────────────────────────
LITHO = [
    ('g 线 436nm', '1970s', '接触式 / 投影式曝光起步'),
    ('h 线 405nm', '1980s', '分辨率提升'),
    ('i 线 365nm', '1980s', '更短波长继续缩小'),
    ('ArF 193nm', '1990s', 'DUV 时代开启，单次曝光做不出更小图形'),
    ('浸没式 ArF 193nm', '2004', '超纯水压缩折射率，多重曝光撑住 90–7nm'),
    ('EUV 13.5nm', '2019', '反射式掩模，首次突破波长限制'),
]
NODES = [
    ('90nm', '2004'), ('45nm', '2008'), ('28nm', '2010'), ('14nm', '2015'),
    ('7nm', '2018'), ('5nm', '2020'), ('3nm', '2022'), ('2nm', '2025'),
]
FIG2_W, FIG2_H = 1160, 520


def fig2():
    o = []
    a = o.append
    a('<svg viewBox="0 0 %d %d" width="100%%" style="display:block;height:auto" role="img" aria-label="光刻波长演进与半导体制程节点年表：从 g 线 436nm 到 EUV 13.5nm，制程节点从 90nm 到 2nm，标出摩尔定律放缓与 EUV 量产两个拐点">'
      % (FIG2_W, FIG2_H))
    a('  <g font-family="Outfit, \'PingFang SC\', sans-serif">')

    # 上排：光刻波长
    a('    <text x="30" y="40" font-size="13" font-weight="600" fill="%s">光刻波长演进</text>' % INK)
    a('    <text x="130" y="40" font-size="11" fill="%s">每一次换波长，都是为了在更小的图形上仍能成像</text>' % MUTED)
    x = 30
    for i, (w, yr, note) in enumerate(LITHO):
        bw = 172
        last = (i == len(LITHO) - 1)
        col = ACCENT if last else MUTED
        a('    <rect x="%d" y="58" width="%d" height="112" rx="10" fill="%s" fill-opacity="%s" stroke="%s" stroke-opacity=".5"/>'
          % (x, bw, ACCENT if last else '#8a8a80', '.10' if last else '.05', col))
        a('    <text x="%d" y="88" font-size="13" font-weight="600" fill="%s">%s</text>' % (x + 12, INK, w))
        a('    <text x="%d" y="108" font-size="11" font-family="JetBrains Mono, monospace" fill="%s">%s</text>' % (x + 12, col, yr))
        yy = 132
        for ln in [note[:13], note[13:26]]:
            if ln:
                a('    <text x="%d" y="%d" font-size="11" fill="%s">%s</text>' % (x + 12, yy, INK2, ln))
                yy += 16
        if i < len(LITHO) - 1:
            a('    <line x1="%d" y1="114" x2="%d" y2="114" stroke="%s" stroke-width="1.4" marker-end="url(#f2Arrow)"/>'
              % (x + bw + 2, x + bw + 10, MUTED))
        x += bw + 14
    a('    <defs><marker id="f2Arrow" markerWidth="8" markerHeight="8" refX="6.5" refY="2.8" orient="auto">'
      '<path d="M0,0 L6.5,2.8 L0,5.6 Z" fill="%s"/></marker></defs>' % MUTED)

    # 拐点标注
    x_euv = 30 + 5 * (172 + 14)
    a('    <line x1="%d" y1="44" x2="%d" y2="58" stroke="%s" stroke-width="1.4" stroke-dasharray="5 4"/>' % (x_euv + 8, x_euv + 8, ACCENT))
    a('    <line x1="%d" y1="170" x2="%d" y2="186" stroke="%s" stroke-width="1.4" stroke-dasharray="5 4"/>' % (x_euv + 8, x_euv + 8, ACCENT))
    a('    <text x="%d" y="200" font-size="11" fill="%s" text-anchor="middle">EUV 首次量产 2019</text>' % (x_euv + 8, ACCENT))

    # 下排：制程节点
    a('    <text x="30" y="248" font-size="13" font-weight="600" fill="%s">制程节点年表</text>' % INK)
    a('    <text x="130" y="248" font-size="11" fill="%s">节点号是密度指标而非物理尺寸，各家定义不同，不可直接横向比较</text>' % MUTED)
    a('    <line x1="30" y1="296" x2="1130" y2="296" stroke="%s" stroke-width="1.6"/>' % LINE)
    nw = 137
    for i, (node, yr) in enumerate(NODES):
        cx = 30 + i * nw + nw // 2
        a('    <circle cx="%d" cy="296" r="5" fill="#fff" stroke="%s" stroke-width="2"/>' % (cx, ACCENT))
        a('    <text x="%d" y="282" font-size="12.5" font-weight="600" fill="%s" text-anchor="middle">%s</text>' % (cx, INK, node))
        a('    <text x="%d" y="320" font-size="11" font-family="JetBrains Mono, monospace" fill="%s" text-anchor="middle">%s</text>' % (cx, MUTED, yr))
    # 摩尔定律放缓区间
    x1 = 30 + 1 * nw
    x2 = 30 + 4 * nw
    a('    <rect x="%d" y="340" width="%d" height="34" rx="8" fill="%s" fill-opacity=".07" stroke="%s" stroke-opacity=".3"/>' % (x1, x2 - x1, RUST, RUST))
    a('    <text x="%d" y="362" font-size="11.5" fill="%s" text-anchor="middle">摩尔定律放缓区间（约 2005–2015）</text>' % ((x1 + x2) // 2, RUST))

    # 底部结论
    a('    <rect x="30" y="396" width="1100" height="96" rx="12" fill="%s" fill-opacity=".05" stroke="%s"/>' % (ACCENT, LINE))
    a('    <text x="50" y="424" font-size="12" fill="%s">两个拐点：<tspan font-weight="600" fill="%s">2005 年前后</tspan>——制程红利放缓，靠缩小单个器件拿不到性能了；'
      '<tspan font-weight="600" fill="%s">2019 年</tspan>——EUV 量产，图形化第一次不再受波长限制。</text>' % (INK2, INK, ACCENT))
    a('    <text x="50" y="450" font-size="12" fill="%s">但节点号仍在按节奏前进：90nm 用了 8 年（2004→2012 量级），14nm→7nm 约 3 年，7nm→2nm 约 7 年 —— <tspan font-weight="600" fill="%s">节奏变慢不是因为做不出来，而是每一步都要更贵的设备和更难的良率</tspan>。</text>' % (INK2, INK))
    a('    <text x="50" y="476" font-size="11.5" fill="%s">2026 年处在 2nm 与 GAA 的窗口：物理尺寸已近极限，性能增量改由封装、三维结构与材料承担。</text>' % MUTED)
    a('  </g>')
    a('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    print(fig1())
    print('<!-- ===== -->')
    print(fig2())
    print('已生成 semi_fig1.svg / semi_fig2.svg')
