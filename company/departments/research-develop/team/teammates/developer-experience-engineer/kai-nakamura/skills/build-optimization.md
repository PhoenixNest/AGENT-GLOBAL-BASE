---
version: "1.0.0"
---

| Competency                  | Description                                                                                    | Quality Criteria                                                                                                                           |
| --------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Gradle Configuration Cache  | Cache serialization, task input/output declaration, configuration phase optimization           | Achieves 100% configuration cache compatibility; identifies and fixes cache-incompatible tasks; reduces configuration phase to < 2 seconds |
| Bazel Remote Caching        | Remote cache server setup, action caching, content-addressable storage, cache hit optimization | Configures remote cache for team-wide build acceleration; achieves > 70% cache hit rate; designs hermetic build rules                      |
| Incremental Build Design    | Task input/output declarations, file change detection, up-to-date checks                       | All tasks declare inputs/outputs correctly; incremental builds < 10% of clean build time; no unnecessary task re-execution                 |
| Build Scan Analysis         | Gradle Enterprise scan interpretation, bottleneck identification, trend analysis               | Identifies slowest tasks and dependencies; tracks build time trends over releases; correlates build time with codebase changes             |
| CI Pipeline Parallelization | Stage decomposition, dependency-based parallelism, resource allocation, artifact sharing       | Designs CI pipelines with maximum parallelism; reduces CI time by > 50% through parallelization; optimizes resource utilization            |
| Build Time SLO Management   | SLO definition, monitoring, alerting, regression detection, budget tracking                    | Defines build time SLOs per project; monitors build time trends; alerts on SLO violations; tracks build time budget consumption            |

## Execution Guidance

### Gradle Configuration Cache

```kotlin
// gradle.properties
org.gradle.configuration-cache=true
org.gradle.configuration-cache.parallel=true
org.gradle.caching=true
org.gradle.parallel=true
org.gradle.daemon=true
org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g -XX:+UseParallelGC

// build.gradle.kts — Configuration cache compatibility
plugins {
    id("java")
    id("org.jetbrains.kotlin.jvm") version "1.9.20"
}

// Problem: Using project evaluation during configuration phase
// ❌ BAD — breaks configuration cache
// val version = project.findProperty("appVersion") ?: "1.0.0"
// tasks.register("printVersion") {
//     doLast { println(version) }
// }

// ✅ GOOD — use providers for lazy evaluation
val appVersion = providers.gradleProperty("appVersion").orElse("1.0.0")

tasks.register("printVersion") {
    val version = appVersion  // Provider evaluated at execution time
    doLast { println(version.get()) }
}

// Task input/output declaration for incremental builds
tasks.register<Zip>("packageAssets") {
    // Declare inputs — task only runs if these change
    inputs.dir("src/main/assets")
    inputs.file("src/main/assets-manifest.json")

    // Declare outputs — enables up-to-date check
    archiveFileName.set("assets.zip")
    destinationDirectory.set(layout.buildDirectory.dir("distributions"))

    from("src/main/assets")
}

// Avoiding configuration cache violations
// ❌ Violation: accessing build script classpath during configuration
// val classpath = buildscript.configurations["classpath"]

// ✅ Fix: use provider for classpath resolution
val classpathProvider = configurations.named("classpath")

// Common configuration cache violations and fixes:
// 1. Task creation based on file system scanning
//    ❌ File("src").listFiles().forEach { ... }
//    ✅ layout.projectDirectory.dir("src").asFileTree.forEach { ... }
//
// 2. Using System.getProperty during configuration
//    ❌ System.getProperty("os.name")
//    ✅ providers.systemProperty("os.name")
//
// 3. Modifying project state during task execution
//    ❌ project.extra.set("key", value) in doLast
//    ✅ Use local variables or write to file
```

### Bazel Remote Caching

