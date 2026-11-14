#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「算力过剩之后：瓶颈从技术问题变成供给问题」图。

用法：python3 scripts/figures/gen_semi3.py（打印 SVG）
      或由 scripts/figures/build_figures.py 统一生成 / 回写。

[INPUT]: depends on wiki/09-半导体的发展进程.md
[OUTPUT]: exports the figure on how the bottleneck changes character in leap 7
[POS]: the producer of the third semiconductor figure
[PROTOCOL]: Update this header on change, then check CLAUDE.md
"""

INK, INK2, MUTED, LINE, ACCENT, RUST = '#14171e', '#3a4256', '#7c7a72', '#e9e3d6', '#2f6f5e', '#c97b3f'

NODES = [
    ('跃迁 1', '电子管 / 晶体管', '造不出更快的器件', 's'),
    ('跃迁 2', 'ISA 商业化', '造不便宜、买不到', 's'),
    ('跃迁 3', 'RISC / Cache', '访存延迟', 's'),
    ('跃迁 4', '多核 / SMP', '顺序代码不够用', 's'),
    ('跃迁 5', 'GPU / CUDA', '并行编程太难', 's'),
    ('跃迁 6', '数据中心专用化', '集群带不动', 's'),
    ('跃迁 7', '内存墙 / AI 工厂', '算力有了，数据供不上', 'h'),
    ('跃迁 8', 'RISC-V 底座', 'ISA 换不动了', 'h'),
]

VB_W, VB_H = 1160, 540
X0, X1 = 88, 1072
STEP = (X1 - X0) / 7
AXIS_Y = 214
BAND_Y = AXIS_Y + 84          # 298
BAND_H = 84
ROW2_Y = BAND_Y + BAND_H + 16 # 398


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def gen():
    o = []
    a = o.append
    a('<svg viewBox="0 0 %d %d" width="100%%" style="display:block;height:auto" role="img" aria-label="瓶颈的性质在跃迁 7 发生转变：前六次的瓶颈是技术问题，要靠发明与设计解决；跃迁 7 与 8 的瓶颈是供给问题，只能等产能、电力与生态">'
      % (VB_W, VB_H))
    a('  <defs>')
    a('    <marker id="r3Arrow" markerWidth="9" markerHeight="9" refX="7" refY="3.2" orient="auto">')
    a('      <path d="M0,0 L7,3.2 L0,6.4 Z" fill="%s"/>' % ACCENT)
    a('    </marker>')
    a('  </defs>')
    a('  <g font-family="Outfit, \'PingFang SC\', sans-serif">')

    # ── 顶部：两个事实 ──────────────────────────────────────────
    a('    <rect x="20" y="18" width="1120" height="86" rx="12" fill="#2f6f5e" fill-opacity=".05" stroke="#e9e3d6"/>')
    a('    <text x="40" y="44" font-size="12.5" font-weight="600" fill="%s">两个事实</text>' % INK)
    a('    <text x="620" y="44" font-size="12.5" font-weight="600" fill="%s">怎么读这两个事实</text>' % INK)
    a('    <text x="40" y="70" font-size="12" fill="%s">2 年增速：算力 <tspan font-weight="600" fill="%s">3.0×</tspan> · 内存带宽 <tspan font-weight="600" fill="%s">1.6×</tspan> · 互连 <tspan font-weight="600" fill="%s">1.4×</tspan></text>'
      % (INK2, INK, INK, INK))
    a('    <text x="40" y="92" font-size="12" fill="%s">折算 20 年：算力约 <tspan font-weight="600" fill="%s">60 万倍</tspan> · DRAM 带宽约 <tspan font-weight="600" fill="%s">100 倍</tspan> · 互连约 <tspan font-weight="600" fill="%s">30 倍</tspan></text>'
      % (INK2, INK, INK, INK))
    a('    <text x="620" y="70" font-size="11.5" fill="%s">倍数差 = 此前六次里，架构必须替存储与互连吸收掉的量</text>' % MUTED)
    a('    <text x="620" y="92" font-size="11.5" fill="%s">到 2023–2026，架构手段用尽，这笔账再也吸收不掉</text>' % MUTED)

    # ── 中部：八节点路线 ──────────────────────────────────────
    a('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#d8d2c4" stroke-width="2.4" marker-end="url(#r3Arrow)"/>'
      % (X0 - 40, AXIS_Y, X1 + 36, AXIS_Y))
    for i, (num, name, bot, kind) in enumerate(NODES):
        cx = X0 + i * STEP
        col = RUST if kind == 'h' else ACCENT
        a('    <text x="%d" y="%d" font-size="11" font-family="JetBrains Mono, monospace" fill="%s" text-anchor="middle">%s</text>'
          % (cx, AXIS_Y - 62, col, esc(num)))
        a('    <text x="%d" y="%d" font-size="12.5" font-weight="600" fill="%s" text-anchor="middle">%s</text>'
          % (cx, AXIS_Y - 42, INK, esc(name)))
        a('    <circle cx="%d" cy="%d" r="8" fill="#fff" stroke="%s" stroke-width="2.6"/>' % (cx, AXIS_Y, col))
        a('    <text x="%d" y="%d" font-size="11.5" fill="%s" text-anchor="middle">%s</text>'
          % (cx, AXIS_Y + 32, INK2, esc(bot)))
        a('    <text x="%d" y="%d" font-size="10" fill="%s" text-anchor="middle">%s</text>'
          % (cx, AXIS_Y + 52, col, '供给问题' if kind == 'h' else '技术问题'))

    # 分界线：跃迁 6 与 7 之间
    sx = X0 + 5.5 * STEP
    a('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6" stroke-dasharray="6 4"/>'
      % (sx, AXIS_Y - 80, sx, AXIS_Y + 68, RUST))
    a('    <text x="%d" y="%d" font-size="11.5" font-weight="600" fill="%s" text-anchor="middle">跃迁 7 · 瓶颈换人</text>'
      % (sx, AXIS_Y - 88, RUST))

    # ── 底部：两类约束（上下两行通栏） ─────────────────────────
    a('    <rect x="20" y="%d" width="1120" height="%d" rx="12" fill="%s" fill-opacity=".07" stroke="%s" stroke-opacity=".3"/>'
      % (BAND_Y, BAND_H, ACCENT, ACCENT))
    a('    <text x="40" y="%d" font-size="13" font-weight="600" fill="%s">跃迁 1–6：技术问题</text>' % (BAND_Y + 26, ACCENT))
    a('    <text x="40" y="%d" font-size="11.5" fill="%s">还没被解决 —— 需要发明与设计：缓存、并发抽象、编程模型、互连与调度</text>' % (BAND_Y + 48, INK2))
    a('    <text x="40" y="%d" font-size="11.5" fill="%s">难点大，但<tspan font-weight="600" fill="%s">方向由研发决定</tspan>，不必等别人给你额度</text>' % (BAND_Y + 68, INK2, INK))

    a('    <rect x="20" y="%d" width="1120" height="%d" rx="12" fill="%s" fill-opacity=".10" stroke="%s" stroke-opacity=".45"/>'
      % (ROW2_Y, BAND_H, RUST, RUST))
    a('    <text x="40" y="%d" font-size="13" font-weight="600" fill="%s">跃迁 7–8：供给问题</text>' % (ROW2_Y + 26, RUST))
    a('    <text x="40" y="%d" font-size="11.5" fill="%s">技术已解决 —— 缺的是<tspan font-weight="600" fill="%s">产能与额度</tspan>：HBM、CoWoS、电力、机位</text>' % (ROW2_Y + 48, INK2, INK))
    a('    <text x="40" y="%d" font-size="11.5" fill="%s">只能等别人扩产：CoWoS 新增产能 2027–2028 才释放</text>' % (ROW2_Y + 68, INK2))

    a('    <text x="20" y="%d" font-size="12" fill="%s"><tspan font-weight="600" fill="%s">这条分界决定了平台建设的打法</tspan>：前六次可以靠设计与流程跨越；这一次必须先问物理账，再问组织账。</text>'
      % (ROW2_Y + BAND_H + 30, INK2, INK))
    a('  </g>')
    a('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    print(gen())
