---
name: ios-testing-quality-ios-accessibility
description: "Ios skill: Ios Accessibility"
---

# iOS Accessibility

**Category:** Mobile Engineering — iOS Accessibility (a11y)
**Owner:** iOS Engineer (Arjun Mehta)

## Overview

This skill implements iOS accessibility covering VoiceOver optimization, Dynamic Type support, Switch Control compatibility, accessibility identifier management, and automated accessibility auditing tools. It applies to Stage 5 (Development) where all UI must be built accessibly from the start, Stage 6 (Code Review) where accessibility conformance is audited, and Stage 8 (Integrity Verification) where the CDO verifies IDS accessibility specifications are realized.

## Competency Dimensions

| Dimension                 | Description                                                                                                | Proficiency Indicators                                                                                                        |
| ------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| VoiceOver                 | Accessibility labels, hints, traits, notifications, custom actions, rotor items                            | All UI elements have meaningful labels; custom actions for complex interactions; VoiceOver navigation is logical and complete |
| Dynamic Type              | Text scaling,ContentSizeCategory observation, layout adaptation, maximum size testing, custom font scaling | App fully functional at XXXL font size; layouts adapt gracefully; no text truncation or overlap at any size                   |
| Switch Control            | Focus management, focus groups, scan styles, custom gestures, point scanning                               | All interactive elements reachable via Switch Control; logical focus order; custom gestures for complex interactions          |
| Accessibility Identifiers | Systematic naming convention, test-auditable identifiers, consistency across platforms                     | Every interactive element has a11y identifier; identifiers follow naming convention; XCUITests use identifiers exclusively    |
| Audit Tools               | Accessibility Inspector, Accessibility Scanner, automated checks, manual VoiceOver testing                 | Automated a11y checks in CI; manual VoiceOver test script executed per release; audit tool findings tracked and resolved      |

## Execution Guidance

### VoiceOver — Production Implementation

**Accessibility Labels and Hints:**

```swift
// MARK: - UIKit

class UserCardView: UIView {

    private let avatarImageView = UIImageView()
    private let nameLabel = UILabel()
    private let emailLabel = UILabel()
    private let onlineIndicator = UIView()
    private let deleteButton = UIButton()

    override init(frame: CGRect) {
        super.init(frame: frame)
        setupAccessibility()
    }

    required init?(coder: NSCoder) { fatalError() }

    func configure(with user: User) {
        nameLabel.text = user.name
        emailLabel.text = user.email
        avatarImageView.image = user.avatar

        // Update accessibility when data changes
        updateAccessibility(for: user)
    }

    private func setupAccessibility() {
        // Make the entire card accessible as a single element
        isAccessibilityElement = true
        accessibilityTraits = [.button]

        // Delete button
        deleteButton.accessibilityLabel = "Delete user"
        deleteButton.accessibilityHint = "Removes this user from the list"
        deleteButton.accessibilityTraits = .button
    }

    private func updateAccessibility(for user: User) {
        // Compound label — describes the element's purpose and state
        accessibilityLabel = "\(user.name), \(user.email)${user.isOnline ? ", online" : ", offline"}"
        accessibilityHint = "Double tap to view profile"
        accessibilityValue = user.isOnline ? "Online" : "Offline"
    }
}

// MARK: - SwiftUI

struct UserCardView: View {
    let user: User

    var body: some View {
        HStack(spacing: 12) {
            AsyncImage(url: user.avatarURL) { image in
                image
                    .resizable()
                    .scaledToFill()
            } placeholder: {
                ProgressView()
            }
            .accessibilityHidden(true)  // Decorative — context provided by parent

            VStack(alignment: .leading, spacing: 4) {
                Text(user.name)
                    .font(.headline)
                Text(user.email)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            if user.isOnline {
                Circle()
                    .fill(.green)
                    .frame(width: 12, height: 12)
                    .accessibilityHidden(true)  // Decorative
            }
        }
        .padding()
        .accessibilityElement(children: .combine)  // Combine child elements
        .accessibilityLabel("\(user.name), \(user.email)")
        .accessibilityValue(user.isOnline ? "Online" : "Offline")
        .accessibilityAddTraits(.isButton)
        .accessibilityHint("Double tap to view profile")
    }
}
```

