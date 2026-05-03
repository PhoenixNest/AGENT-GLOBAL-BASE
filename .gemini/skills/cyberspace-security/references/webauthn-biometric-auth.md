---
name: webauthn-biometric-auth
description: Implement WebAuthn/FIDO2 passwordless authentication — covering credential registration, authentication assertion verification, and platform authenticator integration — as the company's primary web authentication mechanism replacing password-based login.
version: "1.0.0"
---

# Webauthn Biometric Auth

| Competency               | Description                                         | Quality Criteria                                                                                                           |
| ------------------------ | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Credential Registration  | Implement the WebAuthn registration ceremony        | Server generates challenge with proper randomness (≥ 16 bytes); `attestationObject` verified; credential public key stored |
| Authentication Assertion | Implement the WebAuthn authentication ceremony      | Server verifies `clientDataJSON`, `authenticatorData`, and signature; replay attack prevention via challenge tracking      |
| Platform Authenticator   | Integrate with Face ID, Touch ID, and Windows Hello | `authenticatorSelection.authenticatorAttachment = "platform"` enforced; UX handles authenticator absence gracefully        |
| Fallback Handling        | Provide secure fallback for unsupported browsers    | Progressive enhancement: WebAuthn where supported; TOTP fallback for unsupported platforms; no password fallback in scope  |

## Execution Guidance

### Registration Flow

```typescript
// 1. Server: generate options
const options = generateRegistrationOptions({
  rpName: "Company App",
  rpID: "app.company.com",
  userName: user.email,
  attestationType: "none", // Simplewebauthn recommended
  authenticatorSelection: {
    authenticatorAttachment: "platform",
    residentKey: "required",
    userVerification: "required",
  },
});

// 2. Client: call browser API
const credential = await startRegistration(options);

// 3. Server: verify and store
const verification = await verifyRegistrationResponse({
  response: credential,
  expectedChallenge: options.challenge,
  expectedOrigin: "https://app.company.com",
  expectedRPID: "app.company.com",
});
```

### Security Requirements

| Requirement          | Value                                   |
| -------------------- | --------------------------------------- |
| Challenge randomness | ≥ 16 bytes from CSPRNG                  |
| Challenge expiry     | 5 minutes                               |
| User verification    | `required` (not `preferred`)            |
| Origin validation    | Exact match — no wildcards              |
| Credential storage   | Public key only — never the private key |
