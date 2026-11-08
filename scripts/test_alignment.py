#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""两条线的逐项对齐校验。

检查计算线（四段台阶）与连接/接入线（四个阶段）是否严格一一对应：

  1. 计算线四张台阶图齐全，阶段号 1–4 无缺无重
  2. 计算线的跃迁区间合并后正好覆盖八次跃迁，不重叠、不遗漏
  3. 连接/接入线四张阶段图齐全，阶段号 1–4 无缺无重
  4. 同一阶段号的两张图，跃迁区间完全一致
  5. 每张图 data-events 里的每个名称都必须出现在该图的实际文本里
     （数据标记不能与画出来的内容脱节）
  6. wiki/03 的对齐表每一行与两张图的数据一致

用法：
  python3 scripts/test_alignment.py
退出码 0 = 全部对齐，1 = 存在错位
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCH = ROOT / 'visualization' / '04-architecture.html'
THIRD = ROOT / 'visualization' / '03-third.html'
WIKI = ROOT / 'wiki' / '03-第三次工业革命.md'

ALL_LEAPS = list(range(1, 9))          # 八次跃迁
EXPECT_LEAPS = ['1–3', '4–5', '6', '7–8']

problems = []
notes = []


def bad(msg):
    problems.append(msg)


def svg_figures(path, cls):
    """取出带 class=cls 的 <svg>，解析 data-stage / data-leaps / data-events。"""
    t = path.read_text(encoding='utf-8')
    out = []
    for m in re.finditer(r'<svg\b([^>]*)>(.*?)</svg>', t, re.S):
        attrs, body = m.group(1), m.group(2)
        if 'class="%s"' % cls not in attrs:
            continue
        st = re.search(r'data-stage="([^"]+)"', attrs)
        lp = re.search(r'data-leaps="([^"]+)"', attrs)
        ev = re.search(r'data-events="([^"]+)"', attrs)
        pr = re.search(r'data-peers="([^"]+)"', attrs)
        if not (st and lp and ev):
            bad('%s：有一张 %s 图缺少 data-* 标记' % (path.name, cls))
            continue
        texts = [re.sub(r'<[^>]+>', '', x) for x in re.findall(r'<text\b[^>]*>(.*?)</text>', body, re.S)]
        out.append({
            'stage': int(st.group(1)),
            'leaps': lp.group(1),
            'events': ev.group(1).split('|'),
            'peers': pr.group(1) if pr else '',
            'texts': texts,
            'body': body,
        })
    return out


def wiki_rows():
    """解析 wiki/03 的对齐表，返回 [(stage, 台阶, 跃迁, 阶段, 关键节点)]。"""
    t = WIKI.read_text(encoding='utf-8')
    rows = []
    for line in t.splitlines():
        if not line.strip().startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 5 or not cells[0].isdigit():
            continue
        if '计算线台阶' in line:          # 表头
            continue
        rows.append({
            'stage': int(cells[0]),
            'step': cells[1],
            'leaps': cells[2],
            'stage_name': cells[3],
            'events': [e.strip() for e in re.split(r'[、,，]', cells[4]) if e.strip()],
        })
    return rows


def leap_list(s):
    """'1–3' → [1,2,3]；'6' → [6]"""
    out = []
    for part in s.replace(',', '，').split('，'):
        part = part.strip()
        if not part:
            continue
        if '–' in part:
            a, b = part.split('–')
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def main():
    if not (ARCH.exists() and THIRD.exists() and WIKI.exists()):
        print('找不到 04-architecture.html / 03-third.html / wiki/03')
        return 1

    steps = svg_figures(ARCH, 'stepfig')
    stages = svg_figures(THIRD, 'stagefig')

    # 1. 计算线齐全
    step_by_stage = {f['stage']: f for f in steps}
    if sorted(step_by_stage) != [1, 2, 3, 4]:
        bad('计算线台阶图阶段号应为 1–4，实际 %s' % sorted(step_by_stage))
    else:
        notes.append('计算线：4 张台阶图，阶段号 1–4 无缺无重')

    # 2. 跃迁区间正好覆盖八次跃迁
    covered = []
    for i in range(1, 5):
        f = step_by_stage.get(i)
        if not f:
            continue
        if f['leaps'] != EXPECT_LEAPS[i - 1]:
            bad('计算线台阶 %d 的跃迁区间应为 %s，实际 %s' % (i, EXPECT_LEAPS[i - 1], f['leaps']))
            continue
        a, b = f['leaps'].split('–') if '–' in f['leaps'] else (f['leaps'], f['leaps'])
        covered.extend(range(int(a), int(b) + 1))
    if sorted(covered) != ALL_LEAPS:
        bad('八次跃迁覆盖不全或有重叠：%s' % sorted(covered))
    else:
        notes.append('八次跃迁：1–3 / 4–5 / 6 / 7–8 分段完整，覆盖无重叠无遗漏')

    # 3. 第二线齐全
    stage_by_stage = {f['stage']: f for f in stages}
    if sorted(stage_by_stage) != [1, 2, 3, 4]:
        bad('连接/接入线阶段图阶段号应为 1–4，实际 %s' % sorted(stage_by_stage))
    else:
        notes.append('连接/接入线：4 张阶段图，阶段号 1–4 无缺无重')

    # 4. 同一阶段跃迁区间一致
    for i in range(1, 5):
        a = step_by_stage.get(i)
        b = stage_by_stage.get(i)
        if not a or not b:
            continue
        if a['leaps'] != b['leaps']:
            bad('阶段 %d 跃迁区间错位：计算线 %s，连接/接入线 %s' % (i, a['leaps'], b['leaps']))
    notes.append('同阶段跃迁区间：4/4 一致')

    # 5. data-events 必须出现在图的实际文本里
    for label, figs in (('计算线', steps), ('连接/接入线', stages)):
        for f in figs:
            joined = ' '.join(f['texts'])
            for e in f['events']:
                if e not in joined:
                    bad('%s 阶段 %d：data-events 里的「%s」在图中找不到' % (label, f['stage'], e))
    notes.append('图内事件名：全部能在对应 SVG 文本中找到（标记与画出来的一致）')

    # 6. wiki 对齐表逐项比对
    rows = wiki_rows()
    if len(rows) != 4:
        bad('wiki/03 对齐表应有 4 行，实际 %d 行' % len(rows))
    else:
        for r in rows:
            i = r['stage']
            a = step_by_stage.get(i)
            b = stage_by_stage.get(i)
            if not a or not b:
                continue
            if r['leaps'] != a['leaps']:
                bad('wiki 对齐表阶段 %d 的跃迁区间 %s 与计算线 %s 不符' % (i, r['leaps'], a['leaps']))
            if r['leaps'] != b['leaps']:
                bad('wiki 对齐表阶段 %d 的跃迁区间 %s 与连接/接入线 %s 不符' % (i, r['leaps'], b['leaps']))
            if r['events'] != b['events']:
                bad('wiki 对齐表阶段 %d 的关键节点 %s 与图中 %s 不符'
                    % (i, r['events'], b['events']))
            if b['peers'] and not r['stage_name'].startswith(b['peers']):
                bad('wiki 对齐表阶段 %d 的阶段名「%s」与图上的「%s」不符'
                    % (i, r['stage_name'], b['peers']))
    notes.append('wiki/03 对齐表：4 行的跃迁区间与关键节点与两张图逐项一致')

    print('=== 两条线对齐校验 ===')
    for n in notes:
        print('  ✓', n)
    if problems:
        print('\n=== 错位 %d 项 ===' % len(problems))
        for p in problems:
            print('  ✗', p)
        return 1
    print('\n全部对齐。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
