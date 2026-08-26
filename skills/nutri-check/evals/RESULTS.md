# nutri-check 评测记录

每次 `eval_run.py` 自动追加一段(最新在文件末尾)。分数是**单跑快照、有噪声**,
只记分数/失败项/产出去向,不含产出正文(故隐私安全)。

## 2026-08-22 12:17 -0700  (980fc21, judge=claude-sonnet-5)
- triggering: 26/26  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 0 / 跳过 4  (跳过: cap-001, cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)

## 2026-08-22 12:37 -0700  (6114ea4, judge=claude-sonnet-5)
- triggering: 26/26  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 1 / 跳过 3  (跳过: cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)

## 2026-08-22 13:51 -0700  (3ba6737, judge=claude-sonnet-5)
- triggering: 26/26  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 1 / 跳过 3  (跳过: cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)

## 2026-08-23 15:37 -0700  (86ed65a, judge=claude-sonnet-5)
- triggering: 26/26  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 1 / 跳过 3  (跳过: cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)
- 判读:本跑是**回归验证**——description 的排除项由「找营养师或医生(→care-scout)」
  删成「找营养师(→care-scout)」后重跑。删「或医生」的理由:"营养师"与"营养分析"
  共享"营养"二字,是真实的高危误触发,必须留;"医生"与"算某份食物热量"语义距离极远,
  不构成混淆,反而给模型多一个反向拉力(如"医生让我控糖,算算这碗粥多少糖"本该触发)。
  与上一跑(3ba6737)同为 26/26,14 正 12 负全部保持原判,确认无回归。

## 2026-08-25 22:23 -0700  (052a461, judge=claude-sonnet-5)
- triggering: 26/26  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 1 / 跳过 3  (跳过: cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)
- 判读:改名跑(nutrition-analyzer → nutri-check,中文名「食物营养分析」→「营养体检」)。
  本技能自己的 description **一字未改**,只动了 `name` 与文件夹,所以这一跑测的不是
  改动效果,而是**确认改名没有意外碰坏什么** —— 26/26 与前两跑完全一致,确认干净。
  真正需要盯的是姊妹技能 care-scout:它的 description 里那条护栏指路牌由
  「→nutrition-analyzer」改成了「→nutri-check」,那才是活的改动,同日同样满分(22/22)。

## 2026-08-25 23:28 -0700  (d4e8a35, judge=claude-sonnet-5)
- triggering: 26/26  (负例全过: True)  [单跑快照,有噪声]
- capability: 已判 1 / 跳过 3  (跳过: cap-002, cap-003, cap-004)
  产出:逐次在 outputs/(gitignore、可重生);认可的存 golden/(入库、当可视基线)

