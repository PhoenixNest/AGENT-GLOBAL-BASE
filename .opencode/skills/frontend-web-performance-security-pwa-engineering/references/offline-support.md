# Offline Support

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

    window.addEventListener("online", () => this._setStatus(true));
    window.addEventListener("offline", () => this._setStatus(false));

    // Also check via service worker
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.addEventListener("message", (event) => {
        if (event.data?.type === "NETWORK_STATUS") {
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
  const banner = document.getElementById("network-banner");
  if (!online) {
    banner.textContent = "You are offline. Some features may be limited.";
    banner.className = "network-banner network-banner-offline";
    banner.hidden = false;
  } else {
    banner.textContent = "Back online!";
    banner.className = "network-banner network-banner-online";
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
    this.dbName = "weather-pwa-db";
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
        if (!db.objectStoreNames.contains("weather")) {
          const weatherStore = db.createObjectStore("weather", {
            keyPath: "cityId",
          });
          weatherStore.createIndex("timestamp", "timestamp", { unique: false });
          weatherStore.createIndex("city", "city", { unique: false });
        }

        // Outbox for queued writes
        if (!db.objectStoreNames.contains("outbox")) {
          const outboxStore = db.createObjectStore("outbox", {
            keyPath: "id",
            autoIncrement: true,
          });
          outboxStore.createIndex("timestamp", "timestamp", { unique: false });
          outboxStore.createIndex("status", "status", { unique: false });
        }
      };

      request.onsuccess = (event) => resolve(event.target.result);
      request.onerror = () => reject(request.error);
    });
  }

  async cacheWeather(cityId, data) {
    const tx = this.db.transaction("weather", "readwrite");
    const store = tx.objectStore("weather");
    await store.put({
      cityId,
      ...data,
      timestamp: Date.now(),
      cachedAt: new Date().toISOString(),
    });
  }

  async getCachedWeather(cityId) {
    const tx = this.db.transaction("weather", "readonly");
    const store = tx.objectStore("weather");
    return new Promise((resolve, reject) => {
      const request = store.get(cityId);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async addToOutbox(request) {
    const tx = this.db.transaction("outbox", "readwrite");
    const store = tx.objectStore("outbox");
    await store.add({
      ...request,
      timestamp: Date.now(),
      status: "pending",
    });
  }

  async getPendingOutbox() {
    const tx = this.db.transaction("outbox", "readonly");
    const store = tx.objectStore("outbox");
    const index = store.index("status");
    return new Promise((resolve, reject) => {
      const request = index.getAll("pending");
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  // Clean up stale cached data (older than 24 hours)
  async cleanStaleCache(maxAgeMs = 24 * 60 * 60 * 1000) {
    const tx = this.db.transaction("weather", "readwrite");
    const store = tx.objectStore("weather");
    const index = store.index("timestamp");
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
