# 生信自学指南 · 生物信息学课程配套自学资源

一个用纯 HTML / CSS / JS 构建的静态站点，作为高校生物信息学课程的配套自学资源（面向本科生）。
无构建步骤，直接托管于 GitHub Pages。**全站中英双语**（右上角 EN / 中文 切换，偏好保存在 localStorage）。

## 课程模块（13 个）

- 基础环境：Linux 与命令行、序列比对与 BLAST、RNA-seq 实战
- 序列与进化：多序列比对与可视化、蛋白质序列分析/结构与功能预测、肽与蛋白质设计、系统发育分析
- 基因组与组学：核酸序列分析与基因组学、多组学联合分析（GWAS / 通路 / 基因定位）
- 实验与应用：分子生物学（引物 / 载体 / CRISPR）、虚拟筛选与计算机辅助药物设计
- 资源：常用生物信息数据库、生信软件与本地工具推荐

## 结构

```
index.html                 首页（模块卡片列表）
about.html                 关于页
posts/*.html               各课程模块教程页（中英双语）
assets/css/style.css       样式（浅色/深色主题 + 双语显隐）
assets/js/main.js          主题切换 + 中英双语切换 + 模块搜索
```

## 本地预览

```bash
python -m http.server 8000
# 打开 http://localhost:8000
```

## 新增一个课程模块

1. 复制 `posts/` 下任意一篇教程，改标题与正文。
2. 同一段内容用 `<div class="lang-zh">…</div>` 与 `<div class="lang-en">…</div>` 包裹两份；
   标题 / 标签 / 按钮等短文本用 `<span class="lang-zh">…</span>` / `<span class="lang-en">…</span>`。
3. 在 `index.html` 的 `#post-list` 里加一张 `<li class="post-card">` 卡片，并在 `data-title` 里同时写入中英文关键词以便搜索。

## 部署到 GitHub Pages

将本仓库推送到 GitHub 的 `main` 分支根目录，在仓库 **Settings → Pages** 选择 `main` 分支、`/ (root)` 即可。
