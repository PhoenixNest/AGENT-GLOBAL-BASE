# Cross-Device Testing

## Cross-Device Testing

### Device Farm Integration

| Service           | Device Coverage               | Integration Method        | Cost Model              | Best For                      |
| ----------------- | ----------------------------- | ------------------------- | ----------------------- | ----------------------------- |
| AWS Device Farm   | 200+ real Android/iOS devices | AWS CLI, API              | Pay per device-minute   | Comprehensive device coverage |
| Firebase Test Lab | 50+ real + virtual devices    | gcloud CLI, Gradle plugin | Free tier + pay per use | Android-first teams           |
| BrowserStack      | 3000+ devices/browsers        | REST API, SDKs            | Subscription            | Cross-browser + mobile        |
| Sauce Labs        | 1000+ real + emulated devices | REST API, W3C WebDriver   | Subscription            | Enterprise teams              |
| LambdaTest        | 3000+ browsers/devices        | REST API, Selenium        | Subscription            | Budget-conscious teams        |

### OS Matrix Coverage

| Platform | OS Versions to Test                   | Rationale                         |
| -------- | ------------------------------------- | --------------------------------- |
| Android  | API 33 (13), API 31 (12), API 30 (11) | Current + 2 previous major        |
| Android  | API 28 (9)                            | Minimum supported (if applicable) |
| iOS      | iOS 17, iOS 16                        | Current + 1 previous major        |
| iOS      | iOS 15                                | Minimum supported (if applicable) |

**Browser/Device Coverage Matrix:**

| Browser          | Mobile                 | Tablet             | Desktop      |
| ---------------- | ---------------------- | ------------------ | ------------ |
| Chrome           | Pixel 7, Galaxy S23    | iPad, Galaxy Tab   | Chrome 120+  |
| Safari           | iPhone 15, iPhone SE   | iPad Air, iPad Pro | Safari 17+   |
| Firefox          | —                      | —                  | Firefox 120+ |
| Edge             | —                      | —                  | Edge 120+    |
| Samsung Internet | Galaxy S23, Galaxy A54 | Galaxy Tab S9      | —            |

### Coverage Prioritization

| Priority       | Devices/Browsers                                 | Coverage Goal   | Execution Frequency |
| -------------- | ------------------------------------------------ | --------------- | ------------------- |
| P0 — Critical  | Primary device per platform (Pixel 7, iPhone 15) | 100% of screens | Every PR            |
| P1 — Important | Secondary devices (tablet, small phone, old OS)  | 90% of screens  | Nightly             |
| P2 — Extended  | Edge cases (old browser, foldable, fold/unfold)  | 75% of screens  | Weekly              |
| P3 — Complete  | Full device farm matrix                          | 100% of matrix  | Pre-release only    |

---
