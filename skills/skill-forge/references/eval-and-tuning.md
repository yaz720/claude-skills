# 评测与调优(eval & tuning)

## 两类测试,分开跑、分开报

| | 触发测试 (triggering) | 能力测试 (capability) |
|---|---|---|
| 测什么 | description 会不会正确 / 误触发 | 触发后活干得好不好、产出对不对 |
| 调什么 | `description` | 正文 / 脚本 |
| 怎么判 | 正例该触发、负例不该触发 | LLM 裁判 + 硬检查 |

**报告分栏**给,别混——两者失败原因和修法完全不同。

## 测试用例格式

`evals/triggering/cases.yaml`:
```yaml
- { id: trig-001, input: "帮我把这个技能打包发到我的技能库", expect: fire }
- { id: trig-neg-003, input: "帮我画一张架构流程图",        expect: no-fire }  # 护栏:该由 figure-forge 接
```

`evals/capability/cases.yaml`:
```yaml
- id: cap-002
  input: "造一个把 markdown 转成周报的技能"
  check:                       # LLM 裁判逐条判 + 可含硬检查
    - "生成了双兼容目录结构"
    - "description 以差异化价值开头且 ≤1024 字符"
    - "带了否定例"
```

## 达标线(每技能自带,不搞全局线)

`evals/bar.yaml`:
```yaml
triggering: { pass_rate: 0.9, negatives_must_pass: all }   # 负例必须全过,防误触
capability: { judge_pass_rate: 0.8, runs: 3 }              # 跑 3 次取稳定,防方差
judge_model: claude-sonnet-5                                # 缺省 Sonnet;判错才升 claude-opus-5
```

## 裁判(LLM judge)

- **缺省用 Claude Sonnet(`claude-sonnet-5`)**:够可靠,又便宜到能跑 3 次取稳定;
- **判错才升 Opus(`claude-opus-5`)**;**别用 Haiku 当裁判**(细致度不够,只配做数字数这种硬检查);
- **固定低随机度** + **明确 rubric**(就是 cases 里的 `check`)+ **结构化结论**(每条 pass/fail + 理由)。

## ⚠ preflight 前置(否则评测会骗你)

`skill-creator` 的自动触发优化(run_loop)依赖 `claude -p`。**CLI 登录令牌过期时**:
- 评测会**静默把所有触发读成 0**;
- "改写描述"那步会**崩**。
所以**评测 / 优化前先跑 `claude -p "OK"` 确认认证**(`preflight.sh` 已包含)。

## 半自动调优(档二):棘轮机制

目标:给"**已自测、带成绩单**"的修改建议(diff),**用户点头才落地**。防"按下葫芦浮起瓢"。

- **单一总分 + 全量回归**:只维护一套完整测试集;每个候选改动都对**整套**重跑、算一个**总分**。
  不逐条局部修(那会震荡)。
- **棘轮(ratchet)**:当前最好叫 `best`,候选只有**总分严格变高**才上位,否则丢弃。
  权衡型(A升B降、净值不升)**不自动收**,抛给人工判。
- **为什么不死循环**:总分**单调递增 + 有上界(全过封顶)= 必收敛、必停**。
- **无进展预算**:连续 N 次候选打不过 `best` → 判 plateau,停。

## 停止条件

1. 到达 `bar.yaml` 达标线 → 成功停;
2. 无进展预算耗尽 → plateau,停;
3. 手动叫停。

**区分真 plateau 与基准盲区**:若候选**全同分 / 全 0**,不是"改不动",是**基准量不出差别**
(重叠型技能,或认证过期)。此时报「基准盲区,请人工判」,别报"已优化到最好"。

plateau 时如实上报「最好做到 X/Y,卡在这几条」,由人决定:接受现状 / 结构性重写(能力缺口靠改 description 救不了)/ 复核测试本身是否公平。

## 分支安全

- 调优在 `tune/<name>` 分支上跑;`main` 永远 = last-known-good;
- 被棘轮采纳的每步 = 一个 commit;被否决的候选**不 commit、不留痕**;
- 结束你点头 **merge**,合完**自动删分支**(呼应全局 CLAUDE.md)。
