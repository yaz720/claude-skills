# 改名 checklist

技能改名会牵动多处。**改名前逐项过一遍**,漏一处就会出现"装了旧名 / 软链断 / 打包名不对 /
别的技能指向一个不存在的技能"。

清单分两段:**第一段是被改名技能自己的连带物**(1–7),**第二段是它在别处留下的引用**(8)。
第二段最容易漏——因为它不在你正在改的那个文件夹里。

## 一、被改名技能自己(7 处)

1. **技能 `name`**(`SKILL.md` frontmatter 的 `name:`)
2. **文件夹名** `skills/<old>/` → `skills/<new>/`(用 `git mv`,保留文件历史)
3. **`.claude-plugin/plugin.json`** 的 `name`(若已做 L3)
4. **`.claude-plugin/marketplace.json`** 的 `plugins[].name` 和 `source`
5. **`.skill` 包**:`dist/<old>.skill` → 重打成 `dist/<new>.skill`(**删旧的**,否则留下孤儿包)
6. **软链**:`~/.claude/skills/<old>` → 删掉,重建指向 `<new>`
   ```bash
   rm ~/.claude/skills/<old>
   ln -s ~/Desktop/claude-skills/skills/<new> ~/.claude/skills/<new>
   ```
7. **GitHub repo 名**(仅当技能独占一个库时;monorepo 内改技能名不涉及库名)
8. **技能自己的中文名 / 标题**:`README.md` 首行标题、总库 README 的技能表与目录树
   (含目录树的空格对齐——新旧名长度不同会错位)

## 二、别处对它的引用(最易漏)

改名不是一个文件夹的事。**一个成熟技能会被兄弟技能反复点名**,典型有四类:

| 类型 | 在哪 | 是否进模型上下文 |
|---|---|---|
| **护栏指路牌** | 兄弟技能 `SKILL.md` 的 description:"不要触发:…(→`<old>`)" | ✅ **活的**,直接影响触发 |
| **"不负责"清单** | 兄弟技能 `README.md` | ❌ 仅给人看 |
| **评测用例注释** | 兄弟技能 `evals/triggering/cases.yaml` 的 `# → <old>` | ❌ 测试代码 |
| **举例 / 历史叙述** | skill-forge 自己的命名规范举例、评测踩坑记录 | ❌ 文档 |

四类都该改(否则读者会去找一个不存在的技能),但**只有第一类改完需要重跑触发评测**。

### 传导:兄弟技能的 `.skill` 包也过时了

这是最隐蔽的一步。**你改了兄弟技能的文件,它的包就旧了。**

判据很简单——看**改动的文件进不进包**:

- 改了兄弟技能的 `SKILL.md` 或 `README.md` → **进包,必须重打**
- 只改了兄弟技能的 `evals/` → **不进包,不用重打**(打包时 evals 被 skip)

包是给人下载安装的。里面封着一个指向已注销技能的指路牌,比仓库里留个旧字串严重得多。

## 顺序建议

1. `git mv` 文件夹 + 改 `SKILL.md` 的 `name`;
2. 改软链(立刻生效,可当场验证技能仍能加载);
3. **全库扫一遍旧名**,把二、里那四类引用一次改净;
4. 改清单文件(plugin.json / marketplace.json);
5. **重打受影响的所有包**——被改名技能的 + 每个 `SKILL.md`/`README.md` 被改动的兄弟技能的;删旧包;
6. 若动了任何 description(第一类引用),**重跑触发评测**;
7. commit + push;
8. 若改了 GitHub repo 名:GitHub 会自动重定向旧名,但本地 remote 建议更新
   `git remote set-url origin https://github.com/<user>/<new>.git`。

## 自检

前两条是文本层,第三条是**包内层**——`.skill` 是 zip,普通 `grep -r` 扫不进去,
这正是最容易漏检的地方。

```bash
# 1) 软链没断 + frontmatter 对上
ls -la ~/.claude/skills/<new> && grep -n "^name:" skills/<new>/SKILL.md

# 2) 全库文本层零残留(含 README / description / 用例注释)
grep -rn "<old>" . --exclude-dir=.git --exclude-dir=__pycache__ || echo "✅ 文本层干净"

# 3) 所有 .skill 包内零残留 —— 二进制,必须解开来看
for s in dist/*.skill; do
  n=$(unzip -p "$s" '*' 2>/dev/null | grep -c "<old>"; true)
  [ "${n:-0}" = 0 ] || echo "❌ $(basename "$s"): $n 处旧名"
done

# 4) 没有旧名孤儿包
ls dist/ | grep "<old>" && echo "❌ 有孤儿包" || echo "✅ 无孤儿包"
```

## 踩过的坑

`doctor-finder` → `care-scout` 那次:文件夹、name、软链、自己的包都对了,**但漏了三个兄弟技能的包**
(`form-forge` 1 处、`nutrition-analyzer` 2 处、`skill-forge` 7 处仍封着旧名)。
原因就是当时的 checklist 只想着"被改名的那个技能",没想到改名会**反向波及**别人,
而别人的包也因此需要重打。上面自检的第 3 条就是为这个加的。
