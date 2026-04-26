---
name: android-security-ci-cd-ci-cd
description: Android CI/CD pipeline — Gradle optimization (configuration cache, build cache), GitHub Actions workflows, Firebase App Distribution for beta releases, Crashlytics crash reporting, Detekt/ktlint quality gates, and Renovate dependency automation. Owned by Jan Kowalski (Android Engineer). Use during Stage 5 (Development) for build infrastructure setup and Stage 7 (Automated Testing) for CI test orchestration. Trigger: android CI/CD, gradle optimization, github actions, firebase distribution, crashlytics, detekt, ktlint, build pipeline, quality gates.
prerequisites:
  - android-language-core-implementation

version: "1.0.0"
---

# Android CI/CD

**Category:** Mobile Engineering — Android DevOps
**Owner:** Android Engineer (Jan Kowalski)

## Overview

This skill establishes continuous integration and delivery pipelines for Android applications covering Gradle optimization, GitHub Actions workflows, Firebase App Distribution for beta testing, and crash reporting integration. It applies to Stage 5 (Development) where build infrastructure is configured, Stage 6 (Code Review) where CI gates enforce quality standards, and Stage 7 (Automated Testing) where the full test suite runs in CI.

## Competency Dimensions

| Dimension                 | Description                                                                                                       | Proficiency Indicators                                                                                         |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Gradle Optimization       | Configuration cache, build cache, parallel execution, module dependency graph, build profiling                    | Clean build <3 minutes on CI; incremental build <30 seconds; zero dynamic version resolution in release builds |
| GitHub Actions            | Workflow composition, matrix builds, caching strategies, artifact management, environment secrets                 | Parallel test execution across API levels; efficient dependency caching; secure secret management              |
| Firebase App Distribution | Distribution groups, release notes automation, tester feedback, in-app update integration                         | Beta releases distributed within 5 minutes of merge; tester feedback integrated into defect tracking           |
| Crash Reporting           | Firebase Crashlytics, custom keys, NDK crash handling, ANR monitoring, breadcrumb logging                         | Crash-free rate >99.5%; all crashes have actionable context; ANR rate <0.5%                                    |
| Build Quality Gates       | Detekt linting, ktlint formatting, dependency analysis, binary compatibility validation, code coverage thresholds | PR blocked on lint failures; dependency updates tracked via automated PRs; API surface changes tracked         |

## Execution Guidance

### Gradle Optimization — Production Configuration

**Root build.gradle.kts:**

```kotlin
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.android.library) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.kapt) apply false
    alias(libs.plugins.hilt) apply false
    alias(libs.plugins.ksp) apply false
}

// Global build configuration
subprojects {
    tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile>().configureEach {
        kotlinOptions {
            jvmTarget = JavaVersion.VERSION_17.toString()
            freeCompilerArgs = listOf(
                "-opt-in=kotlin.RequiresOptIn",
                "-opt-in=kotlinx.coroutines.ExperimentalCoroutinesApi",
                "-Xjsr305=strict"  // Strict nullability for Java interop
            )
        }
    }
}
```

**App build.gradle.kts — Release optimization:**

```kotlin
android {
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            // Enable R8 full mode for maximum optimization
            isR8FullMode = true
            // Signing configuration
            signingConfig = signingConfigs.getByName("release")
        }
        debug {
            isMinifyEnabled = false
            // Enable debug tools
            isDebuggable = true
            applicationIdSuffix = ".debug"
        }
    }

    // Enable build features
    buildFeatures {
        compose = true
        buildConfig = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = libs.versions.compose.compiler.get()
    }
}

// Dependency optimization
dependencies {
    // Use version catalog for consistent versions
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.viewmodel.ktx)
    implementation(libs.compose.ui)
    implementation(libs.compose.material3)
    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)

    // Release-only dependencies
    releaseImplementation(libs.leakcanary.android.noop)
    debugImplementation(libs.leakcanary.android)
}
```

**gradle.properties — Performance tuning:**

```properties
# Gradle daemon
org.gradle.daemon=true
org.gradle.jvmargs=-Xmx4096m -Dfile.encoding=UTF-8 -XX:+UseParallelGC

# Parallel and configuration cache
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configuration-cache=true
org.gradle.configureondemand=true

# Kotlin incremental compilation
kotlin.incremental=true
kotlin.incremental.useClasspathSnapshot=true
kotlin.caching.enabled=true

# Android specific
android.useAndroidX=true
android.nonTransitiveRClass=true
android.enableR8.fullMode=true
android.defaults.buildfeatures.buildconfig=true
android.nonFinalResIds=false
```

