// AppCoordinator.swift — Centralised navigation orchestration
final class AppCoordinator {
    private let navigationController: UINavigationController

    init(window: UIWindow) {
        navigationController = UINavigationController()
        window.rootViewController = navigationController
    }

    func start() {
        let rootVC = HomeViewController()
        rootVC.delegate = self
        navigationController.setViewControllers([rootVC], animated: false)
    }
}

extension AppCoordinator: HomeViewControllerDelegate {
    func didSelectProfile() {
        let profileVC = ProfileViewController()
        navigationController.pushViewController(profileVC, animated: true)
    }

    func didRequestSettings() {
        let settingsVC = SettingsViewController()
        let navVC = UINavigationController(rootViewController: settingsVC)
        navVC.modalPresentationStyle = .formSheet
        navigationController.present(navVC, animated: true)
    }
}