# COPPA & Platform Compliance

**Last Updated:** April 9, 2026

---

## 1. COPPA (Children's Online Privacy Protection Act)

### 1.1 Overview

COPPA is a US federal regulation that applies to online services (including games) that collect personal information from children **under 13**. It is enforced by the FTC with penalties up to **$50,120 per violation**.

**Key principle:** If your game is "directed to children" OR you have actual knowledge that users include children under 13, COPPA applies.

### 1.2 Is Your Game "Directed to Children"?

The FTC uses a multi-factor test. Answer these questions:

| Factor                                                                                  | If YES → COPPA Likely Applies |
| --------------------------------------------------------------------------------------- | ----------------------------- |
| Subject matter is child-oriented (cartoons, toys, games for kids)                       | ✅                            |
| Visual content includes child-oriented activities or characters                         | ✅                            |
| Use of animated characters or child-oriented activities/incentives                      | ✅                            |
| Age of models (if any) are children                                                     | ✅                            |
| Presence of child-oriented celebrities or voices appealing to children                  | ✅                            |
| Language is child-directed                                                              | ✅                            |
| Advertising on the service is directed to children                                      | ✅                            |
| Competent and reliable empirical evidence shows audience is primarily children under 13 | ✅                            |

**For casual mini-games:** If your game uses cartoon art, simple mechanics, bright colors, or family-friendly themes, it is **likely** to be classified as child-directed by the FTC's test, even if your stated target audience is all ages.

### 1.3 COPPA Requirements (If Applicable)

| Requirement                      | What It Means                                                                                     | Implementation                                                                                  |
| -------------------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Verifiable parental consent**  | Must obtain consent from parent/guardian before collecting any personal information from children | Age gate + parental consent flow (credit card verification, signed consent form, or video call) |
| **Privacy policy**               | Must post a clear, comprehensive privacy policy describing data practices for children            | Privacy policy must specifically address children's data                                        |
| **Data minimization**            | Collect only information reasonably necessary for participation                                   | Do not collect device ID, location, behavioral data from children                               |
| **No conditional participation** | Cannot require children to provide more information than necessary                                | No "give us your email to play"                                                                 |
| **Parental rights**              | Parents can review, delete, and refuse further collection of their child's data                   | Parental dashboard or contact mechanism                                                         |
| **Data security**                | Must maintain reasonable procedures to protect children's data                                    | Encryption, access controls, retention limits                                                   |
| **Data retention limits**        | Retain children's data only as long as reasonably necessary                                       | Automatic deletion after inactivity period                                                      |

### 1.4 What Counts as "Personal Information" Under COPPA

| Data Type                                            | COPPA Classification                                      |
| ---------------------------------------------------- | --------------------------------------------------------- |
| Name, email, phone number                            | ✅ Personal information                                   |
| Device ID (IDFA, GAID, advertising identifier)       | ✅ Personal information                                   |
| IP address                                           | ✅ Personal information                                   |
| Geolocation (precise)                                | ✅ Personal information                                   |
| Photos, videos, audio containing child's image/voice | ✅ Personal information                                   |
| Persistent identifiers (cookies, session tokens)     | ✅ Personal information (even if no other data collected) |
| Behavioral data combined with persistent identifier  | ✅ Personal information                                   |
| **Aggregate/de-identified data**                     | ❌ Not personal information (if truly de-identified)      |

### 1.5 COPPA Compliance Strategy

**Option A: Don't Target Children (Recommended for Casual Mini-Games)**

| Action                       | Detail                                                           |
| ---------------------------- | ---------------------------------------------------------------- |
| Set age rating to 12+ / 9+   | On App Store and Google Play, set minimum age rating above 12    |
| Avoid child-oriented content | No cartoon characters, no toys, no child-oriented themes         |
| No behavioral advertising    | Disable personalized ads for all users (use contextual ads only) |
| Privacy policy states 13+    | Clearly state game is not directed to children under 13          |
| Age gate on first launch     | "Are you 13 or older?" — if no, restrict data collection         |