**Custom Accessibility Actions:**

```swift
// UIKit — custom actions for VoiceOver users
class TaskItemView: UIView {

    var onToggleComplete: (() -> Void)?
    var onDelete: (() -> Void)?
    var onSnooze: (() -> Void)?

    override var accessibilityCustomActions: [UIAccessibilityCustomAction]? {
        get {
            [
                UIAccessibilityCustomAction(
                    name: isCompleted ? "Mark Incomplete" : "Mark Complete",
                    target: self,
                    selector: #selector(toggleComplete)
                ),
                UIAccessibilityCustomAction(
                    name: "Delete Task",
                    target: self,
                    selector: #selector(deleteTask)
                ),
                UIAccessibilityCustomAction(
                    name: "Snooze Task",
                    target: self,
                    selector: #selector(snoozeTask)
                )
            ]
        }
        set { }
    }

    @objc private func toggleComplete() -> Bool {
        onToggleComplete?()
        return true
    }

    @objc private func deleteTask() -> Bool {
        onDelete?()
        return true
    }

    @objc private func snoozeTask() -> Bool {
        onSnooze?()
        return true
    }
}

// SwiftUI — custom actions
struct TaskItemView: View {
    let task: TaskModel
    let onToggleComplete: () -> Void
    let onDelete: () -> Void
    let onSnooze: () -> Void

    var body: some View {
        HStack {
            Text(task.title)
            Spacer()
            if task.isCompleted {
                Image(systemName: "checkmark.circle.fill")
                    .foregroundStyle(.green)
            }
        }
        .padding()
        .accessibilityAction(named: task.isCompleted ? "Mark Incomplete" : "Mark Complete") {
            onToggleComplete()
        }
        .accessibilityAction(named: "Delete") {
            onDelete()
        }
        .accessibilityAction(named: "Snooze") {
            onSnooze()
        }
    }
}
```

**Accessibility Notifications for Dynamic Content:**

```swift
// UIKit — announce dynamic content changes
class CartBadgeView: UIView {

    var itemCount: Int = 0 {
        didSet {
            updateAccessibility()
        }
    }

    private func updateAccessibility() {
        accessibilityLabel = "Shopping cart"
        accessibilityValue = "\(itemCount) item\(itemCount == 1 ? "" : "s")"

        // Announce change to VoiceOver users
        UIAccessibility.post(
            notification: .announcement,
            argument: "Cart updated. \(itemCount) item\(itemCount == 1 ? "" : "s")"
        )
    }
}

// SwiftUI — accessibility live region
struct CartBadgeView: View {
    let itemCount: Int

    var body: some View {
        Image(systemName: "cart.fill")
            .overlay(alignment: .topTrailing) {
                if itemCount > 0 {
                    Text("\(itemCount)")
                        .font(.caption2.bold())
                        .foregroundStyle(.white)
                        .padding(4)
                        .background(.red, in: Circle())
                }
            }
            .accessibilityLabel("Shopping cart")
            .accessibilityValue("\(itemCount) item\(itemCount == 1 ? "" : "s")")
            .accessibilityRespondsToUserInteraction(false)
    }
}
```

### Dynamic Type — Full Support

