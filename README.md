# 生信自学指南 · 生物信息学课程配套自学资源

一个用纯 HTML / CSS / JS 构建的静态站点，作为高校生物信息学课程的配套自学资源（主要面向生物、农学等专业的本科生或低年级硕士研究生）。无构建步骤，直接托管于 GitHub Pages。

## 结构

```
index.html                 首页（文章列表）
about.html                 关于页
posts/*.html               文章页
assets/css/style.css       样式（含浅色/深色主题）
assets/js/main.js          主题切换 + 文章搜索
```

## 本地预览

```bash
python -m http.server 8000
# 打开 http://localhost:8000
```

## 新增一个课程模块

1. 复制 `posts/` 下任意一篇教程，改标题与正文。
2. 在 `index.html` 的 `#post-list` 里加一张 `<li class="post-card">` 卡片，并更新 `data-title` 以便搜索。
3. 把 `GH_USER_PLACEHOLDER` 替换成你的 GitHub 用户名（导航与关于页）。

## 部署到 GitHub Pages

将本仓库推送到 GitHub 的 `main` 分支根目录，在仓库 **Settings → Pages** 选择 `main` 分支、`/ (root)` 即可。
