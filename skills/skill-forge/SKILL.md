---
name: skill-forge
description: >-
  Scaffold, test-tune, and ship a NEW Claude Code skill end-to-end — the engineering parts the
  model won't do on its own and that the official skill-creator leaves out: a dual-compatible
  folder layout (works both bare-copied and as a plugin), preflight checks, triggering + capability
  evals with a scored report, git/GitHub publish to your skills repo, a downloadable .skill package,
  and harvesting real-world failures back into the eval set. It also migrates an older skill (loose
  folder, lone SKILL.md, or packaged .skill) into this layout. It wraps the official skill-creator for
  the writing step and adds the create → test → publish → harvest loop around it. Trigger 触发词:
  造技能、新建/创建技能、移植/收编/导入现有技能、打包技能、发布/分发技能、给技能做评测、调技能的触发词/description、
  把翻车案例加进测试集、build/package/ship/migrate a skill, skill eval, tune a skill's triggering.
  不要触发 (do NOT trigger):
  merely running or using an existing skill; ordinary writing/coding tasks; drawing diagrams or charts
  (that is figure-forge's job); or only editing project CLAUDE.md rules.
---

# skill-forge (锻技坊)

一个**造技能的技能**。它在官方 `skill-creator` 之上包一层**编排**,补官方没有的工程环节,把
**造 → 测 → 发 → 回收**串成闭环。撰写正文这一步转交官方 skill-creator;其余由本技能负责。

> **为什么它值得被触发**:模型只在"这个技能能提供它自己做不到的东西"时才会翻它。本技能的差异化价值
> 不是"帮你写技能"(那和内建重叠),而是**脚手架、预检、评测调优、git/GitHub 发布、失败回收**。
> description 也据此起草。

## 什么时候用我 / 什么时候别用我

**用我**:要新建一个技能;**要把一个旧技能移植 / 收编进本框架**;要给技能打包 / 发布 / 分发;要给技能做评测或调触发词;要把一个真实翻车案例加进测试集。

**别用我**:只是运行 / 使用某个已存在的技能;一般写文档或写代码;画图或做图表(那是 figure-forge 的活);只想改项目 `CLAUDE.md` 规则。

---

## 工作流(照此逐步,细节按需读 references)

### 1. 构思 Ideate
先想清楚三件事,别急着建文件:
- **差异化价值**:这技能比模型内建**多提供**了什么?(自触发概率正比于此)
- **触发 / 不触发**:中英文触发词 + **否定例**(尤其容易误触的相邻场景)。
- **落位(第一步就定,关乎隐私,别拖)**:**问用户一句**——「这个技能是 **①可公开分享**、**②私有但跨项目复用**,还是 **③只服务某个项目**?」
  - ① 公开 → 源进**公开总库**(scaffold/migrate 用 `--repo <公开总库>`),软链到 `~/.claude/skills/`。
  - ② 私有跨项目 → 源进**私有总库**(`--repo <私有 repo>`,一个 private repo),同样软链激活。
  - ③ 项目专属 → 源进那个项目的 `.claude/skills/<name>/`(`--project <path>`),跟项目走、不进任何总库、免软链。
  - **🔒 隐私红线**:公开总库 = 公开,**私密内容绝不进公开总库**;拿不准就先放私有 / 项目内。区分"整个技能私有"(换个家)与"技能公开、只夹带私密片段"(把私密剥离到项目 `CLAUDE.md` / 环境变量 / gitignore 的本地数据,见「边界」)。
  - 具体是哪几个仓、路径、哪个仓是 private,**记在账户级 `~/.claude/CLAUDE.md`(私有)或私有总库自己的 README**,技能里只留通用规则。
  - ⚠️ **别写进公开总库的 README**:那个文件人人可见,在里面点名私有库,等于对外广播「我有一个叫 xxx-private 的仓」。公开总库的 README 只说本库放什么,不提有没有私有姊妹库。规则本身(三种落位、隐私红线)不敏感,**敏感的是私有仓的名字与路径**——把这两者分开放。
- **命名(kebab-case)**:技能名一律**全小写**,**多个词之间用连字符 `-` 连**(如 `doctor-finder`、`figure-forge`、`skill-forge`)。
  - 校验正则:`^[a-z0-9]+(-[a-z0-9]+)*$`(scaffold / migrate 自动把关)。
  - ⚠ 单个**连写词**(如 `figureforge`)虽能过正则,但**违背本约定**——词边界要用 `-` 断开,保持全库一致、可读、可预测显式命令名。改名牵动多处,见 `references/rename-checklist.md`。

→ 触发设计详见 `references/triggering-design.md`。

### 2. 脚手架 Scaffold
```bash
python skills/skill-forge/scripts/scaffold.py <new-skill-name> [--repo ~/Desktop/claude-skills] [--project <path>]
```
生成**双兼容**目录(`skills/<name>/` 既能裸拷、又能当 plugin)+ `SKILL.md` 模板 + `evals/` 模板。
→ 布局与三种安装方式详见 `references/packaging.md`。

### 2′. 移植现有技能 Migrate(scaffold 的替代入口)
手上有**早于本框架**的旧技能(散装文件夹 / 只有一个 `SKILL.md` / 已打包 `.skill`),用它收编进标准布局:
```bash
python skills/skill-forge/scripts/migrate.py <源> [--name <kebab-name>] [--repo ~/Desktop/claude-skills] [--project <path>]
```
**非破坏**(不动原件)、**保留**源里已有正文 / references / scripts / 已写好的 evals、只**补齐**缺失骨架(与 scaffold 同模板)、目标已存在则拒绝(除非 `--force`)。移植 = 接在第 3 步之前,之后照常 preflight→eval→package→publish。
→ 详见 `references/migration.md`。

### 3. 落位 / 激活 Activate
把源软链进激活区(全局或项目)。scaffold 会提示具体命令,形如:
```bash
ln -s ~/Desktop/claude-skills/skills/<name> ~/.claude/skills/<name>
```

### 4. 撰写 Author
把正文撰写**交给官方 skill-creator**。起草 `description` 时**默认做到**:
- 以**差异化价值开头**(不是泛泛"帮你做 X");
- 精确"push"(点名触发场景)+ **补否定例**;
- **中英文触发词**并列;
- 起草后**自动核对 ≤ 1024 字符**(打包成 `.skill` 会校验,超了会失败)。

### 5. 预检 Preflight
```bash
bash skills/skill-forge/scripts/preflight.sh <path/to/skill>
```
- `claude -p "OK"` 验 CLI 认证 —— ⚠ **认证过期时,触发评测会静默把所有触发读成 0,且"改写描述"步会崩**;
- 核对 description 字数 ≤ 1024。
**评测 / 打包前必先 preflight。**

### 6. 测试 Test
```bash
python skills/skill-forge/scripts/eval_run.py <path/to/skill>
```
先跑**触发测试**、再跑**能力测试**,出**分栏报告**。

**基线要趁早,别等技能"完美"**(基线是棘轮的锚,没它就判不了改动更好/更差):
- **触发基线立刻做**——description 一诞生就能测、又便宜,第一时间抓描述缺陷(doctor-finder 就是这样抓到"找某类医生"漏触发的)。
- **能力基线按成熟度推迟**——它要技能真跑出产出;工具/核心流程还没就绪就先把能力用例写好、标 pending,等能产出再跑。成熟度由本技能(模型)判断,够格了就主动建议用户做一次基线。

⚠ **重叠型技能(画图 / 写文本这类)触发基准会失灵**:模型直接内联做了、不翻技能,导致候选描述**同分**。
检测到"全同分 / 全 0"时报「**基准盲区,请人工判**」,别据此误判描述质量。
→ 详见 `references/eval-and-tuning.md`。

### 7. 调优 Tune(半自动,档二)
针对失败项,给出**已自测、带成绩单**的修改建议(diff),**用户点头才落地**。机制:
- **单一总分 + 全量回归 + 棘轮**:每个候选改动对整套测试集重跑、算总分,**只收严格变高**的;
- **无进展预算**:连续 N 次打不过 best 就判 plateau、停;区分真 plateau 与基准盲区;
- **分支隔离**:在 `tune/<name>` 分支上跑,`main` 永远 last-known-good,点头才 merge。
- 触发类建议改 `description`、能力类建议改正文/脚本,**分栏给,别混**。
- **不动靶子(红线)**:调优只改技能、**不改测试集**——动了 = 移动球门自己进球,测量作废;要改用例那是"改规格",单独做(见下方「评测生命周期与基线策略」)。
→ 详见 `references/eval-and-tuning.md`。

### 8. 打包 Package
```bash
bash skills/skill-forge/scripts/package.sh <path/to/skill> <repo-root>/dist
```
调官方 `package_skill.py` 生成 / 重打 `dist/<name>.skill`。
**改过 SKILL.md 必重打**;打包会再校验 ≤1024(第二道闸)。

### 9. 发布 Publish
- `git commit` 把【源 + `dist/<name>.skill`】一起提交;
- **pre-push 涉密守卫**:推前扫一遍有没有误写密钥 / 凭据(总库缺省 public);
- push 到 `claude-skills`;
- **推后深度验证**:抓远程实际内容核对关键改动,而非只看本地(见全局 CLAUDE.md)。

### 10. 回收 Harvest(真闭环)
线上翻车、**或评测 / 试用时发现集里还没有的新失败模式**时:
```bash
bash skills/skill-forge/scripts/harvest.sh <path/to/skill> "<失败输入>" <fire|no-fire|capability>
```
把这个真实案例记进该技能的 `evals/`,成为防回归的新测试。**测试集是用出来的,不是一次性造的。**

---

## 评测生命周期与基线策略
用例不是一次性造出来的,它有生命周期;不同阶段对它的态度不同:

1. **播种(建 / 迁时)**:scaffold / migrate 只给 TODO 占位。**别停在占位**——据技能用途**起草一版候选用例**(触发正负例 + 能力 rubric),**给用户过目、同意后落地**。
2. **基线**:触发基线**立刻跑**(便宜、早抓描述缺陷);能力基线**待技能能真产出**时再跑(见第 6 步)。**基线是棘轮的锚——没有它,后续改动无从判断更好 / 更差。**
3. **调优红线**:精调若为达成**现有**测试集(如改 description 让触发过),**绝不动用例**——靶子不动才测得准(见第 7 步)。
4. **改规格才动用例**:只有技能**该做什么**变了(范围 / 意图),才有意识地改 / 加用例;这是**独立的一次"改靶子"**,单独做、说清,别夹在调优里偷改。
5. **增长**:发现失败 → 收进 evals 当回归测试。来源有两类**都要收**:**线上翻车** 和 **评测 / 试用时发现的**(用 `harvest.sh`,第 10 步)。注意:**新增一条真实失败用例 = 扩覆盖(鼓励)**,和第 3 条"不动靶子"不冲突——被禁的是**编辑 / 删除已有用例**去凑分。已在集里、这次没过的用例本就留着当待修目标;要记的是集里**还没有的新失败模式**。
6. **留档**:`eval_run.py` 每跑一次**自动**把分数追加到 `evals/RESULTS.md`(可回看演进、据此重测),连同改动一起提交。

**产出怎么存(三层,别混)**:
- **分数历史** `evals/RESULTS.md` —— 小、无隐私,**入库**。
- **黄金参考** `evals/capability/golden/` —— 少量**认可的**标准产出,**入库**,当"问 → 答"可视基线 / 回归对照。
- **逐次产出** `evals/capability/outputs/` —— 可重生、可能含隐私(如真实医生数据),**gitignore、不入库**;**隐私敏感技能绝不提交原始产出**(这正是 doctor-finder 能力测试"跳过"而非造假的原因)。

**管理**:每技能自带 `evals/`(随技能进 git、可 diff);`bar.yaml` 是达标线;用例尽量**注明出处**(手写 / harvest / 规格变更)。→ 详见 `references/eval-and-tuning.md`。

## 改名注意
技能改名牵动多处(name / 文件夹 / plugin.json / marketplace.json / .skill / 软链 / GitHub repo)。
**任何改名前先读 `references/rename-checklist.md`。**

## 边界(不写进这个可分享技能)
"永远走我的封装""总库库名 / marketplace 名 / package_skill.py 的机器路径 / 裁判模型偏好"这类
**项目专有或强制规则**,放**账户级 `~/.claude/CLAUDE.md` 或项目级 `CLAUDE.md`**,不写进本技能
——技能只放通用、可移植的 know-how。

**同一条边界也适用于仓库自己的 README**:公开仓的 README 和技能正文一样是对外的,别把私有仓名、
内部路径、个人工作流细节写进去。判据不是"这是不是规则",而是"这行字被陌生人看到会不会泄露什么"。
