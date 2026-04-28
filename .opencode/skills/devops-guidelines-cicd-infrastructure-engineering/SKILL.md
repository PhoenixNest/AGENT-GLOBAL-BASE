---
name: devops-guidelines-cicd-infrastructure-engineering
description: CI/CD infrastructure engineering for mobile pipelines — self-hosted runners, build agent scaling, distributed caching (Redis/S3), pipeline observability, and infrastructure-as-code for GitHub Actions, GitLab CI, and Bitrise. Owned by Thomas Zhang (DevOps Lead). Use during Stage 4 (Implementation Plan) for CI/CD infrastructure design and Stage 5 (Development) for pipeline provisioning. Trigger: CI/CD infrastructure, self-hosted runners, build agents, distributed cache, pipeline observability, GitHub Actions, GitLab CI, Bitrise, infrastructure as code.
prerequisites:
  - devops-guidelines-ci-cd-optimization

version: "1.0.0"
---

# CI/CD Infrastructure Engineering

## Overview

End-to-end CI/CD architecture design, build pipeline optimization, multi-platform build engineering, pipeline security hardening, and i18n pipeline automation. This skill enables a DevOps lead to design, implement, and maintain the continuous integration and delivery infrastructure that powers parallel development across Android, iOS, Cross-Platform (KMP/Flutter), and localization pipelines.

## Competency Dimensions

| Dimension                   | Proficiency Level | Key Capabilities                                                                  |
| --------------------------- | ----------------- | --------------------------------------------------------------------------------- |
| CI/CD Architecture          | Expert            | GitLab CI, ArgoCD, pipeline-as-code, multi-stage workflows, artifact management   |
| Build Pipeline Optimization | Expert            | Parallel execution, caching strategies, incremental builds, build time reduction  |
| Multi-Platform Builds       | Expert            | Android (Gradle), iOS (Xcode), KMP (Kotlin Multiplatform), Flutter — parallelized |
| Pipeline Security           | Advanced          | Secret management, signed artifacts, supply chain security, runner isolation      |
| i18n Pipeline Engineering   | Expert            | String extraction automation, TMS integration, translation validation, l10n QA    |
| Infrastructure as Code      | Advanced          | Terraform, Ansible, Kubernetes manifests for CI/CD infrastructure                 |
| GitOps Workflows            | Advanced          | Declarative infrastructure, automated deployments, drift detection                |

## Execution Guidance

### CI/CD Architecture (GitLab CI, ArgoCD)

**Pipeline Topology:**

```
commit → lint → unit-test → build → integration-test → security-scan → staging-deploy → e2e-test → release
```

**GitLab CI Structure:**

- `.gitlab-ci.yml` as the single source of truth for pipeline definition
- Stage-based organization with explicit dependencies between stages
- Use `needs:` keyword for DAG (Directed Acyclic Graph) execution — jobs run as soon as dependencies are satisfied, not waiting for entire stages
- Implement pipeline templates (`.gitlab-scripts/`) for shared configurations across platform pipelines

**GitLab CI Best Practices:**

- Define reusable job templates with `extends:` for common configurations
- Use `rules:` instead of deprecated `only:/except:` for conditional job execution
- Implement manual approval gates for production deployments (`when: manual`)
- Configure pipeline schedules for nightly full-test runs and weekly dependency scans
- Use CI/CD variables with masking and protection for secrets

**ArgoCD for Deployment:**

- GitOps model: deployment manifests stored in Git, ArgoCD syncs cluster state to Git
- Application definitions as Helm charts or Kustomize overlays per environment (dev, staging, prod)
- Automated sync with health checks; alert on drift between Git and cluster state
- Implement progressive delivery: canary → blue-green → full rollout with automated rollback on health check failure

### Build Pipeline Optimization

**Caching Strategy:**

- **Dependency cache:** Cache `~/.gradle/caches/`, `Pods/`, `flutter/.pub-cache/` with hash-based keys (checksum of lockfiles)
- **Build cache:** Enable Gradle build cache, Xcode DerivedData caching, Flutter incremental compilation
- **Layer caching (Docker):** Order Dockerfile instructions from least to most frequently changed; use multi-stage builds
- **Cache invalidation:** Use content-based cache keys (hash of relevant files), not time-based

**Parallel Execution:**

- Split test suites by module/feature with parallel execution across multiple runners
- Platform-parallel builds: Android, iOS, KMP, Flutter builds run simultaneously on dedicated runners
- Shard E2E tests: distribute test cases across N runners, aggregate results
- Use `parallel:matrix:` in GitLab CI for cross-platform parameterized jobs

