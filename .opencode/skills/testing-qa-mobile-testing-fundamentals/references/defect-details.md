# Defect Details

## Defect Details

### D-001: App crashes on deep link navigation

**Severity:** P0
**Platform:** Android
**Reproduction Rate:** 100%
**Steps to Reproduce:**

1. Install app v2.1.0
2. Open link `myapp://product/123` from external app
3. App crashes immediately

**Expected:** App opens Product detail screen
**Actual:** App crashes with NullPointerException

**Stack Trace:**

```

java.lang.NullPointerException: Product ID is null
at com.company.app.ProductDetailActivity.onCreate(ProductDetailActivity.kt:45)

```

**Device:** Pixel 7, Android 14
**Priority:** Immediate fix required for release

```

---
```
