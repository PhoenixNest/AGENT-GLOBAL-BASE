---
name: testing-qa-mobile-appium-detox
description: Appium and Detox cross-platform test automation — WebDriver protocol, React Native testing, hybrid app automation, device cloud integration, and cross-platform E2E test framework design for mobile applications. Owned by Rachel Kim (Test Automation Lead). Use during Stage 5 (Development) for test framework selection and Stage 7 (Testing) for cross-platform E2E test execution. Trigger: Appium, Detox, cross-platform testing, WebDriver, React Native testing, hybrid app automation, device cloud, E2E framework.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
---

# Appium 2.0 & Detox — Cross-Platform E2E Test Automation

**Category:** Mobile Test Automation — Cross-Platform Frameworks
**Owner:** SDET Mobile #2 (Tobias Weber)

## Overview

This skill covers Appium 2.0's driver/plugin architecture for universal mobile test automation and Detox's gray-box synchronization approach for React Native applications. Appium 2.0 provides a standardized WebDriver protocol interface across Android, iOS, and emerging platforms, while Detox offers deterministic React Native testing through direct synchronization with the JS thread and native modules.

Together, these frameworks address the full cross-platform testing spectrum: Appium for native, hybrid, and web-view applications across device matrices, and Detox for React Native apps where white-box synchronization eliminates the flaky timing issues inherent in black-box approaches.

## Competency Dimensions

| Dimension                            | Description                                                                                                                                                                                                          | Proficiency Indicators                                                                                                                                                                                                                                                                                       |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Appium 2.0 Architecture**          | Server/driver/plugin separation, `appium` CLI, driver installation (`uiautomator2`, `xcuitest`), plugin ecosystem (`device-farm`, `relaxed-caps`, `images`), session capabilities, W3C WebDriver protocol compliance | Drivers installed via `appium driver install`; plugins configured in `appium server --use-plugins`; desired capabilities follow W3C `alwaysMatch/firstMatch` format; session management handles concurrent connections; server logs analyzed for driver-level errors                                         |
| **Appium Driver Ecosystem**          | UiAutomator2 driver (Android), XCUITest driver (iOS), Espresso driver (Android alternative), Safari driver (iOS web), Chrome driver (Android web), Mac2 driver (macOS desktop)                                       | Correct driver selected per platform: `uiautomator2` for Android native, `xcuitest` for iOS native; Espresso driver used when app-under-test uses Espresso for internal testing; web-view contexts switched via `driver.setContext()`; hybrid app tests use `driver.getContexts()` to enumerate web views    |
| **Appium Plugin Configuration**      | `relaxed-caps` for simplified capability handling, `images` for image-based element location, `device-farm` for multi-device orchestration, `execute-driver` for custom command injection                            | Plugins loaded via `appium server --use-plugins=images,relaxed-caps`; image-based location used as fallback when accessibility IDs unavailable; relaxed-caps eliminates `appium:` prefix requirement for standard caps; custom plugins extend command set via `driver.execute('custom:command', args)`       |
| **Detox Gray-Box Testing**           | Direct app compilation with Detox framework, synchronization with JS thread, native module mocking, `detox build` / `detox test` workflow, Jest integration, device/launcher configuration                           | App compiled with `detox build --configuration ios.sim.debug`; tests use `await element(by.id('id')).tap()`; synchronization automatic — no explicit waits; mock native modules via `device.setURLBlacklist()` for network stubbing; Jest runner configured with `detox-circus` environment                  |
| **Detox Synchronization Strategies** | Idle state detection, network request tracking, animation synchronization, custom synchronization via `detoxSync`, handling long-running operations, background app simulation                                       | Detox waits for both JS runloop and main runloop to idle; `device.setURLBlacklist()` excludes polling endpoints from sync tracking; `detox.resetBefore()` between tests; custom sync barriers via `await device.synchronize()`; background simulation via `device.sendToHome()` / `await device.launchApp()` |
| **React Native Test Patterns**       | Component ID propagation (`testID` prop), scrollable list testing, modal/dialog handling, push notification simulation, deep link testing, biometric authentication testing                                          | Every interactive RN component has `testID` matching accessibility ID; long lists use `await element(by.type('RCTScrollView')).atIndex(0).swipe('up')`; modals tested via `await element(by.label('modalTitle')).atIndex(0).tap()`; deep links via `device.launchApp({url: 'myapp://path'})`                 |
| **E2E Test Flakiness Prevention**    | Deterministic waits, test isolation, state reset, network mocking, timing-independent assertions, quarantine mode for intermittent failures, retry analysis                                                          | Zero `sleep()` calls; `detox.resetBefore()` clears state; network stubs via `mock-server` or `msw`; flaky tests identified via `jest-circus` retry stats; quarantined tests tagged with `@flaky`; root-cause analysis distinguishes app race conditions from test timing issues                              |

