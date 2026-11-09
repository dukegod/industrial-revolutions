#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""比对「页面里嵌的 SVG」与「生成器输出」是否逐字一致。

防止**脚本改了、页面没改**这类漂移 —— 页面照旧显示旧图，脚本却以为已经更新，
下一次回写就会把页面整体改掉，肉眼很难发现。

用法：
    python3 scripts/figures/verify_embedded.py          # 全量比对
    python3 scripts/figures/verify_embedded.py 05-fig3  # 只比某一张

退出码 0 = 全部一致。
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SITE = ROOT / 'visualization'

sys.path.insert(0, str(HERE))

import registry   # noqa: E402
import svgutil    # noqa: E402
from build_figures import generate  # noqa: E402


def first_diff(a, b):
    """返回两段文本第一处不同的上下文，便于定位。"""
    la, lb = a.split('\n'), b.split('\n')
    for i, (x, y) in enumerate(zip(la, lb), 1):
        if x != y:
            return '第 %d 行不同：\n      页面：%s\n      生成：%s' % (i, x[:120], y[:120])
    if len(la) != len(lb):
        return '行数不同：页面 %d 行，生成 %d 行' % (len(la), len(lb))
    return '内容相同但格式不同'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ids', nargs='*')
    args = ap.parse_args()

    specs = registry.FIGURES
    if args.ids:
        specs = [s for s in specs if s['id'] in args.ids]
        unknown = set(args.ids) - {s['id'] for s in specs}
        if unknown:
            print('未知图 id：%s' % ', '.join(sorted(unknown)))
            return 1

    bad = 0
    for spec in specs:
        svg = generate(spec)
        path = SITE / spec['page']
        text = path.read_text(encoding='utf-8')
        hit = svgutil.find_svg(text, spec['locate'])
        if hit is None:
            bad += 1
            print('✗ %-16s 在 %s 里按 %s 找不到这张图' % (spec['id'], spec['page'], spec['locate'][1]))
            continue
        _s, _e, block = hit
        if svgutil.normalize(block) == svgutil.normalize(svg):
            print('✓ %-16s %s' % (spec['id'], spec['page']))
        else:
            bad += 1
            print('✗ %-16s %s —— 与生成器不一致' % (spec['id'], spec['page']))
            print('    %s' % first_diff(svgutil.normalize(block), svgutil.normalize(svg)))

    print('\n比对 %d 张图，%d 张与生成器不一致' % (len(specs), bad))
    if bad:
        print('跑 `python3 scripts/figures/build_figures.py --splice` 回写页面。')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
