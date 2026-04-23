---
name: frontend-web-performance-security-pwa-engineering
description: 'Frontend Web skill: Pwa Engineering'
---

# Progressive Web App Engineering

## Overview

Progressive Web Apps (PWAs) combine the reach of the web with the capabilities of native applications. They are installable, work offline, support push notifications, and deliver app-like experiences through a browser. For a mobile-first company, PWAs serve as a strategic complement to native apps -- particularly for user acquisition, emerging markets, and platforms where native app store distribution is impractical.

This skill provides comprehensive engineering guidance for building production-grade PWAs, covering web app manifest configuration, service worker architecture, offline strategies, installability criteria, push notification implementation, performance optimization, security hardening, cross-platform compatibility, and Stage 5 integration patterns.

### PWA Capability Matrix

| Capability          | Native iOS     | Native Android   | PWA (Safari)                      | PWA (Chrome)            | PWA (Firefox)  |
| ------------------- | -------------- | ---------------- | --------------------------------- | ----------------------- | -------------- |
| Offline support     | Full           | Full             | Service Worker                    | Service Worker          | Service Worker |
| Push notifications  | APNs           | FCM              | Not supported (iOS 16.4+ limited) | FCM                     | Web Push       |
| Background sync     | Full           | Full             | Not supported                     | Background Sync         | Not supported  |
| File system access  | Full           | Full             | Limited (File System API)         | File System API         | Partial        |
| Biometric auth      | FaceID/TouchID | Fingerprint/Face | WebAuthn                          | WebAuthn                | WebAuthn       |
| Camera/Mic          | Full           | Full             | getUserMedia                      | getUserMedia            | getUserMedia   |
| Bluetooth           | Full           | Full             | Web Bluetooth                     | Web Bluetooth           | Web Bluetooth  |
| NFC                 | Full           | Full             | Not supported                     | Not supported           | Not supported  |
| Home screen install | N/A            | N/A              | Add to Home Screen                | Install Prompt          | Install Prompt |
| Splash screen       | Full           | Full             | Manifest splash                   | Manifest splash         | Limited        |
| Badging             | Full           | Full             | Not supported                     | Badging API             | Not supported  |
| Share target        | Full           | Full             | Not supported                     | Share Target API        | Not supported  |
| Geofencing          | Full           | Full             | Not supported                     | Geofencing (deprecated) | Not supported  |

### PWA Decision Framework

```
┌────────────────────────────────────────────────────────────────────┐
│ WHEN TO BUILD A PWA                                                 │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ BUILD PWA IF:                                               │   │
│  │  - User acquisition is priority (no app store friction)     │   │
│  │  - Emerging markets with limited storage/bandwidth          │   │
│  │  - Content-focused app (news, catalog, reading)             │   │
│  │  - Cross-platform reach with single codebase                │   │
│  │  - SEO/organic discovery is important                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ PREFER NATIVE IF:                                           │   │
│  │  - Heavy device hardware access (NFC, Bluetooth LE)         │   │
│  │  - Complex animations or GPU-intensive rendering            │   │
│  │  - Background processing requirements                       │   │
│  │  - Push notifications are core to product (iOS PWA limit)   │   │
│  │  - App store distribution and monetization strategy         │   │
│  └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────┘
```

### PWA Compliance Checklist

A valid PWA must satisfy all of the following criteria per Lighthouse auditing:

| Criterion                  | Requirement                                    | Verification                         |
| -------------------------- | ---------------------------------------------- | ------------------------------------ |
| **HTTPS**                  | All pages served over HTTPS (localhost exempt) | Lighthouse, manual check             |
| **Service Worker**         | Registered and controlling page                | `navigator.serviceWorker.controller` |
| **Web App Manifest**       | Valid manifest with required fields            | Lighthouse, `about://web-internals`  |
| **Installability**         | Meets browser installability criteria          | `beforeinstallprompt` event fires    |
| **Responsive**             | Works on all viewport sizes                    | Lighthouse, manual testing           |
| **Offline Fallback**       | Custom offline page when network unavailable   | Service worker serves fallback       |
| **Fast on 3G**             | First Contentful Paint < 2.5s on simulated 3G  | Lighthouse performance audit         |
| **No HTTPS Mixed Content** | No insecure resource loads                     | DevTools Security panel              |
| **Page Transitions**       | No perceived jank during navigation            | Performance panel, FPS meter         |
| **Each URL has a URL**     | Deep linking works for every page              | Manual testing, `window.location`    |

