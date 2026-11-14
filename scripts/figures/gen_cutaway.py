#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「同一套抽象结构的两套物理实现」SVG。

用法：python3 scripts/figures/gen_cutaway.py（打印 SVG）
      或由 scripts/figures/build_figures.py 统一生成 / 回写。

[INPUT]: depends on nothing from the repo; the mapping table below is this file's only source of truth
[OUTPUT]: exports the gen() function, returning the "电子管时代 vs 集成电路时代" SVG text
[POS]: the sole producer of the 04-cutaway figure in 04-architecture.html; it renders the component-level view that the seven-layer stack figure abstracts away
[PROTOCOL]: Update this header on change, then check CLAUDE.md

图的结构：左列是电子管时代的实物部件，中间是两个时代共用的抽象层，右列是集成电路时代的实物部件，
底带说明稀缺换了位置。左右两列的箭头指向中间 —— 抽象层没变，变的只是它落在什么硬件上。
"""

VB_W, VB_H = 960, 556

HEAD_Y, HEAD_H = 14, 42
ROW_Y0, ROW_H, ROW_GAP = 70, 48, 6

L_X, L_W = 24, 258          # 电子管时代实物
M_X, M_W = 306, 336         # 抽象层
R_X, R_W = 666, 270         # 集成电路时代实物

BAND_Y, BAND_H = 458, 76

# (抽象层, 该层职责, 电子管时代实物, 集成电路时代实物)
ROWS = [
    ('运算器 · 控制器', '完成算术运算与取指', '电子管与继电器搭出的运算与控制逻辑', 'CPU 内部的运算器与控制器'),
    ('存储器', '暂存程序与中间结果', '汞延迟线 · 磁鼓 · 继电器矩阵', 'DRAM 内存条 · HBM · NVMe 固态盘'),
    ('指令与数据入口', '把程序与数据送进来', '穿孔卡片 · 纸带读入机', '键盘 · 触摸 · 网卡'),
    ('结果出口', '把结果送出去', '纸带输出机 · 曲线仪', '显示器 · 模型 API'),
    ('互联', '把各部件接在一起', '接线盘 · 同轴电缆 · 继电器矩阵', 'PCIe · NVLink · 以太网'),
    ('能源', '提供稳定电压与电流', '高压直流电源 · 灯丝供电', '电源单元 · 高压直流'),
    ('散热', '把热带走', '离心鼓风机与风道', '风扇 · 均热板 · 液冷冷板'),
]


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def gen():
    o = []
    a = o.append
    a('<svg viewBox="0 0 %d %d" width="100%%" style="display:block;height:auto" role="img" aria-label="同一套抽象结构的两套物理实现：左列是电子管时代的实物部件，中间是两个时代共用的抽象层，右列是集成电路时代的实物部件，左右箭头指向中间说明抽象结构没变；底带说明稀缺从体积与发热下沉到硅、内存带宽与电力">'
      % (VB_W, VB_H))
    a('  <defs>')
    a('    <marker id="cutArrL" markerWidth="8" markerHeight="8" refX="6.5" refY="2.8" orient="auto">')
    a('      <path d="M0,0 L6.5,2.8 L0,5.6 Z" fill="#2f6f5e"/>')
    a('    </marker>')
    a('    <marker id="cutArrR" markerWidth="8" markerHeight="8" refX="6.5" refY="2.8" orient="auto">')
    a('      <path d="M0,0 L6.5,2.8 L0,5.6 Z" fill="#2f6f5e"/>')
    a('    </marker>')
    a('  </defs>')
    a('  <g font-family="Outfit, \'PingFang SC\', sans-serif">')

    # ── 表头 ────────────────────────────────────────────────
    heads = [
        (L_X, L_W, '电子管时代 · 实物形态', '1945–1957'),
        (M_X, M_W, '抽象层 · 两个时代共用', '逻辑结构没有变，变的只是它落在什么硬件上'),
        (R_X, R_W, '集成电路时代 · 实物形态', '2020s'),
    ]
    for x, w, title, sub in heads:
        cx = x + w // 2
        a('    <rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="#fff" stroke="#e9e3d6"/>' % (x, HEAD_Y, w, HEAD_H))
        a('    <text x="%d" y="%d" font-size="13" font-weight="600" fill="#14171e" text-anchor="middle">%s</text>' % (cx, HEAD_Y + 20, esc(title)))
        a('    <text x="%d" y="%d" font-size="10.5" fill="#7c7a72" text-anchor="middle">%s</text>' % (cx, HEAD_Y + 35, esc(sub)))
    a('')

    # ── 行 ──────────────────────────────────────────────────
    for i, (layer, role, old, new) in enumerate(ROWS):
        y = ROW_Y0 + i * (ROW_H + ROW_GAP)
        a('    <rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="#fff" stroke="#e9e3d6"/>' % (L_X, y, L_W, ROW_H))
        a('    <rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="#f7f4ec" stroke="#e9e3d6"/>' % (M_X, y, M_W, ROW_H))
        a('    <rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="#fff" stroke="#e9e3d6"/>' % (R_X, y, R_W, ROW_H))
        a('    <rect x="%d" y="%d" width="5" height="%d" rx="2.5" fill="#2f6f5e"/>' % (M_X, y, ROW_H))

        a('    <text x="%d" y="%d" font-size="12" fill="#3a4256">%s</text>' % (L_X + 12, y + 29, esc(old)))
        a('    <text x="%d" y="%d" font-size="12.5" font-weight="600" fill="#14171e">%s</text>' % (M_X + 14, y + 21, esc(layer)))
        a('    <text x="%d" y="%d" font-size="10.5" fill="#7c7a72">%s</text>' % (M_X + 14, y + 38, esc(role)))
        a('    <text x="%d" y="%d" font-size="12" fill="#3a4256">%s</text>' % (R_X + 12, y + 29, esc(new)))

        mid = y + ROW_H // 2
        a('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#2f6f5e" stroke-width="1.4" marker-end="url(#cutArrL)" opacity=".8"/>'
          % (L_X + L_W + 4, mid, M_X - 4, mid))
        a('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#2f6f5e" stroke-width="1.4" marker-end="url(#cutArrR)" opacity=".8"/>'
          % (R_X - 4, mid, M_X + M_W + 4, mid))
    a('')

    # ── 底带：稀缺换了位置 ───────────────────────────────────
    a('    <rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="#c97b3f" fill-opacity=".08" stroke="#c97b3f" stroke-opacity=".45"/>'
      % (L_X, BAND_Y, VB_W - 2 * L_X, BAND_H))
    a('    <text x="%d" y="%d" font-size="13" font-weight="600" fill="#a9663a">稀缺没有消失，它换了位置</text>' % (L_X + 16, BAND_Y + 26))
    a('    <text x="%d" y="%d" font-size="11.5" fill="#3a4256">电子管时代 ↓ 压给下面：体积、发热与灯丝供电 —— 稀缺是「机器有多大、耗多少电」</text>' % (L_X + 16, BAND_Y + 48))
    a('    <text x="%d" y="%d" font-size="11.5" fill="#3a4256">集成电路时代 ↓ 压给下面：硅制程、内存带宽与电力 —— 稀缺是「算力够不够、内存等不等得起」</text>' % (L_X + 16, BAND_Y + 68))
    a('  </g>')
    a('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    print(gen())
