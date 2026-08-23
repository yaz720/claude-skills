# 锻技坊 (skill-forge)

> **状态:🚧 开发中**(触发与能力用例已写好,**尚未跑过基线**——本技能自己还没吃自己的狗粮;
> 跑通并留档后再转 ✅)

一个 Claude Code **技能**:**一个造技能的技能。** 它在官方 `skill-creator` 之上包一层**编排**,补官方没有的工程环节,把**造 → 测 → 发 → 回收**串成闭环。

撰写正文那一步转交官方 skill-creator;其余——脚手架、预检、评测调优、打包、git/GitHub 发布、失败回收——由本技能负责。这也正是它的差异化价值所在:「帮你写技能」和模型内建重叠,**工程闭环**才是模型不会自己做的部分。

## 十步工作流

| 步 | 做什么 | 工具 |
|---|---|---|
| 1 | **构思** —— 差异化价值、触发/否定例、**落位(第一步就定,关乎隐私)**、kebab-case 命名 | `references/triggering-design.md` |
| 2 | **脚手架** —— 生成双兼容目录 + `SKILL.md` 模板 + `evals/` 模板 | `scripts/scaffold.py` |
| 2′ | **移植** —— 把早于本框架的旧技能(散装文件夹 / 单个 SKILL.md / 已打包 `.skill`)收编进标准布局,**非破坏** | `scripts/migrate.py` |
| 3 | **激活** —— 软链进激活区(全局或项目) | `ln -s` |
| 4 | **撰写** —— 转交官方 skill-creator,起草 description 时自动核对 ≤1024 字符 | — |
| 4′ | **README** —— 填掉脚手架生成的骨架:写给**人**看的门面,首行【状态徽标】如实反映评测进度 | — |
| 5 | **预检** —— 验 CLI 认证 + description 字数。**评测/打包前必先跑** | `scripts/preflight.sh` |
| 6 | **测试** —— 触发测试 + 能力测试,出分栏报告,分数自动追加进 `RESULTS.md` | `scripts/eval_run.py` |
| 7 | **调优** —— 针对失败项给**已自测、带成绩单**的 diff,用户点头才落地 | `references/eval-and-tuning.md` |
| 8 | **打包** —— 调官方 `package_skill.py` 生成 `dist/<name>.skill` | `scripts/package.sh` |
| 9 | **发布** —— 源 + `.skill` 一起提交,pre-push 涉密守卫,推后深度验证 | git |
| 10 | **回收** —— 把真实翻车案例记进 `evals/`,成为防回归的新测试 | `scripts/harvest.sh` |

## 几条值得单独说的设计

**落位在第一步就定,因为它关乎隐私。** 开工先问一句:这技能是①可公开分享、②私有但跨项目复用,还是③只服务某个项目?——公开的进公开总库,私有的进私有总库,项目专属的进那个项目的 `.claude/skills/`。**红线:私密内容绝不进公开总库**,拿不准就先放私有或项目内。还要区分"整个技能私有"(换个家)与"技能公开、只夹带私密片段"(把私密剥离到项目 `CLAUDE.md` / 环境变量 / gitignore 的本地数据)。

**基线要趁早,别等技能"完美"。** 基线是棘轮的锚,没它就判不了改动是更好还是更差。触发基线**立刻做**(description 一诞生就能测、又便宜);能力基线**按成熟度推迟**(它要技能真跑出产出)。

**调优不动靶子(红线)。** 精调只改技能、**不改测试集**——动了测试集等于移动球门自己进球,测量作废。要改用例那是"改规格",单独做、说清楚,别夹在调优里偷改。但**新增**一条真实失败用例是扩覆盖,鼓励,不冲突:被禁的是编辑/删除已有用例去凑分。

**⚠ 重叠型技能的触发基准会失灵。** 画图、写文本这类,模型直接内联做了、根本不翻技能,导致候选描述**同分**。检测到"全同分 / 全 0"时会报「基准盲区,请人工判」,不据此误判描述质量。

**产出分三层存,别混。** 分数历史 `RESULTS.md`(小、无隐私,**入库**)/ 黄金参考 `capability/golden/`(少量认可的标准产出,**入库**,当可视基线)/ 逐次产出 `capability/outputs/`(可重生、可能含隐私,**gitignore**)。隐私敏感的技能宁可把能力测试标"跳过",也不提交原始产出。

## 命名与改名

技能名一律 kebab-case:全小写,多个词之间用连字符断开(`care-scout`、`figure-forge`)。单个连写词(`figureforge`)虽能过正则但违背约定。

**改名牵动多处**——`name` 字段 / 文件夹 / plugin.json / marketplace.json / `.skill` 包 / 软链 / GitHub repo。任何改名前先读 `references/rename-checklist.md`。

## 边界

项目专有或强制性的规则——总库库名、`package_skill.py` 的机器路径、裁判模型偏好、「永远走我的封装」这类——**放账户级或项目级 `CLAUDE.md`,不写进本技能**。技能里只留通用、可移植的 know-how。

同一条边界也适用于仓库的 README:公开仓的 README 和技能正文一样是对外的。判据不是"这是不是规则",而是**"这行字被陌生人看到会不会泄露什么"**。

不负责:运行/使用某个已存在的技能;一般写文档或写代码;画图表(→ `figure-forge`);只改项目 `CLAUDE.md` 规则。

## 仓库结构

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能主文件:十步工作流 + 评测生命周期 + 边界 |
| `references/triggering-design.md` | 触发词与否定例的设计方法 |
| `references/packaging.md` | 双兼容布局与三种安装方式 |
| `references/migration.md` | 旧技能收编的细节 |
| `references/eval-and-tuning.md` | 评测机制、棘轮与 plateau、基准盲区 |
| `references/rename-checklist.md` | 改名要动的全部位置 |
| `scripts/` | scaffold / migrate / preflight / eval_run / package / harvest |
| `evals/` | 触发与能力用例(尚未跑基线) |

---

> **安装与分发**:本技能随 `claude-skills` **总库**一起分发,不是独立仓库。
> 装法(软链激活 / 下载 `dist/skill-forge.skill` 一键装)见[总库根 README](../../README.md)。
