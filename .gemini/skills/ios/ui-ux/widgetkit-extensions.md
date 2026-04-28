---
name: widgetkit-extensions
description: This skill implements iOS extension development covering WidgetKit widgets, App Intents for Siri integration, Share Extension for content sharing.
---

# WidgetKit & Extensions

**Category:** Mobile Engineering — iOS Extensions
**Owner:** iOS Engineer (Camila Rodriguez)

## Overview

This skill implements iOS extension development covering WidgetKit widgets, App Intents for Siri integration, Share Extension for content sharing, Today Extension for notification center, and app groups for data sharing between app and extensions. It applies to Stage 5 (Development) where extensions are built alongside the main app, Stage 6 (Code Review) where extension architecture and data sharing are audited, and Stage 8 (Integrity Verification) where extension functionality is verified.

## Competency Dimensions

| Dimension       | Description                                                                                               | Proficiency Indicators                                                                                                                                  |
| --------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| WidgetKit       | Widget configuration, timeline providers, placeholder views, deep links, widget families, reloads         | Widgets display accurate data via timeline; placeholder matches loaded state; deep links navigate to correct app screen; supports all widget families   |
| App Intents     | Intent definition, parameter handling, Siri shortcuts, App Shortcuts, dynamic options, confirmation       | Intents properly defined with parameters; Siri suggestions contextual; dynamic options load efficiently; confirmation provides feedback                 |
| Share Extension | Share view controller, item handling, NSExtensionItem, SLComposeServiceViewController, content processing | All shareable content types handled; content processed in background; extension UI matches app design; proper error handling                            |
| Today Extension | Notification center widget, NCWidgetProviding, expanded/collapsed modes, quick actions                    | Today extension displays at-a-glance info; expanded mode for detailed content; quick actions launch app with context                                    |
| App Groups      | Shared container, UserDefaults suite, file sharing, Core Data sharing, real-time sync                     | App group configured in entitlements; shared data accessed correctly; file coordination for concurrent access; Core Data sharing with separate contexts |

## Execution Guidance

### WidgetKit — Complete Implementation

**Timeline Provider:**

