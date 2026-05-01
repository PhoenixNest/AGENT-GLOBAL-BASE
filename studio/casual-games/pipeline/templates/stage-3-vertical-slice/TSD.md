# Technology Selection Document (TSD) — Template

> **Stage:** 3 — Vertical Slice
> **Producer:** Lead Engineer + Studio Director (Dr. Marcus Vogel)
> **Kill Gate:** KG-3 — Vertical Slice
> **User Approval:** ✅ Required — technology selections lock on approval
> **Warning:** Technology selections made here are **immutable** after User approval.

---

## Document Control

| Field          | Value           |
| :------------- | :-------------- |
| **Game Title** | [Working title] |
| **Version**    | v1.0            |
| **Date**       | YYYY-MM-DD      |
| **Author**     | [Lead Engineer] |

---

## 1. Engine and Platform

| Technology             | Selection                    | Version   | Rationale                                        |
| :--------------------- | :--------------------------- | :-------- | :----------------------------------------------- |
| Game engine            | Unity                        | 6.3 LTS   | Studio standard; LTS support through [year]      |
| Scripting backend      | IL2CPP                       | —         | Required for iOS; performance benefit on Android |
| Rendering pipeline     | [URP / HDRP / Built-in]      | [Version] | [Rationale]                                      |
| Graphics API (iOS)     | Metal                        | —         | [Rationale]                                      |
| Graphics API (Android) | Vulkan + OpenGL ES3 fallback | —         | [Rationale]                                      |

---

## 2. Backend Services

| Category             | Technology                | Provider             | Rationale         |
| :------------------- | :------------------------ | :------------------- | :---------------- |
| Backend-as-a-Service | [e.g. PlayFab / Firebase] | [Microsoft / Google] | [Rationale]       |
| Authentication       | [Selection]               | [Provider]           | [Rationale]       |
| Cloud save           | [Selection]               | [Provider]           | [Rationale]       |
| Leaderboards         | [Selection]               | [Provider]           | [Rationale]       |
| Push notifications   | [FCM / APNs]              | [Google / Apple]     | Platform standard |

---

## 3. Analytics and Monetisation

| Category              | Technology                       | Provider   | Rationale                         |
| :-------------------- | :------------------------------- | :--------- | :-------------------------------- |
| Analytics SDK         | [e.g. GameAnalytics / Amplitude] | [Provider] | [Rationale]                       |
| Ad network (rewarded) | [e.g. IronSource / AppLovin]     | [Provider] | [Rationale]                       |
| Ad mediation          | [e.g. MAX / LevelPlay]           | [Provider] | [Rationale]                       |
| IAP                   | Unity IAP                        | Unity      | Cross-platform receipt validation |

---

## 4. CI/CD and Development Tools

| Category        | Technology                                | Rationale       |
| :-------------- | :---------------------------------------- | :-------------- |
| Source control  | Git (this repository)                     | Studio standard |
| CI/CD           | [e.g. Unity Cloud Build / GitHub Actions] | [Rationale]     |
| Code review     | [e.g. GitHub PR]                          | [Rationale]     |
| Issue tracking  | [e.g. Jira / GitHub Issues]               | [Rationale]     |
| Crash reporting | [e.g. Firebase Crashlytics]               | [Rationale]     |

---

## 5. Third-Party SDKs and Licences

| SDK     | Version | Licence   | Risk    | Approved? |
| :------ | :------ | :-------- | :------ | :-------: |
| [SDK 1] | [X.X]   | [Licence] | [H/M/L] |     ☐     |
| [SDK 2] | [X.X]   | [Licence] | [H/M/L] |     ☐     |

> CSO asset screening required for all third-party SDKs before Stage 3 close.

---

## 6. Security Technology

| Requirement                | Technology                       | Notes                          |
| :------------------------- | :------------------------------- | :----------------------------- |
| API security               | HTTPS + JWT                      | TLS 1.2+ minimum               |
| Certificate pinning        | [Library]                        | Payment endpoints only         |
| Server-side IAP validation | Platform receipt validation APIs | [Notes]                        |
| Anti-cheat                 | Server-authoritative economy     | No client-side currency grants |

---

## 7. Technology Freeze Acknowledgement

By signing below, all parties acknowledge that the technology selections in this document are **locked** upon User approval. Any subsequent change requires:

1. A new ADR documenting the change, rationale, and impact
2. Studio Director + User approval of the new ADR
3. Full Stage 3 re-evaluation of affected systems

| Role            | Agent            | Signature           | Date       |
| :-------------- | :--------------- | :------------------ | :--------- |
| Lead Engineer   | [Name]           | ☐ Signed            | YYYY-MM-DD |
| Studio Director | Dr. Marcus Vogel | ☐ Signed            | YYYY-MM-DD |
| CEO             | User             | ☐ Approved (frozen) | YYYY-MM-DD |
