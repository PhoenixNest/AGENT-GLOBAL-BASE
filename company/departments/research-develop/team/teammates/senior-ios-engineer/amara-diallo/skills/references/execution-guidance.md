---
version: "1.0.0"
---

----------- | ---------------------------- | ------------------------------------- | ------------------------- |
| **PR Check** | Pull Request created/updated | Build, lint, unit tests | `CI_BRANCH` = PR branch |
| **Develop Build** | Push to `develop` | Build, all tests, TestFlight beta | `CONFIGURATION` = Debug |
| **Release Build** | Push to `main` or tag | Build, all tests, App Store upload | `CONFIGURATION` = Release |
| **Nightly** | Schedule (daily 2am) | Full test suite, snapshot tests, lint | All checks |

### Fastlane — Complete Configuration

**Fastfile:**

```ruby
# fastlane/Fastfile

default_platform(:ios)

platform :ios do

  # MARK: - Setup

  before_all do |lane, options|
    # Ensure clean state
    clear_derived_data if options[:clean]

    # Setup code signing
    setup_ci if is_ci?
  end

  after_all do |lane, options|
    # Clean up
    cleanup_build_artifacts
  end

  error do |lane, exception, options|
    # Notify on failure
    slack(
      message: "Fastlane failed on #{lane}: #{exception.message}",
      success: false
    )
  end

  # MARK: - Lanes

  desc "Run all linting and static analysis"
  lane :lint do
    swiftlint(
      mode: :lint,
      config_file: ".swiftlint.yml",
      raise_issue: true
    )

    swiftlint(
      mode: :analyze,
      config_file: ".swiftlint.yml",
      raise_issue: true
    )
  end

  desc "Run unit tests"
  lane :test do |options|
    run_tests(
      workspace: "App.xcworkspace",
      scheme: "App",
      devices: ["iPhone 15"],
      clean: true,
      output_types: "junit",
      output_directory: "./fastlane/test_output",
      skip_build: options[:skip_build] || false
    )
  end

  desc "Build the app"
  lane :build do |options|
    configuration = options[:configuration] || "Release"

    gym(
      scheme: "App",
      workspace: "App.xcworkspace",
      configuration: configuration,
      clean: true,
      output_directory: "./fastlane/build",
      output_name: "App-#{configuration}.ipa",
      export_method: configuration == "Release" ? "app-store" : "ad-hoc",
      include_symbols: true,
      include_bitcode: false
    )
  end

  desc "Upload to TestFlight"
  lane :beta do
    pilot(
      ipa: "./fastlane/build/App-Debug.ipa",
      skip_submission: false,
      distribute_external: false,
      groups: ["Beta Testers"],
      changelog: last_git_commit[:message],
      notify_testers: true
    )
  end

  desc "Upload to App Store"
  lane :release do |options|
    version = options[:version] || get_version_number

    gym(
      scheme: "App",
      configuration: "Release",
      export_method: "app-store"
    )

    upload_to_app_store(
      skip_metadata: false,
      skip_screenshots: true,
      submit_for_review: options[:submit] || false,
      automatic_release: options[:auto_release] || false,
      phased_release: true,
      submission_information: {
        add_id_info_uses_idfa: false
      }
    )
  end

  desc "Generate screenshots"
  lane :screenshots do
    snapshot(
      scheme: "AppSnapshotTests",
      devices: ["iPhone 15", "iPhone 15 Pro Max", "iPad Pro (12.9-inch) (6th generation)"],
      languages: ["en-US", "ja-JP", "pt-BR"],
      clean: true,
      output_directory: "./fastlane/screenshots",
      overwrite: true
    )
  end

  desc "Full CI pipeline"
  lane :ci do
    lint
    test
    build(configuration: "Debug")
    beta
  end

  desc "Release pipeline"
  lane :release_pipeline do |options|
    ensure_git_branch(branch: "main")
    ensure_git_status_clean

    increment_build_number
    build(configuration: "Release")
    release(submit: options[:submit], auto_release: options[:auto_release])
  end

  # MARK: - Helper Methods

  def cleanup_build_artifacts
    # Remove intermediate build files
    FileUtils.rm_rf("./fastlane/build")
  end
end
```

**Matchfile (Code Signing):**

```ruby
# fastlane/Matchfile

git_url("git@github.com:example-app/certificates.git")
storage_mode("git")
type("development")
app_identifier(["com.example.app", "com.example.app.widget", "com.example.app.share"])
username("developer@example.com")

# For CI
if is_ci?
  readonly(true)
end
```

**Appfile:**

```ruby
# fastlane/Appfile

app_identifier("com.example.app")
apple_id("developer@example.com")
team_id("ABCD123456")

for_platform :ios do
  for_lane :release do
    app_identifier("com.example.app")
  end

  for_lane :beta do
    app_identifier("com.example.app")
  end
end
```

### Crashlytics Integration

**AppDelegate setup:**