```swift
import WidgetKit
import SwiftUI

// MARK: - Timeline Entry

struct UserStatsEntry: TimelineEntry {
    let date: Date
    let totalTasks: Int
    let completedTasks: Int
    let streak: Int
    let nextTask: TaskModel?
    let configuration: IntentConfiguration
}

// MARK: - Intent Configuration

struct IntentConfiguration: AppIntent {
    static var title: LocalizedStringResource = "User Stats Widget"

    @Parameter(title: "User", default: "default")
    var userId: String
}

// MARK: - Timeline Provider

struct UserStatsProvider: AppIntentTimelineProvider {

    func placeholder(in context: Context) -> UserStatsEntry {
        UserStatsEntry(
            date: Date(),
            totalTasks: 12,
            completedTasks: 8,
            streak: 5,
            nextTask: TaskModel(title: "Review PR", dueDate: Date().addingTimeInterval(3600)),
            configuration: IntentConfiguration()
        )
    }

    func snapshot(for configuration: IntentConfiguration, in context: Context) async -> UserStatsEntry {
        // Quick snapshot for widget gallery
        let stats = try? await fetchUserStats(userId: configuration.userId)
        return UserStatsEntry(
            date: Date(),
            totalTasks: stats?.totalTasks ?? 0,
            completedTasks: stats?.completedTasks ?? 0,
            streak: stats?.streak ?? 0,
            nextTask: stats?.nextTask,
            configuration: configuration
        )
    }

    func timeline(for configuration: IntentConfiguration, in context: Context) async -> Timeline<UserStatsEntry> {
        var entries: [UserStatsEntry] = []

        // Generate timeline for next 6 hours
        let currentDate = Date()
        for hourOffset in 0..<6 {
            let entryDate = Calendar.current.date(byAdding: .hour, value: hourOffset, to: currentDate)!

            let stats = try? await fetchUserStats(userId: configuration.userId)
            let entry = UserStatsEntry(
                date: entryDate,
                totalTasks: stats?.totalTasks ?? 0,
                completedTasks: stats?.completedTasks ?? 0,
                streak: stats?.streak ?? 0,
                nextTask: stats?.nextTask,
                configuration: configuration
            )
            entries.append(entry)
        }

        // Reload at end of timeline
        return Timeline(entries: entries, policy: .atEnd)
    }

    func recommendations() -> [AppIntentRecommendation<IntentConfiguration>] {
        [
            AppIntentRecommendation(
                intent: IntentConfiguration(userId: "default"),
                description: "Your daily task statistics"
            )
        ]
    }

    private func fetchUserStats(userId: String) async throws -> UserStats {
        // Fetch from shared app group container
        let containerURL = FileManager.default.containerURL(
            forSecurityApplicationGroupIdentifier: "group.com.example.app"
        )!
        let statsURL = containerURL.appendingPathComponent("widget_stats.json")

        guard let data = try? Data(contentsOf: statsURL) else {
            return UserStats(totalTasks: 0, completedTasks: 0, streak: 0, nextTask: nil)
        }

        return try JSONDecoder().decode(UserStats.self, from: data)
    }
}

// MARK: - Widget View

struct UserStatsWidgetView: View {
    var entry: UserStatsProvider.Entry

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            // Header
            HStack {
                Image(systemName: "chart.bar.fill")
                    .foregroundStyle(.blue)
                Text("Your Stats")
                    .font(.headline)
            }

            // Stats grid
            HStack(spacing: 16) {
                StatView(value: entry.totalTasks, label: "Total")
                StatView(value: entry.completedTasks, label: "Done")
                StatView(value: entry.streak, label: "Streak")
            }

            // Next task
            if let nextTask = entry.nextTask {
                NextTaskView(task: nextTask)
            }
        }
        .containerBackground(.fill.tertiary, for: .widget)
    }
}

struct StatView: View {
    let value: Int
    let label: String

    var body: some View {
        VStack(spacing: 2) {
            Text("\(value)")
                .font(.title2.bold())
            Text(label)
                .font(.caption2)
                .foregroundStyle(.secondary)
        }
    }
}

struct NextTaskView: View {
    let task: TaskModel

    var body: some View {
        HStack {
            Image(systemName: "clock.fill")
                .foregroundStyle(.orange)
            VStack(alignment: .leading) {
                Text(task.title)
                    .font(.subheadline)
                Text(task.dueDate, style: .relative)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
        .padding(.top, 4)
    }
}

// MARK: - Widget Configuration

struct UserStatsWidget: WidgetBundle {
    var body: some Widget {
        UserStatsWidget()
    }
}

struct UserStatsWidget: Widget {
    let kind: String = "UserStatsWidget"

    var body: some WidgetConfiguration {
        AppIntentConfiguration(
            kind: kind,
            intent: IntentConfiguration.self,
            provider: UserStatsProvider()
        ) { entry in
            UserStatsWidgetView(entry: entry)
                .containerBackground(.fill.tertiary, for: .widget)
        }
        .supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
        .configurationDisplayName("User Stats")
        .description("View your task completion statistics at a glance.")
    }
}
```

### App Intents — Siri Integration

```swift
import AppIntents
import Foundation

// MARK: - App Intent for Custom Action

struct CreateTaskIntent: AppIntent {
    static var title: LocalizedStringResource = "Create Task"
    static var description: IntentDescription = "Create a new task in the app"
    static var openAppWhenRun: Bool = true

    @Parameter(title: "Task Name")
    var taskName: String

    @Parameter(title: "Due Date")
    var dueDate: Date?

    @Parameter(title: "Priority", optionsProvider: PriorityOptionsProvider())
    var priority: TaskPriority

    func perform() async throws -> some IntentResult & ReturnsValue<TaskEntity> {
        let task = try await TaskService.createTask(
            name: taskName,
            dueDate: dueDate,
            priority: priority
        )

        return .result(
            value: TaskEntity(from: task),
            dialogue: "Created task: \(taskName)"
        )
    }
}

// MARK: - Dynamic Options Provider

struct PriorityOptionsProvider: DynamicOptionsProvider {
    func results() async throws -> [TaskPriority] {
        TaskPriority.allCases
    }
}

enum TaskPriority: String, AppEnum {
    case low, medium, high

    static var typeDisplayRepresentation: TypeDisplayRepresentation = "Priority"

    static var caseDisplayRepresentations: [TaskPriority: DisplayRepresentation] = [
        .low: "Low",
        .medium: "Medium",
        .high: "High"
    ]
}

// MARK: - App Shortcut

struct CreateTaskShortcut: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: CreateTaskIntent(),
            phrases: [
                "Create a task in \(.applicationName)",
                "Add task to \(.applicationName)"
            ],
            shortTitle: "Create Task",
            systemImageName: "plus.circle.fill"
        )
    }
}

// MARK: - Intent Entity (for returning results)

struct TaskEntity: AppEntity {
    var id: String
    var name: String
    var isCompleted: Bool

    static var typeDisplayRepresentation: TypeDisplayRepresentation = "Task"

    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(title: "\(name)")
    }

    static var defaultQuery = TaskQuery()

    init(from task: TaskModel) {
        self.id = task.id.uuidString
        self.name = task.name
        self.isCompleted = task.isCompleted
    }
}

struct TaskQuery: EntityQuery {
    func entities(for identifiers: [String]) async throws -> [TaskEntity] {
        // Fetch entities by ID
        []
    }

    func suggestedEntities() async throws -> [TaskEntity] {
        // Return recent tasks for suggestions
        []
    }
}
```