## Execution Guidance

### Appium 2.0 — Core Patterns

**1. Server Setup & Driver Installation**

```bash
# Install Appium 2.0
npm install -g appium

# Install drivers
appium driver install uiautomator2   # Android
appium driver install xcuitest        # iOS

# Install plugins
appium plugin install images
appium plugin install relaxed-caps
appium plugin install device-farm

# Start server with plugins
appium --use-plugins=images,relaxed-caps,device-farm
```

**2. Android Test (Python — WebDriverIO equivalent patterns)**

```python
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "14"
    options.device_name = "Pixel 6"
    options.app = "/path/to/app-debug.apk"
    options.automation_name = "uiautomator2"
    options.no_reset = False
    options.full_reset = True
    options.new_command_timeout = 120

    # Relaxed caps plugin allows omitting 'appium:' prefix
    driver = webdriver.Remote(
        "http://localhost:4723",
        options=options
    )
    yield driver
    driver.quit()

def test_login_flow(driver):
    # Wait for element (explicit wait pattern)
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    wait = WebDriverWait(driver, 15)
    email_field = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "emailField"))
    )
    email_field.send_keys("test@company.com")

    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "passwordField").send_keys("SecurePass123!")
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "loginButton").click()

    # Verify navigation
    home_title = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "homeScreenTitle"))
    )
    assert "Welcome" in home_title.text
```

**3. iOS Test (JavaScript — WebDriverIO)**

```javascript
const wdio = require("webdriverio");

const opts = {
  port: 4723,
  capabilities: {
    platformName: "iOS",
    platformVersion: "17.0",
    deviceName: "iPhone 15",
    app: "/path/to/MyApp.app",
    automationName: "XCUITest",
    noReset: false,
    fullReset: true,
    newCommandTimeout: 120,
    wdaLaunchTimeout: 120000,
  },
};

async function runTest() {
  const driver = await wdio.remote(opts);

  try {
    // Login flow
    const emailField = await driver.$("~emailField");
    await emailField.setValue("test@company.com");

    const passwordField = await driver.$("~passwordField");
    await passwordField.setValue("SecurePass123!");

    const loginButton = await driver.$("~loginButton");
    await loginButton.click();

    // Wait for home screen
    const homeTitle = await driver.$("~homeScreenTitle");
    await homeTitle.waitForExist({ timeout: 15000 });
    const text = await homeTitle.getText();
    console.assert(
      text.includes("Welcome"),
      `Expected welcome message, got: ${text}`,
    );

    // Scroll test
    const productList = await driver.$("~productList");
    await productList.swipeUp();

    // Verify last item visible
    const lastItem = await driver.$("~product-item-99");
    await lastItem.waitForDisplayed({ timeout: 5000 });
  } finally {
    await driver.deleteSession();
  }
}

runTest();
```

**4. Hybrid App — WebView Context Switching**

```python
def test_hybrid_app_checkout(driver):
    # Start in native context
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "checkoutButton").click()

    # Switch to WebView context
    contexts = driver.contexts
    # contexts = ['NATIVE_APP', 'WEBVIEW_com.company.app']
    webview_context = [c for c in contexts if 'WEBVIEW' in c][0]
    driver.switch_to.context(webview_context)

    # Now interact with web elements
    from selenium.webdriver.common.by import By
    card_input = driver.find_element(By.CSS_SELECTOR, "#cardNumber")
    card_input.send_keys("4111111111111111")

    driver.find_element(By.CSS_SELECTOR, "#payButton").click()

    # Switch back to native for confirmation
    driver.switch_to.context('NATIVE_APP')
    confirmation = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "orderConfirmation")
    assert confirmation.is_displayed()
```

**5. Image-Based Element Location (Images Plugin)**

```python
# When accessibility ID is unavailable (third-party SDK, legacy screen)
def test_legacy_screen_interaction(driver):
    # Use template image to locate button
    driver.find_element(
        AppiumBy.IMAGE,
        "/path/to/templates/checkout_button.png"
    ).click()

    # Verify with image template
    confirmation_img = driver.find_element(
        AppiumBy.IMAGE,
        "/path/to/templates/order_confirmed.png"
    )
    assert confirmation_img.is_displayed()
```

### Detox — Core Patterns

**1. Configuration (`detox.config.js`)**