---

## Web App Manifest

The web app manifest is a JSON file that provides the browser with metadata about the web application, enabling installability and native-like presentation.

### Complete Manifest Configuration

```json
{
  "name": "WeatherPWA - Real-Time Weather Forecasts",
  "short_name": "WeatherPWA",
  "description": "Get real-time weather forecasts for any location with beautiful visualizations.",
  "start_url": "/?utm_source=pwa&utm_medium=pwa",
  "scope": "/",
  "display": "standalone",
  "display_override": ["window-controls-overlay", "standalone", "minimal-ui", "browser"],
  "orientation": "any",
  "background_color": "#1a1a2e",
  "theme_color": "#16213e",
  "categories": ["weather", "utilities"],
  "lang": "en",
  "dir": "ltr",
  "id": "/?source=pwa",
  "icons": [
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-192x192-maskable.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-512x512-maskable.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/icons/icon-any.svg",
      "sizes": "any",
      "type": "image/svg+xml",
      "purpose": "any monochrome"
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/home.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide",
      "label": "Weather home screen with 7-day forecast"
    },
    {
      "src": "/screenshots/detail-mobile.png",
      "sizes": "750x1334",
      "type": "image/png",
      "form_factor": "narrow",
      "label": "Detailed weather view for selected city"
    }
  ],
  "shortcuts": [
    {
      "name": "Current Location",
      "short_name": "Here",
      "description": "View weather for your current location",
      "url": "/current?source=pwa-shortcut",
      "icons": [
        {
          "src": "/icons/shortcut-location.png",
          "sizes": "96x96"
        }
      ]
    },
    {
      "name": "Saved Locations",
      "short_name": "Saved",
      "description": "View your saved favorite cities",
      "url": "/saved?source=pwa-shortcut",
      "icons": [
        {
          "src": "/icons/shortcut-star.png",
          "sizes": "96x96"
        }
      ]
    }
  ],
  "share_target": {
    "action": "/share",
    "method": "POST",
    "enctype": "multipart/form-data",
    "params": {
      "title": "title",
      "text": "text",
      "url": "url",
      "files": [
        {
          "name": "location",
          "accept": ["text/plain"]
        }
      ]
    }
  }
}
```

