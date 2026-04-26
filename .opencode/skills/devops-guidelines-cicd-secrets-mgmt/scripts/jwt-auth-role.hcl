vault write auth/jwt/role/github-ci-mobile-app \
  role_type="jwt" \
  bound_audiences="https://vault.company.internal" \
  bound_subject="repo:our-org/mobile-app:ref:refs/heads/main" \
  user_claim="repository" \
  ttl="5m" \
  policies="github-ci-mobile-app"