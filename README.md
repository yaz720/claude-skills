# claude-skills

yaz720 的 Claude Code **公开技能总库**——所有可分享自建技能的源头,也是将来对外分发的 marketplace。

> **三种落位**:可公开的放本库;**私有、跨项目**的放姊妹私有库 `claude-skills-private`(private);**只服务单个项目**的放该项目自己的 `.claude/skills/`。三者同一套 skill-forge 流程,区别只在"源码落在哪"。🔒 私密内容绝不进本公开库。

每个技能放在 `skills/<name>/`,打好的可下载包放在 `dist/<name>.skill`。

## 目录

```
claude-skills/
├─ dist/                     # 打包产物(.skill),供下载一键装
└─ skills/
   ├─ skill-forge/           # 锻技坊:造技能的技能(造→测→发→回收 闭环)
   ├─ figure-forge/          # 把想法/数据/草图变成可下载的 SVG+PNG 图
   ├─ doctor-finder/         # 医疗从业者查找(开发中 🚧)
   └─ second-opinion-panel/  # 圆桌会诊:三轮结构化辩论 + 中英双语会诊报告
```

## 技能一览

| 技能 | 中文名 | 一句话 | 状态 |
|---|---|---|---|
| [skill-forge](skills/skill-forge/) | 锻技坊 | 在官方 skill-creator 之上,补齐脚手架 / 预检 / 评测调优 / git 发布 / 失败回收,把造技能串成闭环 | ✅ |
| [figure-forge](skills/figure-forge/) | 铸图坊 | 把一个想法、一组数据、或一张草图,变成可下载的 SVG + PNG 图文件(流程图/架构图/对比图/柱状折线饼图等),交付的是真文件而非内联预览 | ✅ |
| [doctor-finder](skills/doctor-finder/) | 医疗从业者查找 | 从"我有个健康问题"到"找到合适的从业者并预约"的完整流程:类型推荐、真实专长判断、多平台评分解读、负评分析、预约话术 | 🚧 开发中 |
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
