---
name: ios-infrastructure-ios-performance
description: "iOS performance optimization — Instruments profiling (Time Profiler, Allocations, Leaks), memory management, launch time optimization, three-tier image caching, rendering pipeline tuning, and table view performance. Owned by Seo-Yeon Park (iOS Lead). Use during Stage 5 (Development) for performance-critical code and Stage 8 (Integrity Verification) for launch time and memory benchmarks. Trigger: ios performance, instruments, time profiler, allocations, leaks, launch time, memory leak, nscache, image caching, offscreen rendering, scroll performance, signpost."
prerequisites:
  - ios-infrastructure-ios-implementation

version: "1.0.0"
---

# iOS Performance

**Category:** Mobile Engineering — iOS Performance Optimization
**Owner:** Senior iOS Engineer (Mei Chen)

## Overview

This skill implements comprehensive iOS performance optimization covering Instruments profiling, memory management, launch time optimization, image caching strategies, and rendering pipeline tuning. It applies to Stage 5 (Development) where performance is built in from the start, Stage 6 (Code Review) where performance regressions are caught, and Stage 8 (Integrity Verification) where launch time, memory footprint, and frame rate are measured against targets.

## Competency Dimensions

| Dimension                    | Description                                                                                               | Proficiency Indicators                                                                                                                    |
| ---------------------------- | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Instruments Profiling        | Time Profiler, Allocations, Leaks, VM Tracker, Energy Log, System Trace                                   | Identifies performance bottlenecks within 2 profiling sessions; interprets call tree correctly; uses signposts for custom instrumentation |
| Memory Management            | ARC optimization, retain cycle detection, weak/unowned references, memory warnings, purgeable data        | Zero memory leaks in Allocations instrument; memory warning handling implemented; large objects use `NSPurgeableData`                     |
| Launch Time Optimization     | App launch phases, dylib loading, main thread work minimization, pre-main optimization, metric collection | Cold launch <2 seconds; main thread work during launch <100ms; deferred initialization for non-critical services                          |
| Image Caching & Optimization | Image decompression, downscaling, caching layers, progressive loading, HEIF/WEBP support                  | Images loaded at display size (no GPU scaling); decompression on background thread; LRU cache with memory/disk limits                     |
| Rendering Performance        | Offscreen rendering elimination, layer rasterization, table view cell optimization, Core Text performance | Scroll performance at 60fps; cell reuse efficient; no synchronous image decoding on main thread                                           |

## Execution Guidance

### Instruments — Production Profiling Workflow

**Signpost instrumentation for custom measurements:**

```swift
import os

private let performanceLogger = Logger(subsystem: Bundle.main.bundleIdentifier!, category: "performance")

// MARK: - Signpost Points
func measureDataLoading(_ operation: @autoclosure () throws -> Void) rethrows {
    let signposter = OSSignposter(subsystem: Bundle.main.bundleIdentifier!, category: "data_loading")
    let state = signposter.makeSignpostID()

    signposter.emitEvent("Start loading", signpostID: state)
    defer {
        signposter.emitEvent("Finished loading", signpostID: state)
    }
    try operation()
}

// Usage
measureDataLoading {
    let users = try await userRepository.fetchUsers()
    await MainActor.run {
        self.users = users
    }
}
```

**Time Profiler workflow:**

1. Open Instruments → Time Profiler
2. Select target app and click Record
3. Exercise the feature being profiled
4. Stop recording and switch to "Call Tree" view
5. Check "Invert Call Tree" and "Hide System Libraries"
6. Identify top self-weight functions — these are optimization targets

**Allocations workflow for memory profiling:**

1. Open Instruments → Allocations
2. Enable "Record Reference Counts"
3. Record while exercising the feature
4. Use "Mark Generation" to snapshot memory at key points
5. Compare generations to identify memory growth
6. Filter by allocation size to find largest objects

### Memory Management — Production Discipline

**Retain cycle detection and prevention:**

