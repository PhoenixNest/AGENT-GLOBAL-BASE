---
name: devops-guidelines-bazel-build-system
description: "Devops skill: Bazel Build System"
---

# Bazel Build System

## Overview

This skill covers Bazel build system migration strategies, remote execution configuration, and build cache optimization for large-scale monorepo projects. It is used by Developer Experience engineers during Stage 5 (Development) for build system optimization and Stage 8 (Integrity Verification) for build infrastructure conformance.

## When to Migrate to Bazel

- Monorepo with 500+ source files and build times exceeding 10 minutes.
- Multiple build tools in use (Gradle, npm, Make) causing inconsistent developer experience.
- Need for hermetic, reproducible builds across different environments.

## Migration Phases

1. **Coexistence**: Bazel runs alongside existing build tool — wraps the existing build, validates output parity.
2. **Incremental adoption**: High-impact targets migrated first (large, frequently-built modules).
3. **Full migration**: All targets built with Bazel; legacy build tooling removed.
4. **Remote execution**: Build distributed across cluster for massive speed gains.

## Remote Execution Setup

```python
# .bazelrc
build --remote_cache=grpcs://build-cache.internal:9092
build --remote_executor=grpcs://build-executor.internal:9092
build --remote_download_toplevel
```

**Cache key strategy**:

- Action cache: content-addressed storage of inputs and outputs.
- Remote cache hit rate target: >70% for typical developer workflow.
- Cache eviction policy: LRU with 30-day retention.

## Build Performance Tuning

- Hermetic toolchains: pinned compiler/SDK versions, no system dependency assumptions.
- Fine-grained targets: 50-200 files per BUILD target.
- Strict dependency declarations: `deps` must list all direct dependencies.

**Performance targets**:

- Full build from clean state: <5 minutes for 1M LOC monorepo.
- Incremental build (single file change): <30 seconds.
- Remote cache hit rate: >70%.
