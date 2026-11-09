#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SVG 几何检查 —— 找出「肉眼看不出来」的排版事故。

检查五项：
1. **同基线文本重叠** —— 同一行基线（|Δy| ≤ 3px）上两段文本横向相交或贴得过近。
2. **画布越界** —— 文本横向超出 viewBox。
3. **文字溢出所属色块** —— 文字所在的最小矩形装不下它（检测器只查画布边界时
   查不出这一类；上一轮据此在半导体图 1 上抓到 6 处）。
4. **SVG 内混入 HTML 标签** —— `<b>` / `<strong>` / `<br>` 等，浏览器会把它们
   当未知元素，内容会被甩出画布。
5. **id 重复** —— 同一张图里渐变 / marker 的 id 必须唯一，否则 `url(#gup1)`
   会串到第一张图上。

用法：
    python3 scripts/figures/check_svg.py                 # 检查全站页面里的所有图
    python3 scripts/figures/check_svg.py 某个.svg        # 检查单个文件
    python3 scripts/figures/check_svg.py 03-third.html   # 检查某个页面
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SITE = ROOT / 'visualization'

sys.path.insert(0, str(HERE))

import svgutil  # noqa: E402

# 文本贴边的容忍度：小于这个像素间距视为「贴太近」
NEAR_GAP = 4
# 文字溢出色块的容忍度
BLOCK_TOL = 4


def check_svg(svg):
    """返回问题列表。"""
    problems = []
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if not vb:
        return ['缺少 viewBox']
    vw = float(vb.group(1))

    items = svgutil.texts_of(svg)
    rects = svgutil.rects_of(svg)

    boxes = []
    for x, y, fs, anchor, text in items:
        left, right = svgutil.text_span(x, y, fs, anchor, text)
        boxes.append((left, y, right, text, anchor))
        # 1) 画布越界
        if right > vw or left < 0:
            problems.append('越界 「%s」 [%s] 左=%.0f 右=%.0f 画布=%.0f'
                            % (text[:26], anchor, left, right, vw))
            continue
        # 2) 文字溢出所属色块
        cands = [r for r in rects
                 if r[0] <= x <= r[0] + r[2] and r[1] <= y <= r[1] + r[3]]
        if cands:
            rx, ry, rw, rh = min(cands, key=lambda r: r[2] * r[3])
            if right > rx + rw + BLOCK_TOL:
                problems.append('溢出色块 「%s」 右端 %.0f 超出所属块右边界 %.0f（块 %.0f,%.0f %.0fx%.0f）'
                                % (text[:26], right, rx + rw, rx, ry, rw, rh))

    # 3) 同基线重叠 / 贴太近
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            if abs(a[1] - b[1]) > 3:
                continue
            gap = max(b[0], a[0]) - min(a[2], b[2])
            if a[2] > b[0] and b[2] > a[0]:
                if gap >= NEAR_GAP:
                    continue
                problems.append('重叠/贴边 「%s」 [%.0f-%.0f] × 「%s」 [%.0f-%.0f] @y=%.0f 间隙=%.0f'
                                % (a[3][:22], a[0], a[2], b[3][:22], b[0], b[2], a[1], gap))
            elif -12 < gap < NEAR_GAP:
                problems.append('间隙不足 「%s」 [%.0f-%.0f] × 「%s」 [%.0f-%.0f] @y=%.0f 间隙=%.0f'
                                % (a[3][:22], a[0], a[2], b[3][:22], b[0], b[2], a[1], gap))

    # 4) SVG 内混入 HTML 标签
    for tag in ('b', 'strong', 'br', 'i', 'em', 'div', 'span'):
        if re.search(r'<%s[ >]' % tag, svg):
            problems.append('SVG 内混入非法 HTML 标签 <%s>' % tag)

    # 5) id 重复
    ids = re.findall(r'\sid="([^"]+)"', svg)
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        problems.append('id 重复：%s' % ', '.join(sorted(dup)))

    return problems


def collect(targets):
    """产出 (名称, svg 文本) 列表。"""
    out = []
    for t in targets:
        if t.suffix == '.svg':
            out.append((t.name, t.read_text(encoding='utf-8')))
        elif t.suffix == '.html':
            text = t.read_text(encoding='utf-8')
            for i, (_s, _e, block) in enumerate(svgutil.iter_svgs(text), 1):
                if 'viewBox="0 0 24 24"' in block:
                    continue          # 导航图标
                out.append(('%s#%d' % (t.name, i), block))
    return out


def main():
    if len(sys.argv) > 1:
        targets = [Path(a) for a in sys.argv[1:]]
    else:
        targets = sorted(p for p in SITE.glob('*.html')
                         if p.name != 'computer-architecture-evolution.html')

    total, bad, svg_count = 0, 0, 0
    for name, svg in collect(targets):
        svg_count += 1
        problems = check_svg(svg)
        total += len(problems)
        if problems:
            bad += 1
            print('✗ %s' % name)
            for p in problems:
                print('    %s' % p)
    print('\n检查 %d 张图，问题 %d 处（%d 张图有问题）' % (svg_count, total, bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
