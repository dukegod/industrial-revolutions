# scripts/
> L2 | Parent: ../CLAUDE.md

构建与校验工具。全部只用 Python 标准库，无第三方依赖，无安装步骤。脚本不改内容 —— 内容以 `wiki/` 为准，脚本只保证表达层的一致性。

## 成员清单

`build.py`: 站点构建；同步导航树、页脚、跨页链接与编号；`--check` 只报告是否有待构建内容；幂等
`verify.py`: 全站十一项校验 —— 链接可达、标签配平、树形导航、编号一致、旧文件名残留、页脚顺序、术语计数、关键数字、资源引用可达、孤儿资源、wiki 口径一致
`test_verify.py`: verify.py 的逻辑自测；改动 verify.py 后必须跑
`test_alignment.py`: 三条线的逐项对齐校验（计算线 / 连接线 / 物理线的阶段与事件是否对得上）
`README.md`: 脚本用法、改结构时改哪里、新增关键数字时怎么办
`figures/`: 图形生成与防漂移，见 figures/CLAUDE.md

## 纪律

- 只用标准库；不引入依赖，不引入构建步骤
- 校验脚本失败即退出码 1，不做「警告但放过」——放过的就是没人看的
- 改校验逻辑必须同步改 `test_verify.py`

Laws: complete membership · one line per file · parent link · technical terms first
[PROTOCOL]: Update this header on change, then check CLAUDE.md
