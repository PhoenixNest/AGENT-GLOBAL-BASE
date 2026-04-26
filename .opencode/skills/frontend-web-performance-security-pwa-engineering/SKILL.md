---
name: frontend-web-performance-security-pwa-engineering
description: Progressive Web App engineering — web app manifest configuration, service worker architecture, offline strategies, push notifications, installability criteria, and cross-platform compatibility. Owned by Amira Voss (Frontend Chapter Lead). Use during Stage 3 (Architecture) for PWA strategy decisions and Stage 5 (Development) for PWA implementation. Trigger: pwa, progressive web app, service worker, offline support, push notifications, web app manifest, installable web.
prerequisites:
  - frontend-web-overview

version: "1.0.0"
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
    window.addEventListener("beforeinstallprompt", (event) => {
      // Prevent the default browser prompt
      event.preventDefault();
      // Store the event for later use
      this.deferredPrompt = event;
      this._notifyListeners("available");
    });

    // Detect when PWA is installed
    window.addEventListener("appinstalled", () => {
      this._isInstalled = true;
      this.deferredPrompt = null;
      this._notifyListeners("installed");
    });
  }

  _checkInstalled() {
    return (
      window.matchMedia("(display-mode: standalone)").matches ||
      window.navigator.standalone === true
    );
  }

  async promptInstall() {
    if (this._isInstalled) {
      console.log("App is already installed");
      return false;
    }

    if (!this.deferredPrompt) {
      console.log("Install prompt not available");
      return false;
    }

    // Show the prompt
    this.deferredPrompt.prompt();

    // Wait for user response
    const { outcome } = await this.deferredPrompt.userChoice;
    console.log(`Install prompt ${outcome}`);

    this.deferredPrompt = null;
    return outcome === "accepted";
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
  if (state === "available") {
    document.getElementById("install-banner").hidden = false;
  } else if (state === "installed") {
    document.getElementById("install-banner").hidden = true;
  }
});

document
  .getElementById("install-button")
  .addEventListener("click", async () => {
    const accepted = await installer.promptInstall();
    if (accepted) {
      document.getElementById("install-banner").hidden = true;
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
    <li>
      Tap the <strong>Share</strong> button <span class="share-icon">⎋</span>
    </li>
    <li>Scroll down and tap <strong>"Add to Home Screen"</strong></li>
    <li>Tap <strong>"Add"</strong> in the top-right corner</li>
  </ol>
  <p>WeatherPWA will appear on your home screen like a native app.</p>
</div>

<script>
  // Detect iOS Safari
  const isIOS =
    /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  const isStandalone = window.matchMedia("(display-mode: standalone)").matches;

  if (isIOS && !isStandalone) {
    document.getElementById("ios-install-guide").hidden = false;
  }
</script>
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

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`web-app-manifest.md`](references/web-app-manifest.md) — Web App Manifest
- [`service-workers.md`](references/service-workers.md) — Service Workers
- [`offline-support.md`](references/offline-support.md) — Offline Support
- [`push-notifications.md`](references/push-notifications.md) — Push Notifications
- [`performance-optimization.md`](references/performance-optimization.md) — Performance Optimization
- [`security.md`](references/security.md) — Security
- [`cross-platform-considerations.md`](references/cross-platform-considerations.md) — Cross-Platform Considerations
- [`stage-5-integration.md`](references/stage-5-integration.md) — Stage 5 Integration