```swift
import FirebaseCore
import FirebaseCrashlytics

@main
class AppDelegate: UIResponder, UIApplicationDelegate {

    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        FirebaseApp.configure()

        // Set user identifier for crash correlation
        if let userId = AuthManager.shared.currentUserId {
            Crashlytics.crashlytics().setUserID(userId)
        }

        // Set custom keys for crash context
        Crashlytics.crashlytics().setCustomValue(
            Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "unknown",
            forKey: "app_version"
        )
        Crashlytics.crashlytics().setCustomValue(
            Bundle.main.infoDictionary?["CFBundleVersion"] as? String ?? "unknown",
            forKey: "build_number"
        )
        Crashlytics.crashlytics().setCustomValue(
            UIDevice.current.systemVersion,
            forKey: "ios_version"
        )
        Crashlytics.crashlytics().setCustomValue(
            deviceModel(),
            forKey: "device_model"
        )

        return true
    }

    private func deviceModel() -> String {
        var systemInfo = utsname()
        uname(&systemInfo)
        return withUnsafePointer(to: &systemInfo.machine) {
            $0.withMemoryRebound(to: CChar.self, capacity: 1) { String(cString: $0) }
        }
    }
}

// MARK: - Breadcrumb Logging

extension Crashlytics {
    static func log(_ message: String) {
        crashlytics().log(message)
    }

    static func set(key: String, value: Any) {
        crashlytics().setCustomValue(value, forKey: key)
    }
}

// Usage in repository
class UserRepository {
    func fetchUser(id: String) async throws -> User {
        Crashlytics.log("Fetching user: \(id)")

        do {
            let user = try await apiClient.get("/users/\(id)")
            return user
        } catch {
            Crashlytics.log("Failed to fetch user \(id): \(error.localizedDescription)")
            Crashlytics.set(key: "failed_user_id", value: id)
            throw error
        }
    }
}

// MARK: - Non-Fatal Exception Reporting

func reportNonFatalError(_ error: Error, context: [String: Any] = [:]) {
    Crashlytics.crashlytics().record(error: error)
    context.forEach { key, value in
        Crashlytics.crashlytics().setCustomValue(value, forKey: key)
    }
}
```

### SwiftLint Configuration

```yaml
# .swiftlint.yml

# Rules to opt in
opt_in_rules:
  - empty_count
  - closure_spacing
  - contains_over_first_not_nil
  - discouraged_object_literal
  - empty_string
  - fatal_error_message
  - first_where
  - flatmap_over_map_reduce
  - force_unwrapping
  - implicitly_unwrapped_optional
  - last_where
  - multiline_arguments
  - multiline_function_chains
  - redundant_nil_coalescing
  - sorted_first_last
  - unneeded_parentheses_in_closure_argument
  - vertical_parameter_alignment_on_call

# Rules to disable
disabled_rules:
  - trailing_whitespace # Handled by formatter

# Configuration
line_length:
  warning: 120
  error: 200

file_length:
  warning: 400
  error: 600

type_body_length:
  warning: 300
  error: 500

function_body_length:
  warning: 50
  error: 80

cyclomatic_complexity:
  warning: 10
  error: 15

nesting:
  type_level: 3
  function_level: 3

identifier_name:
  min_length: 2
  excluded:
    - id
    - x
    - y
    - i
    - j

force_unwrapping: error

# Excluded paths
excluded:
  - Pods/
  - DerivedData/
  - fastlane/
  - .build/
  - ci_scripts/
```

### CI Build Time Optimization

**Build settings for CI:**

```
# Xcode Build Settings for CI

# Enable incremental compilation
SWIFT_COMPILATION_MODE = wholemodule  # Release only
SWIFT_OPTIMIZATION_LEVEL = "-O"       # Release
SWIFT_OPTIMIZATION_LEVEL = "-Onone"   # Debug

# Precompile headers
GCC_PRECOMPILE_PREFIX_HEADER = YES

# Disable code signing for test builds (Xcode Cloud handles this)
CODE_SIGNING_ALLOWED = NO  # For unit test builds only

# Parallel indexing
ENABLE_USER_SCRIPT_SANDBOXING = YES

# Debug information format
DEBUG_INFORMATION_FORMAT = dwarf-with-dsym  # Release
DEBUG_INFORMATION_FORMAT = dwarf            # Debug
```

**Parallel test execution in Xcode Cloud:**

```bash
# ci_scripts/ci_pre_xcodebuild.sh — Enable parallel testing
#!/bin/zsh
set -e

# Set number of test runners based on available cores
NUM_CORES=$(sysctl -n hw.ncpu)
TEST_RUNNERS=$((NUM_CORES > 4 ? 4 : NUM_CORES))

echo "Using $TEST_RUNNERS parallel test runners"
defaults write com.apple.dt.XCBuild NumberOfTestRunnerProcesses -int $TEST_RUNNERS
```
