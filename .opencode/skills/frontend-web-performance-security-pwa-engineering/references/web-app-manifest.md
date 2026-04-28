# Web App Manifest

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
  "display_override": [
    "window-controls-overlay",
    "standalone",
    "minimal-ui",
    "browser"
  ],
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
    <meta
      name="apple-mobile-web-app-status-bar-style"
      content="black-translucent"
    />
    <meta name="apple-mobile-web-app-title" content="WeatherPWA" />
    <link rel="apple-touch-icon" href="/icons/icon-192x192.png" />
    <link
      rel="apple-touch-icon"
      sizes="180x180"
      href="/icons/icon-192x192.png"
    />

    <!-- Theme color for browser UI -->
    <meta name="theme-color" content="#16213e" />

    <!-- Favicon -->
    <link
      rel="icon"
      type="image/png"
      sizes="32x32"
      href="/icons/favicon-32x32.png"
    />
    <link
      rel="icon"
      type="image/png"
      sizes="16x16"
      href="/icons/favicon-16x16.png"
    />
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
