---
name: bazel-build-system
description: Configure and optimize Bazel build system for large-scale Android and multi-language monorepo builds — implementing hermetic builds, remote caching, and query-based dependency analysis to minimize CI build times.
version: "1.0.0"
---

# Bazel Build System

| Competency            | Description                                                   | Quality Criteria                                                                                                 |
| --------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| BUILD File Authorship | Write Bazel BUILD files for Android, Kotlin, and Java targets | All targets are hermetic (no env variable dependencies); deps are explicitly listed; no globs for source files   |
| Remote Caching        | Configure Bazel remote cache with BuildBuddy or GCS backend   | Cache hit rate > 90% on CI incremental builds; cache write only from trusted CI machines                         |
| Dependency Analysis   | Use `bazel query` and `bazel aquery` for build graph analysis | Identifies unused deps with `unused_deps`; maps critical path for longest build chains; detects circular deps    |
| Build Performance     | Profile and optimize build critical path                      | Bazel profile analyzed with `bazel analyze-profile`; top-5 slowest actions identified and optimized each quarter |

## Execution Guidance

### Hermetic Build Requirements

Bazel builds must be hermetic — meaning they produce identical outputs regardless of the machine state:

- No `genrule` commands that depend on system tools not declared as `toolchain_type`
- No file reads from outside the workspace root
- All timestamps and non-deterministic outputs handled with `--nostamp`

### Remote Cache Setup

```python
# .bazelrc
build --remote_cache=grpcs://remote.buildbuddy.io
build --remote_header=x-buildbuddy-api-key=<key>
build --remote_upload_local_results  # Only in CI
build:ci --remote_upload_local_results
```

Local developer machines should read from cache but not write — prevents cache poisoning from dirty local environments.