### Manifest Linking

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>WeatherPWA</title>

    <!-- Manifest reference -->
    <link rel="manifest" href="/manifest.json" />

    <!-- iOS meta tags (Apple doesn't use manifest for everything) -->
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <meta name="apple-mobile-web-app-title" content="WeatherPWA" />
    <link rel="apple-touch-icon" href="/icons/icon-192x192.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/icons/icon-192x192.png" />

    <!-- Theme color for browser UI -->
    <meta name="theme-color" content="#16213e" />

    <!-- Favicon -->
    <link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="/icons/favicon-16x16.png" />
    <link rel="shortcut icon" href="/icons/favicon.ico" />
  </head>
</html>
```

### Display Mode Behavior

| Display Mode              | Browser UI        | URL Bar                  | Status Bar               | Use Case                           |
| ------------------------- | ----------------- | ------------------------ | ------------------------ | ---------------------------------- |
| `browser`                 | Full chrome       | Visible                  | Visible                  | Regular web browsing               |
| `minimal-ui`              | Minimal chrome    | Hidden (gesture reveals) | Visible                  | Web apps needing URL access        |
| `standalone`              | No chrome         | Hidden                   | System only              | Native-like app experience         |
| `fullscreen`              | None              | Hidden                   | Hidden (gesture reveals) | Games, media, immersive apps       |
| `window-controls-overlay` | Title bar overlay | Hidden                   | System only              | Desktop PWAs with custom title bar |

### Maskable Icons

Maskable icons are critical for Android adaptive icon support. Without them, icons may appear distorted or improperly cropped on Android launchers.

```xml
<!-- SVG maskable icon template -->
<svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <clipPath id="safe-area">
            <!-- Safe area: 40% padding to avoid icon truncation -->
            <rect x="102" y="102" width="308" height="308" rx="77" />
        </clipPath>
    </defs>
    <!-- Background: full bleed to edge -->
    <rect width="512" height="512" fill="#16213e" />
    <!-- Icon content: clipped to safe area -->
    <g clip-path="url(#safe-area)">
        <text x="256" y="320" text-anchor="middle" font-size="200" fill="white">W</text>
    </g>
</svg>
```

---

## Service Workers

Service workers are the backbone of PWA offline capabilities. They act as a programmable network proxy, intercepting all network requests from the controlled scope and enabling caching, offline fallbacks, and background processing.

### Service Worker Lifecycle

```
┌──────────────────────────────────────────────────────────────────────┐
│ SERVICE WORKER LIFECYCLE                                              │
│                                                                       │
│  Register ──▶ Install ──▶ Installed ──▶ Activate ──▶ Activated       │
│      │          │                       │                  │          │
│      │     Precache assets        Claim clients       Ready to       │
│      │     (CACHE_NAME-v1)        (clients.claim())   fetch          │
│      │          │                       │                  │          │
│      │          ▼                       ▼                  ▼          │
│      │     install event          activate event     fetch event     │
│      │     cache.addAll()       cache.delete(old)    cache.match()   │
│      │                                                               │
│      │◀─────────────────────── Update Check ─────────────────────────▶│
│      │         (byte-diff detected on SW script or import)           │
│      ▼                                                               │
│  Waiting (if skipWaiting not called) ──▶ skipWaiting() ──▶ Activate  │
│  (user navigates away from all tabs                                  │
│   using old SW)                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Service Worker Strategy: Workbox

Workbox is the recommended service worker library, providing caching strategies, precaching, and routing abstractions.

```javascript
// sw.js - Service Worker with Workbox
import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate, NetworkOnly } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { BackgroundSyncPlugin } from 'workbox-background-sync';
import { cacheNames } from 'workbox-core';

// Self-managed precaching (generated by workbox-build or workbox-webpack-plugin)
precacheAndRoute(self.__WB_MANIFEST);

// Runtime caching strategies
registerRoute(
  // Cache API responses with network-first strategy
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-cache',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 5 * 60, // 5 minutes
        purgeOnQuotaError: true,
      }),
    ],
  })
);

registerRoute(
  // Cache weather images with cache-first strategy
  ({ url }) => url.pathname.match(/\.(png|jpg|jpeg|svg|gif|webp)$/),
  new CacheFirst({
    cacheName: 'image-cache',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
        purgeOnQuotaError: true,
      }),
    ],
  })
);

registerRoute(
  // Cache Google Fonts with stale-while-revalidate
  ({ url }) =>
    url.origin === 'https://fonts.googleapis.com' || url.origin === 'https://fonts.gstatic.com',
  new StaleWhileRevalidate({
    cacheName: 'google-fonts',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 10,
        maxAgeSeconds: 365 * 24 * 60 * 60, // 1 year
      }),
    ],
  })
);

// Offline fallback page
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({
    cacheName: 'pages-cache',
    fallbackToNetwork: false,
    plugins: [
      {
        handlerDidError: async () => {
          return caches.match('/offline.html');
        },
      },
    ],
  })
);

// Background sync for queued API requests
const bgSyncPlugin = new BackgroundSyncPlugin('weather-sync-queue', {
  maxRetentionTime: 24 * 60, // Retry for 24 hours (in minutes)
  onSync: async ({ queue }) => {
    let entry;
    while ((entry = await queue.shiftRequest())) {
      try {
        await fetch(entry.request);
        console.log('Background sync successful:', entry.request.url);
      } catch (error) {
        await queue.unshiftRequest(entry);
        throw error;
      }
    }
  },
});

registerRoute(
  ({ url }) => url.pathname.startsWith('/api/save'),
  new NetworkOnly({
    plugins: [bgSyncPlugin],
  }),
  'POST'
);

// Service worker activation
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.filter((name) => name !== cacheNames.runtime).map((name) => caches.delete(name))
      );
    })
  );
  return self.clients.claim();
});
```

### Custom Service Worker (No Workbox)

For lightweight PWAs where Workbox overhead is unacceptable:

```javascript
// sw-lightweight.js
const CACHE_NAME = 'weather-pwa-v1';
const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/offline.html',
  '/css/main.css',
  '/js/app.js',
  '/icons/icon-192x192.png',
  '/manifest.json',
];

// Install: precache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) =>
        Promise.all(
          cacheNames.filter((name) => name !== CACHE_NAME).map((name) => caches.delete(name))
        )
      )
      .then(() => self.clients.claim())
  );
});

// Fetch: network-first for API, cache-first for static
self.addEventListener('fetch', (event) => {
  const { request } = event;

  if (request.url.includes('/api/')) {
    // Network-first for API
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response.ok) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, responseClone);
            });
          }
          return response;
        })
        .catch(() => caches.match(request))
    );
  } else if (request.destination === 'document') {
    // Network-first for pages, fallback to offline page
    event.respondWith(fetch(request).catch(() => caches.match('/offline.html')));
  } else {
    // Cache-first for static assets
    event.respondWith(
      caches.match(request).then((cachedResponse) => cachedResponse || fetch(request))
    );
  }
});
```

### Caching Strategy Decision Matrix

| Content Type              | Strategy                      | Rationale                                     | Fallback             |
| ------------------------- | ----------------------------- | --------------------------------------------- | -------------------- |
| App shell (HTML, CSS, JS) | Cache First (precache)        | Deterministic, versioned builds               | N/A (always cached)  |
| API responses             | Network First, Cache Fallback | Fresh data preferred, offline support         | Stale cached data    |
| Images (static)           | Cache First                   | Never change, save bandwidth                  | Placeholder image    |
| Images (dynamic)          | Stale While Revalidate        | Show cached immediately, update in background | Cached image         |
| User-generated content    | Network Only                  | Must be fresh, no offline equivalent          | Offline notification |
| Fonts                     | Stale While Revalidate        | Load immediately, update if changed           | System font fallback |
| Offline page              | Cache Only                    | Always available                              | HTML inline fallback |

---

## Offline Support

### Offline Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│ OFFLINE ARCHITECTURE                                                  │
│                                                                       │
│  ┌─────────────────┐     ┌──────────────────┐     ┌────────────────┐ │
│  │   Online Mode   │     │  Degraded Mode   │     │  Offline Mode  │ │
│  │                 │     │                  │     │                │ │
│  │ - Live API data │     │ - Stale cache    │     │ - Cached data  │ │
│  │ - Real-time     │     │ - Queued writes  │     │ - Read only    │ │
│  │ - Sync active   │     │ - Partial sync   │     │ - UI banner    │ │
│  │ - Push active   │     │ - Retry pending  │     │ - Queue saves  │ │
│  └────────┬────────┘     └────────┬─────────┘     └───────┬────────┘ │
│           │                       │                        │          │
│           ▼                       ▼                        ▼          │
│  ┌──────────────────────────────────────────────────────────────────┐│
│  │                    IndexedDB / Cache Storage                      ││
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐  ││
│  │  │  API Cache   │ │  App Shell   │ │  Request Queue (outbox)  │  ││
│  │  │  (5 min TTL) │ │  (permanent) │ │  (retry on reconnect)    │  ││
│  │  └──────────────┘ └──────────────┘ └──────────────────────────┘  ││
│  └──────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────┘
```

### Offline Detection and UI

```javascript
// Network status monitor
class NetworkStatus {
  constructor() {
    this._online = navigator.onLine;
    this._listeners = [];

    window.addEventListener('online', () => this._setStatus(true));
    window.addEventListener('offline', () => this._setStatus(false));

    // Also check via service worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data?.type === 'NETWORK_STATUS') {
          this._setStatus(event.data.online);
        }
      });
    }
  }

  _setStatus(online) {
    if (this._online !== online) {
      this._online = online;
      this._listeners.forEach((fn) => fn(online));
    }
  }

  onChange(fn) {
    this._listeners.push(fn);
    fn(this._online);
    return () => {
      this._listeners = this._listeners.filter((l) => l !== fn);
    };
  }

  get isOnline() {
    return this._online;
  }
}

