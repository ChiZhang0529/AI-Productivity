# Google AdSense Setup Guide

## Quick Setup

### Step 1: Get Your Publisher ID
1. Log into [Google AdSense](https://www.google.com/adsense)
2. Your Publisher ID is shown at the top: `pub-XXXXXXXXXXXXXXXX`

### Step 2: Replace Placeholder IDs
Search and replace in all HTML files:

| Placeholder | Replace With |
|-------------|--------------|
| `YOUR_PUBLISHER_ID` | Your Publisher ID (e.g., `pub-1234567890123456`) |
| `HOME-HERO-AD` | Your ad unit ID from AdSense dashboard |
| `HOME-BELOW-FEATURES` | Your ad unit ID |
| `BLOG-ABOVE-LIST` | Your ad unit ID |
| `ARTICLE-BELOW-TITLE` | Your ad unit ID |
| `ARTICLE-IN-CONTENT` | Your ad unit ID |
| `ARTICLE-BELOW-CONTENT` | Your ad unit ID |
| `PAGE-BELOW-INTRO` | Your ad unit ID |
| `FOOTER-AD` | Your ad unit ID |

### Step 3: Create Ad Units in AdSense
1. Go to AdSense Dashboard → **Ad units** → **By size**
2. Create ad units for each placement:
   - **Responsive ads** (recommended for most placements)
   - **In-article ads** (for article content)
   - **Horizontal ads** (for footer)

### Step 4: Wait for Approval
- New AdSense accounts need **2-4 weeks** for approval
- During review, use placeholder ads or test ads

---

## Ad Placement Summary

### Homepage (`index-adsense.html`)
| Position | Ad Format | Notes |
|----------|-----------|-------|
| Below hero | Responsive | After CTA buttons |
| Below articles | Responsive | After article grid |
| Above footer | Horizontal | Before footer links |

### Article Page (`article-adsense.html`)
| Position | Ad Format | Notes |
|----------|-----------|-------|
| Below title/excerpt | In-article | After author intro |
| In-content | In-article | After 2nd paragraph (auto-injected) |
| Below content | Responsive | Before tags |
| Above related | Responsive | Before related articles |

### Blog Listing (`blog-adsense.html`)
| Position | Ad Format | Notes |
|----------|-----------|-------|
| Below header | Responsive | After page description |
| Between rows | Responsive | After first row |

---

## Ad Format Reference

### Responsive (Recommended)
```html
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXX"
     data-ad-slot="XXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true">
</ins>
```

### In-Article
```html
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-client="ca-pub-XXXXX"
     data-ad-slot="XXXXX"
     data-ad-format="in-article">
</ins>
```

### Fixed Size (Horizontal)
```html
<ins class="adsbygoogle"
     style="display:block; width:100%; height:90px;"
     data-ad-client="ca-pub-XXXXX"
     data-ad-slot="XXXXX"
     data-ad-format="horizontal">
</ins>
```

---

## Google AdSense Policies (Must Follow)

### ✅ Allowed
- Maximum 3 ads per page (below content counts)
- Clear labeling as "Advertisement"
- Ads that blend with site design
- Sufficient spacing around ads

### ❌ Not Allowed
- Clickbait layout (ads mimicking content)
- Placing ads too close to interactive elements
- Encouraging clicks (arrows, "click here")
- Stacking ads vertically
- More than one ad above the fold on mobile

---

## Testing Ads (Before Site Approval)

### Enable Test Mode
Add this to enable test ads without affecting your stats:

```javascript
adsbygoogle.push({
  google_ad_client: "ca-YOUR_PUBLISHER_ID",
  enable_page_level_ads: true
});
```

### Use Test Ad Units
Google provides test IDs for development:
- **Publisher ID**: `ca-pub-5752804389868708`
- **Test Ad Slot**: `6995827397`

---

## Performance Tips

1. **Start with Auto Ads** - Let Google optimize placement
2. **Use AdSense experiments** - Test different ad formats
3. **Balance UX** - Ads shouldn't disrupt reading flow
4. **Monitor viewability** - Target 70%+ viewability
5. **Check PageSpeed** - Ads can slow load time; use async scripts

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Ads not showing | Check Publisher ID is correct |
| Layout broken | Use responsive format |
| Mobile issues | Test with `data-full-width-responsive="true"` |
| Low RPM | Add more ad placements strategically |
| Policy violation | Review [AdSense policies](https://support.google.com/adsense/answer/48182) |

---

## Files with AdSense

- `index-adsense.html` - Homepage with ads
- `article-adsense.html` - Article page with ads  
- `blog-adsense.html` - Blog listing with ads
- `js/adsense.js` - Configuration helper

Replace your current files with the `-adsense` versions after setup.
