// AppDelegate or SceneDelegate
func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
    guard let url = URLContexts.first?.url else { return }
    DeepLinkRouter.navigate(to: url, from: window?.rootViewController)
}

enum DeepLinkRouter {
    static func navigate(to url: URL, from rootVC: UIViewController?) {
        let path = url.pathComponents.dropFirst() // remove leading "/"
        guard let rootVC = rootVC else { return }

        switch path.first {
        case "product":
            guard let id = path.dropFirst().first else { return }
            navigateToProduct(id, from: rootVC)
        case "settings":
            navigateToSettings(from: rootVC)
        default:
            break
        }
    }

    private static func navigateToProduct(_ id: String, from rootVC: UIViewController) {
        if let tabVC = rootVC as? UITabBarController,
           let nav = tabVC.selectedViewController as? UINavigationController {
            let detailVC = ProductDetailViewController(productId: id)
            nav.pushViewController(detailVC, animated: true)
        }
    }
}