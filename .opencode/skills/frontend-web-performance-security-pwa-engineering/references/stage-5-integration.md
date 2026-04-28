# Stage 5 Integration

## Stage 5 Integration

During Stage 5 (Development), the PWA is built as part of the web frontend codebase. The web frontend lead owns the PWA implementation, while backend services must support offline data sync and push notification delivery.

```
┌──────────────────────────────────────────────────────────────────────┐
│ STAGE 5: PWA DEVELOPMENT TASKS                                        │
│                                                                       │
│  Web Frontend Team:                                                   │
│  ├── Set up web app manifest and serve at /manifest.json              │
│  ├── Implement service worker with caching strategies                 │
│  ├── Build offline fallback UI and IndexedDB store                    │
│  ├── Implement install prompt and iOS install guide                   │
│  ├── Set up push notification subscription flow                       │
│  ├── Optimize Core Web Vitals (LCP, INP, CLS)                        │
│  ├── Implement CSP headers and security headers                       │
│  └── Test PWA compliance via Lighthouse CI                            │
│                                                                       │
│  Backend Team:                                                        │
│  ├── Implement VAPID key management for push notifications            │
│  ├── Build push notification delivery service                         │
│  ├── Support offline data API (stale-while-revalidate headers)        │
│  └── Implement web push subscription management endpoints             │
│                                                                       │
│  CTO Internal Review (before Stage 6):                                │
│  ├── Lighthouse PWA audit: 100% score required                        │
│  ├── Service worker registration verified on all pages                │
│  ├── Offline page serves correctly with airplane mode test            │
│  ├── Install prompt fires on Chrome Android                           │
│  ├── All security headers present and correct                         │
│  └── Core Web Vitals pass on simulated 3G connection                  │
└──────────────────────────────────────────────────────────────────────┘
```

### Lighthouse CI Configuration

```json
// .lighthouserc.json
{
  "ci": {
    "collect": {
      "url": [
        "http://localhost:3000/",
        "http://localhost:3000/weather",
        "http://localhost:3000/settings"
      ],
      "numberOfRuns": 3,
      "settings": {
        "chromeFlags": "--no-sandbox"
      }
    },
    "assert": {
      "assertions": {
        "categories:pwa": ["error", { "minScore": 1 }],
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["error", { "minScore": 1 }],
        "categories:seo": ["warn", { "minScore": 0.9 }],
        "service-worker": "error",
        "installable-manifest": "error",
        "offline-start-url": "error",
        "works-offline": "error",
        "maskable-icon": "error"
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

---