```python
# WORKSPACE
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# .bazelrc — Remote cache configuration
# Build with remote cache
build --remote_cache=grpcs://cache.company.com:9092
build --remote_instance_name=company-monorepo

# Authentication (use service account)
build --google_default_credentials

# Local cache fallback
build --disk_cache=/tmp/bazel-cache

# Remote execution (optional)
# build --remote_executor=grpcs://build.company.com:9092

# Cache optimization
build --remote_download_toplevel  # Only download top-level outputs
build --experimental_remote_download_regex=.*\\.jar$  # Or specific patterns

# BUILD file — Hermetic rule definition
java_library(
    name = "user-service",
    srcs = glob(["src/main/java/**/*.java"]),
    deps = [
        "//lib:common-utils",
        "@maven//:com_google_guava_guava",
        "@maven//:io_grpc_grpc_netty",
    ],
    # Explicitly declare resources for caching
    resources = glob(["src/main/resources/**/*"]),
    # Resource strip prefix for correct classpath
    resource_strip_prefix = "src/main/resources",
)

# Custom rule with proper inputs/outputs
def _custom_codegen_impl(ctx):
    # Declare all inputs
    inputs = [ctx.file.template, ctx.file.config]

    # Declare all outputs
    output = ctx.actions.declare_file(ctx.attr.name + ".java")

    # Action with explicit inputs and outputs
    ctx.actions.run(
        executable = ctx.executable._codegen_tool,
        arguments = [
            "--template", ctx.file.template.path,
            "--config", ctx.file.config.path,
            "--output", output.path,
        ],
        inputs = inputs,
        outputs = [output],
        mnemonic = "Codegen",
        progress_message = "Generating %s" % output.short_path,
    )

    return [DefaultInfo(files = depset([output]))]

custom_codegen = rule(
    implementation = _custom_codegen_impl,
    attrs = {
        "template": attr.label(mandatory = True, allow_single_file = True),
        "config": attr.label(mandatory = True, allow_single_file = True),
        "_codegen_tool": attr.label(
            default = "//tools:codegen",
            executable = True,
            cfg = "exec",
        ),
    },
)
```

### Incremental Build Design

```
Incremental build performance targets:

| Build Type | Target | Measurement |
|------------|--------|-------------|
| Clean build | < 5 minutes | `./gradlew clean build` |
| Incremental (single file change) | < 30 seconds | Change 1 file, rebuild |
| Configuration phase | < 2 seconds | `./gradlew help --scan` |
| Test (no code changes) | < 10 seconds | `./gradlew test` |
| CI build (full) | < 15 minutes | CI pipeline |
```

**Identifying incremental build issues:**

```bash
# Run build with info to see task execution
./gradlew build --info 2>&1 | grep "UP-TO-DATE\|EXECUTING\|FROM-CACHE"

# Expected output for incremental build:
# > Task :compileJava UP-TO-DATE
# > Task :processResources UP-TO-DATE
# > Task :classes UP-TO-DATE
# > Task :compileTestJava FROM-CACHE
# > Task :test EXECUTING  # Only test task runs

# If too many tasks execute on incremental build, investigate:
# 1. Missing input/output declarations
# 2. Tasks using non-deterministic inputs (timestamps, random)
# 3. Tasks modifying files they don't declare as outputs

# Build scan analysis
./gradlew build --scan
# Opens build scan URL with detailed task timing and cache analysis
```

### Build Scan Analysis

```markdown
# Build Scan Interpretation Guide

## Key Metrics

| Metric                | Good    | Warning  | Critical |
| --------------------- | ------- | -------- | -------- |
| Total build time      | < 3 min | 3-8 min  | > 8 min  |
| Configuration time    | < 2s    | 2-5s     | > 5s     |
| Dependency resolution | < 10s   | 10-30s   | > 30s    |
| Test execution        | < 5 min | 5-15 min | > 15 min |
| Cache hit rate        | > 70%   | 40-70%   | < 40%    |

## Bottleneck Identification

1. **Timeline view:** Identify sequential tasks that could be parallel
2. **Task duration:** Top 10 slowest tasks
3. **Dependency graph:** Find critical path through task graph
4. **Cache analysis:** Tasks not using cache — why?
5. **Configuration analysis:** Plugins adding configuration overhead

## Common Bottlenecks

| Symptom                    | Cause                                          | Fix                                               |
| -------------------------- | ---------------------------------------------- | ------------------------------------------------- |
| Long configuration phase   | Too many plugins, eager task creation          | Use lazy configuration, apply plugins selectively |
| Tests always re-run        | Non-deterministic test inputs, missing outputs | Declare test inputs, use build cache              |
| Dependency resolution slow | Dynamic versions, missing local cache          | Use locked versions, enable dependency cache      |
| Compilation slow           | Large source sets, annotation processors       | Split modules, configure incremental compilation  |
| Low cache hit rate         | Non-hermetic builds, environment-dependent     | Fix build rules, use remote cache                 |
```

