# Cross-Platform Considerations

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
