# Push Notifications

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
self.addEventListener("push", (event) => {
  const data = event.data?.json() ?? {};
  const { title, body, icon, badge, tag, actions, data: payload } = data;

  const options = {
    body: body || "You have a new notification",
    icon: icon || "/icons/icon-192x192.png",
    badge: badge || "/icons/badge-96x96.png",
    tag: tag || "default",
    renotify: !!tag,
    silent: false,
    data: payload,
    actions: actions || [
      { action: "view", title: "View", icon: "/icons/action-view.png" },
      {
        action: "dismiss",
        title: "Dismiss",
        icon: "/icons/action-dismiss.png",
      },
    ],
    vibrate: [200, 100, 200],
    timestamp: Date.now(),
  };

  event.waitUntil(
    self.registration.showNotification(title || "WeatherPWA", options),
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();

  if (event.action === "view") {
    event.waitUntil(
      clients
        .matchAll({ type: "window", includeUncontrolled: true })
        .then((windowClients) => {
          // Focus existing window if available
          for (const client of windowClients) {
            if (client.url.includes(event.notification.data?.url || "/")) {
              return client.focus();
            }
          }
          // Otherwise open new window
          return clients.openWindow(event.notification.data?.url || "/");
        }),
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
  await fetch("/api/push/subscribe", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(subscription),
  });
}

function urlBase64ToUint8Array(base64String) {
  const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, "+").replace(/_/g, "/");
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