// Usage in app
const networkStatus = new NetworkStatus();

networkStatus.onChange((online) => {
  const banner = document.getElementById('network-banner');
  if (!online) {
    banner.textContent = 'You are offline. Some features may be limited.';
    banner.className = 'network-banner network-banner-offline';
    banner.hidden = false;
  } else {
    banner.textContent = 'Back online!';
    banner.className = 'network-banner network-banner-online';
    banner.hidden = false;
    setTimeout(() => {
      banner.hidden = true;
    }, 3000);
  }
});
```

### Offline Data Strategy

```javascript
// IndexedDB wrapper for offline data
class OfflineStore {
  constructor() {
    this.dbName = 'weather-pwa-db';
    this.version = 1;
    this.db = null;
  }

  async init() {
    this.db = await this._openDB();
  }

  _openDB() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        // Weather data store
        if (!db.objectStoreNames.contains('weather')) {
          const weatherStore = db.createObjectStore('weather', {
            keyPath: 'cityId',
          });
          weatherStore.createIndex('timestamp', 'timestamp', { unique: false });
          weatherStore.createIndex('city', 'city', { unique: false });
        }

        // Outbox for queued writes
        if (!db.objectStoreNames.contains('outbox')) {
          const outboxStore = db.createObjectStore('outbox', {
            keyPath: 'id',
            autoIncrement: true,
          });
          outboxStore.createIndex('timestamp', 'timestamp', { unique: false });
          outboxStore.createIndex('status', 'status', { unique: false });
        }
      };

      request.onsuccess = (event) => resolve(event.target.result);
      request.onerror = () => reject(request.error);
    });
  }

  async cacheWeather(cityId, data) {
    const tx = this.db.transaction('weather', 'readwrite');
    const store = tx.objectStore('weather');
    await store.put({
      cityId,
      ...data,
      timestamp: Date.now(),
      cachedAt: new Date().toISOString(),
    });
  }

  async getCachedWeather(cityId) {
    const tx = this.db.transaction('weather', 'readonly');
    const store = tx.objectStore('weather');
    return new Promise((resolve, reject) => {
      const request = store.get(cityId);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async addToOutbox(request) {
    const tx = this.db.transaction('outbox', 'readwrite');
    const store = tx.objectStore('outbox');
    await store.add({
      ...request,
      timestamp: Date.now(),
      status: 'pending',
    });
  }

  async getPendingOutbox() {
    const tx = this.db.transaction('outbox', 'readonly');
    const store = tx.objectStore('outbox');
    const index = store.index('status');
    return new Promise((resolve, reject) => {
      const request = index.getAll('pending');
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  // Clean up stale cached data (older than 24 hours)
  async cleanStaleCache(maxAgeMs = 24 * 60 * 60 * 1000) {
    const tx = this.db.transaction('weather', 'readwrite');
    const store = tx.objectStore('weather');
    const index = store.index('timestamp');
    const cutoff = Date.now() - maxAgeMs;

    return new Promise((resolve, reject) => {
      const request = index.openCursor(IDBKeyRange.upperBound(cutoff));
      request.onsuccess = (event) => {
        const cursor = event.target.result;
        if (cursor) {
          cursor.delete();
          cursor.continue();
        } else {
          resolve();
        }
      };
      request.onerror = () => reject(request.error);
    });
  }
}
```

---

## Installability

### Installability Criteria (Chrome/Edge)

| Criterion                 | Requirement                                                | How to Verify                    |
| ------------------------- | ---------------------------------------------------------- | -------------------------------- |
| **Not already installed** | User hasn't installed the PWA                              | Browser handles this             |
| **HTTPS**                 | Served over HTTPS                                          | `location.protocol === 'https:'` |
| **Service Worker**        | Has registered SW with fetch handler                       | `navigator.serviceWorker.ready`  |
| **Valid Manifest**        | With `short_name` or `name`, `icons` (192px+), `start_url` | Lighthouse audit                 |
| **Engagement**            | User has interacted with site (varies by browser)          | Browser heuristic                |
| **No install dismissed**  | User hasn't previously dismissed install prompt            | Browser state                    |

### Custom Install Prompt

```javascript
class PWAInstaller {
  constructor() {
    this.deferredPrompt = null;
    this._listeners = [];
    this._isInstalled = this._checkInstalled();

    this._bindEvents();
  }

  _bindEvents() {
    // Capture the beforeinstallprompt event
    window.addEventListener('beforeinstallprompt', (event) => {
      // Prevent the default browser prompt
      event.preventDefault();
      // Store the event for later use
      this.deferredPrompt = event;
      this._notifyListeners('available');
    });

    // Detect when PWA is installed
    window.addEventListener('appinstalled', () => {
      this._isInstalled = true;
      this.deferredPrompt = null;
      this._notifyListeners('installed');
    });
  }

  _checkInstalled() {
    return (
      window.matchMedia('(display-mode: standalone)').matches ||
      window.navigator.standalone === true
    );
  }

  async promptInstall() {
    if (this._isInstalled) {
      console.log('App is already installed');
      return false;
    }

    if (!this.deferredPrompt) {
      console.log('Install prompt not available');
      return false;
    }

    // Show the prompt
    this.deferredPrompt.prompt();

    // Wait for user response
    const { outcome } = await this.deferredPrompt.userChoice;
    console.log(`Install prompt ${outcome}`);

    this.deferredPrompt = null;
    return outcome === 'accepted';
  }

  onChange(callback) {
    this._listeners.push(callback);
  }

  _notifyListeners(state) {
    this._listeners.forEach((cb) => cb(state));
  }

  get isInstalled() {
    return this._isInstalled;
  }

  get isAvailable() {
    return !!this.deferredPrompt && !this._isInstalled;
  }
}

// Usage
const installer = new PWAInstaller();

installer.onChange((state) => {
  if (state === 'available') {
    document.getElementById('install-banner').hidden = false;
  } else if (state === 'installed') {
    document.getElementById('install-banner').hidden = true;
  }
});

document.getElementById('install-button').addEventListener('click', async () => {
  const accepted = await installer.promptInstall();
  if (accepted) {
    document.getElementById('install-banner').hidden = true;
  }
});
```

### iOS Install Prompt

iOS does not fire `beforeinstallprompt`. Instead, guide users manually:

```html
<!-- iOS install instructions -->
<div id="ios-install-guide" class="ios-guide" hidden>
  <h3>Install WeatherPWA on your iPhone</h3>
  <ol>
    <li>Tap the <strong>Share</strong> button <span class="share-icon">⎋</span></li>
    <li>Scroll down and tap <strong>"Add to Home Screen"</strong></li>
    <li>Tap <strong>"Add"</strong> in the top-right corner</li>
  </ol>
  <p>WeatherPWA will appear on your home screen like a native app.</p>
</div>

<script>
  // Detect iOS Safari
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  const isStandalone = window.matchMedia('(display-mode: standalone)').matches;

  if (isIOS && !isStandalone) {
    document.getElementById('ios-install-guide').hidden = false;
  }
</script>
```

---

## Push Notifications

### Push Notification Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│ PUSH NOTIFICATION FLOW                                                │
│                                                                       │
│  ┌──────────┐     ┌──────────────┐     ┌──────────────┐              │
│  │  Client   │────▶│  Push Svc    │────▶│  App Server  │              │
│  │ (Browser) │     │  (FCM/APNs)  │     │  (Backend)   │              │
│  │          │◀────│              │◀────│              │              │
│  │  - SW    │     │  - Routes    │     │  - Triggers  │              │
│  │  - Push  │     │  - Delivers  │     │  - Payloads  │              │
│  │  - Ntfy  │     │  - Queues    │     │  - Schedules │              │
│  └──────────┘     └──────────────┘     └──────────────┘              │
│       │                                                             │
│       ▼                                                             │
│  ┌──────────────────────────────────────────────┐                   │
│  │  User receives notification:                 │                   │
│  │  - Shown by service worker push handler      │                   │
│  │  - Click handler navigates to relevant page  │                   │
│  │  - Actions (reply, dismiss) handled by SW    │                   │
│  └──────────────────────────────────────────────┘                   │
└──────────────────────────────────────────────────────────────────────┘
```

### Push Notification Implementation

```javascript
// In service worker
self.addEventListener('push', (event) => {
  const data = event.data?.json() ?? {};
  const { title, body, icon, badge, tag, actions, data: payload } = data;

  const options = {
    body: body || 'You have a new notification',
    icon: icon || '/icons/icon-192x192.png',
    badge: badge || '/icons/badge-96x96.png',
    tag: tag || 'default',
    renotify: !!tag,
    silent: false,
    data: payload,
    actions: actions || [
      { action: 'view', title: 'View', icon: '/icons/action-view.png' },
      {
        action: 'dismiss',
        title: 'Dismiss',
        icon: '/icons/action-dismiss.png',
      },
    ],
    vibrate: [200, 100, 200],
    timestamp: Date.now(),
  };

  event.waitUntil(self.registration.showNotification(title || 'WeatherPWA', options));
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'view') {
    event.waitUntil(
      clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
        // Focus existing window if available
        for (const client of windowClients) {
          if (client.url.includes(event.notification.data?.url || '/')) {
            return client.focus();
          }
        }
        // Otherwise open new window
        return clients.openWindow(event.notification.data?.url || '/');
      })
    );
  }
});

// In application code
async function subscribeToPushNotifications() {
  const registration = await navigator.serviceWorker.ready;

  // Get push subscription
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(process.env.VAPID_PUBLIC_KEY),
  });

  // Send subscription to server
  await fetch('/api/push/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(subscription),
  });
}

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = atob(base64);
  return Uint8Array.from([...rawData].map((char) => char.charCodeAt(0)));
}
```

### Push Notification Platform Limitations

| Platform              | Push Support  | Notes                                             |
| --------------------- | ------------- | ------------------------------------------------- |
| Chrome/Edge (Android) | Full          | FCM Web Push, VAPID keys                          |
| Chrome/Edge (Desktop) | Full          | FCM Web Push, VAPID keys                          |
| Firefox (Desktop)     | Full          | Mozilla Push Service                              |
| Safari (macOS)        | Partial       | Requires Apple Push Notifications via certificate |
| Safari (iOS)          | Not supported | No push for PWAs on iOS                           |
| Samsung Internet      | Full          | Uses FCM                                          |

---

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
<link rel="stylesheet" href="/css/main.css" media="print" onload="this.media='all'" />
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
self.addEventListener('fetch', (event) => {
  // Keep fetch handler minimal
  if (event.request.url.includes('/api/weather')) {
    event.respondWith(networkFirst(event.request));
  } else {
    event.respondWith(cacheFirst(event.request));
  }
});

// Use cache.addAll in install (parallel by default)
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      cache.addAll([
        // These load in parallel
        '/',
        '/index.html',
        '/css/main.css',
        '/js/app.js',
      ])
    )
  );
});
```

---

## Security

### PWA Security Checklist

| Security Control               | Implementation                                           | Priority |
| ------------------------------ | -------------------------------------------------------- | -------- |
| **HTTPS Only**                 | HSTS header, redirect HTTP to HTTPS                      | P0       |
| **Content Security Policy**    | CSP header restricting resource sources                  | P0       |
| **Subresource Integrity**      | SRI hashes for external scripts                          | P1       |
| **X-Frame-Options**            | Prevent clickjacking via SAMEORIGIN                      | P1       |
| **X-Content-Type-Options**     | Prevent MIME sniffing with nosniff                       | P1       |
| **Referrer-Policy**            | Limit referrer info with strict-origin-when-cross-origin | P2       |
| **Permissions-Policy**         | Restrict browser features                                | P2       |
| **Service Worker Scope**       | Limit SW scope to minimum required                       | P1       |
| **No Sensitive Data in Cache** | Never cache authentication tokens, PII                   | P0       |

### Content Security Policy for PWA

```html
<meta
  http-equiv="Content-Security-Policy"
  content="
    default-src 'self';
    script-src 'self' 'wasm-unsafe-eval';
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    img-src 'self' data: blob: https:;
    font-src 'self' https://fonts.gstatic.com;
    connect-src 'self' https://api.weather.example.com;
    media-src 'self';
    object-src 'none';
    frame-src 'none';
    worker-src 'self';
    manifest-src 'self';
    base-uri 'self';
    form-action 'self';
    upgrade-insecure-requests;
"
/>
```

---

## Cross-Platform Considerations

### iOS PWA Limitations

| Feature                  | Status on iOS Safari               | Workaround                              |
| ------------------------ | ---------------------------------- | --------------------------------------- |
| Service Worker           | Supported (iOS 11.3+)              | Works, but limited background execution |
| Push Notifications       | Not supported (iOS 17 and earlier) | Use in-app notifications, email         |
| Background Sync          | Not supported                      | Queue in IndexedDB, sync on next open   |
| File System Access       | Not supported                      | Use `<input type="file">` fallback      |
| Web Bluetooth            | Supported (iOS 16.4+)              | Works with user gesture                 |
| Web NFC                  | Not supported                      | No workaround                           |
| Web Share Target         | Not supported                      | Use standard Web Share API              |
| Periodic Background Sync | Not supported                      | No workaround                           |
| Badging API              | Not supported                      | No workaround                           |
| Geofencing               | Not supported                      | No workaround                           |

### Android PWA Advantages

| Feature                  | Status on Chrome Android      |
| ------------------------ | ----------------------------- |
| Service Worker           | Full support                  |
| Push Notifications       | Full (FCM Web Push)           |
| Background Sync          | Full support                  |
| File System Access       | Full (File System Access API) |
| Web Bluetooth            | Full support                  |
| Web NFC                  | Not supported                 |
| Web Share Target         | Full support                  |
| Periodic Background Sync | Supported (with permission)   |
| Badging API              | Full support                  |
| Geofencing               | Deprecated (was supported)    |

---

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

## References

| Resource                    | Description                        | URL                                                                                            |
| --------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------- |
| MDN PWA Guide               | Comprehensive PWA documentation    | https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps                              |
| Google PWA Checklist        | Official PWA development checklist | https://web.dev/pwa-checklist/                                                                 |
| Workbox Documentation       | Service worker library docs        | https://developer.chrome.com/docs/workbox/                                                     |
| web.dev PWA                 | PWA articles and codelabs          | https://web.dev/progressive-web-apps/                                                          |
| Lighthouse Docs             | PWA auditing documentation         | https://developer.chrome.com/docs/lighthouse/                                                  |
| Web App Manifest Spec       | W3C specification                  | https://w3c.github.io/manifest/                                                                |
| Service Worker Spec         | W3C specification                  | https://w3c.github.io/ServiceWorker/                                                           |
| iOS PWA Limitations         | Apple's PWA capabilities           | https://developer.apple.com/documentation/xcode/making-a-web-clip-installable-on-a-home-screen |
| Can I Use - Service Workers | Browser support matrix             | https://caniuse.com/serviceworkers                                                             |
| PWA Builder                 | Microsoft PWA tooling              | https://www.pwabuilder.com/                                                                    |
| Core Web Vitals             | Performance metrics                | https://web.dev/vitals/                                                                        |
| Web Push Protocol           | IETF RFC 8030                      | https://www.rfc-editor.org/rfc/rfc8030                                                         |
