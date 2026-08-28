# care-scout 评测记录

每次 `eval_run.py` 自动追加一段(最新在文件末尾)。分数是**单跑快照、有噪声**,
只记分数/失败项/产出去向,不含产出正文(故隐私安全)。

## 2026-08-13 22:07 -0700  (cfd56c5, judge=claude-sonnet-5)
- triggering: 21/22  (负例全过: True)  [单跑快照,有噪声]
    - ❌ trig-002: expect=fire fired=False
- capability: 已判 0 / 跳过 4  (跳过: cap-001, cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)

## 2026-08-23 15:38 -0700  (86ed65a, judge=claude-sonnet-5)
- triggering: 22/22  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 0 / 跳过 4  (跳过: cap-001, cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)
- 判读:上一跑挂着的 trig-002 这次过了,但**不能记作已修复**——本次 description
  一字未改(doctor-finder → care-scout 只动了 name 与文件夹),没有任何可能修复它的
  改动。所以 21/22 → 22/22 只能是裁判的运行间方差。该用例是否真的稳,要多跑几次
  看分布才能定论;在此之前仍按"边界用例"对待。

## 2026-08-25 22:24 -0700  (052a461, judge=claude-sonnet-5)
- triggering: 22/22  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 0 / 跳过 4  (跳过: cap-001, cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)

## 2026-08-25 23:26 -0700  (d4e8a35, judge=claude-sonnet-5)
- triggering: 22/22  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 0 / 跳过 4  (跳过: cap-001, cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)
- 判读:supp-research → supplement-scout 改名跑。本技能 description 里那条护栏
  指路牌由「补剂选购(→supp-research)」改成「(→supplement-scout)」,属于活的改动,
  22/22 确认无回归。
- **trig-002 累计分布**(「帮我推荐一个会说中文的皮肤科医生,要接受PPO保险」):
  4 跑里 3 过 —— 08-13 失败,08-23 / 08-25 两跑 / 本跑均通过。这期间该用例的
  description **从未改动过**,所以三连过不是修复的结果,是方差收敛的证据:
  倾向判定 08-13 那次为裁判噪声。基数仍小(n=4),不改用例、不标"已修",
  但可以从"边界用例"降格为"留观"——下次再失败才需要认真查。

## 2026-08-27 19:42 -0700  (04487e9, judge=claude-sonnet-5)
- triggering: 22/22  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 0 / 跳过 4  (跳过: cap-001, cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)

