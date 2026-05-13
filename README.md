# AI Productivity 静态博客

一个面向海外的 AI 内容分享博客，使用 HTML + Tailwind CSS 构建，可部署到 Vercel 或 GitHub Pages。

## 项目简介

主要分享 AI 相关内容，包括 ChatGPT 使用技巧、AI 生产力工具、提示词优化等。

## 功能特性

- **响应式设计** - 移动端优先，适配所有设备
- **深色主题** - 参考 theainest.com 设计的深色 UI
- **SEO 优化** - 内置 meta 标签、Open Graph、Twitter Card
- **文章管理** - 通过 `js/articles.js` 管理所有文章
- **静态部署** - 无需后端，可直接部署到任何静态托管服务

## 文件结构

```
static-blog/
├── index.html          # 首页
├── blog.html           # 文章列表页
├── article.html        # 文章详情页（支持 URL 参数）
├── about.html          # 关于页面
├── contact.html        # 联系页面
├── privacy.html        # 隐私政策
├── js/
│   └── articles.js     # 文章数据
├── posts/             # 文章 Markdown 源文件
└── posts_html/        # 文章静态 HTML 版本
```

## 快速开始

1. **克隆仓库**
2. **编辑文章** - 修改 `js/articles.js` 添加新文章
3. **自定义** - 修改网站名称、颜色、内容
4. **部署** - 推送到 GitHub Pages 或使用 Vercel 部署

## 部署

### GitHub Pages
1. 推送代码到 GitHub 仓库
2. 进入仓库 Settings > Pages
3. 选择 `main` 分支和 `/ (root)` 文件夹
4. 保存 - 站点将位于 `username.github.io/repo-name`

### Vercel
1. 推送代码到 GitHub
2. 访问 [vercel.com](https://vercel.com)
3. 导入 GitHub 仓库
4. Vercel 自动识别静态站点 - 点击部署

---
Made with ❤️ using HTML + Tailwind CSS