**Option B: Comply with COPPA (If Targeting All Ages)**

| Action                             | Detail                                            |
| ---------------------------------- | ------------------------------------------------- |
| Implement parental consent flow    | Before collecting any data from users under 13    |
| Disable all behavioral advertising | Use only contextual (non-targeted) ads            |
| Minimize data collection           | Only collect data strictly necessary for gameplay |
| Implement data deletion mechanism  | Allow parents to request deletion                 |
| Document compliance posture        | Maintain records of compliance decisions          |

---

## 2. GDPR-K (General Data Protection Regulation — Children)

### 2.1 Overview

GDPR Article 8 requires parental consent for processing personal data of children **under 16** (EU member states may lower to 13). This applies if your game is available in the EU.

### 2.2 GDPR-K Requirements

| Requirement          | Detail                                                       |
| -------------------- | ------------------------------------------------------------ |
| **Age of consent**   | 16 (or 13–15 depending on EU member state)                   |
| **Parental consent** | Required for children below applicable age threshold         |
| **Privacy notice**   | Must be in clear, plain language that a child can understand |
| **Data protection**  | Same standards as adults, with additional safeguards         |

### 2.3 COPPA vs. GDPR-K Comparison

| Aspect           | COPPA (US)                  | GDPR-K (EU)                         |
| ---------------- | --------------------------- | ----------------------------------- |
| Age threshold    | Under 13                    | Under 16 (or 13–15 by member state) |
| Consent required | Verifiable parental consent | Parental consent                    |
| Scope            | Personal information        | Personal data                       |
| Enforcement      | FTC                         | Data Protection Authorities (DPAs)  |
| Maximum fine     | $50,120 per violation       | €20M or 4% global revenue           |

---

## 3. Google Play Families Policy

### 3.1 Applicability

The Families Policy applies if your app:

- Targets children in its content (as determined by Google)
- Is included in the "Designed for Families" program
- Has a target audience age group that includes users under 13

### 3.2 Key Requirements

| Requirement                  | Detail                                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Privacy policy**           | Must be accessible from the app's store listing AND within the app                                     |
| **Family policy compliance** | Must comply with all Families Policy requirements                                                      |
| **Ads policy**               | If showing ads, must comply with Families Ads Program (no behavioral targeting, no cross-app tracking) |
| **Age rating**               | Must have accurate IARC (International Age Rating Coalition) rating                                    |
| **Data safety section**      | Must accurately disclose data collection and sharing practices                                         |

### 3.3 Families Ads Program

If your app is classified as child-directed, ads must comply:

| Rule                          | Detail                                                              |
| ----------------------------- | ------------------------------------------------------------------- |
| **No behavioral advertising** | Ads cannot be targeted based on user data                           |
| **No cross-app tracking**     | Ad SDKs cannot track users across apps                              |
| **Approved ad networks only** | Only ad networks that comply with Families Ads Program              |
| **No interest-based ads**     | All ads must be contextual (based on app content, not user profile) |

**Affected SDKs:** AdMob, Unity Ads, ironSource, and AppLovin all have COPPA/Families-compliant modes that must be enabled.

---

## 4. App Store Age Ratings

### 4.1 Age Rating Categories

| Rating  | Description                          | Content Restrictions                      |
| ------- | ------------------------------------ | ----------------------------------------- |
| **4+**  | No objectionable material            | Suitable for all ages                     |
| **9+**  | May contain infrequent mild content  | Mild cartoon violence, mild language      |
| **12+** | May contain moderate content         | Moderate violence, mature themes          |
| **17+** | May contain frequent intense content | Strong violence, mature/suggestive themes |

### 4.2 Rating Questionnaire

When submitting to App Store, you complete a questionnaire covering:

