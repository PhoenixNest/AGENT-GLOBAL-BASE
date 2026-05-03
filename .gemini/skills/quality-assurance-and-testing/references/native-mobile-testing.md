---
name: native-mobile-testing
description: Write native mobile UI tests for Android (Compose UI Test, Espresso) and iOS (XCUITest) — covering critical user journeys, deep link navigation, and accessibility testing — as part of the Stage 7 automated test suite.
version: "1.0.0"
---

# Native Mobile Testing

| Competency            | Description                                                        | Quality Criteria                                                                                                          |
| --------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Compose UI Testing    | Write UI tests for Jetpack Compose screens using Compose Test APIs | Uses semantic nodes (not implementation details); tests work with any Compose layout change that doesn't change semantics |
| XCUITest              | Write XCUITest tests for SwiftUI and UIKit screens                 | Uses accessibility identifiers (not raw coordinates); tests run reliably on both simulator and physical device            |
| Deep Link Testing     | Verify deep link navigation to all app destinations                | Programmatic deep link triggering; verifies correct screen appears with expected state; tests all deep link parameters    |
| Accessibility Testing | Verify accessibility compliance in UI tests                        | Axe-mobile or built-in a11y scanner run as part of UI test suite; no missing content descriptions on interactive elements |

## Execution Guidance

### Compose UI Test Pattern

```kotlin
@get:Rule val composeTestRule = createAndroidComposeRule<MainActivity>()

@Test
fun productList_displaysProducts() {
    composeTestRule.apply {
        onNodeWithText("Product Name").assertIsDisplayed()
        onNodeWithContentDescription("Add to cart").performClick()
        onNodeWithText("Added to cart").assertIsDisplayed()
    }
}
```

### XCUITest Pattern

```swift
func testProductListDisplaysItem() {
    let app = XCUIApplication()
    app.launch()

    let productCell = app.cells["product-cell-1"]
    XCTAssertTrue(productCell.waitForExistence(timeout: 5))
    productCell.tap()

    let detailTitle = app.staticTexts["product-detail-title"]
    XCTAssertTrue(detailTitle.waitForExistence(timeout: 3))
}
```

Use `accessibilityIdentifier` to tag elements in production code for XCUITest targeting — never rely on raw coordinates or text strings that change with localization.