### Share Extension

```swift
import UIKit
import UniformTypeIdentifiers
import Social

class ShareViewController: SLComposeServiceViewController {

    private let appGroupIdentifier = "group.com.example.app"

    override func isContentValid() -> Bool {
        // Validate content before enabling post button
        return !contentText.isEmpty || extensionContext?.inputItems.count ?? 0 > 0
    }

    override func didSelectPost() {
        // Process shared content
        processSharedContent { [weak self] success in
            if success {
                self?.completeRequest(returningItems: nil, completionHandler: nil)
            } else {
                self?.displayError("Failed to share content")
            }
        }
    }

    private func processSharedContent(completion: @escaping (Bool) -> Void) {
        guard let extensionItem = extensionContext?.inputItems.first as? NSExtensionItem,
              let attachments = extensionItem.attachments else {
            completion(false)
            return
        }

        // Process each attachment
        for provider in attachments {
            // Handle URLs
            if provider.hasItemConformingToTypeIdentifier(UTType.url.identifier) {
                provider.loadItem(forTypeIdentifier: UTType.url.identifier, options: nil) { [weak self] (url, error) in
                    if let url = url as? URL {
                        self?.saveSharedURL(url)
                    }
                }
            }

            // Handle Images
            if provider.hasItemConformingToTypeIdentifier(UTType.image.identifier) {
                provider.loadItem(forTypeIdentifier: UTType.image.identifier, options: nil) { [weak self] (image, error) in
                    if let imageURL = image as? URL {
                        self?.saveSharedImage(imageURL)
                    } else if let uiImage = image as? UIImage {
                        self?.saveSharedImage(uiImage)
                    }
                }
            }

            // Handle Text
            if provider.hasItemConformingToTypeIdentifier(UTType.text.identifier) {
                provider.loadItem(forTypeIdentifier: UTType.text.identifier, options: nil) { [weak self] (text, error) in
                    if let text = text as? String {
                        self?.saveSharedText(text)
                    }
                }
            }
        }

        completion(true)
    }

    private func saveSharedURL(_ url: URL) {
        // Save to shared container
        let containerURL = FileManager.default.containerURL(
            forSecurityApplicationGroupIdentifier: appGroupIdentifier
        )!
        let shareFileURL = containerURL.appendingPathComponent("shared_content.json")

        // Append to existing shared content
        var sharedItems: [SharedItem] = []
        if let data = try? Data(contentsOf: shareFileURL) {
            sharedItems = (try? JSONDecoder().decode([SharedItem].self, from: data)) ?? []
        }

        sharedItems.append(SharedItem(type: .url, content: url.absoluteString, date: Date()))

        try? JSONEncoder().encode(sharedItems).write(to: shareFileURL)
    }

    private func saveSharedImage(_ image: UIImage) {
        // Save image to shared container
        let containerURL = FileManager.default.containerURL(
            forSecurityApplicationGroupIdentifier: appGroupIdentifier
        )!
        let imagesDir = containerURL.appendingPathComponent("shared_images")

        try? FileManager.default.createDirectory(at: imagesDir, withIntermediateDirectories: true)

        let imageURL = imagesDir.appendingPathComponent(UUID().uuidString + ".jpg")
        if let jpegData = image.jpegData(compressionQuality: 0.8) {
            try? jpegData.write(to: imageURL)
        }
    }

    private func saveSharedText(_ text: String) {
        let containerURL = FileManager.default.containerURL(
            forSecurityApplicationGroupIdentifier: appGroupIdentifier
        )!
        let shareFileURL = containerURL.appendingPathComponent("shared_content.json")

        var sharedItems: [SharedItem] = []
        if let data = try? Data(contentsOf: shareFileURL) {
            sharedItems = (try? JSONDecoder().decode([SharedItem].self, from: data)) ?? []
        }

        sharedItems.append(SharedItem(type: .text, content: text, date: Date()))
        try? JSONEncoder().encode(sharedItems).write(to: shareFileURL)
    }

    private func displayError(_ message: String) {
        // Show error to user
        let alert = UIAlertController(
            title: "Error",
            message: message,
            preferredStyle: .alert
        )
        alert.addAction(UIAlertAction(title: "OK", style: .default) { [weak self] _ in
            self?.cancelRequest()
        })
        present(alert, animated: true)
    }
}

struct SharedItem: Codable {
    enum ItemType: String, Codable {
        case url, image, text
    }

    let type: ItemType
    let content: String
    let date: Date
}
```