```swift
// MARK: - UIKit Dynamic Type

class ArticleView: UIView {

    private let titleLabel = UILabel()
    private let bodyLabel = UILabel()
    private let authorLabel = UILabel()

    override init(frame: CGRect) {
        super.init(frame: frame)
        setupLabels()
        setupLayout()
    }

    required init?(coder: NSCoder) { fatalError() }

    private func setupLabels() {
        // Use dynamic type text styles
        titleLabel.font = UIFont.preferredFont(forTextStyle: .headline)
        titleLabel.adjustsFontForContentSizeCategory = true
        titleLabel.numberOfLines = 0

        bodyLabel.font = UIFont.preferredFont(forTextStyle: .body)
        bodyLabel.adjustsFontForContentSizeCategory = true
        bodyLabel.numberOfLines = 0

        authorLabel.font = UIFont.preferredFont(forTextStyle: .caption1)
        authorLabel.adjustsFontForContentSizeCategory = true
        authorLabel.numberOfLines = 0
    }

    private func setupLayout() {
        // Use Auto Layout — adapts to font size changes
        let container = UIStackView(arrangedSubviews: [titleLabel, bodyLabel, authorLabel])
        container.axis = .vertical
        container.spacing = 8
        container.translatesAutoresizingMaskIntoConstraints = false

        addSubview(container)

        NSLayoutConstraint.activate([
            container.topAnchor.constraint(equalTo: safeAreaLayoutGuide.topAnchor, constant: 16),
            container.leadingAnchor.constraint(equalTo: leadingAnchor, constant: 16),
            container.trailingAnchor.constraint(equalTo: trailingAnchor, constant: -16),
            container.bottomAnchor.constraint(equalTo: bottomAnchor, constant: -16)
        ])
    }

    // Respond to content size category changes
    override func traitCollectionDidChange(_ previousTraitCollection: UITraitCollection?) {
        super.traitCollectionDidChange(previousTraitCollection)

        if traitCollection.hasDifferentContentSizeCategory(comparedTo: previousTraitCollection) {
            // Layout automatically updates due to Auto Layout
            // But we can make additional adjustments here
            adjustLayoutForLargeFonts()
        }
    }

    private func adjustLayoutForLargeFonts() {
        let contentSize = traitCollection.preferredContentSizeCategory

        if contentSize.isAccessibilityCategory {
            // Extra large fonts — reduce spacing, limit lines
            bodyLabel.numberOfLines = 5
        } else {
            bodyLabel.numberOfLines = 0
        }
    }
}

extension UITraitCollection {
    func hasDifferentContentSizeCategory(comparedTo previous: UITraitCollection?) -> Bool {
        guard let previous else { return true }
        return preferredContentSizeCategory != previous.preferredContentSizeCategory
    }
}

// MARK: - SwiftUI Dynamic Type

struct ArticleView: View {
    let title: String
    let body: String
    let author: String

    @Environment(\.dynamicTypeSize) var dynamicTypeSize

    var body: some View {
        VStack(alignment: .leading, spacing: dynamicTypeSpacing) {
            Text(title)
                .font(.headline)
                .lineLimit(dynamicTypeSize.isAccessibilitySize ? 2 : nil)

            Text(body)
                .font(.body)
                .lineLimit(dynamicTypeSize.isAccessibilitySize ? 5 : nil)

            Text("By \(author)")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .padding()
    }

    private var dynamicTypeSpacing: CGFloat {
        dynamicTypeSize.isAccessibilitySize ? 12 : 8
    }
}

// MARK: - Custom Font Scaling

struct CustomFontModifier: ViewModifier {
    let textStyle: UIFont.TextStyle
    @Environment(\.dynamicTypeSize) var dynamicTypeSize

    func body(content: Content) -> some View {
        let font = UIFont.preferredFont(forTextStyle: textStyle)
        let scaledFont = font.withSize(
            font.pointSize * dynamicTypeSize.ratio
        )

        content
            .font(.system(size: scaledFont.pointSize))
    }
}

extension View {
    func customDynamicFont(textStyle: UIFont.TextStyle) -> some View {
        modifier(CustomFontModifier(textStyle: textStyle))
    }
}
```

### Switch Control — Compatibility

```swift
// MARK: - Focus Groups (UIKit)

class FormSectionView: UIView {

    private let stackView = UIStackView()

    override init(frame: CGRect) {
        super.init(frame: frame)
        setupFocusGroup()
    }

    required init?(coder: NSCoder) { fatalError() }

    private func setupFocusGroup() {
        // Group related elements for Switch Control scanning
        accessibilityElements = stackView.arrangedSubviews

        // Set logical focus order
        stackView.arrangedSubviews.enumerated().forEach { index, view in
            view.accessibilityElements = [view]
            view.accessibilityNavigationStyle = .sequential
        }
    }
}

// MARK: - Accessibility Container (UIKit)

class CustomDrawingView: UIView {

    private var accessibleSubElements: [AccessibleElement] = []

    override var isAccessibilityElement: Bool { false }

    override func accessibilityElementCount() -> Int {
        accessibleSubElements.count
    }

    override func accessibilityElement(at index: Int) -> Any? {
        guard index < accessibleSubelements.count else { return nil }
        return accessibleSubElements[index]
    }

    override func index(ofAccessibilityElement element: Any) -> Int {
        guard let element = element as? AccessibleElement else { return NSNotFound }
        return accessibleSubElements.firstIndex(where: { $0 === element }) ?? NSNotFound
    }

    func addAccessibleElement(_ element: AccessibleElement) {
        accessibleSubElements.append(element)
    }
}

class AccessibleElement: UIAccessibilityElement {
    var onTap: (() -> Void)?

    override func accessibilityActivate() -> Bool {
        onTap?()
        return true
    }
}
```

