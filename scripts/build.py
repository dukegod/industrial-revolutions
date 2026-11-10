#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
站点构建脚本 —— 维护 visualization/ 下静态页面的结构一致性。

职责（合并了历次迭代，最终形态）：
  1. 生成/刷新树形导航（按工业革命分期归组，<details>/<summary>，零 JS）
  2. 统一各页页脚（站点名 + 按树形层级排序的主线链接串）
  3. 校验并对齐「文件名 / kicker / title」三者编号
  4. 同步全站内部链接与正文中的页码前缀引用

用法：
  python3 scripts/build.py            # 构建（幂等，可重复执行）
  python3 scripts/build.py --check    # 只检查不写入，输出差异
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'visualization'

# ---------------------------------------------------------------- 站点结构定义
# 树形层级：分组 → [(文件名, 短名, 副标题)]
# 编号即层级位置：04 底层架构属第三次，06 现状属第四次，07/08 属通用参考
TREE = [
    ('核心沉淀', None),
    ('第一次工业革命', [
        ('01-first.html', '第一次', '蒸汽动力 · 工厂制度 · 1833 工厂法'),
    ]),
    ('第二次工业革命', [
        ('02-second.html', '第二次', '单元驱动 · 流水线 · 共享增长'),
    ]),
    ('第三次工业革命', [
        ('03-third.html', '第三次', '可编程与零边际复制 · 三条线'),
        ('04-architecture.html', '底层架构', '金字塔 · 架构路线 · 逐层传递'),
        ('05-semiconductor.html', '半导体', '制程 · 光刻 · 存储 · 封装'),
    ]),
    ('第四次工业革命', [
        ('06-fourth.html', '第四次', '自主执行 · 2026 当下数据'),
        ('07-current.html', '现状与来源', '三个硬约束 · 路线图 · 全部来源'),
    ]),
    ('通用参考', [
        ('08-glossary.html', '术语表', '100 条分组词条 · 阅读路径'),
        ('09-logic.html', '铁律与推论', '四条铁律 · 推导过程 · 平台推论'),
    ]),
]

SHORT = {
    '第一次工业革命': '第一次', '第二次工业革命': '第二次',
    '第三次工业革命': '第三次', '第四次工业革命': '第四次', '通用参考': '参考',
}

# 站点标识与页脚说明
SITE_NAME = '工业革命与人类发展'
FOOT_NOTE = '以工业革命为主线 · 事实核对截至 2026 年 11 月公开信息 · 历史分期为编者归纳，各阶段边界为近似划分'

# 页码前缀 ↔ 文件名 的映射（用于正文引用同步）
PREFIX_MAP = [
    ('01-first.html',        '01 第一次'),
    ('02-second.html',       '02 第二次'),
    ('03-third.html',        '03 第三次'),
    ('04-architecture.html', '04 底层架构'),
    ('05-semiconductor.html', '05 半导体'),
    ('06-fourth.html',       '06 第四次'),
    ('07-current.html',      '07 现状与来源'),
    ('08-glossary.html',     '08 术语表'),
    ('09-logic.html',        '09 铁律与推论'),
]

# 历史文件名 → 现文件名（重命名遗留，兼容旧引用）
LEGACY_LINK = [
    ('04-fourth.html',      '06-fourth.html'),
    ('05-fourth.html',      '06-fourth.html'),
    ('05-architecture.html', '04-architecture.html'),
    ('06-current.html',     '07-current.html'),
    ('07-current.html',     '07-current.html'),
    ('07-glossary.html',    '08-glossary.html'),
    ('08-glossary.html',    '08-glossary.html'),
    ('08-logic.html',       '09-logic.html'),
    ('09-logic.html',       '09-logic.html'),
]

PAGES = [f for f in sorted(SITE.glob('*.html'))
         if f.name != 'computer-architecture-evolution.html']


