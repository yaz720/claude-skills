# 补剂深调 (supplement-scout)

> **状态:🚧 开发中**(触发与能力用例已写好,**尚未跑过基线**;跑通并留档后再转 ✅)

一个用于 Claude 的 **Skill**,对美国 OTC 市场上的某一类营养补充剂(Dietary Supplements)进行系统化深度调研,输出专业、结构清晰、有科学依据的中文调研报告。

## 这个技能做什么

当你想了解某类营养补充剂时,它会:

- 先向你收集需求(调研哪类补剂、使用者画像)
- 用**知识分层 + 聚焦搜索**的策略调研:基础科学知识直接用,临床共识需搜索验证,市场与产品信息完全依赖搜索
- 覆盖 15–20 个候选品牌/产品,经过硬性门槛淘汰 + 五维度打分体系筛选
- 按固定的十章框架产出报告(Executive Summary、膳食来源、化学形态对比、营养素协同网络、剂型对比、推荐剂量、功效与证据、品牌推荐等),并附认证机构说明与参考文献

## 触发场景

用户提到营养补充剂、保健品、维生素、矿物质、鱼油、益生菌、supplement、OTC supplement、营养品调研、补剂对比等话题时触发。也适用于了解某种营养素的剂型、化学形态、吸收率、适用人群、品牌推荐等场景——即使只是随口问"XX 补充剂哪个好"。

## 仓库结构

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能主文件:YAML frontmatter(触发描述)+ 完整调研工作流与报告框架 |
| `appendix_certifications.md` | 预生成的静态附录:USP Verified、NSF Certified for Sport、NSF Contents Certified、GMP 四项认证,以及 ConsumerLab、Labdoor、Clean Label Project 三家第三方检测机构的详解与认证价值速查表。生成报告时直接附于参考文献之前,无需重新生成 |

## 使用方式

1. 将本技能打包为 `.skill` 文件后安装,或将 `supplement-scout/` 目录放入 Claude 的技能目录(`SKILL.md` 与 `appendix_certifications.md` 需位于同一技能文件夹内)。
2. 在对话中提出补剂相关的调研需求,技能会自动触发并按流程产出报告。

> 打包命令(需 skill-creator 工具):`python -m scripts.package_skill <path/to/supplement-scout>`

## 报告输出

- 语言:默认中文(专业术语附英文原文),除非明确要求英文
- 长度:不少于 3000 字
- 格式:Markdown,化学形态对比、协同营养素速查表、品牌打分等使用表格;正文引用以 `[1][2]` 编号标注,末尾附完整参考文献列表
