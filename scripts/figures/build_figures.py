#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成全部登记在册的图，并（可选）回写到页面。

用法：
    python3 scripts/figures/build_figures.py            # 只生成到 out/
    python3 scripts/figures/build_figures.py --splice    # 生成并回写页面
    python3 scripts/figures/build_figures.py 05-fig3     # 只处理某一张

回写策略：一张一张替换，每张替换后重新读文件 —— 不做批量偏移替换。
（批量替换会让前一次替换改变字符串长度，后续匹配的偏移全部失效，
产出 `<figure<svg` 这类坏 HTML，肉眼看不出来。）
"""
import argparse
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SITE = ROOT / 'visualization'
OUT = HERE / 'out'

sys.path.insert(0, str(HERE))

import registry   # noqa: E402
import svgutil    # noqa: E402


def generate(spec):
    """按登记表生成一张图的 SVG 文本。"""
    mod = importlib.import_module(spec['module'])
    fn = getattr(mod, spec['func'])
    if 'arg' in spec:
        return fn(spec['arg'])
    return fn()


def splice(spec, svg):
    """把生成结果回写进页面；返回 True 表示已替换。"""
    path = SITE / spec['page']
    text = path.read_text(encoding='utf-8')
    hit = svgutil.find_svg(text, spec['locate'])
    if hit is None:
        print('  ✗ %s：在 %s 里按 %s 找不到这张图' % (spec['id'], spec['page'], spec['locate'][1]))
        return False
    s, e, old = hit
    if svgutil.normalize(old) == svgutil.normalize(svg):
        return True                       # 已经一致，不动文件
    path.write_text(text[:s] + svg.strip() + text[e:], encoding='utf-8')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--splice', action='store_true', help='生成后回写进页面')
    ap.add_argument('ids', nargs='*', help='只处理这些图 id')
    args = ap.parse_args()

    specs = registry.FIGURES
    if args.ids:
        specs = [s for s in specs if s['id'] in args.ids]
        unknown = set(args.ids) - {s['id'] for s in specs}
        if unknown:
            print('未知图 id：%s' % ', '.join(sorted(unknown)))
            return 1

    OUT.mkdir(exist_ok=True)
    changed = 0
    for spec in specs:
        svg = generate(spec)
        (OUT / ('%s.svg' % spec['id'])).write_text(svg.strip() + '\n', encoding='utf-8')
        if args.splice:
            if splice(spec, svg):
                changed += 1
        print('  · %-16s %-24s %6d 字符' % (spec['id'], spec['page'], len(svg)))

    print('\n共 %d 张，已输出到 %s' % (len(specs), OUT))
    if args.splice:
        print('已回写 %d 张' % changed)
    return 0


if __name__ == '__main__':
    sys.exit(main())