**Build profiling and optimization workflow:**

```bash
# Generate build profile
./gradlew :app:assembleRelease --profile

# Open profile report (opens in browser)
open build/reports/profile/profile-*.html

# Analyze APK size
./gradlew :app:analyzeReleaseBundle

# Check dependency tree for duplicates
./gradlew :app:dependencies --configuration releaseRuntimeClasspath

# Identify unused resources
./gradlew :app:lintRelease
```

### GitHub Actions — Complete CI Pipeline

```yaml
# .github/workflows/android-ci.yml
name: Android CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

# Cancel redundant workflow runs
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  GRADLE_OPTS: -Dorg.gradle.daemon=false -Dorg.gradle.jvmargs="-Xmx4g"

jobs:
  lint:
    name: Lint & Static Analysis
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: "zulu"
          java-version: "17"

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3
        with:
          cache-encryption-key: ${{ secrets.GRADLE_ENCRYPTION_KEY }}

      - name: Run ktlint
        run: ./gradlew ktlintCheck

      - name: Run Detekt
        run: ./gradlew detekt

      - name: Run lint
        run: ./gradlew lintRelease

      - name: Upload lint reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: lint-reports
          path: "**/build/reports/lint-results-*.html"

  unit-test:
    name: Unit Tests
    runs-on: ubuntu-latest
    timeout-minutes: 20

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: "zulu"
          java-version: "17"

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3

      - name: Run unit tests with coverage
        run: ./gradlew testDebugUnitTest jacocoTestReport

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: unit-test-results
          path: "**/build/test-results/testDebugUnitTest/*.xml"

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: "**/build/reports/jacoco/"

  instrumented-test:
    name: Instrumented Tests (API ${{ matrix.api-level }})
    runs-on: ubuntu-latest
    timeout-minutes: 45
    strategy:
      matrix:
        api-level: [30, 33, 34]

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: "zulu"
          java-version: "17"

      - name: Enable KVM
        run: |
          echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' | sudo tee /etc/udev/rules.d/99-kvm4all.rules
          sudo udevadm control --reload-rules
          sudo udevadm trigger --name-match=kvm

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3

      - name: Run instrumented tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: ${{ matrix.api-level }}
          arch: x86_64
          profile: Nexus 6
          script: ./gradlew connectedDebugAndroidTest

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: instrumented-test-results-api-${{ matrix.api-level }}
          path: "**/build/outputs/androidTest-results/"

  build-release:
    name: Build Release APK
    runs-on: ubuntu-latest
    timeout-minutes: 30
    needs: [lint, unit-test]

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: "zulu"
          java-version: "17"

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3

      - name: Decode signing keystore
        run: echo "${{ secrets.RELEASE_KEYSTORE_BASE64 }}" | base64 --decode > app/release.keystore

      - name: Build Release AAB
        run: ./gradlew :app:bundleRelease
        env:
          SIGNING_KEYSTORE: release.keystore
          SIGNING_KEY_ALIAS: ${{ secrets.SIGNING_KEY_ALIAS }}
          SIGNING_KEY_PASSWORD: ${{ secrets.SIGNING_KEY_PASSWORD }}
          SIGNING_STORE_PASSWORD: ${{ secrets.SIGNING_STORE_PASSWORD }}

      - name: Upload AAB
        uses: actions/upload-artifact@v4
        with:
          name: release-aab
          path: app/build/outputs/bundle/release/*.aab
```

### Firebase App Distribution — Beta Pipeline

```yaml
# .github/workflows/beta-release.yml
name: Beta Release

on:
  push:
    branches: [develop]

jobs:
  beta-release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: "zulu"
          java-version: "17"

      - name: Build Release APK
        run: ./gradlew :app:assembleRelease

      - name: Distribute to Firebase
        uses: wzieba/Firebase-Distribution-Github-Action@v1
        with:
          appId: ${{ secrets.FIREBASE_APP_ID }}
          serviceCredentialsFileContent: ${{ secrets.FIREBASE_CREDENTIALS }}
          groups: beta-testers
          file: app/build/outputs/apk/release/app-release.apk
          releaseNotes: |
            ${{ github.event.head_commit.message }}

            Build: ${{ github.sha }}
            Branch: ${{ github.ref_name }}
```

