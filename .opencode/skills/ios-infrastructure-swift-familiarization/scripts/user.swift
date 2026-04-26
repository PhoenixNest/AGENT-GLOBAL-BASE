// Value types (structs) — preferred for data models
struct User {
    let id: UUID
    var name: String
    let email: String
}

// Reference types (classes) — for identity and shared state
class UserService {
    static let shared = UserService()
    private init() {}
    private var cache: [UUID: User] = [:]
}

// Optionals — Swift's null safety
let optionalValue: String? = nil
if let value = optionalValue {
    print(value)
}
let defaultValue = optionalValue ?? "default"