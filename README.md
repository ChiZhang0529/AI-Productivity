# Static Blog Website

A clean, responsive, SEO-optimized static blog built with HTML and Tailwind CSS. Deployable directly to Vercel or GitHub Pages.

## Features

- **Responsive Design** - Mobile-first approach, perfect on all devices
- **SEO Optimized** - Built-in meta tags, Open Graph, Twitter cards, structured data
- **Fast Loading** - Pure HTML/CSS, no heavy frameworks, Tailwind via CDN
- **Easy to Maintain** - Add articles by editing a single JavaScript file
- **Clean Code** - Well-organized, commented, easy to customize

## Pages Included

| Page | Description |
|------|-------------|
| `index.html` | Homepage with hero, featured articles, newsletter |
| `blog.html` | Article listing with category filters and sorting |
| `article.html` | Single article view with related posts |
| `about.html` | About page with team and mission |
| `contact.html` | Contact form with validation |
| `privacy.html` | Privacy policy (GDPR compliant) |

## Project Structure

```
static-blog/
├── index.html          # Homepage
├── blog.html           # Blog listing
├── article.html        # Single article (uses URL params)
├── about.html          # About page
├── contact.html        # Contact page
├── privacy.html        # Privacy policy
├── js/
│   └── articles.js     # Article data - edit this to add posts!
└── README.md           # This file
```

## Quick Start

1. **Clone or Download** this repository
2. **Edit articles** in `js/articles.js` (see below)
3. **Customize** the site name, colors, and content
4. **Deploy** to Vercel or GitHub Pages

## Adding Articles

Open `js/articles.js` and add new articles to the `articles` array:

```javascript
{
  id: "your-article-slug",
  title: "Your Article Title",
  excerpt: "A brief description (max 200 chars)",
  date: "2024-01-15",
  category: "Web Development",
  author: "Author Name",
  tags: ["tag1", "tag2"],
  content: `
    <p>Your HTML content here...</p>
    <h2>Section Title</h2>
    <p>More content...</p>
  `
}
```

## Customization

### Site Name
Search and replace `BlogName` with your site name across all files.

### Colors
Edit the Tailwind config in each HTML file:
```javascript
tailwind.config = {
  theme: {
    extend: {
      colors: {
        primary: '#2563eb',  // Change to your brand color
      }
    }
  }
}
```

### Domain
Update all `https://yourblog.com` references with your actual domain.

### Social Links
Update the social media links in the footer section of each page.

## Deployment

### Vercel (Recommended)

1. Push the code to a GitHub repository
2. Go to [vercel.com](https://vercel.com)
3. Import your GitHub repository
4. Vercel auto-detects static sites - click Deploy
5. Your site will be live at `your-project.vercel.app`

### GitHub Pages

1. Push the code to a GitHub repository
2. Go to repository Settings > Pages
3. Select "Deploy from a branch"
4. Choose `main` branch and `/ (root)` folder
5. Save - site will be at `username.github.io/repo-name`

### Manual Upload

Simply upload all files to any static hosting service (Netlify, Cloudflare Pages, etc.)

## SEO Checklist

- [x] Meta title and description
- [x] Open Graph tags for social sharing
- [x] Twitter Card meta tags
- [x] Semantic HTML structure
- [x] Mobile-responsive design
- [x] Fast loading (no heavy scripts)
- [x] Clean URLs (`article.html?id=slug`)

For better SEO, consider:
- Adding `sitemap.xml`
- Setting up Google Search Console
- Adding Google Analytics
- Implementing structured data (JSON-LD)

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## License

Free to use for personal and commercial projects.

---

Made with ❤️ using HTML + Tailwind CSS