**Incremental Builds:**

- Configure Gradle: `org.gradle.parallel=true`, `org.gradle.caching=true`, `org.gradle.configureondemand=true`
- Configure Xcode: use `xcodebuild` with `-clonedSourcePackagesDirPath` for SPM caching
- Configure Flutter: use `--no-pub` flag when dependencies haven't changed
- Track build times; alert on regressions (>20% increase triggers investigation)

### Multi-Platform Builds (Android/iOS/KMP/Flutter)

**Android (Gradle):**

- Use Gradle 8+ with configuration cache
- Build variants: `assembleDebug` for CI, `assembleRelease` for release candidates
- ProGuard/R8 optimization for release builds; mapping file upload to crash reporting
- APK/AAB signing with CI-stored keystores (never in source control)

**iOS (Xcode):**

- Use `xcodebuild` with `-workspace` and `-scheme` for deterministic builds
- Code signing: use CI-managed certificates and provisioning profiles (Fastlane Match)
- Xcode Cloud or self-hosted macOS runners for native iOS builds
- IPA export with bitcode disabled (Apple deprecated bitcode as of 2023)

**KMP (Kotlin Multiplatform):**

- Shared module builds: `./gradlew :shared:assemble` produces platform-specific artifacts
- Platform-specific compilation: JVM, Android, iOS (via Kotlin/Native)
- Cross-platform test execution: `./gradlew :shared:allTests`
- Expect/actual pattern validation in CI

**Flutter:**

- `flutter build apk --release` for Android, `flutter build ipa --release` for iOS
- Web: `flutter build web --release` for web deployment
- `flutter test` with `--machine` flag for CI-friendly test output
- Flutter analyze: `flutter analyze --no-fatal-infos`

**Parallel Platform Build Orchestration:**

```yaml
# GitLab CI example
stages:
  - build-android
  - build-ios
  - build-kmp
  - build-flutter

build-android:
  stage: build-android
  script: ./gradlew assembleRelease
  tags: [android-runner]

build-ios:
  stage: build-ios
  script: fastlane build_ios
  tags: [macos-runner]

build-kmp:
  stage: build-kmp
  script: ./gradlew :shared:assemble
  tags: [kmp-runner]

build-flutter:
  stage: build-flutter
  script: flutter build apk --release && flutter build ipa --release
  tags: [flutter-runner]
```

### Pipeline Security Hardening

**Secret Management:**

- Use GitLab CI/CD variables with masking (values hidden in logs) and protection (available only on protected branches)
- Rotate secrets automatically using HashiCorp Vault or AWS Secrets Manager with CI integration
- Never store secrets in `.gitlab-ci.yml`, `.env` files, or source code
- Use short-lived tokens (OIDC federation) instead of long-lived API keys where possible

**Runner Isolation:**

- Use ephemeral runners (Docker containers or Kubernetes pods) that are destroyed after each job
- Separate runners per security zone: public runners for OSS, private runners for internal code
- Implement runner authentication tokens with rotation policies
- Monitor runner health: CPU, memory, disk usage alerts

**Signed Artifacts:**

- Sign all build artifacts (APK, AAB, IPA) with platform signing keys
- Generate and store checksums (SHA-256) for all artifacts
- Implement artifact provenance: record build environment, source commit, builder identity
- Use cosign or Sigstore for container image signing

**Supply Chain Security:**

- Scan all dependencies in CI (SCA scanning with Trivy, Snyk, or Dependabot)
- Pin dependency versions; reject wildcard ranges in production builds
- Generate SBOM for every build artifact
- Implement allowlist for approved third-party repositories and registries

### i18n Pipeline Engineering

**String Extraction Automation:**

- **Android:** Extract `strings.xml` from codebase using `lint --check MissingTranslation`; validate all user-facing strings are in resource files
- **iOS:** Extract `Localizable.strings` using `genstrings` or Swift `strings` tool; validate all `NSLocalizedString` calls have keys
- **Flutter:** Extract `arb` files using `flutter gen-l10n`; validate all `AppLocalizations` calls are covered
- **Web:** Extract using i18next parser, react-i18next scanner, or Angular i18n extraction

**TMS (Translation Management System) Integration:**

- Push extracted source strings to TMS (Crowdin, Lokalise, Transifex) via API
- Configure translation memory and glossary per project
- Set up webhooks: TMS notifies CI when translations are ready
- Pull completed translations back into codebase via CI job
- Validate translation completeness: flag missing translations before merge

