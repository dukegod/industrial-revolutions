#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「第三次革命的三条线」SVG。

用法：python3 scripts/figures/gen_twolines.py（打印 SVG）
      或由 scripts/figures/build_figures.py 统一生成 / 回写。
"""

COL_X = [116, 314, 512, 710]
COL_W = 190
LABEL_W = 112
AXIS_Y = 40
L1_Y, L1_H = 92, 90
L2_Y, L2_H = 202, 90
HL_X, HL_W = 512, 190
MERGE_X, MERGE_Y, MERGE_W, MERGE_H = 916, 146, 168, 102
PHYS_Y, PHYS_H = 316, 66
NOTE_Y, NOTE_H = 400, 60
VB_W, VB_H = 1100, 486

PERIODS = [
    ('1945–1995', '奠基期'),
    ('1995–2005', '扩散期'),
    ('2006–2015', '拐点'),
    ('2016–2026', '规模化'),
]

LANES = [
    {
        'name': '计算线', 'note': '算力怎么变便宜', 'y': L1_Y, 'h': L1_H,
        'blocks': [
            ['存储程序 · ISA 契约', '流水线 / Cache'],
            ['多核 / SMP'],
            ['GPU / CUDA', '移动 SoC'],
            ['数据中心专用化', '→ AI 工厂'],
        ],
    },
    {
        'name': '连接与接入线', 'note': '算力怎么送到人手里', 'y': L2_Y, 'h': L2_H,
        'blocks': [
            ['ARPANET → TCP/IP', '→ 万维网'],
            ['宽带 · Web 2.0'],
            ['云计算（2006）', 'iPhone（2007）· 4G', '→ 移动优先'],
            ['5G · 流媒体', '端侧模型'],
        ],
    },
]


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def gen():
    o = []
    a = o.append
    a('<svg viewBox="0 0 %d %d" width="100%%" style="display:block;height:auto" role="img" aria-label="第三次革命的三条线：计算线与连接接入线并行推进，2006到2015年两条线同时到拐点，之后合流为云端算力加口袋终端，也就是今天 Agent 平台的结构原型；底部虚线带是托着它们的物理基础">'
      % (VB_W, VB_H))
    a('  <defs>')
    a('    <marker id="tArrow" markerWidth="8" markerHeight="8" refX="6.5" refY="2.8" orient="auto">')
    a('      <path d="M0,0 L6.5,2.8 L0,5.6 Z" fill="#2f6f5e"/>')
    a('    </marker>')
    a('    <marker id="tArrowR" markerWidth="8" markerHeight="8" refX="6.5" refY="2.8" orient="auto">')
    a('      <path d="M0,0 L6.5,2.8 L0,5.6 Z" fill="#c97b3f"/>')
    a('    </marker>')
    a('  </defs>')
    a('  <g font-family="Outfit, \'PingFang SC\', sans-serif">')

    # 高亮带：2006–2015 交汇列
    a('    <rect x="%d" y="6" width="%d" height="294" rx="12" fill="#c97b3f" fill-opacity=".07" stroke="#c97b3f" stroke-opacity=".45" stroke-dasharray="6 4"/>'
      % (HL_X, HL_W))

    # 时间轴
    centers = [x + COL_W // 2 for x in COL_X]
    a('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#2f6f5e" stroke-width="1.6" marker-end="url(#tArrow)" opacity=".85"/>'
      % (centers[0], AXIS_Y, 900, AXIS_Y))
    for i, (p, ph) in enumerate(PERIODS):
        cx = centers[i]
        hot = (i == 2)
        col = '#c97b3f' if hot else '#2f6f5e'
        a('    <circle cx="%d" cy="%d" r="6" fill="#fff" stroke="%s" stroke-width="2.4"/>' % (cx, AXIS_Y, col))
        a('    <text x="%d" y="62" font-size="13" font-weight="600" fill="#14171e" text-anchor="middle">%s</text>' % (cx, esc(p)))
        a('    <text x="%d" y="79" font-size="10.5" font-family="JetBrains Mono, monospace" fill="%s" text-anchor="middle">%s</text>' % (cx, col, esc(ph)))
    a('')

    # 两条泳道
    for lane in LANES:
        y, h = lane['y'], lane['h']
        a('    <text x="14" y="%d" font-size="12.5" font-weight="600" fill="#14171e">%s</text>' % (y + 30, esc(lane['name'])))
        a('    <text x="14" y="%d" font-size="10.5" fill="#7c7a72">%s</text>' % (y + 47, esc(lane['note'])))
        for c in range(4):
            x = COL_X[c]
            hot = (c == 2)
            a('    <rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="%s" stroke="%s"/>'
              % (x, y, COL_W, h, '#fff' if not hot else '#fdf7f1',
                 '#e9e3d6' if not hot else '#c97b3f'))
            lines = lane['blocks'][c]
            base = y + (30 if len(lines) == 1 else (22 if len(lines) == 2 else 20))
            for li, ln in enumerate(lines):
                a('    <text x="%d" y="%d" font-size="11.5" fill="#3a4256">%s</text>' % (x + 12, base + li * 19, esc(ln)))
            if c < 3:
                a('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#c9c3b6" stroke-width="1.4" marker-end="url(#tArrow)"/>'
                  % (x + COL_W + 2, y + h // 2, x + COL_W + 6, y + h // 2))
        a('')

    # gutter chip：交汇标注
    a('    <rect x="%d" y="%d" width="120" height="20" rx="10" fill="#c97b3f" fill-opacity=".16" stroke="#c97b3f" stroke-opacity=".5"/>'
      % (HL_X + 35, L1_Y + L1_H))
    a('    <text x="%d" y="%d" font-size="10.5" font-weight="600" fill="#a9663a" text-anchor="middle">两条线同时到拐点</text>'
      % (HL_X + 95, L1_Y + L1_H + 14))
    a('')

    # 合流块
    a('    <path d="M902,140 C 912,150 912,168 916,178" fill="none" stroke="#c97b3f" stroke-width="1.6" marker-end="url(#tArrowR)"/>')
    a('    <path d="M902,250 C 912,246 912,232 916,222" fill="none" stroke="#c97b3f" stroke-width="1.6" marker-end="url(#tArrowR)"/>')
    a('    <rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="#c97b3f" fill-opacity=".12" stroke="#c97b3f" stroke-opacity=".5"/>'
      % (MERGE_X, MERGE_Y, MERGE_W, MERGE_H))
    a('    <text x="%d" y="%d" font-size="12.5" font-weight="600" fill="#14171e" text-anchor="middle">云端算力 + 口袋终端</text>'
      % (MERGE_X + MERGE_W // 2, MERGE_Y + 28))
    a('    <text x="%d" y="%d" font-size="11" fill="#3a4256" text-anchor="middle">= 今天 Agent 平台</text>'
      % (MERGE_X + MERGE_W // 2, MERGE_Y + 50))
    a('    <text x="%d" y="%d" font-size="11" fill="#3a4256" text-anchor="middle">的结构原型</text>'
      % (MERGE_X + MERGE_W // 2, MERGE_Y + 68))
    a('    <text x="%d" y="%d" font-size="11" font-weight="600" fill="#a9663a" text-anchor="middle">→ 第四次：执行交出去</text>'
      % (MERGE_X + MERGE_W // 2, MERGE_Y + 88))
    a('')

    # 物理基础：地基带
    a('    <rect x="%d" y="%d" width="788" height="%d" rx="10" fill="#c97b3f" fill-opacity=".06" stroke="#c97b3f" stroke-opacity=".3" stroke-dasharray="6 4"/>'
      % (LABEL_W, PHYS_Y, PHYS_H))
    a('    <text x="14" y="%d" font-size="12.5" font-weight="600" fill="#a9663a">物理基础</text>' % (PHYS_Y + 26))
    a('    <text x="14" y="%d" font-size="10.5" fill="#b3aea2">托着上面两条线的地基</text>' % (PHYS_Y + 43))
    PHYS = [
        '晶体管 · 平面工艺 · 光刻',
        '深亚微米 · 铜互连 · FinFET',
        'EUV · HBM · CoWoS',
        'GAA · 液冷 · High-NA EUV',
    ]
    for i, cell in enumerate(PHYS):
        x = COL_X[i]
        a('    <text x="%d" y="%d" font-size="11.5" fill="#8a5a30">%s</text>' % (x + 12, PHYS_Y + 40, esc(cell)))
        if i:
            a('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#e9e3d6"/>' % (x - 4, PHYS_Y + 10, x - 4, PHYS_Y + PHYS_H - 10))
    a('')

    # 注记：稀缺迁移
    a('    <rect x="%d" y="%d" width="784" height="%d" rx="10" fill="#2f6f5e" fill-opacity=".05" stroke="#e9e3d6"/>'
      % (LABEL_W, NOTE_Y, NOTE_H))
    a('    <text x="%d" y="%d" font-size="11.5" fill="#3a4256">算力变便宜 → 稀缺转向<tspan font-weight="600" fill="#14171e">注意力与信任</tspan>（第三次留给我们的） → 转向<tspan font-weight="600" fill="#14171e">目标与责任</tspan>（第四次要接手的）</text>'
      % (LABEL_W + 16, NOTE_Y + 26))
    a('    <text x="%d" y="%d" font-size="10.5" fill="#7c7a72">三条线缺一条都不成立：物理层管「能不能造出来」，计算线管「怎么算」，连接与接入线管「怎么送」</text>'
      % (LABEL_W + 16, NOTE_Y + 46))
    a('  </g>')
    a('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    print(gen())
