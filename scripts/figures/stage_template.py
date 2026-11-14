#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""「台阶放大图」的共用渲染模板 —— 计算线与连接/接入线共用，保证两套图结构完全一致。

几何（与已入库的四张计算线台阶图逐像素一致）：
  顶部绿带 y=26..90；列头基线 106；带起点 118；带高 126（两行内容）/148（三行）；
  底部暖色带 h=64（两行）/80（三行）。

[INPUT]: depends on nothing
[OUTPUT]: exports render(), the shared layout template for the three families of zoom-in figures
[POS]: the shared template; it guarantees the compute-line and connection-line families are structurally identical
[PROTOCOL]: Update this header on change, then check CLAUDE.md
"""

BAND_TOP = 26
BAND_H = 64
COL_HEAD_Y = 106
ROW_Y0 = 118
ROW_H = 126
ROW_H3 = 148
FOOT_Y2 = 116
FOOT_Y3 = 138
DIV_Y2 = 94
DIV_Y3 = 116
COL_X1, COL_X2, COL_X3 = 62, 270, 580
R1, R2 = 40, 898
BAND_W = 880


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def render(step, idx, head1='跃迁 · 名称', attrs='', grad='', div_right=None):
    """step: {aria, top:[2], bands:[{label,title,period,sub,tech[],rule[],down,up}], bottom:[2|3]}

    attrs：写进 <svg> 开标签的额外属性（class / data-*），供页面对齐校验脚本读取。
    grad：渐变 id 前缀。三族图同页共存时 id 必须互不相同，否则 url(#gup1) 会串到
          第一张图上。入库版本用的是：计算线台阶 ''、连接线阶段 '10'、物理段 '20'，
          这里沿用同一套，保证回写后与页面逐字一致。
    div_right：每条带里那条分隔线的右端点。默认 R2-22；计算线台阶图入库时用的是
          R2（898），两族差 22px，各族单独定。
    """
    y = ROW_Y0
    for b in step['bands']:
        y += (ROW_H if max(len(b['tech']), len(b['rule'])) <= 2 else ROW_H3) + 12
    bh = 64 if len(step['bottom']) == 2 else 80
    canvas_h = y + bh + 14
    if div_right is None:
        div_right = R2 - 22

    o = []
    a = o.append
    a('<svg%s viewBox="0 0 960 %d" width="100%%" style="display:block;height:auto" role="img" aria-label="%s">'
      % (attrs, canvas_h, esc(step['aria'])))
    a('        <defs>')
    a('          <linearGradient id="gup%s%d" x1="0" y1="0" x2="0" y2="1">' % (grad, idx))
    a('            <stop offset="0" stop-color="#2f6f5e" stop-opacity=".16"/>')
    a('            <stop offset="1" stop-color="#2f6f5e" stop-opacity=".05"/>')
    a('          </linearGradient>')
    a('          <linearGradient id="gdn%s%d" x1="0" y1="0" x2="0" y2="1">' % (grad, idx))
    a('            <stop offset="0" stop-color="#c97b3f" stop-opacity=".07"/>')
    a('            <stop offset="1" stop-color="#c97b3f" stop-opacity=".20"/>')
    a('          </linearGradient>')
    a('        </defs>')
    a('        <g font-family="Outfit, \'PingFang SC\', sans-serif">')
    a('')
    a('          <rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="url(#gup%s%d)" stroke="#2f6f5e" stroke-opacity=".35"/>'
      % (R1, BAND_TOP, BAND_W, BAND_H, grad, idx))
    a('          <text x="%d" y="53" font-size="13" font-weight="600" fill="#2f6f5e">%s</text>' % (COL_X1, esc(step['top'][0])))
    a('          <text x="%d" y="75" font-size="11.5" fill="#3a4256">%s</text>' % (COL_X1, esc(step['top'][1])))
    a('')
    a('          <g font-size="10.5" fill="#7c7a72" font-family="JetBrains Mono, monospace">')
    a('            <text x="%d" y="%d">%s</text>' % (COL_X1, COL_HEAD_Y, esc(head1)))
    a('            <text x="%d" y="%d">带来了什么新技术</text>' % (COL_X2, COL_HEAD_Y))
    a('            <text x="%d" y="%d">改变了什么规则</text>' % (COL_X3, COL_HEAD_Y))
    a('          </g>')
    a('')
    yy = ROW_Y0
    for b in step['bands']:
        nn = max(len(b['tech']), len(b['rule']))
        hh = ROW_H if nn <= 2 else ROW_H3
        dv = DIV_Y2 if nn <= 2 else DIV_Y3
        fy = FOOT_Y2 if nn <= 2 else FOOT_Y3
        a('          <rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="#fff" stroke="#e9e3d6"/>' % (R1, yy, BAND_W, hh))
        a('          <rect x="%d" y="%d" width="5" height="%d" rx="2.5" fill="#2f6f5e"/>' % (R1, yy, hh))
        a('          <text x="%d" y="%d" font-size="14"><tspan fill="#14171e" font-weight="600">%s</tspan><tspan fill="#2f6f5e" font-weight="600"> · %s</tspan></text>'
          % (COL_X1, yy + 32, esc(b['label']), esc(b['title'])))
        a('          <text x="%d" y="%d" font-size="11" font-family="JetBrains Mono, monospace" fill="#7c7a72">%s</text>'
          % (COL_X1, yy + 54, esc(b['period'])))
        a('          <text x="%d" y="%d" font-size="11.5" fill="#3a4256">%s</text>' % (COL_X1, yy + 74, esc(b['sub'])))
        for i, line in enumerate(b['tech']):
            a('          <text x="%d" y="%d" font-size="12.5" fill="#3a4256">%s</text>' % (COL_X2, yy + 32 + i * 22, esc(line)))
        for i, line in enumerate(b['rule']):
            a('          <text x="%d" y="%d" font-size="12.5" fill="#3a4256">%s</text>' % (COL_X3, yy + 32 + i * 22, esc(line)))
        a('          <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#e9e3d6"/>' % (COL_X1, yy + dv, div_right, yy + dv))
        a('          <text x="%d" y="%d" font-size="11" fill="#c97b3f">↓ 压给下面：%s</text>' % (COL_X1, yy + fy, esc(b['down'])))
        a('          <text x="%d" y="%d" font-size="11" fill="#2f6f5e">↑ 交付给上层：%s</text>' % (COL_X3, yy + fy, esc(b['up'])))
        a('')
        yy += hh + 12
    a('          <rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="url(#gdn%s%d)" stroke="#c97b3f" stroke-opacity=".35"/>'
      % (R1, yy, BAND_W, bh, grad, idx))
    a('          <text x="%d" y="%d" font-size="13" font-weight="600" fill="#c97b3f">%s</text>' % (COL_X1, yy + 27, esc(step['bottom'][0])))
    for i, line in enumerate(step['bottom'][1:]):
        a('          <text x="%d" y="%d" font-size="11.5" fill="#3a4256">%s</text>' % (COL_X1, yy + 49 + i * 22, esc(line)))
    a('        </g>')
    a('      </svg>')
    return '\n'.join(o)