### App Groups — Data Sharing

```swift
// MARK: - Shared Container Access

final class SharedContainer {

    static let shared = SharedContainer()

    private let groupIdentifier = "group.com.example.app"

    var containerURL: URL {
        FileManager.default.containerURL(
            forSecurityApplicationGroupIdentifier: groupIdentifier
        )!
    }

    // MARK: - Shared UserDefaults

    var sharedDefaults: UserDefaults {
        UserDefaults(suiteName: groupIdentifier)!
    }

    // MARK: - Shared Data

    func saveWidgetData(_ data: WidgetData) {
        let url = containerURL.appendingPathComponent("widget_data.json")
        if let encoded = try? JSONEncoder().encode(data) {
            try? encoded.write(to: url)
        }
    }

    func loadWidgetData() -> WidgetData? {
        let url = containerURL.appendingPathComponent("widget_data.json")
        guard let data = try? Data(contentsOf: url) else { return nil }
        return try? JSONDecoder().decode(WidgetData.self, from: data)
    }

    // MARK: - File Coordination (for concurrent access)

    func saveFileCoordinated(data: Data, to url: URL) throws {
        var error: NSError?
        NSFileCoordinator().coordinate(
            writingItemAt: url,
            options: .forReplacing,
            error: &error
        ) { coordinatedURL in
            try? data.write(to: coordinatedURL)
        }

        if let error = error { throw error }
    }

    func loadFileCoordinated(from url: URL) throws -> Data {
        var resultData: Data?
        var error: NSError?

        NSFileCoordinator().coordinate(
            readingItemAt: url,
            options: .withoutChanges,
            error: &error
        ) { coordinatedURL in
            resultData = try? Data(contentsOf: coordinatedURL)
        }

        if let error = error { throw error }
        return resultData ?? Data()
    }
}

// MARK: - Shared Core Data Stack (App + Widget)

final class SharedCoreDataManager {

    static let shared = SharedCoreDataManager()

    private let groupIdentifier = "group.com.example.app"

    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "AppModel")

        let storeURL = FileManager.default.containerURL(
            forSecurityApplicationGroupIdentifier: groupIdentifier
        )!.appendingPathComponent("AppModel.sqlite")

        let description = NSPersistentStoreDescription(url: storeURL)
        description.shouldMigrateStoreAutomatically = true
        description.shouldInferMappingModelAutomatically = true

        container.persistentStoreDescriptions = [description]

        container.loadPersistentStores { _, error in
            if let error = error {
                print("Core Data load error: \(error)")
            }
        }

        return container
    }()

    var viewContext: NSManagedObjectContext {
        persistentContainer.viewContext
    }

    func save() {
        let context = persistentContainer.viewContext
        if context.hasChanges {
            try? context.save()
        }
    }
}
```

## Pipeline Integration

- **Stage 4 (Implementation Plan):** Extension development tasks included: WidgetKit setup, App Intents definition, Share Extension configuration, App Groups entitlement.
- **Stage 5 (Development):** Primary skill for iOS extension development. All widgets, intents, and extensions built with proper data sharing.
- **Stage 6 (Code Review):** Extension review: timeline accuracy, App Intent parameter handling, Share Extension content processing, App Groups data integrity.
- **Stage 8 (Integrity Verification):** All extensions tested on target devices. Widget timeline accuracy verified. App Intents tested with Siri.

## Quality Standards

- Widget timeline entries cover **minimum 6 hours** with appropriate refresh policy
- Widget placeholder view **matches loaded state** visually — no jarring transition
- All widget families supported (**systemSmall, systemMedium, systemLarge**) unless design restricts
- App Intents have **meaningful phrases** for Siri — at least 2 phrase variations per intent
- Share Extension handles **URL, image, and text** content types at minimum
- App Groups configured in **entitlements** for main app and all extensions
- Shared data accessed via **file coordination** when concurrent access possible
- Widget data saved to **shared container** — widget never makes network requests directly
- App Intent confirmation provides **dialogue feedback** — silent intents are confusing
- Share Extension processes content in **background** — UI responsive during processing
- Today Extension supports both **expanded and collapsed** display modes
