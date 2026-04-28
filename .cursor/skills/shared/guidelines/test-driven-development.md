---
name: test-driven-development
description: Practice Test-Driven Development (TDD) as a design and implementation discipline — writing tests before production code, following the Red-Green-Refactor cycle.
---

# Test-Driven Development

**Category:** Engineering Process
**Owner:** All Engineers

## Purpose

Practice Test-Driven Development (TDD) as a design and implementation discipline — writing tests before production code, following the Red-Green-Refactor cycle, and using test-first thinking to drive clean architecture. This skill covers the TDD workflow, test naming conventions, refactoring safely under test coverage, and when TDD is most valuable.

## Execution Guidance

### The Red-Green-Refactor Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   RED        →  Write a failing test                        │
│              →  Test compiles but fails                     │
│              →  Test defines expected behavior              │
│                                                             │
│   GREEN      →  Write minimum code to make test pass        │
│              →  No optimization, no extra features          │
│              →  Duplicate code is OK at this stage          │
│                                                             │
│   REFACTOR   →  Clean up code while tests stay green        │
│              →  Remove duplication, improve naming          │
│              →  Extract methods, introduce patterns          │
│              →  NEVER change behavior during refactor       │
│                                                             │
│   Repeat → Write next failing test                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### TDD Example — Order Total Calculator

**Step 1: RED — Write the failing test**

```swift
// OrderTotalCalculatorTests.swift
import XCTest
@testable import MyApp

final class OrderTotalCalculatorTests: XCTestCase {

    func test_emptyOrder_hasZeroTotal() {
        // GIVEN
        let calculator = OrderTotalCalculator()
        let order = Order(items: [])

        // WHEN
        let total = calculator.calculateTotal(for: order)

        // THEN
        XCTAssertEqual(total, 0.00, accuracy: 0.01, "Empty order should have zero total")
    }
}
```

**Step 2: GREEN — Write minimum code to pass**

```swift
// OrderTotalCalculator.swift
struct OrderTotalCalculator {
    func calculateTotal(for order: Order) -> Double {
        0.00
    }
}
```

**Step 3: RED — Next test**

```swift
func test_singleItem_returnsItemPrice() {
    // GIVEN
    let calculator = OrderTotalCalculator()
    let item = OrderItem(name: "Headphones", price: 99.99, quantity: 1)
    let order = Order(items: [item])

    // WHEN
    let total = calculator.calculateTotal(for: order)

    // THEN
    XCTAssertEqual(total, 99.99, accuracy: 0.01)
}
```

**Step 4: GREEN — Implement the logic**

```swift
struct OrderTotalCalculator {
    func calculateTotal(for order: Order) -> Double {
        order.items.reduce(0) { $0 + ($1.price * Double($1.quantity)) }
    }
}
```

**Step 5: REFACTOR — Extract and improve (tests stay green)**

```swift
struct OrderTotalCalculator {
    func calculateTotal(for order: Order) -> Double {
        order.items
            .map { lineItemTotal(for: $0) }
            .reduce(0, +)
    }

    private func lineItemTotal(for item: OrderItem) -> Double {
        item.price * Double(item.quantity)
    }
}

// All tests still pass — behavior unchanged, structure improved
```

### TDD Test Naming Convention

```
test_{scenario}_{expectedOutcome}

Examples:
test_emptyOrder_hasZeroTotal
test_singleItem_returnsItemPrice
test_multipleItems_sumsCorrectly
test_discountApplied_reducesTotal
test_discountExceedsTotal_capsAtZero
test_invalidCurrency_throwsError
test_quantityZero_excludesItem
```

### TDD for Mobile ViewModels

