#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""页面内 SVG 的定位 / 取出 / 归一化 —— 生成器与校验脚本共用。"""
import re

SVG_RE = re.compile(r'<svg\b[^>]*>.*?</svg>', re.S)


def opening_tag(block):
    """取 <svg> 的开标签（含右尖括号）。"""
    return block[:block.index('>') + 1]


def iter_svgs(text):
    """产出页面里每一张 SVG：(起始下标, 结束下标, 整块)。"""
    for m in SVG_RE.finditer(text):
        yield m.start(), m.end(), m.group(0)


def find_svg(text, locate):
    """按 registry 的 locate 定位一张图，返回 (start, end, block)；找不到返回 None。

    locate = ('attrs', 'class="stepfig" data-stage="1"')  或
             ('aria',  '缩放方式的三次转移')
    """
    kind, key = locate
    for s, e, block in iter_svgs(text):
        tag = opening_tag(block)
        if kind == 'attrs' and key in tag:
            return s, e, block
        if kind == 'aria' and ('aria-label="%s' % key) in tag:
            return s, e, block
    return None


def normalize(svg):
    """归一化后比较：逐行去首尾空白、去掉空行。

    生成器输出与页面里嵌的版本只在缩进上不同，正文必须逐字一致。
    """
    lines = [ln.strip() for ln in svg.strip().split('\n')]
    return '\n'.join(ln for ln in lines if ln)


def texts_of(svg):
    """取出图里所有 <text>：(x, y, font-size, anchor, 纯文本)。

    纯文本会把换行与缩进折叠成单个空格 —— SVG 默认的 xml:space 行为就是
    折叠空白并去掉首尾空白，不折叠会把源码里的缩进算进宽度，凭空报出「越界」。
    """
    out = []
    pat = re.compile(r'<text x="([\d.]+)" y="([\d.]+)"([^>]*)>(.*?)</text>', re.S)
    for m in pat.finditer(svg):
        x, y, attrs, body = float(m.group(1)), float(m.group(2)), m.group(3), m.group(4)
        plain = ' '.join(re.sub(r'<[^>]+>', '', body).split())
        fs = 12.0
        fm = re.search(r'font-size="([\d.]+)"', attrs)
        if fm:
            fs = float(fm.group(1))
        anchor = 'start'
        am = re.search(r'text-anchor="([^"]+)"', attrs)
        if am:
            anchor = am.group(1)
        out.append((x, y, fs, anchor, plain))
    return out


def text_width(text, font_size):
    """估算文本宽度：CJK 按 1.0em，其余按 0.58em。"""
    return sum(font_size if ord(c) > 0x2E80 else font_size * 0.58 for c in text)


def text_span(x, y, fs, anchor, text):
    """文本的横向区间 [左, 右]。"""
    w = text_width(text, fs)
    if anchor == 'end':
        return x - w, x
    if anchor == 'middle':
        return x - w / 2, x + w / 2
    return x, x + w


def rects_of(svg):
    """取出图里所有 <rect>：(x, y, w, h)，并滤掉装饰性的细条与小方块。"""
    out = []
    for m in re.finditer(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"', svg):
        x, y, w, h = (float(m.group(i)) for i in (1, 2, 3, 4))
        if w < 60 or h < 18:
            continue          # 左侧色条、图标底衬之类，不作为「所属色块」
        out.append((x, y, w, h))
    return out
