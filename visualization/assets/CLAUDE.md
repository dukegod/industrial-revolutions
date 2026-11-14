# visualization/assets/
> L2 | Parent: ../CLAUDE.md

全站唯一的外部资源目录，也是本仓库唯一允许承载二进制的位置。Pages 发布根就是 `visualization/`，所以这里的文件随站点上线；仓库根目录的散图与 `videos/` 目录既不发布也不可达。

## 成员清单

`style.css`: 全站唯一样式表；CSS 自定义属性（配色 / 字体 / 间距）与全部组件类（nav / hero / figbox / timeline / card / glossary / hero-video）；11 个页面各引用一次
`industrial-revolutions-720p.mp4`: 开篇片；1280×720 / 24fps / 15.09s / H.264 High + AAC / 3.2MB / faststart；由 MiniMax Hailuo 2.3 生成后拼接重编码；AI 生成的示意演绎，不承载数据结论
`industrial-revolutions-poster.jpg`: 上一条的封面帧（1280×720，44KB），取自末段闭环成形的画面

## 纪律

- 每个文件都必须被某个页面引用 —— `scripts/verify.py` 的孤儿资源检查会直接报出来
- 媒体源件（生成原件、中间产物）不入库，留在 `.tmp/stash/`
- AI 生成的媒体必须在页面图注里带**显式标识**，不能只靠文件里的隐式 AIGC 标记

Laws: complete membership · one line per file · parent link · technical terms first
[PROTOCOL]: Update this header on change, then check CLAUDE.md