| Category                    | Questions                                         |
| --------------------------- | ------------------------------------------------- |
| Cartoon or fantasy violence | Is violence present? How frequent? How realistic? |
| Realistic violence          | Is violence realistic or graphic?                 |
| Mature/suggestive themes    | Are there romantic or suggestive themes?          |
| Nudity or sexual content    | Is nudity or sexual content present?              |
| Profanity or crude humor    | Is profanity used? How frequently?                |
| Simulated gambling          | Is gambling simulated or depicted?                |
| Alcohol, tobacco, drug use  | Are substances depicted or referenced?            |

**Recommendation:** For casual mini-games, target **4+ or 9+** ratings. Higher ratings significantly reduce discoverability in family categories.

---

## 5. Privacy Policy Requirements

### 5.1 Required Content

| Section                 | Required For               | Detail                                                      |
| ----------------------- | -------------------------- | ----------------------------------------------------------- |
| **Data collection**     | All apps                   | What data is collected, how it's used, who it's shared with |
| **Third-party SDKs**    | All apps                   | List all SDKs and what data they collect                    |
| **Children's privacy**  | If game may attract minors | COPPA/GDPR-K compliance statement                           |
| **Advertising**         | If game shows ads          | How ads are targeted, what data is shared with ad networks  |
| **User rights**         | GDPR compliance            | Right to access, delete, port data                          |
| **Contact information** | All apps                   | How users can contact you about privacy concerns            |

### 5.2 Placement Requirements

| Platform        | Requirement                                                               |
| --------------- | ------------------------------------------------------------------------- |
| **App Store**   | Privacy policy URL in App Store Connect; link in app (Settings → Privacy) |
| **Google Play** | Privacy policy URL in Play Console; link accessible from app              |
| **In-app**      | Accessible from Settings screen                                           |

---

## 6. Compliance Checklist per Release

### Pre-Submission Checklist

| Check                                      | Detail                                      | Owner       |
| ------------------------------------------ | ------------------------------------------- | ----------- |
| Age rating accurate                        | Reflects actual game content                | CPO + CSO   |
| Privacy policy current                     | Updated for any new data collection or SDKs | CSO + Legal |
| COPPA applicability assessed               | Is game directed to children?               | CSO + Legal |
| SDK data practices documented              | All SDKs listed in privacy policy           | CSO         |
| Families Ads Program compliance            | If applicable, ads are contextual only      | CSO         |
| Data safety section accurate (Google Play) | Reflects actual data practices              | CSO         |
| App privacy details accurate (App Store)   | Reflects actual data practices              | CSO         |
| In-game privacy policy accessible          | Link in Settings screen                     | CDO         |

### Ongoing Compliance

| Activity                       | Frequency                                | Owner       |
| ------------------------------ | ---------------------------------------- | ----------- |
| SDK audit                      | Every new SDK addition                   | CSO         |
| Privacy policy review          | Every 6 months or after material changes | CSO + Legal |
| Age rating review              | After any content change                 | CSO         |
| Data retention audit           | Annually                                 | CSO         |
| COPPA/GDPR-K compliance review | Annually or after game update            | CSO + Legal |

---

## 7. External Resources

| Resource                                        | Link                                                                     | Focus                                  |
| ----------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------- |
| FTC COPPA Guidance                              | https://www.ftc.gov/business-guidance/privacy-security/childrens-privacy | Official COPPA compliance guide        |
| "Legal Requirements for Children's Gaming Apps" | https://www.termsfeed.com/blog/childrens-gaming-apps-legal-requirements/ | Practical compliance guide             |
| Google Play Families Policy                     | https://support.google.com/googleplay/android-developer/answer/9892885   | Google's family policy requirements    |
| Apple Age Ratings                               | https://developer.apple.com/app-store/ratings-and-reviews/               | App Store age rating questionnaire     |
| GDPR Article 8                                  | https://gdpr.eu/article-8-conditions-for-child-consent/                  | EU children's data protection          |
| "A Guide to COPPA and Mobile Apps"              | https://www.iubenda.com/en/blog/guide-coppa-mobile-apps/                 | COPPA mobile app guide                 |
| IARC (Age Rating System)                        | https://www.globalratings.org/                                           | International age rating questionnaire |

---

_End of COPPA & Platform Compliance_
