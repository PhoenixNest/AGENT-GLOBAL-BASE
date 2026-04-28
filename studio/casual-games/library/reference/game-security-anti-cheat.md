# Game Security & Anti-Cheat

**Last Updated:** April 9, 2026

---

## 1. Threat Model for Casual Mobile Games

Casual mini-games face different security threats than enterprise applications. The primary attack vectors target the **game economy** and **player experience**.

| Threat                                            | Impact                                                         | Likelihood                                |
| ------------------------------------------------- | -------------------------------------------------------------- | ----------------------------------------- |
| **Memory tampering** (GameGuardian, Cheat Engine) | Currency duplication, score manipulation, unlock all content   | **High**                                  |
| **Save file manipulation**                        | Edit local save files to inflate currency, unlock content      | **High**                                  |
| **Speed hacking**                                 | Accelerate game clock to bypass timers, speed up progression   | **Medium**                                |
| **Ad fraud**                                      | Fake ad impressions to generate illegitimate ad revenue        | **Medium**                                |
| **API abuse**                                     | Direct API calls to backend services bypassing the game client | **Medium**                                |
| **Asset extraction**                              | Rip art/audio assets for use in competing games                | **Low** (acceptable for free-asset games) |
| **Multiplayer cheating** (if applicable)          | Aimbots, wallhacks, matchmaking manipulation                   | **Low** (for single-player casual games)  |

---

## 2. Client-Side Security

### 2.1 IL2CPP (Code Hardening)

**Always use IL2CPP for production builds.** IL2CPP compiles C# to native C++ code, making reverse engineering significantly harder than Mono (which ships readable DLLs).

| Setting                     | Value   | Rationale                                         |
| --------------------------- | ------- | ------------------------------------------------- |
| **Scripting Backend**       | IL2CPP  | Native code is harder to decompile than .NET DLLs |
| **Managed Stripping Level** | High    | Removes unused code, reducing attack surface      |
| **Engine Code Stripping**   | Enabled | Same principle — remove unused engine code        |

### 2.2 Code Obfuscation

IL2CPP obfuscates method names but not string literals or logic flow. For additional protection:

| Tool                        | Type              | Purpose                                                |
| --------------------------- | ----------------- | ------------------------------------------------------ |
| **ByteHide Shield**         | Commercial        | .NET obfuscation + anti-tampering + anti-debug         |
| **Obfuscar**                | Free, open-source | .NET assembly obfuscation (pre-IL2CPP)                 |
| **ProGuard-like for Unity** | N/A               | Not directly available — IL2CPP serves similar purpose |

**Recommendation:** IL2CPP + High stripping level is sufficient for casual games. Commercial obfuscation is only needed for games with valuable in-game economies.

### 2.3 Anti-Tampering Checks

```csharp
// Runtime integrity check — verify the app hasn't been modified
public class IntegrityCheck
{
    public static bool Verify()
    {
        // Check 1: Verify assembly hash
        var assemblyHash = ComputeHash(Assembly.GetExecutingAssembly());
        if (assemblyHash != ExpectedHash) return false;

        // Check 2: Detect debugger attachment
        if (System.Diagnostics.Debugger.IsAttached) return false;

        // Check 3: Detect speed hack (check Time.timeScale)
        if (Mathf.Abs(Time.timeScale - 1.0f) > 0.01f) return false;

        // Check 4: Detect root/jailbreak (platform-specific)
        if (IsDeviceRooted()) return false;

        return true;
    }
}
```

### 2.4 Time Manipulation Prevention

Players can change device clock to bypass timers (daily rewards, cooldown timers).

```csharp
// Server-authoritative time (preferred)
// Fetch current time from backend on game start
private DateTime _serverTime;
private float _elapsedSinceSync;

void Update()
{
    _elapsedSinceSync += Time.deltaTime;
    DateTime currentTime = _serverTime.AddSeconds(_elapsedSinceSync);
    // Use currentTime for all time-based calculations
}

// Local fallback (less secure, but better than nothing)
private DateTime _lastSaveTime;

public TimeSpan GetElapsedTime()
{
    DateTime now = DateTime.UtcNow;
    if (now < _lastSaveTime)
    {
        // Clock was set backwards — use last save time as floor
        return TimeSpan.Zero;
    }
    return now - _lastSaveTime;
}
```

