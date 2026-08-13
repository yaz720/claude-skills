# 改名 checklist

技能改名会牵动多处。**改名前逐项过一遍**,漏一处就会出现"装了旧名 / 软链断 / 打包名不对"。

## 牵动的 7 处

1. **技能 `name`**(`SKILL.md` frontmatter 的 `name:`)
2. **文件夹名** `skills/<old>/` → `skills/<new>/`
3. **`.claude-plugin/plugin.json`** 的 `name`(若已做 L3)
4. **`.claude-plugin/marketplace.json`** 的 `plugins[].name` 和 `source`
5. **`.skill` 包**:`dist/<old>.skill` → 重打成 `dist/<new>.skill`(删旧的)
6. **软链**:`~/.claude/skills/<old>` → 删掉,重建指向 `<new>`
   ```bash
   rm ~/.claude/skills/<old>
   ln -s ~/Desktop/claude-skills/skills/<new> ~/.claude/skills/<new>
   ```
7. **GitHub repo 名**(仅当技能独占一个库时;monorepo 内改技能名不涉及库名)

## 顺序建议

1. 先改文件夹名 + `SKILL.md` 的 `name`;
2. 改软链;
3. 改清单文件(plugin.json / marketplace.json);
4. 重打 `.skill`、删旧包;
5. commit + push;
6. 若改了 GitHub repo 名:GitHub 会自动重定向旧名,但本地 remote 建议更新
   `git remote set-url origin https://github.com/yaz720/<new>.git`。

## 自检

改完跑一遍:
```bash
ls -la ~/.claude/skills/<new>            # 软链没断
grep -n "name:" skills/<new>/SKILL.md    # frontmatter 对上
ls dist/                                 # 只剩新 .skill
```
