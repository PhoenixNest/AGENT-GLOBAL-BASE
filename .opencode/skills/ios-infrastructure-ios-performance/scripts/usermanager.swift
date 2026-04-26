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