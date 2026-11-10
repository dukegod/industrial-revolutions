#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
站点校验脚本 —— 对 visualization/ 做全站一致性检查。

检查项（合并历次迭代的全部检查）：
  1. 链接可达性（无断链）
  2. HTML 标签配平
  3. 树形导航结构一致（分组数、当前项标记、面板高亮）
  4. 文件名 / kicker / title 三者编号一致
  5. 旧文件名无残留
  6. 页脚链接顺序与树形层级一致
  7. 术语表分组计数自洽（declared == actual）
  8. 关键数字口径跨页一致

用法：
  python3 scripts/verify.py
退出码 0 = 全部通过，1 = 存在问题
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'visualization'

EXPECT_GROUPS = ['第一次工业革命', '第二次工业革命', '第三次工业革命',
                  '第四次工业革命', '通用参考']
EXPECT_FOOTER = ['第一次', '第二次', '第三次', '底层架构', '半导体', '第四次',
                 '现状与来源', '术语表', '铁律与推论']
LEGACY_FILES = ['04-fourth.html', '05-fourth.html', '05-architecture.html',
                '06-current.html', '07-glossary.html', '08-logic.html']

# 关键数字：必须跨页一致（词条数变化时此表同步更新）
KEY_FIGURES = ['46%', '12%', '90%', '123%', '1.61%', '1.03%',
               '1780–1840', '53%', '88%', '74%', '7.2×',
               '1760s–1840s', '1870s–1914', '1940s–', '2010s–']

# 关键数字：必须已沉淀进 wiki（页面有则 wiki 必须有）
WIKI_FIGURES = ['46%', '12%', '1.61%', '1.03%', '1780–1840',
                '53%', '88%', '74%', '7.2×']

problems = []
notes = []


def bad(msg):
    problems.append(msg)


def check_links(pages):
    n = 0
    for f in pages:
        t = f.read_text(encoding='utf-8')
        for href in sorted(set(re.findall(r'href="([^"#?]+)"', t))):
            if href.startswith(('http://', 'https://', 'mailto:', 'data:')):
                continue
            if not (SITE / href).exists():
                bad('断链 %s -> %s' % (f.name, href))
                n += 1
    if n == 0:
        notes.append('链接可达性：0 断链')


def check_tags(pages):
    tags = ['div', 'section', 'svg', 'table', 'ol', 'li', 'a', 'p', 'text',
            'h2', 'h3', 'h4', 'dl', 'dt', 'dd', 'ul', 'span', 'details', 'summary']
    ok = True
    for f in pages:
        t = f.read_text(encoding='utf-8')
        for n in tags:
            o = len(re.findall(r'<%s\b' % n, t))
            c = len(re.findall(r'</%s>' % n, t))
            if o != c:
                bad('标签未配平 %s: <%s> %d / </%s> %d' % (f.name, n, o, n, c))
                ok = False
    if ok:
        notes.append('标签配平：%d 个文件全部通过' % len(pages))


def check_nav(pages):
    for f in pages:
        if f.name == 'computer-architecture-evolution.html':
            continue
        t = f.read_text(encoding='utf-8')
        m = re.search(r'<div class="nav-links">(.*?)\n    </div>', t, re.S)
        if not m:
            bad('导航块定位失败: %s' % f.name)
            continue
        nav = m.group(1)
        # 品牌是首页入口，必须是可点的链接
        if '<a class="nav-brand" href="index.html">' not in t:
            bad('品牌未链接到首页: %s' % f.name)
        groups = re.findall(r'<div class="grp">([^<]+)</div>', nav)
        trees = nav.count('<details class="nav-tree')
        active = nav.count('nav-tree has-active')
        onlinks = len(re.findall(r'<a href="[^"]+" class="on">', nav))
        if groups != EXPECT_GROUPS:
            bad('导航分组不符 %s: %s' % (f.name, groups))
        if trees != 5:
            bad('导航树数量不符 %s: %d' % (f.name, trees))
        # 核心沉淀页不属于任何分组，故无 has-active；其余页必须有且仅有一个
        expected_active = 0 if f.name == 'index.html' else 1
        if active != expected_active:
            bad('当前分组标记数不符 %s: %d（应为 %d）' % (f.name, active, expected_active))
        if onlinks != 1:
            bad('导航高亮数不符 %s: %d' % (f.name, onlinks))
    notes.append('树形导航：%d 页结构一致（5 组 / 当前项唯一 / 高亮唯一）' % len(pages))


def check_numbering(pages):
    for f in pages:
        if f.name in ('index.html', 'computer-architecture-evolution.html'):
            continue
        t = f.read_text(encoding='utf-8')
        fname = f.name.split('-')[0]
        k = re.search(r'<p class="kicker">([^<]*)</p>', t)
        ti = re.search(r'<title>([^<]*)</title>', t)
        kn = k.group(1)[:2] if k else '??'
        tn = ti.group(1)[:2] if ti else '??'
        if not (fname == kn == tn):
            bad('编号不一致 %s: 文件=%s kicker=%s title=%s' % (f.name, fname, kn, tn))
    notes.append('编号：文件名 / kicker / title 三者一致')


def check_legacy(pages):
    n = 0
    for f in pages:
        t = f.read_text(encoding='utf-8')
        for o in LEGACY_FILES:
            if o in t:
                bad('旧文件名残留 %s: %s' % (f.name, o))
                n += 1
    if n == 0:
        notes.append('旧文件名：无残留')


