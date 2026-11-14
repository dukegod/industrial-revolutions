#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「物理层三个岔路：现状与判定条件」SVG。

用法：python3 scripts/figures/gen_forks.py（打印 SVG）
      或由 scripts/figures/build_figures.py 统一生成 / 回写。

[INPUT]: depends on wiki/10-能源与工业革命.md
[OUTPUT]: exports the three-fork figure of the physical layer with its decision conditions
[POS]: the producer of the physical-layer fork figure
[PROTOCOL]: Update this header on change, then check CLAUDE.md
"""

FORKS = [
    {
        'id': 'cooling',
        'title': '岔路一 · 散热形态',
        'branches': [('冷板式', '#2f6f5e'), ('浸没式', '#c97b3f')],
        'settled': ['2025 年中国液冷市场中冷板式占 93.5%',
                    '未来 3–5 年仍是主流方案',
                    'GB/T 48023-2026 冷板式液冷国标',
                    '2026-08 发布、2027-02 实施'],
        'trigger': ['单柜功率 >200kW 时浸没才占优',
                    '100 柜 × 20kW：浸没初始投资高约 1000 万',
                    '年省 190 万，6 年是 TCO 交叉点'],
        'unknown': ['冷却液工质无统一标准',
                    '（硅油 / 氟化液 / PG25 / EG25 / 去离子水）',
                    '浸没式液冷液占系统价值量约 60%'],
    },
    {
        'id': 'chip',
        'title': '岔路二 · 芯片形态',
        'branches': [('通用 GPU', '#2f6f5e'), ('定制 ASIC', '#c97b3f')],
        'settled': ['2026 年定制 ASIC 出货增速 44.6%',
                    '首次超过商用 GPU 的 16.1%',
                    'NVIDIA 仍约占 AI 芯片 70%',
                    '共设计市场 Broadcom+Marvell 约 95%'],
        'trigger': ['工作负载是否固定',
                    '推理侧架构稳定、重复到十亿级，定制才划算',
                    '训练与研究侧仍需通用性'],
        'unknown': ['定制芯片是多代 co-design 的对赌',
                    '模型架构换代，已定制的硅成沉没成本',
                    '成本数亿美元 + 2–3 年，须靠规模摊薄'],
    },
    {
        'id': 'stack',
        'title': '岔路三 · 堆叠形态',
        'branches': [('混合键合', '#2f6f5e'), ('微凸点', '#c97b3f')],
        'settled': ['混合键合逻辑侧已量产',
                    'SoIC 6μm · Foveros Direct 9μm',
                    'Foveros Direct 2026 上半年出货',
                    '内存侧被推迟'],
        'trigger': ['JEDEC 2026-01 放宽 HBM 高度上限',
                    '（775μm），HBM4 16 层可继续用微凸点',
                    '混合键合推迟到 HBM4E / HBM5'],
        'unknown': ['逻辑堆叠现量产仅 2–3 层',
                    '三道闸门叠加：reticle 858mm²、',
                    '层数良率相乘、逐层热阻累加',
                    '8–16 层仍在论文阶段'],
    },
]

X_NAME = 14
X_SET, W_SET = 200, 292
X_TRG, W_TRG = 516, 302
X_UNK, W_UNK = 842, 330
BLOCK_H = 152
GAP = 14
TOP_H = 46
VIEW_W = 1190
VIEW_H = TOP_H + 3 * BLOCK_H + 2 * GAP + 32


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def gen():
    o = []
    a = o.append
    a('<svg class="forkfig" data-forks="cooling|chip|stack" data-forknames="散热形态|芯片形态|堆叠形态" viewBox="0 0 %d %d" width="100%%" style="display:block;height:auto" role="img" aria-label="物理层的三个岔路：散热形态冷板与浸没、芯片形态通用GPU与定制ASIC、堆叠形态混合键合与微凸点；每条给出已定型的现状、岔路口的判定条件，以及仍然不确定的部分">'
      % (VIEW_W, VIEW_H))
    a('  <g font-family="Outfit, \'PingFang SC\', sans-serif">')

    a('    <rect x="0" y="0" width="%d" height="%d" rx="10" fill="#2f6f5e" fill-opacity=".07" stroke="#2f6f5e" stroke-opacity=".22"/>'
      % (VIEW_W, TOP_H - 8))
    a('    <text x="%d" y="26" font-size="12.5" fill="#3a4256">三条岔路都<tspan font-weight="600" fill="#14171e">已经有了判定条件</tspan>——不再是不确定，而是「在什么条件下换道」：换道的门槛与时间表都已给出，剩下的不确定项单独列出。</text>'
      % (X_NAME))

    y = TOP_H
    for f in FORKS:
        a('    <rect x="0" y="%d" width="%d" height="%d" rx="12" fill="#fff" stroke="#e9e3d6"/>' % (y, VIEW_W, BLOCK_H))
        a('    <rect x="0" y="%d" width="4" height="%d" rx="2" fill="#2f6f5e"/>' % (y, BLOCK_H))

        a('    <text x="%d" y="%d" font-size="13" font-weight="600" fill="#14171e">%s</text>' % (X_NAME + 12, y + 30, esc(f['title'])))
        for i, (nm, col) in enumerate(f['branches']):
            a('    <text x="%d" y="%d" font-size="11.5" fill="%s">%s</text>' % (X_NAME + 12, y + 60 + i * 22, col, esc(nm)))
            a('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2" opacity=".55"/>'
              % (X_NAME + 78, y + 56 + i * 22, X_NAME + 96, y + 56 + i * 22, col))

        cols = [
            (X_SET, W_SET, '已定型的现状', '#2f6f5e', f['settled'], '#3a4256'),
            (X_TRG, W_TRG, '岔路口的判定条件', '#c97b3f', f['trigger'], '#3a4256'),
            (X_UNK, W_UNK, '仍然不确定', '#b3aea2', f['unknown'], '#7c7a72'),
        ]
        for cx, cw, label, lcol, lines, tcol in cols:
            a('    <text x="%d" y="%d" font-size="10.5" font-family="JetBrains Mono, monospace" fill="%s">%s</text>'
              % (cx, y + 30, lcol, esc(label)))
            for i, ln in enumerate(lines):
                a('    <text x="%d" y="%d" font-size="11.5" fill="%s">%s</text>' % (cx, y + 53 + i * 20, tcol, esc(ln)))
        a('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#e9e3d6"/>' % (X_SET + W_SET + 10, y + 16, X_SET + W_SET + 10, y + BLOCK_H - 16))
        a('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#e9e3d6"/>' % (X_TRG + W_TRG + 10, y + 16, X_TRG + W_TRG + 10, y + BLOCK_H - 16))
        y += BLOCK_H + GAP

    a('    <text x="%d" y="%d" font-size="10.5" fill="#7c7a72">来源与口径见 wiki「08 数据来源与口径」；灰字一栏为当前确实没有定论的部分，不做推测。</text>'
      % (X_NAME, VIEW_H - 12))
    a('  </g>')
    a('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    print(gen())