### CI Pipeline Parallelization

```yaml
# GitHub Actions — Parallel CI Pipeline
name: CI Pipeline
on:
  pull_request:
    branches: [main]

jobs:
  # Stage 1: Independent checks (run in parallel)
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./gradlew lint
      - run: ./gradlew ktlintCheck

  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4] # Test sharding
      fail-fast: false
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 21
      - name: Run tests (shard ${{ matrix.shard }})
        run: ./gradlew test --tests "shard-${{ matrix.shard }}/*"
      - uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ matrix.shard }}
          path: build/test-results/test/

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - run: ./gradlew integrationTest

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./gradlew dependencyCheckAnalyze

  # Stage 2: Depends on Stage 1 completion
  build:
    needs: [lint, unit-tests]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./gradlew assemble

  # Stage 3: Depends on Stage 2
  deploy-staging:
    needs: [build, integration-tests, security-scan]
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh staging
```

**CI time optimization techniques:**

| Technique               | Time Savings | Implementation                       |
| ----------------------- | ------------ | ------------------------------------ |
| Test sharding           | 60-75%       | Split tests across N runners         |
| Build cache             | 40-60%       | Remote cache shared across CI runs   |
| Affected tests          | 50-80%       | Only run tests for changed modules   |
| Incremental compilation | 70-90%       | Compiler reuses previous compilation |
| Parallel execution      | 30-50%       | `--parallel` flag, max workers       |
| Artifact reuse          | 20-40%       | Share build artifacts between stages |

### Build Time SLO Management

```markdown
# Build Time SLOs

## SLO Definitions

| Pipeline                | SLO      | Measurement                  | Alert Threshold |
| ----------------------- | -------- | ---------------------------- | --------------- |
| Local clean build       | < 5 min  | Developer survey + telemetry | P95 > 8 min     |
| Local incremental build | < 30 sec | Developer survey + telemetry | P95 > 60 sec    |
| CI build (PR)           | < 15 min | CI pipeline duration         | P95 > 20 min    |
| CI build (main)         | < 20 min | CI pipeline duration         | P95 > 30 min    |
| Test suite              | < 10 min | Test stage duration          | P95 > 15 min    |

## Monitoring

- Track build times in Prometheus/Grafana
- Weekly build time trend report
- Monthly build time review in engineering standup

## Regression Detection

- Alert when P95 build time exceeds SLO for 3 consecutive days
- Alert when build time increases by > 20% week-over-week
- Block releases if build time SLO violated for > 1 week

## Budget

- Build infrastructure budget: $X/month
- Cache hit rate target: > 70%
- CI runner utilization: 60-80%
```

## Pipeline Integration

**Stage 4 (Implementation Plan):** Build system configuration included as infrastructure tasks. Build time SLOs defined per project. CI pipeline designed with parallelization.

**Stage 5 (Development):** Gradle/Bazel configuration optimized for incremental builds. Remote cache configured. Build scan analysis performed weekly.

**Stage 6 (Code Review):** Review build configuration for incremental build compatibility. Check task input/output declarations. Validate cache hit rates.

**Stage 7 (Testing):** Build time measured as part of test execution. CI pipeline duration tracked. Build regression tests validate incremental behavior.

## Quality Standards

| Metric                            | Target                     | Measurement                  |
| --------------------------------- | -------------------------- | ---------------------------- |
| Configuration cache compatibility | 100% of tasks compatible   | `--configuration-cache` test |
| Incremental build time            | < 10% of clean build time  | Build timing comparison      |
| Remote cache hit rate             | > 70%                      | Build cache metrics          |
| CI pipeline duration (P95)        | < 15 minutes               | CI monitoring                |
| Build time SLO compliance         | > 95% of builds within SLO | SLO dashboard                |
| Build regression rate             | < 1 per month              | Build trend analysis         |
