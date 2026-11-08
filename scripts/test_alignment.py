#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三条线的逐项对齐校验。

第三次革命有三条线：

  计算线        四段台阶（八次架构跃迁）        04-architecture.html  class="stepfig"
  连接与接入线   四个阶段（互联网与移动设备）    03-third.html        class="stagefig"
  物理基础线     四个物理段（半导体·通信·能源）  03-third.html        class="physfig"

三条线段号一一对应，每段覆盖同一批跃迁。这个脚本自动验这种对应关系：

  1. 三条线各自的阶段号 1–4 齐全，无缺无重
  2. 计算线的跃迁区间合并后正好覆盖八次跃迁，不重叠、不遗漏
  3. 同阶段号的三张图，跃迁区间完全一致
  4. 每张图 data-events 里的每个名称都必须出现在该图的实际文本里
     （数据标记不能与画出来的内容脱节）
  5. wiki/03 的两张对齐表逐行与三张图的数据一致

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

ALL_LEAPS = list(range(1, 9))
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
        })
    return out


def wiki_tables():
    """解析 wiki/03 的对齐表，按表头第 4 列区分类型。

    返回 {'conn': [...], 'phys': [...]}；每行含 stage / step / leaps / name / events。
    """
    t = WIKI.read_text(encoding='utf-8')
    out = {'conn': [], 'phys': []}
    kind = None
    for line in t.splitlines():
        s = line.strip()
        if not s.startswith('|'):
            kind = None
            continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if '计算线台阶' in s:
            kind = 'phys' if len(cells) > 3 and cells[3] == '物理段' else ('conn' if len(cells) > 3 and cells[3] == '连接与接入线阶段' else None)
            continue
        if kind is None or len(cells) < 5 or not cells[0].isdigit():
            continue
        out[kind].append({
            'stage': int(cells[0]),
            'step': cells[1],
            'leaps': cells[2],
            'name': cells[3],
            'events': [e.strip() for e in re.split(r'[、,，]', cells[4]) if e.strip()],
        })
    return out


def leap_list(s):
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
    for f in (ARCH, THIRD, WIKI):
        if not f.exists():
            print('找不到 %s' % f)
            return 1

    steps = svg_figures(ARCH, 'stepfig')
    stages = svg_figures(THIRD, 'stagefig')
    phys = svg_figures(THIRD, 'physfig')
    tables = wiki_tables()

    lines = [('计算线', steps), ('连接与接入线', stages), ('物理基础线', phys)]

    # 1. 三条线阶段号齐全
    for name, figs in lines:
        by_stage = {f['stage']: f for f in figs}
        if sorted(by_stage) != [1, 2, 3, 4]:
            bad('%s 的阶段号应为 1–4，实际 %s' % (name, sorted(by_stage)))
        else:
            notes.append('%s：4 张图，阶段号 1–4 无缺无重' % name)

    step_by = {f['stage']: f for f in steps}
    stage_by = {f['stage']: f for f in stages}
    phys_by = {f['stage']: f for f in phys}

    # 2. 八次跃迁覆盖完整
    covered = []
    for i in range(1, 5):
        f = step_by.get(i)
        if not f:
            continue
        if f['leaps'] != EXPECT_LEAPS[i - 1]:
            bad('计算线台阶 %d 的跃迁区间应为 %s，实际 %s' % (i, EXPECT_LEAPS[i - 1], f['leaps']))
            continue
        covered.extend(leap_list(f['leaps']))
    if sorted(covered) != ALL_LEAPS:
        bad('八次跃迁覆盖不全或有重叠：%s' % sorted(covered))
    else:
        notes.append('八次跃迁：1–3 / 4–5 / 6 / 7–8 分段完整，覆盖无重叠无遗漏')

    # 3. 三条线同阶段跃迁区间一致
    for i in range(1, 5):
        ref = step_by.get(i)
        for name, by in (('连接与接入线', stage_by), ('物理基础线', phys_by)):
            f = by.get(i)
            if not ref or not f:
                continue
            if ref['leaps'] != f['leaps']:
                bad('阶段 %d 跃迁区间错位：计算线 %s，%s %s' % (i, ref['leaps'], name, f['leaps']))
    notes.append('同阶段跃迁区间：三条线 4/4 一致')

    # 4. data-events 必须出现在图的实际文本里
    for name, figs in lines:
        for f in figs:
            joined = ' '.join(f['texts'])
            for e in f['events']:
                if e not in joined:
                    bad('%s 阶段 %d：data-events 里的「%s」在图中找不到' % (name, f['stage'], e))
    notes.append('图内事件名：三条线全部能在对应 SVG 文本中找到（标记与画出来的一致）')

    # 5. wiki 两张对齐表逐行比对
    for kind, by, label in (('conn', stage_by, '连接与接入线'), ('phys', phys_by, '物理基础线')):
        rows = tables[kind]
        if len(rows) != 4:
            bad('wiki/03 %s 对齐表应有 4 行，实际 %d 行' % (label, len(rows)))
            continue
        for r in rows:
            i = r['stage']
            ref = step_by.get(i)
            f = by.get(i)
            if not ref or not f:
                continue
            if r['leaps'] != ref['leaps']:
                bad('wiki %s 对齐表阶段 %d 的跃迁区间 %s 与计算线 %s 不符' % (label, i, r['leaps'], ref['leaps']))
            if r['leaps'] != f['leaps']:
                bad('wiki %s 对齐表阶段 %d 的跃迁区间 %s 与图中 %s 不符' % (label, i, r['leaps'], f['leaps']))
            if r['events'] != f['events']:
                bad('wiki %s 对齐表阶段 %d 的关键节点 %s 与图中 %s 不符' % (label, i, r['events'], f['events']))
        notes.append('wiki/03 %s 对齐表：4 行的跃迁区间与关键节点与图中逐项一致' % label)

    print('=== 三条线对齐校验 ===')
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
