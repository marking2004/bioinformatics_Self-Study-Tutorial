# 生信自学精简指南 · Bioinformatics Self-Study Guide

高校生物信息学课程配套的自学资源站，把命令行、序列分析、组学、结构预测等拆成可自学的模块（面向本科生）。

> An undergraduate bioinformatics course companion that breaks command line, sequence analysis, omics and structure prediction into self-study modules.

## 访问 / Visit

- 中文：https://marking2004.github.io/bioinformatics_Self-Study-Tutorial/
- English：https://marking2004.github.io/bioinformatics_Self-Study-Tutorial/en/

## 内容 / Contents

- 多序列比对与可视化、蛋白质序列分析/结构与功能预测、肽与蛋白质设计、系统发育分析
- 核酸序列分析与基因组学、多组学联合分析（GWAS / 通路 / 基因定位）
- 分子生物学（引物 / 载体 / CRISPR）、虚拟筛选与计算机辅助药物设计
- 常用生物信息数据库、生信软件与本地工具推荐
- MSA & visualization, protein analysis / structure & function prediction, peptide & protein design, phylogenetics
- nucleic-acid & genomics, multi-omics integration (GWAS / pathways / gene mapping)
- molecular biology (primer / vector / CRISPR), virtual screening & computer-aided drug design
- common bioinformatics databases, software and local-tool recommendations

## 技术 / Tech

基于 Hugo 构建，托管于 GitHub Pages；全站中英双语按 URL 切换（中文在 `/`，英文在 `/en/`）。

> Built with Hugo and hosted on GitHub Pages; the whole site is bilingual, switched by URL (Chinese at `/`, English at `/en/`).

## 本地预览 / Local preview

```bash
# 在 hugo/ 源码目录下
hugo server -D
# 打开 http://localhost:1313/bioinformatics_Self-Study-Tutorial/
```

## 目录结构 / Project layout

```
hugo/                        # 站点源码（本地维护，不进仓库根）
  layouts/                    # 模板（页眉/页脚/首页/文章）
  content/posts/*.md          # 各课程模块（中文）
  content/posts/*.en.md       # 对应英文翻译
  static/assets/              # 样式与脚本
public/                      # hugo 构建产物，部署到仓库根
```

## 部署 / Deploy

将 `hugo/` 构建出的 `public/` 目录上传到仓库 `main` 分支根目录，并在仓库
**Settings → Pages** 选择 `main` 分支、`/ (root)` 即可。也可用 Contents API 批量上传。

> Upload the built `public/` directory to the repo root on the `main` branch, then enable Pages
> (Settings → Pages → `main` branch, `/ (root)`).