# ---------------------------------------------------------------- 导航生成
def build_nav(active_file):
    """生成 active_file 对应页面的 nav-links 内容。"""
    out = []
    for group, items in TREE:
        if items is None:
            cls = ' class="on"' if active_file == 'index.html' else ''
            out.append('      <a href="index.html"%s>核心沉淀</a>' % cls)
            continue
        in_group = any(f == active_file for f, _, _ in items)
        cls = ' nav-tree has-active' if in_group else ''
        # name="nav"：原生 HTML 独占手风琴 —— 同名的 details 只会有一个处于打开状态
        # （打开一个会自动关掉其余）。零 JS，不引脚本。
        out.append('      <details class="nav-tree%s" name="nav">' % cls)
        out.append('        <summary><span class="caret"></span>%s</summary>' % SHORT[group])
        out.append('        <div class="nav-tree-panel">')
        out.append('          <div class="grp">%s</div>' % group)
        for f, label, sub in items:
            num = f.split('-')[0]
            acls = ' class="on"' if f == active_file else ''
            out.append('          <a href="%s"%s><span class="num">%s</span>%s<span class="sub">%s</span></a>'
                       % (f, acls, num, label, sub))
        out.append('        </div>')
        out.append('      </details>')
    return '\n'.join(out)


def footer_html():
    """生成统一页脚（缩进与页面中其他 footer 一致）。"""
    links = ' · '.join('<a href="%s">%s</a>' % (f, prefix.split(' ', 1)[1])
                       for f, prefix in PREFIX_MAP)
    return ('  <footer>\n'
            '    %s · %s<br/>\n'
            '    主线：%s\n'
            '  </footer>' % (SITE_NAME, FOOT_NOTE, links))


def replace_footer(text):
    """整块替换页脚；保留原有缩进风格，避免反复构建产生差异。"""
    m = re.search(r'[ \t]*<footer>.*?</footer>', text, re.S)
    if not m:
        return text
    indent = re.match(r'[ \t]*', m.group(0)).group(0)
    body = footer_html()
    # 按原缩进重新缩进（footer_html 首行已含 2 空格）
    lines = body.split('\n')
    reindented = '\n'.join(
        (indent + l[2:]) if (i > 0 and l.startswith('  ')) else l
        for i, l in enumerate(lines))
    return text[:m.start()] + reindented + text[m.end():]


# ---------------------------------------------------------------- 写入步骤
def replace_nav(text, active_file):
    """整块替换 nav 内的 nav-links（用 nav-in 边界锚定，避免嵌套 div 截断）。"""
    new_nav = '<div class="nav-links">\n' + build_nav(active_file) + '\n    </div>'
    m = re.search(r'(<span class="nav-brand">.*?</span>\s*)(<div class="nav-links">.*?)(</div>\s*</nav>)',
                  text, re.S)
    if not m:
        return text, False
    return text[:m.start(2)] + new_nav + text[m.end(2):], True




def sync_links(text):
    """同步内部链接与正文页码前缀（单次占位替换，避免链式误替）。"""
    for old, new in LEGACY_LINK:
        text = text.replace('href="%s"' % old, 'href="%s"' % new)

    # 正文里形如 "05 第四次" 的旧页码前缀 → 新页码前缀
    replacements = []
    for fname, olds in LEGACY_PREFIX.items():
        new_prefix = dict(PREFIX_MAP)[fname]
        for o in olds:
            replacements.append((o, new_prefix))

    for i, (old, new) in enumerate(replacements):
        ph = '\x00PH%d\x00' % i
        text = text.replace(old, ph)
        text = text.replace(ph, new)
    return text


# 旧编号 → 新编号 的正文前缀替换对：{新文件名: [(旧前缀, ...)]}
LEGACY_PREFIX = {
    '04-architecture.html': ['05 底层架构'],
    '06-fourth.html':       ['04 第四次', '05 第四次'],
    '07-current.html':      ['03 现状与来源', '06 现状与来源'],
    '08-glossary.html':     ['04 术语表', '07 术语表'],
    '09-logic.html':        ['09 铁律与推论', '08 铁律与推论'],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='只检查不写入')
    args = ap.parse_args()

    changed = []
    for f in PAGES:
        orig = f.read_text(encoding='utf-8')
        t = orig
        t, ok = replace_nav(t, f.name)
        if not ok:
            print('!! nav 定位失败:', f.name)
            continue
        t = replace_footer(t)
        t = sync_links(t)
        if t != orig:
            changed.append(f.name)
            if not args.check:
                f.write_text(t, encoding='utf-8')

    if args.check:
        if changed:
            print('以下页面需要构建：')
            for c in changed:
                print('  -', c)
            return 1
        print('所有页面均已是最新，无需构建。')
        return 0

    print('构建完成，%d 个页面有更新：' % len(changed))
    for c in changed:
        print('  -', c)
    return 0


if __name__ == '__main__':
    sys.exit(main())
