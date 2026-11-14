#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""负向测试：确认 verify.py 的 wiki 标签错位检查真的能抓到错误。

用法：python3 scripts/test_verify.py
退出码 0 = 判据仍然有效，1 = 判据已失效，必须改回 verify.py

[INPUT]: depends on scripts/verify.py
[OUTPUT]: exports negative tests proving each check actually catches the error it claims to
[POS]: the self-test of the gate; run it after every change to verify.py
[PROTOCOL]: Update this header on change, then check CLAUDE.md
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from verify import _label_conflict  # noqa: E402

SITE = ROOT / 'visualization'
WIKI = ROOT / 'wiki'

# (标签, 目标文件, 期望是否应报错)
cases = [
    ('06 底层架构', SITE / '06-fourth.html', True),       # 编号对得上但名称对不上
    ('04 底层架构', SITE / '04-architecture.html', False),
    ('03 第三次工业革命', SITE / '03-third.html', False),
    ('06 第四次工业革命', SITE / '06-fourth.html', False),
    ('08 术语表', SITE / '08-glossary.html', False),
    ('07 现状与来源', SITE / '07-current.html', False),
    ('09 铁律与推论', SITE / '09-logic.html', False),
    ('05 半导体', SITE / '05-semiconductor.html', False),
    ('03 第三次工业革命 内部章', SITE / '03-third.html', False),
    ('07 术语表', WIKI / '07-术语表.md', False),
    ('05 推进逻辑四铁律', WIKI / '05-推进逻辑四铁律.md', False),
    ('06 电子计算机八次跃迁', WIKI / '06-电子计算机八次跃迁.md', False),
    ('09 半导体的发展进程', WIKI / '09-半导体的发展进程.md', False),
    ('08 数据来源与口径', WIKI / '08-数据来源与口径.md', False),
    ('知识索引', WIKI / 'README.md', False),            # 索引页不参与名称校验
    ('07 术语表', WIKI / '06-电子计算机八次跃迁.md', True),  # 编号错位
]

ok = True
for label, target, expect_err in cases:
    assert target.exists(), target
    got = _label_conflict(label, target)
    hit = got is not None
    status = 'PASS' if hit == expect_err else 'FAIL'
    if hit != expect_err:
        ok = False
    print('%s  「%s」-> %-34s 命中=%-6s 期望报错=%s'
          % (status, label, target.name, got or '无', expect_err))

print('\n全部通过。' if ok else '\n存在失败用例。')
raise SystemExit(0 if ok else 1)
