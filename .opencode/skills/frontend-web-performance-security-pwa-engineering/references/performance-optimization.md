# Performance Optimization

## Performance Optimization

### Core Web Vitals Targets

| Metric                              | Good    | Needs Improvement | Poor    | Measurement      |
| ----------------------------------- | ------- | ----------------- | ------- | ---------------- |
| **LCP** (Largest Contentful Paint)  | < 2.5s  | 2.5s - 4.0s       | > 4.0s  | Load performance |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms - 500ms     | > 500ms | Responsiveness   |
| **CLS** (Cumulative Layout Shift)   | < 0.1   | 0.1 - 0.25        | > 0.25  | Visual stability |
| **FCP** (First Contentful Paint)    | < 1.8s  | 1.8s - 3.0s       | > 3.0s  | Initial render   |
| **TTFB** (Time to First Byte)       | < 800ms | 800ms - 1.8s      | > 1.8s  | Server response  |

### PWA-Specific Optimizations

```html
<!-- Preload critical resources -->
<link rel="preload" href="/css/main.css" as="style" />
<link rel="preload" href="/js/app.js" as="script" />
<link rel="preload" href="/fonts/inter-var.woff2" as="font" crossorigin />
<link rel="preload" href="/images/hero.webp" as="image" />

<!-- Preconnect to external origins -->
<link rel="preconnect" href="https://api.weather.example.com" />
<link rel="preconnect" href="https://api.weather.example.com" crossorigin />
<link rel="dns-prefetch" href="https://analytics.example.com" />

<!-- Defer non-critical CSS -->
<link
  rel="stylesheet"
  href="/css/main.css"
  media="print"
  onload="this.media='all'"
/>
<noscript><link rel="stylesheet" href="/css/main.css" /></noscript>

<!-- Async/defer scripts -->
<script src="/js/app.js" defer></script>
<script src="/js/analytics.js" async></script>
```

### Service Worker Performance

```javascript
// Avoid blocking the main thread in service worker
// BAD: Synchronous work in fetch handler
// self.addEventListener('fetch', (event) => {
//     const result = heavyComputation(); // Blocks SW thread
//     event.respondWith(fetch(event.request));
// });

// GOOD: Offload heavy work
self.addEventListener("fetch", (event) => {
  // Keep fetch handler minimal
  if (event.request.url.includes("/api/weather")) {
    event.respondWith(networkFirst(event.request));
  } else {
    event.respondWith(cacheFirst(event.request));
  }
});

// Use cache.addAll in install (parallel by default)
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      cache.addAll([
        // These load in parallel
        "/",
        "/index.html",
        "/css/main.css",
        "/js/app.js",
      ]),
    ),
  );
});
```

---
