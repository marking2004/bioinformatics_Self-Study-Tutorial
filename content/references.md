---
title: "参考资料"
date: 2026-10-05
draft: false
---

这里收集一批**适合本科生自学**的生物信息学外部教程与代码项目，按"英文 / 中文"分组。它们大多免费、开源，且偏重"动手跑命令"。把它们当作本站的补充阅读材料即可——遇到不懂的工具或概念，先回来翻对应的模块。

## 英文资源（重命令行 / 基因组，适合入门）

- **[learn-genomics-in-linux](https://github.com/doxeylab/learn-genomics-in-linux)**（滑铁卢大学）：任务式命令行基因组学教程，从 Linux → BLAST → 组装 → 注释 → 转录组，一步一步带着跑，最贴本站定位。
- **[Fundamentals-of-Bioinformatics](https://github.com/NIGMS/Fundamentals-of-Bioinformatics)**（达特茅斯学院）：Bash + 云计算 + Conda 的 Jupyter 教程，含从 SRA 下数据、组装注释基因组的完整流程。
- **[genomics-workshop](https://github.com/datacarpentry/genomics-workshop)**（The Carpentries）：经典基因组学工作坊教材，适合零基础小班/自学。
- **[bioinformatics_tutorials](https://github.com/faylward/bioinformatics_tutorials)**（弗吉尼亚理工）：由浅入深、前后衔接的短教程，前 10 篇建议按顺序学。
- **[learning-bioinformatics-at-home](https://github.com/Uzocodex/learning-bioinformatics-at-home)**（哈佛信息学整理）：Unix / R / Python / 统计 / RNA-seq / 单细胞 的超全链接大礼包，适合当索引书签。
- **[DTC-Bioinformatic-Course](https://github.com/beajorrin/DTC-Bioinformatic-Course)**（基于 WSL）：在 Windows 上用 WSL 跑生信的入门课，**对国内 Windows 用户特别友好**。
- **[Rosalind](https://rosalind.info)**（非 GitHub）：经典生信算法刷题平台，用 Python/Biopython 解题，练手感首选。

## 中文资源（母语友好，社区活跃）

- **[生信技能树 Jimmy（jmzeng1314）](https://github.com/jmzeng1314)**：国内最活跃的生信公益社区之一；配套论坛 [bio-info-trainee.com](http://www.bio-info-trainee.com/) 与 B 站"100 小时生信工程师教学视频"免费公开。
- **[徐洲更（xuzhougeng）](https://github.com/xuzhougeng)**：《生信初学者指南》作者，文字通俗、上手快。
- **[生信菜鸟团博客](http://www.bio-info-trainee.com/)**：从入门到进阶的推文目录，长期更新的实战笔记。

## 补充资源（华人 / 数学与数据科学基础）

以下资源多为原中国国内高校或华裔研究者维护；其中数学与数据科学部分，特别适合补本站的"前置功"：

- **[bioinfomatics（xulinpan）](https://github.com/xulinpan/bioinfomatics)**：以抑癌基因 **PTEN** 为真实案例的可复现生信教程，结合公开数据库记录 + Python 流程 + 分章 LaTeX 讲义（共 22 章），串起"数据库 → 序列 → 蛋白 → 结构域 → 比对 → 系统发育 → 结构(AlphaFold) → 变异 → 表达 → 富集 → 网络 → 分子对接 → 分子动力学 → 机器学习 → 多组学"。与本站综合实战思路一致，适合想看一个完整范例的本科生。（注：仓库名拼写为 bioinfomatics。）
- **[mathds（xulinpan）](https://github.com/xulinpan/mathds)**：用 **R bookdown** 写的《数据科学数学》本科教材雏形，12 章覆盖函数与模型、向量矩阵、数据几何、概率、统计推断、线性回归、分类、优化、正则化与高维、降维等。生信所需的数学 / 统计底子可在此补。
- **[dataScience（xulinpan）](https://github.com/xulinpan/dataScience)**：云南大学机器学习课程讲义（含 R 与 Python 简介、KNN、logistic 回归、ggplot2 等），中文、偏应用，适合作为生信统计 / 机器学习的入门补充。
- **[bioinfo-for-dummies（h4rvey-g）](https://github.com/h4rvey-g/bioinfo-for-dummies)**：中文生信入门书《学个毛生信》的 Quarto 源码，面向零基础，含实战、延伸阅读等章节。母语友好，适合先建立直觉。

## 使用建议

0. 代码约定：命令行 / 工具步骤统一用 **bash**（与编程语言无关，因为 BLAST、mafft、samtools 等本质是 shell 程序）；**数据分析、作图、统计**环节同时给 **R 与 Python** 两种写法，任选其一即可。
1. 先在本站建立整体框架，再挑 1–2 个上面的项目深入。
2. 遇到命令行卡住，优先看 learn-genomics-in-linux 与 DTC-Bioinformatic-Course。
3. 想刷题练编程，去 Rosalind；想跟中文视频，去生信技能树 B 站。
4. 所有外部链接请遵守各自项目的开源协议与署名要求。
