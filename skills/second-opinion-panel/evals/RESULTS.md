# second-opinion-panel（圆桌会诊）评测记录

每次 `eval_run.py` 自动追加一段(最新在文件末尾)。分数是**单跑快照、有噪声**,
只记分数/失败项/产出去向,不含产出正文(故隐私安全)。

## 2026-08-21 18:29 -0700  (4418882, judge=claude-sonnet-5)
- triggering: 23/23  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 0 / 跳过 4  (跳过: cap-001, cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)

## 2026-08-21 19:24 -0700  (2f8ca63, judge=claude-sonnet-5)
- triggering: 22/23  (负例全过: True)  [单跑快照,有噪声]
    - ❌ trig-006: expect=fire fired=False
- capability: 已判 0 / 跳过 4  (跳过: cap-001, cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)


  注:本次 trig-006(「西医说我是肠易激,中医怎么说?想对比看看」)判 no-fire,是**单跑噪声,不是改名造成的回归**。
  用同一裁判对该条复采样核验过:旧名 `mdt-consult` 5/5 触发,新名 `second-opinion-panel` 15 次里 14 次触发
  (先 4/5,再补 10/10)。description 未做任何改动,用例也未改。这条属于裁判边界抖动,记下待观察。
