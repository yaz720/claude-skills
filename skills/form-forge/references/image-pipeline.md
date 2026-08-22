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

### 四、深层肌肉要配双图

被别的肌肉整个盖住的（股中间肌、肩胛下肌、腹横肌），正面高亮图只能看个大概位置。
解剖学的标准办法有两个，**任选其一另配一张**：

- **横断面**：把肢体横切一刀。例如 Gray's 的大腿中段横断面 `Gray432 color.png`，
  一眼看清股中间肌贴着股骨躲在股直肌正后方
- **深层视图**：把盖在上面那层揭掉再画

两张一起才讲得清它在哪。对照表里给这类肌肉留双图位。

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