```swift
// CORRECT: Weak reference to prevent retain cycle
class UserManager {
    var onUserUpdated: ((User) -> Void)?

    func setup() {
        // Closure captures `self` — use weak to prevent cycle
        onUserUpdated = { [weak self] user in
            self?.handleUserUpdate(user)
        }
    }

    private func handleUserUpdate(_ user: User) {
        // Handle update
    }
}

// WRONG: Strong capture creates retain cycle
class UserManager {
    var onUserUpdated: ((User) -> Void)?

    func setup() {
        onUserUpdated = { user in  // Strong capture of `self`
            self.handleUserUpdate(user)  // Retain cycle!
        }
    }
}

// Delegate pattern — always weak
protocol UserManagerDelegate: AnyObject {
    func userManager(_ manager: UserManager, didUpdateUser user: User)
}

class UserManager {
    weak var delegate: UserManagerDelegate?  // Weak — delegate owns manager
}
```

**Memory warning handling:**

```swift
@MainActor
class ImageCache {
    static let shared = ImageCache()

    private var cache: NSCache<NSString, UIImage> = {
        let cache = NSCache<NSString, UIImage>()
        cache.countLimit = 100  // Max 100 images
        cache.totalCostLimit = 100 * 1024 * 1024  // 100MB
        return cache
    }()

    init() {
        // NSCache automatically purges on memory warning
        // But we can also respond explicitly
        NotificationCenter.default.addObserver(
            forName: UIApplication.didReceiveMemoryWarningNotification,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            self?.cache.removeAllObjects()
            print("ImageCache: cleared on memory warning")
        }
    }

    func image(forKey key: String) -> UIImage? {
        cache.object(forKey: key as NSString)
    }

    func setImage(_ image: UIImage, forKey key: String) {
        // Cost is approximate bytes in memory
        let cost = image.size.width * image.size.height * 4
        cache.setObject(image, forKey: key as NSString, cost: Int(cost))
    }
}
```

**NSPurgeableData for large temporary data:**

```swift
func processLargeFile(url: URL) async throws {
    // Use purgeable data — OS can reclaim if memory pressure
    let data = try NSPurgeableData(contentsOf: url)
    data.beginContentAccess()
    defer { data.endContentAccess() }

    // Process data — if memory pressure occurs, OS can purge
    let result = try await processData(data)
    return result
}
```

### Launch Time Optimization

**App launch phases:**

```
1. dylib loading     ← System loads frameworks (not much you can do)
2. rebase/binding    ← Fixing up pointers (not much you can do)
3. ObjC setup        ← +load methods, class registration (can optimize)
4. main()            ← Your code starts here (can optimize significantly)
```

**Pre-main optimization:**

```swift
// AVOID: +load methods — they run during pre-main and block launch
// Use +initialize or explicit registration instead

// AVOID: Many small dynamic frameworks — each adds dylib loading time
// Combine related code into fewer frameworks

// MEASURE: Environment variable to track pre-main time
// Edit Scheme → Run → Arguments → Add:
// DYLD_PRINT_STATISTICS=YES
```

**Post-main optimization — defer non-critical work:**

```swift
@main
class AppDelegate: UIResponder, UIApplicationDelegate {

    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {

        // CRITICAL: Only essential setup on main thread
        setupCoreServices()
        configureAppearance()
        setupRootViewController()

        // DEFERRED: Non-critical work after first render
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
            self.setupAnalytics()
            self.setupPushNotifications()
            self.precacheInitialData()
        }

        // DEFERRED: Heavy initialization on background thread
        DispatchQueue.global(qos: .utility).async {
            self.setupDatabase()
            self.warmupImageCache()
        }

        return true
    }

    private func setupCoreServices() {
        // Only services needed for first screen
        DependencyContainer.registerCoreServices()
    }

    private func configureAppearance() {
        // Global UI appearance — lightweight
        UINavigationBar.appearance().tintColor = .systemBlue
    }

    private func setupRootViewController() {
        // Must be fast — this is what user sees
        window = UIWindow(frame: UIScreen.main.bounds)
        window?.rootViewController = RootViewController()
        window?.makeKeyAndVisible()
    }
}
```