**Translation Quality Checks:**

- Validate string format specifiers match between source and translation (`%s`, `%d`, `%1$s`)
- Check for placeholder consistency: ensure all placeholders in source exist in translation
- Length validation: flag translations exceeding UI space limits (especially for German, Russian)
- Right-to-left validation: ensure Arabic/Hebrew translations display correctly in RTL layout mode
- Pseudo-localization testing: use pseudo-translated strings to catch hardcoded text and layout issues

**i18n Pipeline Flow:**

```
code commit → extract strings → validate extraction → push to TMS → TMS translation →
webhook trigger → pull translations → validate completeness → validate formatting →
commit translations → trigger localized build → run l10n regression tests
```

### Infrastructure as Code

**Terraform for CI/CD Infrastructure:**

- Define runner infrastructure (EC2 instances, Kubernetes clusters, macOS builders) in Terraform
- Version Terraform state with remote backends (S3 + DynamoDB locking)
- Use modules for reusable infrastructure patterns (runner pool, artifact storage, network config)
- Implement `terraform plan` in CI on every infrastructure change; require approval before `apply`

**Kubernetes for CI/CD:**

- Deploy GitLab Runner as Kubernetes deployment with auto-scaling (HPA based on job queue depth)
- Use namespace isolation per project/environment
- Configure resource quotas and limit ranges for CI jobs
- Implement network policies to restrict runner access to only required services

### GitOps Workflows

**Principles:**

- All infrastructure and application configuration in Git
- Automated sync: Git state → cluster state (via ArgoCD or Flux)
- Pull-based deployments: cluster pulls from Git (not pushed from CI)
- Audit trail: every change tracked in Git history with PR review

**Implementation:**

- Monorepo or multi-repo structure for infrastructure Git repositories
- Environment promotion: dev → staging → prod via Git branch or directory promotion
- Automated PR creation for dependency updates (Renovate, Dependabot)
- Drift detection: alert when cluster state diverges from Git state
- Rollback: `git revert` + ArgoCD sync for instant rollback

## Pipeline Integration

| Pipeline Stage                | CI/CD Infrastructure Activity                                                       |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| Stage 3 (Architecture)        | Define CI/CD architecture in TSD; select tools and topology                         |
| Stage 4 (Implementation Plan) | Configure initial CI/CD pipelines; set up runners and artifact storage              |
| Stage 5 (Development)         | Maintain CI/CD pipelines; optimize build times; manage multi-platform builds        |
| Stage 6 (Code Review)         | Ensure CI gates (lint, test, SAST) pass before code review; review pipeline changes |
| Stage 7 (Testing)             | Orchestrate parallel test execution across platforms; aggregate results             |
| Stage 8 (Integrity)           | Verify artifact signatures, SBOMs, and provenance; validate i18n pipeline outputs   |
| Stage 9 (i18n)                | Execute i18n pipeline: string extraction, TMS sync, translation integration         |
| Stage 10 (Release)            | Execute release pipeline: version bump, artifact signing, platform submission       |

## Quality Standards

- **Build success rate:** >98% of CI builds must pass on the first run
- **Build time targets:** Android <10 min, iOS <15 min, KMP <8 min, Flutter <8 min (full build)
- **Pipeline feedback time:** Lint + unit test results within 5 minutes of commit
- **Artifact integrity:** 100% of release artifacts must be signed with verified provenance
- **i18n completeness:** 100% of source strings extracted and pushed to TMS within 1 hour of merge
- **Security scanning:** 100% of builds scanned for vulnerabilities; critical findings block release
- **Infrastructure drift:** <1% divergence between Git state and deployed state

## Reference Materials

- GitLab CI/CD Documentation: https://docs.gitlab.com/ee/ci/
- ArgoCD Documentation: https://argo-cd.readthedocs.io/
- Fastlane: https://fastlane.tools/
- Gradle Build Optimization: https://docs.gradle.org/current/userguide/performance.html
- Xcode Build Analysis: https://www.swiftbysundell.com/articles/analyzing-xcode-build-performance/
- Terraform Best Practices: https://www.terraform-best-practices.com/
- GitOps Principles: https://opengitops.dev/
- Crowdin API: https://developer.crowdin.com/api/v2/
- Lokalise API: https://api.lokalise.com/
- Sigstore/Cosign: https://docs.sigstore.dev/
