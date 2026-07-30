/* ============================================================
   Paper Trail Forms — site configuration
   This is the ONLY file you need to touch to turn things on.
   ------------------------------------------------------------
   NOTHING here is a secret. Every id below is a public embed id.

   siteUrl       : canonical origin, no trailing slash. Set this the
                   same day the domain is decided; canonical tags and
                   the sitemap generator both read it.
   etsyShopUrl   : the shop front. Empty = every "Browse the shop"
                   element is hidden, so there are never broken links.
   email         : MailerLite embedded form (PUBLIC ids). When both
                   are set, the tool pages offer the email capture.
                   Until then nothing renders — the tools stay free
                   and fully usable with no signup, either way.
   adsenseClient : Google AdSense publisher id. Empty = no ad script
                   loads at all. Update /ads.txt at the same time.
   ============================================================ */
window.SITE_CONFIG = {
  siteUrl: "",
  etsyShopUrl: "https://www.etsy.com/shop/papertrailform",
  email: {
    mlAccount: "",
    mlForm: ""
  },
  adsenseClient: ""
};

(function () {
  var c = window.SITE_CONFIG;

  document.addEventListener("DOMContentLoaded", function () {
    /* Shop links: wire them up, or hide the element entirely. */
    var shop = document.querySelectorAll("[data-shop-link]");
    for (var i = 0; i < shop.length; i++) {
      if (c.etsyShopUrl) shop[i].setAttribute("href", c.etsyShopUrl);
      else shop[i].hidden = true;
    }
    /* Anything that only makes sense once the shop exists. */
    if (!c.etsyShopUrl) {
      var gated = document.querySelectorAll("[data-requires-shop]");
      for (var j = 0; j < gated.length; j++) gated[j].hidden = true;
    }
    /* Email capture stays invisible until a real form id exists. */
    if (!(c.email && c.email.mlAccount && c.email.mlForm)) {
      var mail = document.querySelectorAll("[data-requires-email]");
      for (var k = 0; k < mail.length; k++) mail[k].hidden = true;
    }
  });

  /* AdSense Auto Ads loader — inert until adsenseClient is set. */
  if (!c.adsenseClient) return;
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" +
          c.adsenseClient;
  s.crossOrigin = "anonymous";
  document.head.appendChild(s);
})();
