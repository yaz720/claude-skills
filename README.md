# claude-skills

Claude Code **公开技能总库**——所有可分享自建技能的源头,也是将来对外分发的 marketplace。

每个技能放在 `skills/<name>/`,打好的可下载包放在 `dist/<name>.skill`。

## 目录

```
claude-skills/
├─ dist/                     # 打包产物(.skill),供下载一键装
└─ skills/
   ├─ skill-forge/           # 锻技坊:造技能的技能(造→测→发→回收 闭环)
   ├─ figure-forge/          # 把想法/数据/草图变成可下载的 SVG+PNG 图
   ├─ form-forge/            # 练形坊:把一个动作名变成一张训练动作卡(配图+代偿表+分人记录)
   ├─ supplement-scout/      # 补剂深调:美国 OTC 营养补充剂系统化调研报告
   ├─ nutri-check/           # 营养体检:食材/食谱/照片 → FDA 标签 + PDF 报告(开发中 🚧)
   ├─ care-scout/            # 寻医:医疗从业者甄别与择定(开发中 🚧)
   ├─ rx-scout/              # 问药:类内全员盘点 + 族裔证据加权的选药调研
   ├─ lab-reader/            # 读报告:医学检测报告系统化解读(化验/影像/病理)
   ├─ second-opinion-panel/  # 圆桌会诊:三轮结构化辩论 + 中英双语会诊报告
   └─ service-scout/         # 寻商:本地服务商甄别(驾校/家教/搬家/修车/装修…)(开发中 🚧)
```

## 技能一览

| 技能 | 中文名 | 一句话 | 状态 |
|---|---|---|---|
| [skill-forge](skills/skill-forge/) | 锻技坊 | 在官方 skill-creator 之上,补齐脚手架 / 预检 / 评测调优 / git 发布 / 失败回收,把造技能串成闭环 | ✅ |
| [figure-forge](skills/figure-forge/) | 铸图坊 | 把一个想法、一组数据、或一张草图,变成可下载的 SVG + PNG 图文件(流程图/架构图/对比图/柱状折线饼图等),交付的是真文件而非内联预览 | ✅ |
| [form-forge](skills/form-forge/) | 练形坊 | 把一个动作名变成一张能长期用的训练动作卡:从维基共享资源取版权干净的解剖图(内置拼法变体/作者黑名单/撞词过滤/42 块已验证图源索引)、自绘动作与发力示意图、按固定规格产出中英双语卡(含五列代偿表:谁在代偿/哪儿有感觉/哪块弱),并负责日常归档教练提点与强度 | ✅ |
| [supplement-scout](skills/supplement-scout/) | 补剂深调 | 对美国 OTC 市场某一类营养补充剂做系统化深度调研:知识分层 + 聚焦搜索,15–20 个候选经硬门槛淘汰与五维打分,按十章框架产出报告 | ✅ |
| [nutri-check](skills/nutri-check/) | 营养体检 | 把一组食材/一份食谱/一张营养标签照片/一张成品菜照片,变成可保存的营养报告:逐原料贡献表、可选原料含否两版对照、糖分构成拆解、FDA 标准标签,并落盘为 US Letter PDF 真文件 | 🚧 开发中 |
| [care-scout](skills/care-scout/) | 寻医 | 从"我有个健康问题"到"找到合适的从业者并预约"的完整流程:类型推荐、真实专长判断、多平台评分解读、负评分析、预约话术 | 🚧 开发中 |
| [rx-scout](skills/rx-scout/) | 问药 | 把「该用什么药」变成能带去和医生讨论的选药功课:类内全员盘点(含撤市史)、固定五维横向对比、族裔证据加权(常翻转欧美默认结论)、画像驱动三档筛选、最低有效剂量与联用预案、就诊问题清单 | ✅ |
| [lab-reader](skills/lab-reader/) | 读报告 | 把化验单/影像/病理等检测报告变成系统化的脱敏中文解读:逐项全量+三层参考区间、假异常甄别、红黄绿分级与组合解读、影像对冲措辞解码与偶发瘤焦虑校准、跨期趋势、就诊问题清单 | ✅ |
| [service-scout](skills/service-scout/) | 寻商 | 把「要找个本地服务商」(驾校/家教/搬家/修车/装修…)变成「选定并联系上」:行业情报先行(执照库/定价套路/高发坑)、Yelp/Google 双平台交叉解读与刷评识别、负评主题归类(区分偶发与模式)、双语询价话术 | 🚧 开发中 |
| [second-opinion-panel](skills/second-opinion-panel/) | 圆桌会诊 | 按病情遴选 4-6 位专家(含立场相反的对抗席),主持三轮结构化辩论——独立陈述→交叉质证→收敛定位分歧,产出中英双语会诊报告;用制度化对抗防止过早收敛 | 🚧 开发中 |

## 三种安装方式

1. **plugin**(将来加 `.claude-plugin/` 清单后):
   `/plugin marketplace add yaz720/claude-skills` → `/plugin install <name>@yaz720`
2. **裸拷 / 软链**:把 `skills/<name>/` 拷进 `~/.claude/skills/`,或软链:
   `ln -s ~/Desktop/claude-skills/skills/<name> ~/.claude/skills/<name>`
3. **`.skill` 一键装**:下载 `dist/<name>.skill` → 点 **Save skill**。

## 源 vs 激活

- **源**在本仓库(git / 打包 / dist 都在这);
- **激活**靠软链进 `~/.claude/skills/`(用户级)或 `<项目>/.claude/skills/`(项目级);
- 别拿 `~/.claude/skills/` 当源。