**Launch time measurement:**

```swift
// Measure time from app launch to first frame rendered
private var launchStartTime: TimeInterval = 0

func application(
    _ application: UIApplication,
    willFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
) -> Bool {
    launchStartTime = CACurrentMediaTime()
    return true
}

func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
) -> Bool {
    // ... setup ...

    let launchDuration = CACurrentMediaTime() - launchStartTime
    print("Launch time: \(String(format: "%.3f", launchDuration))s")

    // Report to analytics
    Analytics.track("app_launch_time", value: launchDuration)

    return true
}
```

### Image Caching & Optimization

**Three-tier caching strategy:**

```swift
final class ImageLoader {
    static let shared = ImageLoader()

    // L1: Memory cache (fastest, limited)
    private let memoryCache = NSCache<NSString, UIImage>()

    // L2: Disk cache (fast, larger)
    private let diskCachePath: URL

    // L3: Network (slowest, unlimited)
    private let urlSession: URLSession

    private init() {
        memoryCache.countLimit = 200
        memoryCache.totalCostLimit = 200 * 1024 * 1024  // 200MB

        let cachesDir = FileManager.default.urls(for: .cachesDirectory, in: .userDomainMask)[0]
        diskCachePath = cachesDir.appendingPathComponent("image_cache")

        try? FileManager.default.createDirectory(at: diskCachePath, withIntermediateDirectories: true)

        let config = URLSessionConfiguration.default
        config.urlCache = URLCache(
            memoryCapacity: 50 * 1024 * 1024,
            diskCapacity: 200 * 1024 * 1024
        )
        urlSession = URLSession(configuration: config)
    }

    func loadImage(url: URL) async throws -> UIImage {
        let key = url.absoluteString as NSString

        // L1: Memory cache
        if let cachedImage = memoryCache.object(forKey: key) {
            return cachedImage
        }

        // L2: Disk cache
        if let diskImage = loadFromDisk(url: url) {
            memoryCache.setObject(diskImage, forKey: key)
            return diskImage
        }

        // L3: Network
        let (data, _) = try await urlSession.data(from: url)

        // Decode on background thread
        let image = try await Task.detached(priority: .userInitiated) {
            guard let image = UIImage(data: data) else {
                throw ImageError.decodingFailed
            }
            return image
        }.value

        // Store in caches
        memoryCache.setObject(image, forKey: key)
        saveToDisk(data: data, url: url)

        return image
    }

    private func loadFromDisk(url: URL) -> UIImage? {
        let fileURL = diskCachePath.appendingPathComponent(url.lastPathComponent)
        guard let data = try? Data(contentsOf: fileURL) else { return nil }
        return UIImage(data: data)
    }

    private func saveToDisk(data: Data, url: URL) {
        let fileURL = diskCachePath.appendingPathComponent(url.lastPathComponent)
        try? data.write(to: fileURL, options: .atomic)
    }
}

enum ImageError: Error {
    case decodingFailed
}
```

**Image downscaling to display size:**

```swift
extension UIImage {
    /// Resize image to fit target size — prevents GPU over-scaling
    func resized(to targetSize: CGSize) -> UIImage? {
        let renderer = UIGraphicsImageRenderer(size: targetSize)
        return renderer.image { _ in
            self.draw(in: CGRect(origin: .zero, size: targetSize))
        }
    }

    /// Calculate optimal size for display — maintains aspect ratio
    func optimalSize(for bounds: CGSize, contentMode: UIView.ContentMode) -> CGSize {
        let widthRatio = bounds.width / size.width
        let heightRatio = bounds.height / size.height

        switch contentMode {
        case .scaleAspectFit:
            let ratio = min(widthRatio, heightRatio)
            return CGSize(width: size.width * ratio, height: size.height * ratio)
        case .scaleAspectFill:
            let ratio = max(widthRatio, heightRatio)
            return CGSize(width: size.width * ratio, height: size.height * ratio)
        default:
            return bounds
        }
    }
}

// Usage in cell
func configure(with imageURL: URL, bounds: CGSize) {
    let targetSize = CGSize(width: bounds.width * UIScreen.main.scale,
                           height: bounds.height * UIScreen.main.scale)

    Task {
        let image = try await ImageLoader.shared.loadImage(url: imageURL)
        let resized = image.resized(to: targetSize)
        await MainActor.run {
            self.imageView.image = resized
        }
    }
}
```

