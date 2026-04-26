# Performance Considerations

## Performance Considerations

### Storage Optimization

| Strategy                          | Impact                           | Implementation                            |
| --------------------------------- | -------------------------------- | ----------------------------------------- |
| Lossless PNG compression          | 40-60% size reduction            | `pngcrush`, `optipng`, `pngquant`         |
| Deduplicate identical screenshots | 10-30% storage savings           | Hash-based deduplication (SHA-256)        |
| Compress baselines on cloud       | 50-70% cost reduction            | S3 Intelligent-Tiering, GCS Nearline      |
| Prune old baselines               | Ongoing storage management       | Retain last 10 versions per screen/device |
| Differential storage              | 80-90% reduction vs. full images | Store only diffs + metadata               |

**Storage Estimation Formula:**

```
Total Storage = (Number of screens) x (Number of device configs)
              x (Average screenshot size) x (Number of versions retained)

Example:
  50 screens x 6 device configs x 500 KB x 10 versions = 1.5 GB

With deduplication (20% savings) + compression (50% savings):
  1.5 GB x 0.8 x 0.5 = 600 MB
```

### Diff Computation Time

| Factor                | Impact                            | Mitigation                                   |
| --------------------- | --------------------------------- | -------------------------------------------- |
| Number of screenshots | Linear scaling                    | Parallelize across workers                   |
| Image resolution      | Quadratic scaling (W x H)         | Downscale before comparison for initial pass |
| Comparison algorithm  | O(n) where n = pixel count        | Use SIMD-optimized libraries (odiff)         |
| Threshold calculation | Additional pass over diff regions | Pre-compute ignore regions                   |

**Performance Benchmarks (per 100 screenshot pairs):**

| Tool                     | Resolution | Time               | Method               |
| ------------------------ | ---------- | ------------------ | -------------------- |
| pixelmatch               | 1920x1080  | ~8 seconds         | CPU, single-threaded |
| pixelmatch (worker pool) | 1920x1080  | ~2 seconds         | CPU, 4 workers       |
| odiff                    | 1920x1080  | ~1 second          | Rust, SIMD           |
| resemble.js              | 1920x1080  | ~12 seconds        | CPU, JavaScript      |
| Applitools AI            | 1920x1080  | ~3 seconds (cloud) | Cloud GPU, AI model  |

### Baseline Management at Scale

| Challenge                       | Solution                        | Tool Support                                  |
| ------------------------------- | ------------------------------- | --------------------------------------------- |
| Baseline drift over time        | Periodic full baseline review   | Percy batch review, Applitools batch analysis |
| Branch-specific baselines       | Per-branch baseline isolation   | Percy branch testing, BackstopJS `--config`   |
| Merge conflict on binary images | Store baselines in LFS or cloud | Git LFS, Percy cloud storage                  |
| Baseline versioning             | Tag baselines with git SHA      | Automated tagging in CI                       |
| Cross-platform baseline sync    | Unified baseline manifest       | Custom manifest JSON                          |

---
