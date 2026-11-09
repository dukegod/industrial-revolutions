#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全部「由脚本生成」的图的登记表。

一条记录 = 一张图：它在哪一页、用哪个生成器产出、在页面上靠什么定位它。

- `build_figures.py` 按本表生成 / 回写页面；
- `verify_embedded.py` 按本表比对「页面里嵌的」与「脚本生成的」是否一致，
  防止脚本改了、页面没改（这类漂移肉眼看不出来）。

没有登记的图是**手写图**（见 README「手写图」一节），脚本不碰它们。

定位方式（locate）：
- `('attrs', 'class="stepfig" data-stage="1"')` —— 结构性锚点，最稳；
- `('aria', '缩放方式的三次转移')`      —— 无 class 的图用 aria-label 前缀。
"""

FIGURES = [
    # ── 05 半导体：主题页三张图 ──────────────────────────────────
    {'id': '05-fig1', 'page': '05-semiconductor.html',
     'module': 'gen_semi', 'func': 'fig1',
     'locate': ('aria', '缩放方式的三次转移')},
    {'id': '05-fig2', 'page': '05-semiconductor.html',
     'module': 'gen_semi', 'func': 'fig2',
     'locate': ('aria', '光刻波长演进')},
    {'id': '05-fig3', 'page': '05-semiconductor.html',
     'module': 'gen_semi3', 'func': 'gen',
     'locate': ('aria', '瓶颈的性质在跃迁 7')},

    # ── 03 第三次：三条线总图 + 阶段图 + 物理段图 + 岔路图 ────────
    {'id': '03-twolines', 'page': '03-third.html',
     'module': 'gen_twolines', 'func': 'gen',
     'locate': ('aria', '第三次革命的')},
    {'id': '03-forks', 'page': '03-third.html',
     'module': 'gen_forks', 'func': 'gen',
     'locate': ('attrs', 'class="forkfig"')},

    # ── 04 底层架构：技术架构路线图 ────────────────────────────────
    {'id': '04-roadmap', 'page': '04-architecture.html',
     'module': 'gen_roadmap', 'func': 'gen',
     'locate': ('attrs', 'class="roadmap"')},
]


def _stage_family(prefix, page, cls, func, n=4):
    """三族放大图（stepfig / stagefig / physfig）每族 4 张，按 data-stage 定位。"""
    return [
        {'id': '%s%d' % (prefix, i), 'page': page,
         'module': 'gen_stages', 'func': func, 'arg': i,
         'locate': ('attrs', 'class="%s" data-stage="%d"' % (cls, i))}
        for i in range(1, n + 1)
    ]


FIGURES += _stage_family('04-stepfig-', '04-architecture.html', 'stepfig', 'gen_stepfig')
FIGURES += _stage_family('03-stagefig-', '03-third.html', 'stagefig', 'gen_stagefig')
FIGURES += _stage_family('03-physfig-', '03-third.html', 'physfig', 'gen_physfig')

BY_ID = {f['id']: f for f in FIGURES}
