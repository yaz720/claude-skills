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