---

## 3. Data Protection

### 3.1 Save Data Security

**Never trust client-side save data for economy-critical values** (currency, purchases, unlocks).

| Data Type                                    | Storage Method                        | Security Level                               |
| -------------------------------------------- | ------------------------------------- | -------------------------------------------- |
| **Settings** (volume, language)              | `PlayerPrefs`                         | Low — acceptable (no economic impact)        |
| **Progression** (level reached, high score)  | `PlayerPrefs` or encrypted file       | Medium — validate server-side on submission  |
| **Currency** (coins, gems, premium currency) | **Server-side only**                  | High — never store locally                   |
| **Purchase receipts**                        | Server-side + local cache             | High — validate with platform (Apple/Google) |
| **Session tokens**                           | Encrypted storage (Keychain/Keystore) | High — use platform secure storage           |

### 3.2 Encryption for Local Data

If local storage is necessary (offline mode), encrypt sensitive data:

```csharp
// Simple encryption for save files (not military-grade, but deters casual tampering)
using System.Security.Cryptography;
using System.Text;

public class SaveEncryption
{
    private static readonly byte[] Key = Encoding.UTF8.GetBytes("your-32-char-key-here!!"); // 32 bytes for AES-256
    private static readonly byte[] IV = Encoding.UTF8.GetBytes("16-char-iv-here!"); // 16 bytes for AES

    public static string Encrypt(string plainText)
    {
        using var aes = Aes.Create();
        aes.Key = Key;
        aes.IV = IV;
        var encryptor = aes.CreateEncryptor();
        var bytes = Encoding.UTF8.GetBytes(plainText);
        var encrypted = encryptor.TransformFinalBlock(bytes, 0, bytes.Length);
        return Convert.ToBase64String(encrypted);
    }

    public static string Decrypt(string cipherText)
    {
        using var aes = Aes.Create();
        aes.Key = Key;
        aes.IV = IV;
        var decryptor = aes.CreateDecryptor();
        var bytes = Convert.FromBase64String(cipherText);
        var decrypted = decryptor.TransformFinalBlock(bytes, 0, bytes.Length);
        return Encoding.UTF8.GetString(decrypted);
    }
}
```

**For production:** Use a proper key management system. Never hardcode encryption keys — derive from device-specific identifiers or fetch from backend.

### 3.3 Platform Secure Storage

| Platform    | Secure Storage API                                                     | Purpose                                 |
| ----------- | ---------------------------------------------------------------------- | --------------------------------------- |
| **iOS**     | Keychain Services (via `UnityEngine.iOS.Device.advertisingIdentifier`) | Store session tokens, purchase receipts |
| **Android** | EncryptedSharedPreferences / Keystore                                  | Store session tokens, user preferences  |
| **Unity**   | `SecurePlayerPrefs` (third-party package)                              | Cross-platform secure storage           |

---

## 4. Server-Side Validation

### 4.1 Core Principle: Never Trust the Client

All economy-critical operations must be validated server-side:

| Operation                  | Client Sends            | Server Validates                          |
| -------------------------- | ----------------------- | ----------------------------------------- |
| **Purchase**               | Receipt + product ID    | Receipt with Apple/Google, grant currency |
| **Currency spend**         | Amount + reason         | Has enough currency? Reason valid?        |
| **Level completion**       | Level ID + score + time | Is score achievable? Time realistic?      |
| **Daily reward**           | Claim request           | Has 24h elapsed? Not already claimed?     |
| **Leaderboard submission** | Score                   | Is score within expected range for level? |

### 4.2 Server-Side Economy Architecture

```
Game Client                          Backend Server
┌─────────────────┐                  ┌──────────────────┐
│  Request:       │  ── HTTPS ──→    │  Validate:       │
│  "Claim reward" │                  │  - Player exists  │
│                 │  ←─ JSON ───     │  - Cooldown met   │
│  Response:      │                  │  - Not duplicate  │
│  { coins: 100 } │                  │  Apply:           │
│                 │                  │  - Grant reward   │
│                 │                  │  - Log transaction│
└─────────────────┘                  └──────────────────┘
```

