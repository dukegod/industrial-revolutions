#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「电子计算机技术架构路线」SVG。

用法：python3 scripts/figures/gen_roadmap.py（打印 SVG）
      或由 scripts/figures/build_figures.py 统一生成 / 回写。

[INPUT]: depends on wiki/06-电子计算机八次跃迁.md
[OUTPUT]: exports the technology-architecture roadmap SVG, including the UNDET markers for cells with no evidence
[POS]: the producer of the roadmap figure; it is where the "do not guess" rule is enforced in code
[PROTOCOL]: Update this header on change, then check CLAUDE.md
"""

LABEL_W = 170
COL_X = [174, 420, 666, 912, 1158]
COL_W = 238
ROW_Y0 = 84
ROW_H = 54
BOT_Y = 688
BOT_H = 58
BOT2_Y = 756
BOT3_Y = 824
LEG_Y = 898
VB_W = 1400
VB_H = 950

COLS = [
    {'period': '1945–1995', 'phase': '奠基期 · 跃迁 1–3'},
    {'period': '1995–2015', 'phase': '并行期 · 跃迁 4–5'},
    {'period': '2016–2022', 'phase': '专用化 · 跃迁 6'},
    {'period': '2023–2026', 'phase': 'AI 工厂 · 跃迁 7'},
    {'period': '2026→', 'phase': '前方 · 跃迁 8 途中'},
]

ROWS = [
    {'label': '逻辑部件与封装', 'note': '算力的物理载体',
     'cells': [
         ['电子管 → 晶体管 → 集成电路', '→ VLSI 规模化'],
         ['制程红利 · FinFET', '多核 SoC 单片集成'],
         ['矩阵加速器 · 专用 ASIC', '异构单片'],
         ['Chiplet + 先进封装', '液冷（冷板 / 浸没）'],
         ['定制化 · 域专用加速器', '方向已明，形态未定'],
     ]},
    {'label': '互连', 'note': '机器与机器之间',
     'cells': [
         ['地址总线 → 标准化总线', '（ISA / PCI）'],
         ['片上互连 · NoC', 'NVLink（Scale-up）'],
         ['InfiniBand / RoCE', 'Scale-up 与 Scale-out 成型'],
         ['UBB · 光互连', '机架内带宽成为约束'],
         ['PCIe / IOMMU 标准化', '（服务器平台规范 1.0）'],
     ]},
    {'label': '存储层次', 'note': '数据待在哪里',
     'cells': [
         ['磁芯 → 半导体', 'Cache / DRAM 分层'],
         ['NUMA 拓扑', 'GDDR 与 DDR 分叉'],
         ['HBM + 并行文件系统', '训练数据成为新 IO 瓶颈'],
         ['HBM4 · KV Cache 分层', 'prefill / decode 分离'],
         ['？尚未定位', '下一个存储约束待观察'],
     ]},
    {'label': '执行与并发模型', 'note': '一台机器怎么同时干多件事',
     'cells': [
         ['单指令流 → 流水线', '→ 超标量'],
         ['多核 / SMP → SIMT', '吞吐优先、延迟不敏感'],
         ['集合通信 · 分布式训练', '同步更新取代参数同步'],
         ['推理服务 · Agent 编排', '算力 + 控制 + I/O 混合负载'],
         ['？尚未定位', '负载形态尚未定型'],
     ]},
    {'label': '编程模型与生态', 'note': '人怎么对机器说话',
     'cells': [
         ['机器码 → 汇编', '→ 编译器 · 标准 C'],
         ['线程与内存模型', 'CUDA 与库（生态护城河）'],
         ['分布式训练框架', '集合通信成为一等公民'],
         ['vLLM / SGLang · 兼容层', '调度器本身变成产品'],
         ['多版本二进制 · AI 辅助移植', '碎片化尚未收敛'],
     ]},
    {'label': '规模与交付单元', 'note': '一次买多少、怎么运',
     'cells': [
         ['单机 → 工作站'],
         ['多核 SoC → 机群'],
         ['机架（整柜交付）'],
         ['AI 工厂'],
         ['？尚未定位'],
     ]},
    {'label': '互联网与云', 'note': '算力怎么被送到人手里',
     'cells': [
         ['ARPANET → TCP/IP', '→ 万维网（1991）'],
         ['宽带 · Web 2.0', '云计算（2006 AWS）'],
         ['数据中心成为云的底座', '流媒体 · 短视频规模化'],
         ['模型即服务经互联网分发', 'Agent 工具协议'],
         ['？尚未定位'],
     ]},
    {'label': '移动设备', 'note': '每个人口袋里的通用机',
     'cells': [
         ['蜂窝电话（1983）', '2G GSM · 短信'],
         ['iPhone（2007）触屏 + App 生态', '4G · 移动优先'],
         ['5G（2019）', '移动成为主入口'],
         ['端侧模型 · 端云协同', '手机作为 Agent 终端'],
         ['？尚未定位'],
     ]},
    {'label': '半导体与封装', 'note': '算力的物理载体',
     'cells': [
         ['晶体管 → 平面工艺 → 光刻', '→ 集成电路 / VLSI'],
         ['深亚微米 · 铜互连 · FinFET', '存储器缩放'],
         ['EUV 量产 · HBM · CoWoS', 'Chiplet'],
         ['GAA · High-NA EUV', 'HBM4 · 先进封装'],
         ['定制 ASIC 增速首超 GPU', '混合键合推迟到 HBM4E'],
     ]},
    {'label': '通信与光互连', 'note': '机器与机器怎么连',
     'cells': [
         ['铜缆 → 同轴 → 光纤'],
         ['光骨干网 · 2G / 3G / 4G', '宽带与蜂窝'],
         ['硅光 · 400G / 800G 光模块', '数据中心光互连'],
         ['CPO 共封装光学 · 1.6T', '低轨卫星'],
         ['CPO 首批量产 · 1.6T', '？卫星与光互连形态未定'],
     ]},
    {'label': '能源与散热', 'note': '这套系统的物理天花板',
     'cells': [
         ['风冷 · 机房级供电'],
         ['冷冻水 · 机柜 10–20kW'],
         ['数据中心电力集中化', '30kW 级机柜'],
         ['冷板液冷为主 · 100kW+ 机柜', '变电与选址成为约束'],
         ['冷板 93.5% 主导', '浸没吃 >200kW 高密场景'],
     ]},
]

BOT = [
    ['指令吞吐 → 访存延迟'],
    ['访存延迟 → 互连带宽'],
    ['互连带宽 → 内存容量与带宽'],
    ['内存容量与带宽 → 电力与成本'],
    ['？下一轮主导瓶颈未确定'],
]

BOT2 = [
    ['接入稀缺（拨号与许可）'],
    ['带宽稀缺（骨干网与 CDN）'],
    ['流量与分发稀缺（视频流）'],
    ['入口与注意力稀缺（超级 App）'],
    ['？未确定'],
]

BOT3 = [
    ['器件与工艺'],
    ['互连延迟与漏电'],
    ['封装产能与光模块产能'],
    ['电力与散热'],
    ['？未确定'],
]

UNDET = {(2, 4), (3, 4), (4, 4), (5, 4)}   # (row_idx, col_idx) 尚未定位
FRONT = 4                                   # 前方列
# 2026→ 列里与三个岔路对应的结论，精确标记（供 scripts/test_alignment.py 定位）
FORKKEYS = {
    (8, 4, 0): '定制 ASIC',   # 半导体与封装
    (8, 4, 1): '混合键合',     # 半导体与封装
    (10, 4, 0): '冷板',        # 能源与散热
}


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def gen():
    o = []
    a = o.append
    a('<svg class="roadmap" data-forkkeys="冷板|定制 ASIC|混合键合" viewBox="0 0 %d %d" width="100%%" style="display:block;height:auto" role="img" aria-label="电子计算机技术架构路线：横向时间轴从1945到2026，六条技术维度泳道展示各阶段的替代链，底部为主导瓶颈迁移带，右端虚线列为前方未定项">'
      % (VB_W, VB_H))
    a('  <defs>')
    a('    <marker id="axArrow" markerWidth="9" markerHeight="9" refX="7" refY="3.2" orient="auto">')
    a('      <path d="M0,0 L7,3.2 L0,6.4 Z" fill="#2f6f5e"/>')
    a('    </marker>')
    a('  </defs>')
    a('  <g font-family="Outfit, \'PingFang SC\', sans-serif">')

    # ── 时间轴 ────────────────────────────────────────────
    centers = [x + COL_W // 2 for x in COL_X]
    a('    <line x1="%d" y1="30" x2="%d" y2="30" stroke="#2f6f5e" stroke-width="1.6" marker-end="url(#axArrow)" opacity=".8"/>'
      % (centers[0], VB_W - 14))
    for i, c in enumerate(COLS):
        cx = centers[i]
        col = '#c97b3f' if i == FRONT else '#2f6f5e'
        a('    <circle cx="%d" cy="30" r="6" fill="#fff" stroke="%s" stroke-width="2.4"/>' % (cx, col))
        a('    <text x="%d" y="54" font-size="13" font-weight="600" fill="#14171e" text-anchor="middle">%s</text>'
          % (cx, esc(c['period'])))
        a('    <text x="%d" y="71" font-size="10.5" font-family="JetBrains Mono, monospace" fill="%s" text-anchor="middle">%s</text>'
          % (cx, col, esc(c['phase'])))
    a('')

    # ── 泳道 ──────────────────────────────────────────────
    for r, row in enumerate(ROWS):
        y = ROW_Y0 + r * ROW_H
        if r % 2 == 0:
            a('    <rect x="0" y="%d" width="%d" height="%d" fill="#2f6f5e" fill-opacity=".025"/>' % (y, VB_W, ROW_H))
        a('    <text x="14" y="%d" font-size="12.5" font-weight="600" fill="#14171e">%s</text>' % (y + 22, esc(row['label'])))
        a('    <text x="14" y="%d" font-size="10.5" fill="#7c7a72">%s</text>' % (y + 39, esc(row['note'])))
        a('    <line x1="0" y1="%d" x2="%d" y2="%d" stroke="#e9e3d6"/>' % (y + ROW_H, VB_W, y + ROW_H))
        for c in range(5):
            x = COL_X[c]
            front = (c == FRONT)
            undet = (r, c) in UNDET
            if front:
                a('    <rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="#c97b3f" fill-opacity=".04" stroke="#c97b3f" stroke-opacity=".45" stroke-dasharray="5 4"/>'
                  % (x, y + 4, COL_W, ROW_H - 9))
            else:
                a('    <rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="#fff" stroke="#e9e3d6"/>'
                  % (x, y + 4, COL_W, ROW_H - 9))
            lines = row['cells'][c]
            col = '#b3aea2' if undet else '#3a4256'
            base = y + (24 if len(lines) == 1 else 20)
            for li, ln in enumerate(lines):
                fk = FORKKEYS.get((r, c, li))
                attr = ' data-forkkey="%s"' % fk if fk else ''
                a('    <text x="%d" y="%d"%s font-size="11.5" fill="%s">%s</text>'
                  % (x + 12, base + li * 17, attr, col, esc(ln)))
            if undet:
                a('    <text x="%d" y="%d" font-size="10.5" fill="#b3aea2" text-anchor="end">未定</text>'
                  % (x + COL_W - 12, y + ROW_H - 12))
        a('')

    # ── 主导瓶颈带 ────────────────────────────────────────
    a('    <rect x="0" y="%d" width="%d" height="%d" rx="10" fill="#c97b3f" fill-opacity=".09" stroke="#c97b3f" stroke-opacity=".3"/>'
      % (BOT_Y, VB_W, BOT_H))
    a('    <text x="14" y="%d" font-size="12.5" font-weight="600" fill="#c97b3f">主导瓶颈（计算）</text>' % (BOT_Y + 24))
    a('    <text x="14" y="%d" font-size="10.5" fill="#a97a4f">每一段台阶挤掉的下一个</text>' % (BOT_Y + 41))
    for c in range(5):
        x = COL_X[c]
        front = (c == FRONT)
        if front:
            a('    <rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="none" stroke="#c97b3f" stroke-opacity=".5" stroke-dasharray="5 4"/>'
              % (x, BOT_Y + 5, COL_W, BOT_H - 10))
        col = '#b3aea2' if c == FRONT else '#8a5a30'
        a('    <text x="%d" y="%d" font-size="11.5" fill="%s">%s</text>' % (x + 12, BOT_Y + 32, col, esc(BOT[c][0])))
    a('')

    # ── 主导瓶颈带（连接与接入侧） ──────────────────────────
    a('    <rect x="0" y="%d" width="%d" height="%d" rx="10" fill="#c97b3f" fill-opacity=".05" stroke="#c97b3f" stroke-opacity=".22"/>'
      % (BOT2_Y, VB_W, BOT_H))
    a('    <text x="14" y="%d" font-size="12.5" font-weight="600" fill="#b07a4c">主导瓶颈（连接与接入）</text>' % (BOT2_Y + 24))
    a('    <text x="14" y="%d" font-size="10.5" fill="#b3aea2">这条线挤掉的下一个</text>' % (BOT2_Y + 41))
    for c in range(5):
        x = COL_X[c]
        front = (c == FRONT)
        if front:
            a('    <rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="none" stroke="#c97b3f" stroke-opacity=".4" stroke-dasharray="5 4"/>'
              % (x, BOT2_Y + 5, COL_W, BOT_H - 10))
        col = '#b3aea2' if c == FRONT else '#8a5a30'
        a('    <text x="%d" y="%d" font-size="11.5" fill="%s">%s</text>' % (x + 12, BOT2_Y + 32, col, esc(BOT2[c][0])))
    a('')

    # ── 主导瓶颈带（物理层） ────────────────────────────────
    a('    <rect x="0" y="%d" width="%d" height="%d" rx="10" fill="#c97b3f" fill-opacity=".035" stroke="#c97b3f" stroke-opacity=".18"/>'
      % (BOT3_Y, VB_W, BOT_H))
    a('    <text x="14" y="%d" font-size="12.5" font-weight="600" fill="#b07a4c">主导瓶颈（物理层）</text>' % (BOT3_Y + 24))
    a('    <text x="14" y="%d" font-size="10.5" fill="#b3aea2">托着上面两条线的那层</text>' % (BOT3_Y + 41))
    for c in range(5):
        x = COL_X[c]
        front = (c == FRONT)
        if front:
            a('    <rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="none" stroke="#c97b3f" stroke-opacity=".35" stroke-dasharray="5 4"/>'
              % (x, BOT3_Y + 5, COL_W, BOT_H - 10))
        col = '#b3aea2' if c == FRONT else '#8a5a30'
        a('    <text x="%d" y="%d" font-size="11.5" fill="%s">%s</text>' % (x + 12, BOT3_Y + 32, col, esc(BOT3[c][0])))
    a('')

    # ── 现在线 ────────────────────────────────────────────
    now_x = COL_X[FRONT] - 8
    a('    <line x1="%d" y1="16" x2="%d" y2="%d" stroke="#c97b3f" stroke-width="1.4" stroke-dasharray="6 4"/>'
      % (now_x, now_x, BOT3_Y + BOT_H))
    a('    <text x="%d" y="20" font-size="11" font-weight="600" fill="#c97b3f" text-anchor="end">现在 · 2026-11</text>' % (now_x - 8))
    a('')

    # ── 图例 ──────────────────────────────────────────────
    a('    <text x="14" y="%d" font-size="10.5" fill="#7c7a72">实线框 = 已发生　虚线框 = 前方 / 进行中　灰字「未定」= 尚未定位</text>' % (LEG_Y + 14))
    a('    <text x="14" y="%d" font-size="10.5" fill="#7c7a72">三条瓶颈带分别对应计算线、连接/接入线与物理层；右端只写有依据的方向，未写明的即为不确定</text>' % (LEG_Y + 32))
    a('  </g>')
    a('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    print(gen())
