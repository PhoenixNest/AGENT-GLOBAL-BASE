---
name: unit-test-architecture
description: Design the unit test architecture for Android and iOS mobile code — defining testing layers, mock strategies, coroutine test utilities, and coverage thresholds — ensuring Stage 7 automated testing achieves ≥80% line coverage on business logic layers.
version: "1.0.0"
---

# Unit Test Architecture

| Competency           | Description                                                                         | Quality Criteria                                                                                                                   |
| -------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Test Layering        | Define which layers are unit-tested vs. integration-tested                          | Domain and use case layers: 100% unit test coverage target; Repository layer: integration tests against real DB; UI: snapshot only |
| Android Mocking      | Use MockK and Turbine for ViewModel and repository unit tests                       | MockK for all dependencies; Turbine for Flow/StateFlow assertions; no real network calls in unit tests                             |
| Coroutine Testing    | Test suspend functions and coroutines with `runTest` and `UnconfinedTestDispatcher` | All async code testable without real delays; `StandardTestDispatcher` for controlled virtual time                                  |
| Coverage Enforcement | Enforce coverage thresholds in CI with JaCoCo (Android) and Xcode coverage          | CI fails if business logic layer drops below 80% line coverage; coverage report published to PR comments                           |

## Execution Guidance

### Android ViewModel Test Pattern

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class ProductListViewModelTest {
    @get:Rule val mainDispatcherRule = MainDispatcherRule()

    private val repository = mockk<ProductRepository>()
    private val viewModel by lazy { ProductListViewModel(repository) }

    @Test
    fun `loading products emits success state`() = runTest {
        coEvery { repository.getProducts() } returns listOf(Product("1", "Test"))

        viewModel.uiState.test {
            viewModel.loadProducts()
            assertIs<UiState.Loading>(awaitItem())
            assertIs<UiState.Success>(awaitItem())
        }
    }
}
```

### Coverage Layer Targets

| Layer         | Coverage Target | Tool              |
| ------------- | --------------- | ----------------- |
| Domain models | 100%            | Unit tests        |
| Use cases     | ≥ 90%           | Unit tests        |
| ViewModels    | ≥ 80%           | Unit tests        |
| Repositories  | ≥ 70%           | Integration tests |
| UI components | Snapshot only   | Snapshot tests    |
