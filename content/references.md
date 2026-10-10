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

## 教材与书目

### 纸质教材（仅著录，不提供电子版）

以下均为**在版正式出版物**，本站只作书目著录，**不提供 PDF 下载或扫描件**——请通过图书馆、出版社或正规书店获取。前两本是本站点实验内容的参考体系来源。

| 书名 | 作者 / 主编 | 出版社 | 年份 | ISBN |
|---|---|---|---|---|
| 生物信息学实验指导 | 樊龙江、叶楚玉 主编 | 科学出版社 | 2022 | 978-7-03-072304-8 |
| 生物信息学实验 | 陈铭、原春晖 主编 | 科学出版社 | 2022 | 978-7-03-071689-7 |
| 生物信息学（第二版） | 樊龙江 主编 | 科学出版社 | 2021 | 9787030681010 |
| 生物信息学（第四版） | 陈铭 主编 | 科学出版社 | — | — |
| 生物信息学（101 计划核心教材） | 陈铭、吕晖 主编 | — | — | — |
| 生物信息学分析实践 | 吴祖建 等 编著 | — | — | — |
| 生物信息学 | 王晶晶、蔡赫 编著 | 清华大学出版社 | 2014 | 978-7-302-36241-8 |
| 生物信息学导论——面向高性能计算的算法与应用 | 王勇献、王正华 编著 | 清华大学出版社 | 2011 | 978-7-302-25022-7 |
| 分子进化与系统发育 | 根井正利（M. Nei）、库马尔（S. Kumar） | — | — | — |
| 轻松构建系统发育树：实用操作方法和理论（第 4 版） | B. G. Hall 著；陈士超、傅承新、吴晓运 译 | — | — | — |

说明：标"—"的字段表示暂未核实到可靠出处，留空以待补充，不做推测填写。《生物信息学（第二版）》（樊龙江 主编）的配套教学材料由主编实验室公开在其课题组主页（ibi.zju.edu.cn/bioinplant），需要的读者可自行查找。

### 开放获取的在线教材与课程（可直接点开学）

与纸质书相比，这些资源更新更快、且可免费在线阅读，适合作为本站的即时补充：

- **[Galaxy Training Network](https://training.galaxyproject.org/)**：Galaxy 官方培训网络，按主题组织的完整教程（含中文翻译），从基础到高级，全部可在线跟着做。
- **[EMBL-EBI 培训材料](https://www.ebi.ac.uk/training/)**：欧洲生物信息学研究所的在线课程与教程库，涵盖序列分析、结构、组学，质量很高。
- **[Bioinformatics Algorithms](https://www.bioinformaticsalgorithms.org/)**：Pevzner 与 Compeau 合著的教材官网，配套在线课程与习题，算法讲得透彻。
- **[Modern Statistics for Modern Biology](https://www.huber.embl.de/msmb/)**：Susan Holmes 与 Wolfgang Huber 著，免费在线，专门讲生信需要的统计思维。
- **[Bioconductor 在线书](https://bioconductor.org/books/)**：Bioconductor 官方书库，R 生信分析的权威参考，多本可免费在线阅读。
- **[R for Data Science（第 2 版）](https://r4ds.hadley.nz/)**：Hadley Wickham 等著，免费在线，R 数据处理的现代写法，打基础首选。
- **[Biostar Handbook](https://www.biostarhandbook.com/)**：面向生信实战的系统教程，含大量可复现的命令行示例。
- **[中国大学 MOOC](https://www.icourse163.org/)**：国内高校公开课平台，可搜索"生物信息学"相关课程，母语授课、可跟进度。

想检验自己的掌握程度，用上面英文资源里提到的 **[Rosalind](https://rosalind.info)** 按算法主题刷题即可。

## 使用建议

0. 代码约定：命令行 / 工具步骤统一用 **bash**（与编程语言无关，因为 BLAST、mafft、samtools 等本质是 shell 程序）；**数据分析、作图、统计**环节同时给 **R 与 Python** 两种写法，任选其一即可。
1. 先在本站建立整体框架，再挑 1–2 个上面的项目深入。
2. 遇到命令行卡住，优先看 learn-genomics-in-linux 与 DTC-Bioinformatic-Course。
3. 想刷题练编程，去 Rosalind；想跟中文视频，去生信技能树 B 站。
4. 所有外部链接请遵守各自项目的开源协议与署名要求。
