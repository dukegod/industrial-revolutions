#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成三族「放大图」（共 12 张）—— 三族共用 stage_template，保证结构完全一致。

| 族 | 类名 | 落点页面 | 列头 | 渐变 id 前缀 |
|---|---|---|---|---|
| 计算线四段台阶 | `stepfig` | 04-architecture.html | 跃迁 · 名称 | `gup1` / `gdn1` |
| 连接与接入线四阶段 | `stagefig` | 03-third.html | 节点 · 名称 | `gup101` / `gdn101` |
| 物理基础线四物理段 | `physfig` | 03-third.html | 节点 · 名称 | `gup201` / `gdn201` |

三族在 03-third.html 同页共存，渐变 id 必须互不相同，否则 `url(#gup1)` 会串到
第一张图上（入库版本本来就是按这个约定起的名，这里沿用）。

用法：
    python3 scripts/figures/gen_stages.py             # 打印全部 12 张
    python3 scripts/figures/gen_stages.py phys 3      # 只打印物理段三
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import phys_stages_data   # noqa: E402
import stage_template     # noqa: E402
import stages_data        # noqa: E402
import steps_data         # noqa: E402


def gen_stepfig(i):
    """计算线第 i 段台阶（04-architecture.html）。"""
    leaps, events = steps_data.STEP_META[i]
    attrs = ' class="stepfig" data-stage="%d" data-leaps="%s" data-events="%s"' % (
        i, leaps, '|'.join(events))
    return stage_template.render(steps_data.STEPS[i - 1], i,
                                 head1='跃迁 · 名称', attrs=attrs, grad='', div_right=898)


def gen_stagefig(i):
    """连接与接入线第 i 阶段（03-third.html）。"""
    peers, leaps, _name, events = stages_data.STAGE_META[i]
    attrs = ' class="stagefig" data-stage="%d" data-peers="%s" data-leaps="%s" data-events="%s"' % (
        i, peers, leaps, '|'.join(events))
    return stage_template.render(stages_data.STAGES[i - 1], i,
                                 head1='节点 · 名称', attrs=attrs, grad='10')


def gen_physfig(i):
    """物理基础线第 i 物理段（03-third.html）。"""
    _name, events = phys_stages_data.PHYS_META[i]
    leaps = phys_stages_data.PHYS_LEAPS[i]
    attrs = ' class="physfig" data-stage="%d" data-leaps="%s" data-events="%s"' % (
        i, leaps, '|'.join(events))
    return stage_template.render(phys_stages_data.PHYS_STAGES[i - 1], i,
                                 head1='节点 · 名称', attrs=attrs, grad='20')


FAMILIES = {'step': gen_stepfig, 'stage': gen_stagefig, 'phys': gen_physfig}


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else None
    for fam, fn in FAMILIES.items():
        if which and fam != which:
            continue
        for i in (1, 2, 3, 4):
            print(fn(i))
            print('<!-- ===== -->')
