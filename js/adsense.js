/**
 * Google AdSense Configuration
 * 
 * SETUP INSTRUCTIONS:
 * 1. Replace 'YOUR_PUBLISHER_ID' with your actual AdSense Publisher ID
 *    (format: pub-XXXXXXXXXXXXXXXX)
 * 2. Replace ad slot IDs (data-ad-slot) with your actual ad unit IDs
 *    (found in your AdSense dashboard under "Ad units")
 * 
 * AD PLACEMENT STRATEGY:
 * - index.html: Hero below, between article cards, above footer
 * - blog.html: Above article grid, between rows
 * - article.html: Below title, in-content after paragraph 3, above related
 * - about.html: After intro content
 * - contact.html: After form
 * - privacy.html: In middle of content
 */

const ADSENSE_CONFIG = {
  // REQUIRED: Replace with your AdSense Publisher ID
  publisherId: 'YOUR_PUBLISHER_ID', // e.g., 'pub-1234567890123456'
  
  // AD SLOT CONFIGURATIONS
  slots: {
    // Homepage ads
    homeHero: {
      slotId: 'HOME-HERO-AD',      // Replace with your ad unit ID
      format: 'responsive',
      layout: 'in-article'
    },
    homeBelowFeatures: {
      slotId: 'HOME-BELOW-FEATURES', // Replace with your ad unit ID
      format: 'responsive',
      layout: 'in-article'
    },
    
    // Blog listing ads
    blogAboveList: {
      slotId: 'BLOG-ABOVE-LIST',    // Replace with your ad unit ID
      format: 'responsive',
      layout: 'in-article'
    },
    
    // Article page ads
    articleBelowTitle: {
      slotId: 'ARTICLE-BELOW-TITLE', // Replace with your ad unit ID
      format: 'responsive',
      layout: 'in-article'
    },
    articleInContent: {
      slotId: 'ARTICLE-IN-CONTENT',  // Replace with your ad unit ID
      format: 'in-article',
      layout: 'in-article'
    },
    articleBelowContent: {
      slotId: 'ARTICLE-BELOW-CONTENT', // Replace with your ad unit ID
      format: 'responsive',
      layout: 'in-article'
    },
    
    // Other page ads
    pageBelowIntro: {
      slotId: 'PAGE-BELOW-INTRO',    // Replace with your ad unit ID
      format: 'responsive',
      layout: 'in-article'
    },
    
    // Footer ad (all pages)
    footer: {
      slotId: 'FOOTER-AD',          // Replace with your ad unit ID
      format: 'horizontal',
      layout: 'in-article'
    }
  }
};

/**
 * Creates an AdSense ad unit HTML
 * @param {string} slotName - Name of the ad slot from config
 * @param {string} customClass - Additional CSS classes
 * @returns {string} HTML string for the ad unit
 */
function createAdUnit(slotName, customClass = '') {
  const slot = ADSENSE_CONFIG.slots[slotName];
  if (!slot) return '';
  
  return `
    <div class="adsbygoogle-container ${customClass}">
      <ins class="adsbygoogle"
           style="display:block; width:100%; height:250px;"
           data-ad-client="ca-${ADSENSE_CONFIG.publisherId}"
           data-ad-slot="${slot.slotId}"
           data-ad-format="${slot.format}"
           data-full-width-responsive="true">
      </ins>
    </div>
  `;
}

/**
 * Initialize AdSense and push ads
 * Call this after page load
 */
function initAds() {
  if (typeof adsbygoogle !== 'undefined') {
    (adsbygoogle = window.adsbygoogle || []).push({});
  }
}

/**
 * Insert in-content ad into article body
 * Splits content at approximately 1/3 mark
 * @param {string} content - Original HTML content
 * @param {string} adHtml - Ad unit HTML to insert
 * @returns {string} Content with ad inserted
 */
function insertInContentAd(content, adHtml) {
  // Find the second </p> tag (after intro paragraph)
  let count = 0;
  let insertIndex = -1;
  
  for (let i = 0; i < content.length; i++) {
    if (content.substring(i, i + 4) === '</p>') {
      count++;
      if (count === 2) {
        insertIndex = i + 4;
        break;
      }
    }
  }
  
  if (insertIndex > 0) {
    return content.substring(0, insertIndex) + adHtml + content.substring(insertIndex);
  }
  
  return content;
}
