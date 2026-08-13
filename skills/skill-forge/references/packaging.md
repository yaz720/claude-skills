# 打包与分发(packaging & distribution)

## 技能是自包含的

一个技能 = `SKILL.md` (+ 可选 `scripts/` / `references/` / `evals/`)。三种安装方式并存:

| 方式 | 怎么装 | 来源 |
|---|---|---|
| a) plugin | `/plugin marketplace add yaz720/claude-skills` → `/plugin install <name>@yaz720` | 总库加 `.claude-plugin/` 清单后(L3) |
| b) 裸拷 | 把 `skills/<name>/` 拷进 `~/.claude/skills/`(或软链) | 源目录 |
| c) `.skill` 一键装 | 下载 `dist/<name>.skill` → 点 **Save skill** | `dist/` |

## 源 vs 激活(两个不同的地方)

- **源(source)**:你写、git、打包的地方 = 本地 monorepo `~/Desktop/claude-skills/`。
- **激活(activation)**:Claude 运行时读技能的地方 = `~/.claude/skills/`(用户级)或
  `<项目>/.claude/skills/`(项目级)。
- **别拿 `~/.claude/skills/` 当源**;用**软链**把源接进激活区:
  ```bash
  ln -s ~/Desktop/claude-skills/skills/<name> ~/.claude/skills/<name>
  ```
  好处:改源即全局生效,git / 打包 / dist 全留在 monorepo。

## 双兼容布局

```
claude-skills/
├─ dist/<name>.skill          ← 打包产物,提交进 git,供下载
└─ skills/<name>/             ← 源;整个文件夹既可裸拷,又是 plugin 里的 skills/<name>
   ├─ SKILL.md
   ├─ references/  scripts/  evals/
```

- 脚本用**相对 SKILL.md 的路径**引用,以便随包走;
- 同时在工作流里也写出**可直接执行的命令**,即使脚本路径解析不到也能跑。

## `.skill` 产物规则

- **放仓库根 `dist/`**(不放进技能文件夹,免得裸拷带上冗余包);
- **一个技能一个 `.skill`**,统一收在 `dist/`;
- **提交进 git**(正因为要下载,别 `.gitignore` 掉);
- **改过 SKILL.md 必重打**,否则 `.skill` 是旧的。

打包命令:
```bash
bash scripts/package.sh <path/to/skill> <repo-root>/dist
# 内部调官方 package_skill.py <技能目录> <输出目录> → dist/<name>.skill(会校验 ≤1024)
```

## 升级成完整 marketplace(L3)

总库当下就能裸拷 / `.skill` 装;想做**插件市场分发**时,只加两个清单文件,**技能一个字不改**:

`.claude-plugin/plugin.json`:
```json
{ "name": "<name>", "description": "...", "version": "0.1.0",
  "author": { "name": "yaz720" },
  "homepage": "https://github.com/yaz720/claude-skills",
  "repository": "https://github.com/yaz720/claude-skills" }
```

`.claude-plugin/marketplace.json`:
```json
{ "name": "yaz720", "description": "yaz720's Claude Code plugins",
  "plugins": [ { "name": "<name>", "description": "...", "source": "./skills/<name>" } ] }
```
(参考现有 `~/Desktop/figureforge/.claude-plugin/` 的实际写法。)