---

## 5. SDK Security

### 5.1 Third-Party SDK Risk

Every SDK expands the attack surface. SDKs have full access to:

- Network communication
- File system (within app sandbox)
- Memory space
- Device identifiers

### 5.2 SDK Vetting Checklist

| Check                            | Description                                                             |
| -------------------------------- | ----------------------------------------------------------------------- |
| **Privacy policy exists**        | SDK provider must have a documented privacy policy                      |
| **Data collection documented**   | What data does the SDK collect? Where does it send it?                  |
| **COPPA compliance**             | If game may attract minors, SDK must support COPPA-compliant mode       |
| **Network endpoints documented** | All domains the SDK communicates with must be known and documented      |
| **No hidden permissions**        | SDK must not request excessive OS permissions                           |
| **Open source or auditable**     | Prefer SDKs with open-source components or documented APIs              |
| **Reputable provider**           | Established company with track record (Google, Meta, Unity, ironSource) |

### 5.3 SDK Isolation

| Technique                              | Purpose                                                               |
| -------------------------------------- | --------------------------------------------------------------------- |
| **Initialize SDKs only when needed**   | Don't initialize ad SDK on splash screen — initialize before first ad |
| **Disable SDKs in development builds** | Prevent test data polluting production analytics                      |
| **Monitor SDK network traffic**        | Use proxy tools (Charles, Fiddler) to verify SDK behavior             |
| **Keep SDKs updated**                  | Outdated SDKs may contain known vulnerabilities                       |

---

## 6. Penetration Testing for Games

### 6.1 Game-Specific Attack Vectors

| Vector                   | Test Method                                       | Tool                                      |
| ------------------------ | ------------------------------------------------- | ----------------------------------------- |
| **Memory tampering**     | Attempt to modify currency/score values in memory | GameGuardian (Android), Cheat Engine (PC) |
| **Save file editing**    | Locate and modify save files                      | File explorer + hex editor                |
| **Network interception** | Intercept and modify API requests                 | mitmproxy, Charles Proxy, Burp Suite      |
| **Speed hacking**        | Modify Time.timeScale or device clock             | Device clock manipulation                 |
| **API replay**           | Capture and replay API requests                   | Burp Suite, Postman                       |
| **Asset extraction**     | Extract APK/IPA and recover assets                | APKTool, ipa-extract                      |

### 6.2 Penetration Testing Checklist

| Test                                                 | Pass Criteria                                    |
| ---------------------------------------------------- | ------------------------------------------------ |
| Memory values cannot be modified to inflate currency | Server-side validation rejects impossible values |
| Save files cannot be edited to unlock content        | Encrypted or server-side stored                  |
| API requests cannot be forged                        | Authentication + server-side validation          |
| Speed hacks detected and blocked                     | Time verification (server or heuristic)          |
| Ad fraud not possible                                | Ad impression validation server-side             |
| No sensitive data in plaintext network traffic       | All communication over TLS 1.3                   |

---

## 7. External Resources

| Resource                                   | Link                                                                                                                   | Focus                                 |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| Unity Anti-Cheat Best Practices            | https://docs.bytehide.com/platforms/dotnet/products/shield/frameworks/unity/best-practices                             | IL2CPP, obfuscation, anti-tampering   |
| "Unity Anti-Cheat Integration"             | https://www.getgud.io/blog/unity-anti-cheat-integration-best-practices-and-pitfalls-revealed/                          | Integration patterns and pitfalls     |
| "Protecting Unity Games from Hacking"      | https://medium.com/@sonusprocks/protecting-your-unity-games-from-hacking-best-practices-and-security-tips-76d257bdef65 | Practical security tips               |
| "Mobile Game Security in Unity and Unreal" | https://promon.io/security-news/mobile-game-security-in-unity-and-unreal-reducing-cheat-roi-at-runtime                 | Runtime protection                    |
| OWASP MASVS                                | https://owasp.org/www-project-mobile-app-security-verification-standard/                                               | Mobile security verification standard |

---

_End of Game Security & Anti-Cheat_
