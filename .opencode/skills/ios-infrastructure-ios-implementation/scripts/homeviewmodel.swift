@Observable
final class HomeViewModel {
    var items: [Item] = []
    var isLoading = false
    var errorMessage: String? = nil

    private let getItemsUseCase: GetItemsUseCaseProtocol

    init(getItemsUseCase: GetItemsUseCaseProtocol) {
        self.getItemsUseCase = getItemsUseCase
    }

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }
        do {
            items = try await getItemsUseCase.execute()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}