### Crashlytics Integration

```kotlin
// Application class — initialize and configure Crashlytics
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()

        FirebaseApp.initializeApp(this)

        // Set user identifier for crash correlation
        Firebase.auth.currentUser?.uid?.let { uid ->
            Firebase.crashlytics.setUserId(uid)
        }

        // Set custom keys for crash context
        Firebase.crashlytics.setCustomKey("app_version", BuildConfig.VERSION_NAME)
        Firebase.crashlytics.setCustomKey("build_type", BuildConfig.BUILD_TYPE)
        Firebase.crashlytics.setCustomKey("api_environment", BuildConfig.API_ENVIRONMENT)
    }
}

// Repository layer — log breadcrumb for crash context
class UserRepositoryImpl(
    private val api: UserApi,
    private val dao: UserDao
) : UserRepository {

    override suspend fun getUser(id: String): Result<User> {
        return try {
            Firebase.crashlytics.log("Fetching user: $id")
            val response = api.getUser(id)
            Result.success(response.toDomain())
        } catch (e: Exception) {
            Firebase.crashlytics.log("Failed to fetch user: $id — ${e.message}")
            Firebase.crashlytics.setCustomKey("failed_user_id", id)
            Result.failure(e)
        }
    }
}

// Non-fatal exception reporting
fun reportNonFatalException(exception: Exception, context: Map<String, String> = emptyMap()) {
    context.forEach { (key, value) ->
        Firebase.crashlytics.setCustomKey(key, value)
    }
    Firebase.crashlytics.recordException(exception)
}
```

### Build Quality Gates

**Detekt configuration (detekt.yml):**

```yaml
build:
  maxIssues: 0 # Fail on any issue
  excludeCorrectable: false

complexity:
  ComplexMethod:
    threshold: 15
  LongMethod:
    threshold: 60
  LongParameterList:
    functionThreshold: 6
    constructorThreshold: 7
  TooManyFunctions:
    thresholdInFiles: 15
    thresholdInClasses: 15
    thresholdInInterfaces: 10

style:
  MagicNumber:
    ignorePropertyDeclaration: true
    ignoreAnnotation: true
  UnusedImports:
    active: true
  WildcardImport:
    active: true

exceptions:
  SwallowedException:
    active: true
  TooGenericExceptionCaught:
    active: true
```

**Dependency update automation (Renovate):**

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:base"],
  "packageRules": [
    {
      "matchManagers": ["gradle"],
      "groupName": "Android dependencies",
      "schedule": ["every weekend"]
    },
    {
      "matchPackagePatterns": ["androidx.compose"],
      "groupName": "Compose dependencies"
    }
  ]
}
```

## Pipeline Integration

- **Stage 4 (Implementation Plan):** CI/CD pipeline configuration is a task in the implementation plan with estimated effort for each workflow.
- **Stage 5 (Development):** Build infrastructure configured alongside feature development. Gradle optimization applied from project start.
- **Stage 6 (Code Review):** CI gates enforce lint, ktlint, and detekt standards. PRs cannot merge without passing CI.
- **Stage 7 (Automated Testing):** Full test suite (unit + instrumented) runs in CI on multiple API levels. Coverage reports generated and uploaded.
- **Stage 10 (Release Readiness):** Release build artifacts (AAB) produced by CI pipeline. Crash-free rate verified via Crashlytics dashboard.

## Quality Standards

- Clean CI build time **<3 minutes** (lint + unit tests)
- Incremental CI build time **<30 seconds** (after cache warm)
- Instrumented tests complete in **<45 minutes** across all API levels
- **100%** PRs pass lint, ktlint, and detekt checks before merge
- Detekt maxIssues set to **0** — no quality debt allowed
- Crash-free user rate **>99.5%** (measured over rolling 28-day window)
- ANR rate **<0.5%** (measured over rolling 28-day window)
- Beta releases distributed to Firebase within **5 minutes** of merge to develop
- Release signing keys never stored in repository — use CI secrets only
- All CI workflows have timeout limits to prevent runaway builds
- Dependency updates automated via Renovate with grouped PRs
- Code coverage threshold: domain >80%, presentation >60%, data >70%