### Accessibility Identifiers — Systematic Naming

```swift
// MARK: - Accessibility Identifier Convention

enum A11y {
    // Format: {screen}-{component}-{action/state}
    enum UserList {
        static let screen = "userList-screen"
        static let userCell = { index in "userList-cell-\(index)" }
        static let userName = { index in "userList-name-\(index)" }
        static let userEmail = { index in "userList-email-\(index)" }
        static let deleteButton = { index in "userList-delete-\(index)" }
        static let refreshButton = "userList-refresh"
        static let loadingIndicator = "userList-loading"
        static let emptyState = "userList-empty"
        static let errorMessage = "userList-error"
    }

    enum UserDetail {
        static let screen = "userDetail-screen"
        static let avatar = "userDetail-avatar"
        static let name = "userDetail-name"
        static let email = "userDetail-email"
        static let editButton = "userDetail-edit"
        static let backButton = "userDetail-back"
    }

    enum Settings {
        static let screen = "settings-screen"
        static let themeToggle = "settings-themeToggle"
        static let notificationToggle = "settings-notificationToggle"
        static let logoutButton = "settings-logout"
    }
}

// MARK: - Usage

class UserListViewController: UIViewController {

    private func setupAccessibility() {
        view.accessibilityIdentifier = A11y.UserList.screen
        refreshControl.accessibilityIdentifier = A11y.UserList.refreshButton
        loadingIndicator.accessibilityIdentifier = A11y.UserList.loadingIndicator
        emptyStateLabel.accessibilityIdentifier = A11y.UserList.emptyState
        errorLabel.accessibilityIdentifier = A11y.UserList.errorMessage
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "UserCell", for: indexPath)
        cell.accessibilityIdentifier = A11y.UserList.userCell(indexPath.row)

        let nameLabel = cell.viewWithTag(1) as? UILabel
        nameLabel?.accessibilityIdentifier = A11y.UserList.userName(indexPath.row)

        return cell
    }
}

// MARK: - SwiftUI Usage

struct UserListView: View {
    var body: some View {
        List {
            ForEach(users) { user in
                UserRow(user: user)
                    .accessibilityIdentifier(A11y.UserList.userCell(users.firstIndex(where: { $0.id == user.id }) ?? 0))
            }
        }
        .accessibilityIdentifier(A11y.UserList.screen)
    }
}

// MARK: - XCUITest Usage

func test_userList_displaysUsers() {
    let app = XCUIApplication()
    app.launch()

    // Use accessibility identifiers — not raw text
    let cell = app.cells[A11y.UserList.userCell(0)]
    XCTAssertTrue(cell.waitForExistence(timeout: 10))

    let nameLabel = app.staticTexts[A11y.UserList.userName(0)]
    XCTAssertTrue(nameLabel.exists)
}
```

### Accessibility Audit — Automated + Manual

**Automated checks in CI:**