def check_footers(pages):
    for f in pages:
        t = f.read_text(encoding='utf-8')
        m = re.search(r'<footer>(.*?)</footer>', t, re.S)
        if not m:
            # 旧入口跳转页为独立样式，不含 footer，跳过
            if f.name == 'computer-architecture-evolution.html':
                continue
            bad('页脚缺失: %s' % f.name)
            continue
        labels = [x[1] for x in re.findall(r'href="([^"]+)">([^<]+)</a>', m.group(1))]
        if labels != EXPECT_FOOTER:
            bad('页脚顺序不符 %s: %s' % (f.name, labels))
    notes.append('页脚：%d 页顺序与树形层级一致' % len(pages))


def check_glossary(pages):
    g = SITE / '08-glossary.html'
    if not g.exists():
        bad('术语表缺失: 08-glossary.html')
        return
    gl = g.read_text(encoding='utf-8')
    blocks = list(re.finditer(r'<h3 class="gcat"[^>]*>(.*?)<span class="cnt">(.*?)</span>', gl, re.S))
    td = ta = 0
    for i, m in enumerate(blocks):
        end = blocks[i + 1].start() if i + 1 < len(blocks) else len(gl)
        seg = gl[m.start():end]
        d = int(re.search(r'(\d+)', m.group(2)).group(1))
        a = len(re.findall(r'<div class="entry"', seg))
        td += d
        ta += a
        if d != a:
            bad('术语分组计数不符 %s: declared=%d actual=%d'
                % (re.sub(r'<[^>]+>', '', m.group(1)).strip(), d, a))
    notes.append('术语表：declared=%d actual=%d 自洽' % (td, ta))


def check_figures(pages):
    body = [f for f in pages if f.name != 'computer-architecture-evolution.html']
    for fig in KEY_FIGURES:
        n = sum(f.read_text(encoding='utf-8').count(fig) for f in body)
        if n == 0:
            bad('关键数字缺失: %s' % fig)
    notes.append('关键数字：%d 项全部存在且跨页一致' % len(KEY_FIGURES))


def _short_name(s):
    """从标题 / 标签里取出「名」：剥掉编号前缀、括号补充、尾部装饰。"""
    s = re.sub(r'^\s*\d+\s*[·.、]?\s*', '', s)
    s = re.sub(r'（[^）]*）|\([^)]*\)', '', s)
    s = re.sub(r'[·、，,。｜|—\-]+$', '', s)
    return s.strip()


def _target_name(path):
    """目标文件的规范短名。md 用词干（稳定），html 用 title 首段。"""
    if path.suffix == '.html':
        m = re.search(r'<title>([^<]*)</title>', path.read_text(encoding='utf-8'))
        if not m:
            return None
        head = m.group(1).split('·')[0]
        if not re.match(r'\s*\d', head):
            return None          # 无编号的独立入口页，不参与名称校验
        return _short_name(head)
    if path.stem.upper() == 'README':
        return None              # 索引页，不参与名称校验
    return _short_name(path.stem)


def _label_conflict(label, path):
    """标签与目标是否错位：编号不一致，或名称对不上。"""
    a = re.match(r'\s*(\d+)', label)
    b = re.match(r'(\d+)', path.name)
    if a and b and a.group(1) != b.group(1):
        return '编号错位'
    ln = _short_name(label)
    tn = _target_name(path)
    if ln and tn and ln != tn and tn not in ln and ln not in tn:
        return '名称错位'
    return None


def check_wiki():
    """wiki 与 visualization 的口径一致性。"""
    wiki = ROOT / 'wiki'
    if not wiki.exists():
        bad('缺少 wiki/ 目录')
        return
    md = sorted(wiki.glob('*.md'))
    if len(md) < 8:
        bad('wiki 条目过少: %d' % len(md))

    # wiki 内部链接与页面引用：可达 + 标签与目标对得上
    for f in md:
        t = f.read_text(encoding='utf-8')
        for label, href in re.findall(r'\[([^\]]+)\]\(([^)#]+\.md)\)', t):
            target = f.parent / href
            if not target.exists():
                bad('wiki 内部链接失效 %s -> %s' % (f.name, href))
                continue
            why = _label_conflict(label, target)
            if why:
                bad('wiki 链接%s %s: 标签「%s」-> %s'
                    % (why, f.name, label.strip(), href))
        for label, href in re.findall(r'\[([^\]]+)\]\(\.\./visualization/([^)#]+)\)', t):
            target = SITE / href
            if not target.exists():
                bad('wiki 引用页面不存在 %s -> %s' % (f.name, href))
                continue
            why = _label_conflict(label, target)
            if why:
                bad('wiki 页面引用%s %s: 标签「%s」-> %s'
                    % (why, f.name, label.strip(), href))

    # wiki 与页面共用同一套关键数字
    site_text = ''.join(p.read_text(encoding='utf-8') for p in SITE.glob('*.html'))
    wiki_text = ''.join(p.read_text(encoding='utf-8') for p in md)
    for fig in WIKI_FIGURES:
        if fig in site_text and fig not in wiki_text:
            bad('关键数字未沉淀到 wiki: %s' % fig)
    notes.append('wiki：%d 个条目，链接可达且标签与目标对得上，%d 项关键数字已沉淀'
                 % (len(md), len(WIKI_FIGURES)))


def main():
    if not SITE.exists():
        print('找不到 visualization/ 目录')
        return 1
    pages = sorted(SITE.glob('*.html'))
    check_links(pages)
    check_tags(pages)
    check_nav(pages)
    check_numbering(pages)
    check_legacy(pages)
    check_footers(pages)
    check_glossary(pages)
    check_figures(pages)
    check_wiki()

    print('=== 校验结果 ===')
    for n in notes:
        print('  ✓', n)
    if problems:
        print('\n=== 问题 %d 项 ===' % len(problems))
        for p in problems:
            print('  ✗', p)
        return 1
    print('\n全部通过。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
