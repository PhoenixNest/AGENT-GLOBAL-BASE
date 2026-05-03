---
name: pwa-engineering
description: Build Progressive Web Apps with Service Worker caching strategies, Web App Manifest, background sync, and push notifications — delivering native-app-quality web experiences that work offline and install on mobile home screens.
version: "1.0.0"
---

# PWA Engineering

| Competency         | Description                                                  | Quality Criteria                                                                                                        |
| ------------------ | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Service Worker     | Implement Service Worker with appropriate caching strategies | Cache-first for static assets; network-first for API data; stale-while-revalidate for infrequently updated content      |
| Offline Experience | Design offline-first UX with background sync                 | App remains functional for core tasks offline; background sync queues failed requests; user notified of sync state      |
| Web App Manifest   | Configure manifest for installability across platforms       | Manifest includes all required icons (192px, 512px), `start_url`, `display: standalone`, and `theme_color`              |
| Push Notifications | Implement Web Push API with permission best practices        | Permission requested contextually (not on page load); notification content is actionable; click opens relevant app page |

## Execution Guidance

### Service Worker Caching Strategy

```javascript
// workbox-based strategy (via vite-plugin-pwa)
registerRoute(
  ({ request }) => request.destination === "image",
  new CacheFirst({
    cacheName: "images",
    plugins: [
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 30 * 24 * 60 * 60,
      }),
    ],
  }),
);

registerRoute(
  ({ url }) => url.pathname.startsWith("/api/"),
  new NetworkFirst({ cacheName: "api-cache", networkTimeoutSeconds: 3 }),
);
```

### PWA Audit Checklist (Lighthouse)

| Category          | Target Score |
| ----------------- | ------------ |
| Performance       | ≥ 90         |
| Accessibility     | ≥ 90         |
| Best Practices    | ≥ 90         |
| PWA (installable) | All criteria |

Run `lighthouse --only-categories=performance,accessibility,best-practices,pwa` in CI on every PR targeting the web release branch. Score drops > 5 points block merge.