```swift
import XCTest

final class AccessibilityAuditTests: XCTestCase {

    var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        app = XCUIApplication()
        app.launchArguments = ["--ui-testing"]
        app.launch()
    }

    func test_allScreens_haveAccessibilityIdentifiers() {
        // Check that all interactive elements have identifiers
        let buttons = app.buttons.allElementsBoundByIndex
        let textFields = app.textFields.allElementsBoundByIndex
        let switches = app.switches.allElementsBoundByIndex

        for button in buttons where button.isHittable {
            XCTAssertFalse(
                button.accessibilityIdentifier?.isEmpty ?? true,
                "Button '\(button.label)' missing accessibility identifier"
            )
        }

        for textField in textFields where textField.isHittable {
            XCTAssertFalse(
                textField.accessibilityIdentifier?.isEmpty ?? true,
                "TextField '\(textField.label)' missing accessibility identifier"
            )
        }
    }

    func test_allImages_haveAccessibilityLabels() {
        // Check that meaningful images have accessibility labels
        let images = app.images.allElementsBoundByIndex

        for image in images where image.isHittable {
            let hasLabel = !image.accessibilityLabel.isEmpty
            let isDecorative = image.accessibilityLabel == nil || image.accessibilityLabel?.isEmpty == true

            // If image is interactive, it must have a label
            if image.isHittable {
                XCTAssertTrue(
                    hasLabel || image.accessibilityTraits.contains(.notEnabled),
                    "Image '\(image.label)' missing accessibility label"
                )
            }
        }
    }

    func test_touchTargets_meetMinimumSize() {
        // Minimum touch target: 44x44 points
        let buttons = app.buttons.allElementsBoundByIndex

        for button in buttons where button.isHittable {
            let frame = button.frame
            XCTAssertGreaterThanOrEqual(
                frame.width, 44,
                "Button '\(button.label)' width \(frame.width) < 44pt minimum"
            )
            XCTAssertGreaterThanOrEqual(
                frame.height, 44,
                "Button '\(button.label)' height \(frame.height) < 44pt minimum"
            )
        }
    }
}
```

**Manual VoiceOver test script:**

```markdown
# VoiceOver Manual Test Checklist

## Navigation

- [ ] Can navigate all screens using swipe gestures
- [ ] Rotor allows navigation by headings, links, and form controls
- [ ] Logical reading order matches visual layout
- [ ] No elements skipped or inaccessible

## Interactive Elements

- [ ] All buttons have meaningful labels (not "Button 1", "Button 2")
- [ ] All form fields have associated labels
- [ ] All images have appropriate descriptions (or marked decorative)
- [ ] Custom actions available for complex interactions

## Dynamic Content

- [ ] State changes announced via accessibility notifications
- [ ] Loading states announced ("Loading...")
- [ ] Error messages announced immediately
- [ ] Success confirmations announced

## Dynamic Type

- [ ] All text readable at XXXL font size
- [ ] No text truncation or overlap
- [ ] Scrolling works for overflow content
- [ ] Touch targets remain usable at large font sizes

## Switch Control

- [ ] All interactive elements reachable via point scanning
- [ ] Logical scan order
- [ ] Custom gestures work with Switch Control
```

## Pipeline Integration

- **Stage 2 (Design):** IDS specifies accessibility requirements (contrast ratios, touch target sizes, VoiceOver labels, Dynamic Type support).
- **Stage 5 (Development):** All UI components built with accessibility from the start. No retrofitting after visual completion.
- **Stage 6 (Code Review):** Accessibility audit: label completeness, touch target sizing, Dynamic Type resilience, semantic structure, identifier coverage.
- **Stage 7 (Automated Testing):** Automated accessibility checks in test suite; manual VoiceOver test script execution.
- **Stage 8 (Integrity Verification):** CDO verifies IDS accessibility specifications are realized. Accessibility Inspector audit with zero critical issues.
- **Stage 10 (Release Readiness):** Accessibility conformance is item 2 on the release checklist (Design — all CDO/IDS specifications realized).

## Quality Standards

- **100%** interactive elements have meaningful accessibility labels
- **100%** interactive elements have minimum 44x44pt touch target
- **100%** text scales correctly at all Dynamic Type sizes (XXS to XXXXL)
- App fully usable at **accessibility font sizes** — no truncation or overlap
- **100%** VoiceOver users can complete all core user flows
- **100%** interactive elements have accessibility identifiers (for XCUITest)
- Custom accessibility actions provided for **complex multi-touch interactions**
- Dynamic content changes announced via **UIAccessibility notifications**
- Decorative images marked with `accessibilityHidden(true)` / `.accessibilityHidden(true)`
- Manual VoiceOver test script **executed and signed off** before every release
- Accessibility defects classified as **P0/P1** (not cosmetic) — they block release
- No information conveyed by **color alone** — always paired with text or icon
