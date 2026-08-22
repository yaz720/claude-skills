# 配图流水线：从维基共享资源取版权干净的解剖图

这份文档是本技能最硬的部分，里面每一条都是踩出来的。**照做能省掉三轮返工。**

## 为什么不用现成的健身网站

网上那些「肌肉人做动作、发力部位实时高亮」的图，绝大多数出自 MuscleWiki、
Muscle & Motion、Gymvisual 这类商业站，**有版权**。免费能看不等于能往笔记里搬。

干净的来源只有这几类，全部在维基共享资源上（**Commons 按政策只收自由授权内容**，
所以不必死磕某一个作者）：

| 来源 | 给什么 | 授权 |
|---|---|---|
| Anatomography / BodyParts3D | 灰骨架上目标肌肉标红，部分是旋转动图 | CC BY-SA 2.1 JP |
| Gray's Anatomy (1918) | 经典解剖版画，覆盖极全 | 公有领域 |
| OpenStax College | 彩色带标注的教材图 | CC BY |

**Anatomography 只覆盖约 28 块常用肌肉**，肩背髋很全，但胸大肌、腹肌群、
小腿、竖脊肌它没有。缺口用后两家补，风格略有出入但都能用。

## 先查已验证索引

`assets/muscles.tsv` 收了 **42 块常用肌肉的已验证文件名**（人工逐张目视确认过），
含部位、分量、原始文件名、作者、授权。**先查表，查不到再搜**，能省掉大量试错：

```bash
python scripts/fetch_muscle_images.py --out <图片目录> --from-index          # 全取
python scripts/fetch_muscle_images.py --out <图片目录> --muscles 前锯肌 臀中肌  # 只取几块
```

## 索引外的肌肉：现搜

```bash
python scripts/fetch_muscle_images.py --search "Popliteus" --cn 腘肌 --dry-run   # 先看候选
python scripts/fetch_muscle_images.py --search "Popliteus" --cn 腘肌 --out <目录> # 取第一名
```

搜到并验收合格后，**回 `assets/muscles.tsv` 补一行**，下次就不用再搜。

## 四条踩出来的坑

### 一、拉丁拼法陷阱（最容易误判「没有」）

维基收录的拼法常与教科书不同。**一次搜空绝不等于没有。**

| 教科书 | 维基上实际是 |
|---|---|
| Vastus intermedius | `Vastus intermedialis` |
| Sternocleidomastoid | `Sternocleidomastoideus` |
| External oblique | `Abdominal external oblique` / `Obliquus externus abdominis` |

脚本里的 `SPELLING_HINTS` 已内置这些变体并会自动重试。遇到新的变体，
**补进 `SPELLING_HINTS` 而不是就此认定维基上没有**。

### 二、作者黑名单

图本身合法，但不适合放进健身笔记：

- `Anatomist90` —— 全是**尸体解剖照片**，准确但会吓到人
- `DrJanaOfficial` —— 不少是**视频截图**，糊

脚本已在评分前把这两位过滤掉。

### 三、按词搜会撞车

搜 `external oblique` 会撞上下颌骨的「下颌斜线 external oblique line of mandible」；
搜 `rectus femoris` 会撞上颈部的 `rectus capitis posterior minor`。

所以必须做**严格标题校验**：文件名要含完整目标词组，且不含
`mandible / skull / capitis / cervicis / oculi / oris` 等黑名单词。脚本已实现。

### 四、生物学与非解剖图撞词

不少肌肉名同时是**动植物的种加词**。搜 `Multifidus` 会撞上海百合 `Comaster multifidus`、
海参 `Astichopus multifidus`、红花属 `Carthamus multifidus`、毛茛 `Ranunculus multifidus`，
搜出一堆生态照片。搜 `Piriformis` 会撞上「梨状肌综合征住院天数统计」这类**医学图表**。

脚本已加两道过滤：`BAD_BIOLOGY` 明确黑名单，加上「属名 + 种加词」的正则兜底。

> ⚠ **那条正则只对单词肌肉名启用。** 双词解剖名（`Serratus anterior`）本身就长成
> 「首字母大写属名 + 小写种加词」的样子，无差别套用会把正确结果全滤掉——这是实测踩过的自伤。

### 五、别把「查询失败」当成「维基上没有」

这是最阴险的一条，因为两者的表象完全一样：**空结果**。

连续查询容易被 Commons 限流，如果代码里写的是 `except: continue`，
失败会被静默吞掉，你看到的就是「没有候选」，于是错误地断定这块肌肉维基上没有。

脚本现在的做法：**收集每一次失败并在全部失败时抛错**，明确告诉你
「这不等于没有，多半是限流，隔几秒重试」；查询之间加 0.6 秒节流、失败后退避 2 秒。

自己写抓取逻辑时也照此办理，**永远把「搜到了但没有」和「压根没搜成」分开报**。

### 六、深层肌肉要配双图

被别的肌肉整个盖住的（股中间肌、肩胛下肌、腹横肌），正面高亮图只能看个大概位置。
解剖学的标准办法有两个，**任选其一另配一张**：

- **横断面**：把肢体横切一刀。例如 Gray's 的大腿中段横断面 `Gray432 color.png`，
  一眼看清股中间肌贴着股骨躲在股直肌正后方
- **深层视图**：把盖在上面那层揭掉再画

两张一起才讲得清它在哪。对照表里给这类肌肉留双图位。

## 已知缺口

- **多裂肌 Multifidus** —— 分类目录、前缀、拉丁全称都试过，维基共享资源上没有干净的解剖图。
  卡里只能写文字。哪天找到合适的图再补进 `assets/muscles.tsv`。

## 取图与体积

- **PNG/JPG 用缩略图**：`Special:FilePath/<文件名>?width=700`，别下 4500px 原图
- **GIF 取原图**保住动画，之后用 Pillow 缩到 320px，体积能降七成
  （实测 19MB → 7MB，动画照转）
- 请求**必须带 User-Agent**，否则会被拒
- 下载后校验文件头，拿到重定向页而不是图片时要报错，别把 HTML 存成 `.gif`

## 下载后必须目视验收（这步不是可选的）

```bash
python scripts/contact_sheet.py <图片目录>
```

拼成一张总览图逐格看。**实测第一轮 40 张里有 3 张是错的**：一张视频截图、
一张尸体照、一张下颌骨。黑名单拦不干净所有货色，不看一眼，错图会一直躺在笔记里。

发现错的就换拼法重取，并回 `assets/muscles.tsv` 更正。

## 署名登记

CC BY-SA 要求署名。**每张图都记四项**：本地文件名 / 原始文件名 / 作者 / 授权，
汇总在肌肉名称对照表末尾的「图片来源与授权」表里。公有领域的也一并记，
将来自己回头查来源时用得上。

## 用户自己的图和教练拍的照片

- 用户从别处截的图可以**当参考给你看**，你据此理解动作、自绘一张原创的进库，
  既拿到信息又不欠版权
- **教练拍的本人动作照片/视频截图属于个人身份信息**，应放进用户库里
  不上传的私密附件目录（由用户的项目配置决定具体路径），卡里引用但不进公开仓库
