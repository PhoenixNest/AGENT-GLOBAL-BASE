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