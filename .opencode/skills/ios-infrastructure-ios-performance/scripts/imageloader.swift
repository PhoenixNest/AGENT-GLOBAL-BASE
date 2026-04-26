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