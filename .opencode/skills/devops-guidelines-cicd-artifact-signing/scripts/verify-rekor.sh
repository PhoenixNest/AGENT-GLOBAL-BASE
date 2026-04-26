cosign verify-blob \
  --signature app-release.apk.sig \
  --certificate app-release.apk.pem \
  --certificate-identity="https://github.com/our-org/mobile-app/.github/workflows/release-signing.yml@refs/heads/main" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  --rekor-url="https://rekor.sigstore.dev" \
  app-release.apk