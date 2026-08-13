# claude-skills

yaz720 的 Claude Code **技能总库**——所有自建技能的源头,也是将来对外分发的 marketplace。

每个技能放在 `skills/<name>/`,打好的可下载包放在 `dist/<name>.skill`。

## 目录

```
claude-skills/
├─ dist/                     # 打包产物(.skill),供下载一键装
└─ skills/
   ├─ skill-forge/           # 锻技坊:造技能的技能(造→测→发→回收 闭环)
   └─ doctor-finder/         # 医疗从业者查找(开发中 🚧)
```

## 技能一览

| 技能 | 中文名 | 一句话 | 状态 |
|---|---|---|---|
| [skill-forge](skills/skill-forge/) | 锻技坊 | 在官方 skill-creator 之上,补齐脚手架 / 预检 / 评测调优 / git 发布 / 失败回收,把造技能串成闭环 | ✅ |
| [doctor-finder](skills/doctor-finder/) | 医疗从业者查找 | 从"我有个健康问题"到"找到合适的从业者并预约"的完整流程:类型推荐、真实专长判断、多平台评分解读、负评分析、预约话术 | 🚧 开发中 |

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