```javascript
module.exports = {
  testRunner: {
    args: {
      $0: "jest",
      config: "e2e/jest.config.js",
    },
    jest: {
      setupTimeout: 300000, // 5 min for build + launch
    },
  },
  apps: {
    "ios.debug": {
      type: "ios.app",
      binaryPath: "ios/build/Build/Products/Debug-iphonesimulator/MyApp.app",
      build:
        "xcodebuild -workspace ios/MyApp.xcworkspace -scheme MyApp -configuration Debug -sdk iphonesimulator -derivedDataPath ios/build",
    },
    "android.debug": {
      type: "android.apk",
      binaryPath: "android/app/build/outputs/apk/debug/app-debug.apk",
      build:
        "cd android && ./gradlew assembleDebug assembleAndroidTest -DtestBuildType=debug && cd ..",
    },
  },
  devices: {
    simulator: {
      type: "ios.simulator",
      device: {
        type: "iPhone 15",
      },
    },
    emulator: {
      type: "android.emulator",
      device: {
        avdName: "Pixel_6_API_34",
      },
    },
  },
  configurations: {
    "ios.sim.debug": {
      device: "simulator",
      app: "ios.debug",
    },
    "android.emu.debug": {
      device: "emulator",
      app: "android.debug",
    },
  },
};
```

**2. Jest Configuration (`e2e/jest.config.js`)**

```javascript
module.exports = {
  rootDir: "..",
  testMatch: ["<rootDir>/e2e/**/*.test.js"],
  testTimeout: 120000,
  maxWorkers: 1,
  globalSetup: "detox/runners/jest/globalSetup",
  globalTeardown: "detox/runners/jest/globalTeardown",
  reporters: ["detox/runners/jest/reporter"],
  testEnvironment: "detox/runners/jest/testEnvironment",
  verbose: true,
  setupFilesAfterEnv: ["<rootDir>/e2e/init.js"],
};
```

**3. Test Initialization (`e2e/init.js`)**

```javascript
const detox = require("detox");
const adapter = require("detox/runners/jest/adapter");

jest.setTimeout(300000);

beforeAll(async () => {
  await detox.init();
  await device.launchApp({
    permissions: { notifications: "YES", camera: "YES", photos: "YES" },
    launchArgs: { uiTestingMode: true },
  });
});

beforeEach(async () => {
  await adapter.beforeEach();
});

afterAll(async () => {
  await adapter.afterAll();
  await detox.cleanup();
});
```

**4. Standard Test Suite**

```javascript
describe("Checkout Flow", () => {
  beforeEach(async () => {
    await device.reloadReactNative();
    await loginAsTestUser();
  });

  it("should complete purchase with valid card", async () => {
    // Navigate to checkout
    await element(by.id("cartButton")).tap();
    await element(by.id("checkoutButton")).tap();

    // Fill payment form
    await element(by.id("cardNumberInput")).typeText("4111111111111111");
    await element(by.id("expiryInput")).typeText("1228");
    await element(by.id("cvvInput")).typeText("123");

    // Submit
    await element(by.id("payButton")).tap();

    // Verify confirmation (Detox auto-waits — no explicit wait needed)
    await expect(element(by.id("orderConfirmation"))).toBeVisible();
    await expect(element(by.text("Order confirmed"))).toBeVisible();
  });

  it("should show error for expired card", async () => {
    await element(by.id("cartButton")).tap();
    await element(by.id("checkoutButton")).tap();

    await element(by.id("cardNumberInput")).typeText("4000000000000002");
    await element(by.id("payButton")).tap();

    await expect(element(by.id("errorBanner"))).toBeVisible();
    await expect(element(by.text("Card expired"))).toBeVisible();
  });
});

async function loginAsTestUser() {
  await element(by.id("emailField")).typeText("test@company.com");
  await element(by.id("passwordField")).typeText("SecurePass123!");
  await element(by.id("loginButton")).tap();
  await expect(element(by.id("homeScreenTitle"))).toBeVisible();
}
```

**5. Network Stubbing for Deterministic Tests**

```javascript
// Mock server setup (using MSW or custom mock)
beforeAll(async () => {
  // Blacklist real API endpoints — Detox will wait for these to settle
  await device.setURLBlacklist([
    ".*api\\.company\\.com.*",
    ".*analytics\\.company\\.com.*",
  ]);
});

// Using mock-server in the app's debug build
// App detects UI_TESTING_MODE and routes to mock endpoints
beforeEach(async () => {
  await device.launchApp({
    launchArgs: {
      uiTestingMode: true,
      mockApiBaseUrl: "http://localhost:8080",
    },
    newInstance: true,
  });

  // Configure mock responses
  await mockServer.post("/api/v1/orders", {
    status: 201,
    body: { orderId: "ORD-12345", status: "confirmed" },
  });
});
```

