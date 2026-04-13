# Device Matrix

**Project:** [Project Name]
**Author:** [Platform Lead / Test Lead]
**Date:** YYYY-MM-DD
**Version:** v1
**Referenced Artifacts:** Implementation Plan v1, TEST-RESULTS-REPORT.md v1

---

## Purpose

Defines the minimum device and OS version matrix for testing. Ensures coverage across screen sizes, hardware capabilities, and OS versions that reflect the actual user base.

---

## 1. Android Device Matrix

### OS Version Support

| Android API Level | Android Version | Support Level                        | Minimum Target? |
| ----------------- | --------------- | ------------------------------------ | --------------- |
| [e.g., API 24]    | [Android 7.0]   | ☐ Full / ☐ Partial / ☐ Not Supported | ☐ Yes / ☐ No    |
| [e.g., API 28]    | [Android 9]     | ☐ Full / ☐ Partial / ☐ Not Supported | ☐ Yes / ☐ No    |
| [e.g., API 31]    | [Android 12]    | ☐ Full / ☐ Partial / ☐ Not Supported | ☐ Yes / ☐ No    |
| [e.g., API 34]    | [Android 14]    | ☐ Full / ☐ Partial / ☐ Not Supported | ☐ Yes / ☐ No    |

### Test Devices

| Device                  | Screen Size | Resolution  | RAM   | OS Version   | Test Type | Purpose                  |
| ----------------------- | ----------- | ----------- | ----- | ------------ | --------- | ------------------------ |
| [Pixel 7]               | [6.3"]      | [1080x2400] | [8GB] | [Android 14] | [Primary] | [Flagship baseline]      |
| [Samsung Galaxy A14]    | [6.6"]      | [1080x2408] | [4GB] | [Android 13] | [Low-end] | [Budget device coverage] |
| [Samsung Galaxy Tab A8] | [10.5"]     | [1920x1200] | [4GB] | [Android 12] | [Tablet]  | [Tablet layout testing]  |

### Firebase Test Lab Coverage

| Test Suite             | Device Count       | OS Versions Covered | Notes                 |
| ---------------------- | ------------------ | ------------------- | --------------------- |
| Espresso instrumented  | [N devices]        | [API 24-34]         | [Automated via CI/CD] |
| Play Pre-Launch Report | [All Play devices] | [All supported]     | [Automated on upload] |

---

## 2. iOS Device Matrix

### OS Version Support

| iOS Version | Support Level                        | Minimum Target? | Notes                       |
| ----------- | ------------------------------------ | --------------- | --------------------------- |
| [iOS 15]    | ☐ Full / ☐ Partial / ☐ Not Supported | ☐ Yes / ☐ No    | [Minimum supported version] |
| [iOS 16]    | ☐ Full / ☐ Partial / ☐ Not Supported | ☐ Yes / ☐ No    |                             |
| [iOS 17]    | ☐ Full / ☐ Partial / ☐ Not Supported | ☐ Yes / ☐ No    | [Current version]           |

### Test Devices

| Device            | Screen Size | Resolution  | Chip  | OS Version | Test Type | Purpose                 |
| ----------------- | ----------- | ----------- | ----- | ---------- | --------- | ----------------------- |
| [iPhone 15]       | [6.1"]      | [1179x2556] | [A16] | [iOS 17]   | [Primary] | [Flagship baseline]     |
| [iPhone SE (3rd)] | [4.7"]      | [750x1334]  | [A15] | [iOS 15]   | [Low-end] | [Small screen + old OS] |
| [iPad (10th gen)] | [10.9"]     | [1640x2360] | [A14] | [iOS 16]   | [Tablet]  | [Tablet layout testing] |

### Xcode UI Test Coverage

| Test Suite | Device Count | OS Versions Covered | Notes                     |
| ---------- | ------------ | ------------------- | ------------------------- |
| XCTest UI  | [N devices]  | [iOS 15-17]         | [Run on CI macOS runners] |

---

## 3. Screen Size Buckets

| Bucket                | Android dp Range | iOS pt Range | Devices      | Layout Variant |
| --------------------- | ---------------- | ------------ | ------------ | -------------- |
| Compact (phone)       | < 600dp          | < 667pt      | Phones       | [Layout A]     |
| Regular (large phone) | 600-840dp        | 667-844pt    | Large phones | [Layout B]     |
| Expanded (tablet)     | > 840dp          | > 844pt      | Tablets      | [Layout C]     |

---

## 4. Accessibility Test Devices

| Device       | Assistive Technology     | OS         | Verified?    |
| ------------ | ------------------------ | ---------- | ------------ |
| [iPhone 15]  | VoiceOver                | iOS 17     | ☐ Yes / ☐ No |
| [Pixel 7]    | TalkBack                 | Android 14 | ☐ Yes / ☐ No |
| [iPhone SE]  | VoiceOver + Dynamic Type | iOS 15     | ☐ Yes / ☐ No |
| [Galaxy A14] | TalkBack + Font Scaling  | Android 13 | ☐ Yes / ☐ No |

---

**Reviewed by [Platform Lead] on YYYY-MM-DD**
**Reviewed by Test Lead (Priscilla Oduya) on YYYY-MM-DD**
