# service-scout 评测记录

每次 `eval_run.py` 自动追加一段(最新在文件末尾)。分数是**单跑快照、有噪声**,
只记分数/失败项/产出去向,不含产出正文(故隐私安全)。

## 2026-08-29 22:36 -0700  (0dba349, judge=claude-sonnet-5)
- triggering: 22/22  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 0 / 跳过 3  (跳过: cap-001, cap-002, cap-003)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)

## 2026-08-29 23:03 -0700  (41a6308, judge=claude-sonnet-5)
- triggering: 22/22  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 4 / 跳过 0
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)
  (人工补记:4 用例 19/19 条 check 全过——cap-001 5/5、cap-002 4/4、cap-003 4/4、cap-004 5/5;
   cap-001 的裁判结论因终端截断丢失,已用同一提示词与裁判模型单独补判确认。
   cap-004 为 harvest 自真实首跑的新用例,产出经用户认可提为 golden/cap-004.md。
   另:cap-002 实跑发现行业小抄事实错误——加州搬家 Cal-T 主管机构 2018 年已由 CPUC 移交 BHGS,
   已修正 references/industry-playbooks.md 与该用例 check 措辞,属修正靶子事实错误,非调优改靶。)

## 2026-08-30 08:53 -0700  (3ce0fc6, judge=claude-sonnet-5)
- triggering: 24/24  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 4 / 跳过 0
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)