**6. Scrollable List Testing**

```javascript
it("should scroll to find specific item", async () => {
  const scrollView = element(by.type("RCTScrollView"));

  // Swipe up until target element is visible
  await waitFor(element(by.id("product-item-special")))
    .toBeVisible()
    .whileElement(scrollView)
    .scroll(200, "down");

  await expect(element(by.id("product-item-special"))).toBeVisible();
  await element(by.id("product-item-special")).tap();

  // Verify detail screen
  await expect(element(by.id("productDetailTitle"))).toBeVisible();
});
```

**7. Deep Link Testing**

```javascript
it("should navigate to product detail via deep link", async () => {
  await device.launchApp({
    newInstance: true,
    url: "myapp://product/12345",
    launchArgs: { uiTestingMode: true },
  });

  // App should open directly to product detail
  await expect(element(by.id("productDetailTitle"))).toBeVisible();
  await expect(element(by.text("Product 12345"))).toBeVisible();
});
```

### Flakiness Prevention Strategies

**1. Root Cause Taxonomy**

| Flake Category          | Symptom                                  | Fix                                                             |
| ----------------------- | ---------------------------------------- | --------------------------------------------------------------- |
| **Timing**              | Element not found intermittently         | Use Detox auto-sync or Appium explicit waits; never `sleep()`   |
| **State leakage**       | Test passes in isolation, fails in suite | `device.reloadReactNative()` or `fullReset: true` between tests |
| **Network variability** | Response time causes race conditions     | Mock all network calls; use `setURLBlacklist` for Detox         |
| **Animation**           | Element exists but not hittable          | Wait for animation completion; `assertNoChanges` in Maestro     |
| **Resource contention** | Tests interfere on shared device         | One test session per device; isolate test data per run          |
| **Platform divergence** | Works on iOS, fails on Android           | Use platform-specific selectors where needed; test on both      |

**2. Quarantine & Retry Protocol**

```javascript
// Jest: retry flaky tests automatically
// jest.config.js
module.exports = {
  testRunner: {
    args: {
      retries: 2, // Retry up to 2 times before marking as failed
    },
  },
};

// Detox: retry flag
// detox test --retries 2 --configuration ios.sim.release
```

Tests that fail > 30% of retry attempts are quarantined:

1. Tag with `@quarantine` in test name
2. Move to `e2e/quarantine/` directory
3. File defect with flake rate data
4. Root cause analysis within 2 business days
5. Return to main suite after fix verified with 50 consecutive clean runs

## Pipeline Integration

| Stage                                | Application                                                                                                                                                      |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 5** (Development)            | Set up Detox/Appium test infrastructure alongside React Native feature development; ensure `testID` props added to all interactive components                    |
| **Stage 6** (Code Review)            | Review test code for flakiness anti-patterns: implicit waits, state leakage, inadequate mocking; verify `testID` coverage                                        |
| **Stage 7** (Automated Testing)      | **Primary ownership** — execute Appium device matrix tests and Detox RN suites; manage flaky test quarantine; aggregate cross-platform results; classify defects |
| **Stage 8** (Integrity Verification) | Re-run quarantined tests after fixes; verify E2E journeys across all supported platforms; confirm no functionality removed during bug-fix cycle                  |

## Quality Standards

| Metric                           | Target                                           | Measurement                                                                        |
| -------------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------- |
| Appium test flake rate           | < 5% per 100 runs                                | CI retry analysis; higher tolerance than native due to cross-platform complexity   |
| Detox test flake rate            | < 2% per 100 runs                                | Gray-box synchronization should produce near-deterministic results                 |
| E2E suite execution time         | < 60 minutes for full platform matrix            | Measured from CI pipeline start; parallel device execution required                |
| `testID` coverage (React Native) | 100% of interactive components                   | Automated lint scan for `TouchableOpacity`, `Pressable`, `Button` without `testID` |
| Flaky test quarantine rate       | < 5% of total E2E suite                          | Tests in quarantine should be actively investigated; no test quarantined > 5 days  |
| Network mock coverage            | 100% of external API calls in E2E tests          | No real network calls permitted in CI test runs                                    |
| Device matrix coverage           | Minimum 3 Android + 3 iOS device/OS combinations | Tracked in device farm dashboard; coverage gap = P2 defect                         |
