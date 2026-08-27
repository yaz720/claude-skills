# skill-forge 评测记录

每次 `eval_run.py` 自动追加一段(最新在文件末尾)。分数是**单跑快照、有噪声**,
只记分数/失败项/产出去向,不含产出正文(故隐私安全)。

## 2026-08-27 09:47 -0700  (e6bf397, judge=claude-sonnet-5)
- triggering: 9/9  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 0 / 跳过 2  (跳过: cap-001, cap-002)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)
- 判读:**这是 skill-forge 自己的第一条评测记录**。它一直挂 ✅ 且用例是真用例
  (不是 TODO 骨架),但从建库起就没跑过 —— 造技能的技能自己没做过评测。
- 9/9 全过,但**别把这个满分当成覆盖充分**:用例集 9 条(5 正 4 负)是全库最薄的,
  其余技能在 18–27 条之间。满分更多说明**这几条容易**,而不是描述已经稳。
- **覆盖缺口(宣称了但没有用例守)**:
    - `migrate` / 收编现有技能 —— description 明确列为独立入口("migrates an older
      skill: loose folder, lone SKILL.md, or packaged .skill"),且 supplement-scout
      与 nutri-check 都是经它收编进库的,是真在用的能力,却一条用例都没有。
    - 发布到 git / GitHub。
    - 跑评测并出分栏报告(本次这件事本身)。
  正例只覆盖了造新技能、打包、调触发词、harvest 四件。补齐前,9/9 只是**局部**基线。
- 负例侧四条护栏(画图 → figure-forge、只是运行已有技能、一般写代码、只改 CLAUDE.md 规则)
  全过,这几条是最易误触的方向,过了有意义。