### Table View Performance

```swift
class OptimizedTableViewController: UITableViewController {

    // Prefetching — load data before cell appears
    override func tableView(_ tableView: UITableView, prefetchRowsAt indexPaths: [IndexPath]) {
        for indexPath in indexPaths {
            let url = items[indexPath.row].imageURL
            Task {
                _ = try? await ImageLoader.shared.loadImage(url: url)
            }
        }
    }

    // Cancel prefetching when no longer needed
    override func tableView(_ tableView: UITableView, cancelPrefetchingForRowsAt indexPaths: [IndexPath]) {
        // ImageLoader handles this via NSCache — no explicit cancellation needed
    }

    // Cell configuration — minimal work on main thread
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "ItemCell", for: indexPath) as! ItemCell
        let item = items[indexPath.row]

        cell.titleLabel.text = item.title
        cell.subtitleLabel.text = item.subtitle

        // Set placeholder immediately
        cell.imageView.image = placeholderImage

        // Load image asynchronously
        if let url = item.imageURL {
            Task { @MainActor in
                do {
                    let image = try await ImageLoader.shared.loadImage(url: url)
                    // Check cell is still visible for this item
                    if let visibleIndexPath = tableView.indexPath(for: cell),
                       visibleIndexPath == indexPath {
                        cell.imageView.image = image
                    }
                } catch {
                    // Keep placeholder
                }
            }
        }

        return cell
    }
}
```

### Performance Budget

| Metric                    | Target                   | Measurement                       |
| ------------------------- | ------------------------ | --------------------------------- |
| Cold Launch Time          | <2 seconds               | Xcode Metrics / custom signposts  |
| Hot Launch Time           | <1 second                | Xcode Metrics                     |
| Main Thread Work (Launch) | <100ms                   | Time Profiler                     |
| Frame Rate                | 60fps (120fps ProMotion) | Core Animation instrument         |
| Memory Footprint          | <300MB typical           | Allocations instrument            |
| Memory Warnings           | 0 in normal usage        | OS memory pressure events         |
| Image Memory Cache        | <200MB                   | NSCache cost tracking             |
| Disk Cache Size           | <500MB                   | Periodic cleanup                  |
| Scroll Jank               | 0 dropped frames         | Core Animation — Color Misaligned |

## Pipeline Integration

- **Stage 5 (Development):** Performance optimization built in from the start. Launch time, memory management, and image caching implemented alongside features.
- **Stage 6 (Code Review):** Performance review: Instruments profiling results, memory leak audit, launch time measurement, image caching strategy.
- **Stage 7 (Automated Testing):** Performance regression tests — launch time and memory footprint tracked across builds.
- **Stage 8 (Integrity Verification):** Launch time measured on target devices. Memory profiling confirms no leaks. Frame rate verified at 60fps during scroll-heavy interactions.

## Quality Standards

- Cold launch time **<2 seconds** on iPhone SE (2nd gen) — baseline device
- Hot launch time **<1 second** on all supported devices
- Main thread work during launch **<100ms** — all non-critical work deferred
- **Zero** memory leaks in Allocations instrument (clean Leaks instrument run required)
- Memory footprint **<300MB** during typical usage
- Image loading always at **display size** — no GPU scaling of oversized images
- Image decompression on **background thread** — never on main thread
- Table/Collection view scroll at **60fps** — prefetching enabled for data loading
- NSCache used for memory caching with **explicit size limits**
- Disk cache periodically cleaned up — **<500MB** maximum
- All large object allocations use **purgeable data** where appropriate
- Performance signposts instrumented for all critical code paths
