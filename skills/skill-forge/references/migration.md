# 移植现有技能(migrate an existing skill)

**场景**:你手上有一批**早于本框架**做的技能——散装文件夹、只有一个 `SKILL.md`、或已打包成 `.skill`
——想统一收编进当前 skill-forge 的标准布局(双兼容 monorepo),之后按同一条流水线继续开发。

这条通道由 `scripts/migrate.py` 固化,**不依赖任何单次对话的上下文**:任何时候触发 skill-forge 都能用。

## 一条命令

```bash
# 全局技能 → 收进技能总库 skills/<name>/
python skills/skill-forge/scripts/migrate.py <源> [--name <kebab-name>] [--repo ~/Desktop/claude-skills]

# 项目专属 → 收进 <project>/.claude/skills/<name>/
python skills/skill-forge/scripts/migrate.py <源> --project /path/to/project
```

`<源>` 三种都认:
| 源形态 | 例子 | 处理 |
|---|---|---|
| `.skill` 打包(zip) | `~/Desktop/foo.skill` | 解压 → 找 SKILL.md → 整目录收编 |
| 散装技能文件夹 | `~/old/foo/`(内含 SKILL.md) | 整目录拷入,保留 references/scripts/已有 evals |
| 孤零 SKILL.md | `~/notes/SKILL.md` | 只拷这个文件,其余全补模板 |

## 它做什么 / 不做什么

**做**:
- **非破坏**:只读你的原件,产出是 monorepo 里的一份副本;原件分毫不动。
- **保留**源里已有的正文 / `references/` / `scripts/` / 任何附带资产,以及**已经写好的 evals 用例**。
- **补齐**缺失的标准骨架:`references/`、`scripts/`、`evals/{triggering,capability}/cases.yaml`、`evals/bar.yaml`
  ——用与 `scaffold.py` **完全相同**的模板,让移植来的技能和新建的长一个样。
- **定名**:优先取 `SKILL.md` frontmatter 的 `name:`;没有再用 `--name`,再退到源文件名(kebab 校验)。
- **保护**:目标已存在直接拒绝(要覆盖显式加 `--force`),绝不静默盖掉已有技能。
- 打印 description 近似字数、激活软链命令、以及 preflight/eval 的下一步。

**不做**(交给流水线后续步骤,别指望 migrate 一步到位):
- 不改写 `SKILL.md` 正文,也不自动"提质"description——移植只负责**归位**,好坏由后面 eval/tune 判。
- 不建软链(留你确认落位,和 scaffold 一致)。
- 不打包 `.skill`(那是 package 步)。

## 移植后接标准流水线

移植 = 把旧技能塞回工作流的**第 3 步(落位)之前**;之后一模一样:

1. **激活**:`ln -s <repo>/skills/<name> ~/.claude/skills/<name>`
2. **预检**:`bash scripts/preflight.sh <skill-dir>`(验认证 + description ≤1024)
3. **补 evals**:把占位的 `cases.yaml` 换成真实触发/能力用例(旧技能常常一条测试都没有——这步最值)
4. **测试 / 调优**:`eval_run.py` → 按报告调 description / 正文
5. **打包 / 发布**:`package.sh` → commit 源 + `dist/<name>.skill` → push
6. 上线后翻车 → `harvest.sh` 回收进 evals

## 常见坑

- **frontmatter 不规范**:老技能可能缺 `name:` 或 `description:`。migrate 会尽力解析并告警;
  缺 `name` 就必须 `--name` 指定,缺 `description` 会在 preflight 卡住——补上再走。
- **`--name` 与 frontmatter 的 name 不一致**:migrate 只告警、**不替你改** `SKILL.md`;
  两处必须手动统一(否则激活时以 frontmatter 为准,容易对不上文件夹名)。改名牵连面见 `rename-checklist.md`。
- **description 超 1024**:老技能描述常常又长又散。migrate 只做近似字数提醒,权威闸在 preflight/package;超了先精简再打包。
- **一次移一个**:批量旧技能就对每个各跑一次 migrate;它们各自独立、互不覆盖。