```kotlin
// Test-first approach for Android ViewModel
class ProductDetailViewModelTest {

    @Test
    fun `add to cart with valid product triggers success`() = runTest {
        // RED: Write test for add-to-cart behavior
        val repository = MockProductRepository()
        repository.productResult = Product("1", "Headphones", 99.99, true)

        val viewModel = ProductDetailViewModel(repository)
        viewModel.loadProduct("1")
        testDispatcher.scheduler.advanceUntilIdle()

        var successCalled = false
        viewModel.onAddToCartSuccess = { successCalled = true }

        viewModel.addToCart()

        assertTrue(successCalled)
        assertEquals(1, repository.addToCartCalls)
    }
}

// GREEN: Implement minimum
class ProductDetailViewModel(
    private val repository: ProductRepository
) : ViewModel() {

    var onAddToCartSuccess: (() -> Unit)? = null
    private var product: Product? = null

    fun loadProduct(id: String) {
        viewModelScope.launch {
            product = repository.getProduct(id)
        }
    }

    fun addToCart() {
        val p = product ?: return
        repository.addToCart(p)
        onAddToCartSuccess?.invoke()
    }
}

// REFACTOR: Add error handling, loading states
```

### When TDD Is Most Valuable

| Scenario                 | TDD Value | Reason                                     |
| ------------------------ | --------- | ------------------------------------------ |
| Complex business logic   | ✅ HIGH   | Tests define requirements before code      |
| Algorithm implementation | ✅ HIGH   | Edge cases discovered through test writing |
| API integration layer    | ✅ HIGH   | Contract testing with mocks                |
| Data transformation      | ✅ HIGH   | Input/output pairs are clear test cases    |
| Simple CRUD operations   | ⚠️ MEDIUM | Tests are straightforward but low value    |
| UI layout code           | ⚠️ LOW    | Visual testing is more appropriate         |
| One-off scripts          | ⚠️ LOW    | Overkill for throwaway code                |
| Bug fixes                | ✅ HIGH   | Write reproducing test first, then fix     |

### Bug Fix Workflow with TDD

```
1. User reports bug
2. Write a test that reproduces the bug (RED — test fails)
3. Fix the bug (GREEN — test passes)
4. Refactor if needed (tests stay green)
5. Add the test to regression suite (Stage 7)
```

### Common TDD Mistakes

| Mistake                      | Symptom                          | Correction                             |
| ---------------------------- | -------------------------------- | -------------------------------------- |
| Writing too big a test       | Hard to make pass in one step    | Write smaller, more focused tests      |
| Skipping refactor step       | Code quality degrades over time  | Always refactor after green            |
| Testing implementation       | Tests break on internal changes  | Test behavior, not implementation      |
| Mocking everything           | Tests verify mocks, not behavior | Mock only external boundaries          |
| Not running tests frequently | Long feedback loop               | Run tests after every change           |
| Writing all tests upfront    | Tests become speculative         | One test at a time, red-green-refactor |

## Pipeline Integration

**Stage 5 (Development):** Platform leads practice TDD for business logic and data layers. Bug fixes start with reproducing tests.

**Stage 7 (Testing):** All TDD-written tests become part of the automated regression suite. Test quality reviewed for completeness.

**Stage 8 (Integrity Verification):** Regression test suite includes all TDD tests from bug fixes. Verified that fixed bugs do not reoccur.

## Quality Standards

| Metric                   | Target                             | Measurement              |
| ------------------------ | ---------------------------------- | ------------------------ |
| Test-first ratio         | > 60% tests written before code    | Commit history analysis  |
| Red-Green-Refactor cycle | Average cycle < 10 minutes         | Developer self-reporting |
| Refactor safety          | 0 behavior changes during refactor | Test suite stays green   |
| Bug regression coverage  | 100% bugs have reproducing test    | Defect tracking          |
| Test naming compliance   | 100% follow naming convention      | Code review              |

## Reference Materials

- [Test-Driven Development by Example (Kent Beck)](https://www.oreilly.com/library/view/test-driven-development/0321146530/)
- [Growing Object-Oriented Software, Guided by Tests](https://www.growing-object-oriented-software.com/)
- [TDD in Swift (objc.io)](https://www.objc.io/books/test-driven-development/)
- [The Three Laws of TDD (Uncle Bob)](https://cleancoders.com/episode/the-three-laws-of-tdd)
- `mobile-unit-testing.md` — Mobile unit testing skill
- `code-review-participation.md` — Code review process
