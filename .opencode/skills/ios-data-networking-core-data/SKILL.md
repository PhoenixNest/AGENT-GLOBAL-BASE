---
name: ios-data-networking-core-data
description: 'Ios skill: Core Data'
---

# Core Data

**Category:** Mobile Engineering — iOS Data Persistence
**Owner:** iOS Engineer (Hiroshi Tanaka)

## Overview

This skill implements Core Data for iOS data persistence covering managed object contexts, batch operations, faulting, schema migration, NSFetchedResultsController integration, and performance optimization. It applies to Stage 5 (Development) where local data storage is implemented, Stage 6 (Code Review) where data layer correctness and migration safety are audited, and Stage 7 (Automated Testing) where Core Data tests validate data integrity.

## Competency Dimensions

| Dimension                  | Description                                                                                             | Proficiency Indicators                                                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Managed Object Context     | MOC hierarchy, parent-child contexts, thread confinement, save propagation, undo manager                | Context hierarchy matches use case (view context → background context); thread confinement strictly enforced; save propagation understood   |
| Batch Operations           | NSBatchInsertRequest, NSBatchUpdateRequest, NSBatchDeleteRequest, progress tracking, result processing  | Large datasets processed with batch operations (not individual saves); batch operations report progress; results processed correctly        |
| Faulting & Memory          | Fault objects, fault firing, relationship faults, memory footprint management, stale data handling      | Understands faulting behavior; avoids fault firing in loops; manages memory with context reset for large fetches                            |
| Schema Migration           | Lightweight migration, mapping models, custom migration policies, migration testing, version management | All schema changes have migration paths; lightweight migration enabled; custom migration policies tested; no data loss on migration         |
| NSFetchedResultsController | FRC setup, section support, cache management, delegate integration, table view coordination             | FRC efficiently drives table views; section name key path configured; cache invalidated on model changes; delegate handles all update types |

## Execution Guidance

### Core Data Stack — Production Setup

```swift
import CoreData

final class PersistentContainer {

    // MARK: - Properties

    static let shared = PersistentContainer()

    let container: NSPersistentContainer

    // Main queue context for UI
    var viewContext: NSManagedObjectContext { container.viewContext }

    // Background context for writes
    var backgroundContext: NSManagedObjectContext {
        let context = container.newBackgroundContext()
        context.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
        context.automaticallyMergesChangesFromParent = true
        return context
    }

    private init() {
        // Load model from app bundle
        let modelURL = Bundle.main.url(forResource: "AppModel", withExtension: "momd")!
        let model = NSManagedObjectModel(contentsOf: modelURL)!

        container = NSPersistentContainer(name: "AppModel", managedObjectModel: model)

        // Configure persistent store
        let storeURL = Self.applicationSupportDirectory().appendingPathComponent("AppModel.sqlite")

        let storeDescription = NSPersistentStoreDescription(url: storeURL)
        storeDescription.shouldMigrateStoreAutomatically = true
        storeDescription.shouldInferMappingModelAutomatically = true  // Lightweight migration
        storeDescription.setOption(true as NSNumber, forKey: NSPersistentHistoryTrackingKey)
        storeDescription.setOption(true as NSNumber, forKey: NSPersistentStoreRemoteChangeNotificationPostOptionKey)

        // Journal mode for performance
        storeDescription.setOption("WAL" as NSString, forKey: NSSQLitePragmasOption)

        container.persistentStoreDescriptions = [storeDescription]

        // Optimize view context
        viewContext.automaticallyMergesChangesFromParent = true
        viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
        viewContext.undoManager = nil  // Disable undo for performance (unless needed)
        viewContext.shouldDeleteInaccessibleFaults = true

        container.loadPersistentStores { _, error in
            if let error = error {
                fatalError("Failed to load persistent store: \(error)")
            }
        }

        // Setup history tracking for background context changes
        setupHistoryTracking()
    }

    // MARK: - History Tracking

    private func setupHistoryTracking() {
        let coordinator = container.persistentStoreCoordinator

        NotificationCenter.default.addObserver(
            forName: .NSPersistentStoreRemoteChange,
            object: coordinator,
            queue: .main
        ) { [weak self] _ in
            self?.mergeChangesFromHistory()
        }
    }

    private func mergeChangesFromHistory() {
        let historyRequest = NSPersistentHistoryChangeRequest.fetchHistory(after: lastHistoryToken)

        do {
            let historyResult = try viewContext.execute(historyRequest) as? NSPersistentHistoryResult
            guard let transactions = (historyResult?.result as? [NSPersistentHistoryTransaction]) else { return }

            // Merge into view context
            for transaction in transactions {
                viewContext.mergeChanges(fromContextDidSave: transaction.objectIDNotification())
            }

            // Update token
            lastHistoryToken = transactions.last?.token
        } catch {
            print("Failed to fetch history: \(error)")
        }
    }

    private var lastHistoryToken: NSPersistentHistoryToken?

    // MARK: - Helpers

    private static func applicationSupportDirectory() -> URL {
        FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
    }

    // MARK: - Save

    func saveViewContext() {
        guard viewContext.hasChanges else { return }
        do {
            try viewContext.save()
        } catch {
            print("Failed to save view context: \(error)")
            viewContext.rollback()
        }
    }

    func performBackgroundTask(_ task: @escaping (NSManagedObjectContext) -> Void) {
        container.performBackgroundTask { context in
            context.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
            task(context)
        }
    }
}
```

### Batch Operations — Large Dataset Handling

```swift
// MARK: - Batch Insert

func batchInsertUsers(users: [UserDTO]) throws {
    let context = PersistentContainer.shared.backgroundContext

    let batchRequest = NSBatchInsertRequest(
        entity: User.entity(),
        objects: users.map { userDTO -> [String: Any] in
            [
                "id": userDTO.id,
                "name": userDTO.name,
                "email": userDTO.email,
                "createdAt": userDTO.createdAt,
                "syncStatus": userDTO.syncStatus.rawValue
            ]
        }
    )

    // Process in chunks for memory efficiency
    batchRequest.resultType = .objectIDs

    try context.execute(batchRequest)
    try context.save()
}

// MARK: - Batch Insert with Progress (iOS 15+)

func batchInsertWithProgress(users: [UserDTO]) async throws {
    let context = PersistentContainer.shared.backgroundContext

    let batchRequest = NSBatchInsertRequest(
        entity: User.entity()
    ) { (managedObject: NSManagedObject, index: Int) -> Bool in
        guard index < users.count else { return true }

        let userDTO = users[index]
        if let user = managedObject as? User {
            user.id = userDTO.id
            user.name = userDTO.name
            user.email = userDTO.email
            user.createdAt = userDTO.createdAt
        }
        return false  // Continue
    }

    batchRequest.resultType = .objectIDs
    try context.execute(batchRequest)
    try context.save()
}

// MARK: - Batch Update

func batchUpdateUserSyncStatus(ids: [UUID], status: SyncStatus) throws {
    let context = PersistentContainer.shared.backgroundContext

    let fetchRequest: NSFetchRequest<NSFetchRequestResult> = User.fetchRequest()
    fetchRequest.predicate = NSPredicate(format: "id IN %@", ids.map { $0.uuidString })

    let batchRequest = NSBatchUpdateRequest(fetchRequest: fetchRequest)
    batchRequest.propertiesToUpdate = ["syncStatus": status.rawValue]
    batchRequest.resultType = .updatedObjectIDsResultType

    let result = try context.execute(batchRequest) as? NSBatchUpdateResult
    guard let objectIDs = result?.result as? [NSManagedObjectID] else { return }

    // Merge changes into view context
    let changes = [NSUpdatedObjectsKey: objectIDs]
    NSManagedObjectContext.mergeChanges(
        fromRemoteContextSave: changes,
        into: [PersistentContainer.shared.viewContext]
    )
}

// MARK: - Batch Delete

func batchDeleteUsers(ids: [UUID]) throws {
    let context = PersistentContainer.shared.backgroundContext

    let fetchRequest: NSFetchRequest<NSFetchRequestResult> = User.fetchRequest()
    fetchRequest.predicate = NSPredicate(format: "id IN %@", ids.map { $0.uuidString })

    let batchRequest = NSBatchDeleteRequest(fetchRequest: fetchRequest)
    batchRequest.resultType = .resultTypeObjectIDs

    let result = try context.execute(batchRequest) as? NSBatchDeleteResult
    guard let objectIDs = result?.result as? [NSManagedObjectID] else { return }

    // Merge changes into view context
    let changes = [NSDeletedObjectsKey: objectIDs]
    NSManagedObjectContext.mergeChanges(
        fromRemoteContextSave: changes,
        into: [PersistentContainer.shared.viewContext]
    )
}
```

### NSFetchedResultsController — Table View Integration

```swift
final class UserListDataSource: NSObject {

    // MARK: - Properties

    private let fetchedResultsController: NSFetchedResultsController<User>
    private weak var tableView: UITableView?

    init(
        context: NSManagedObjectContext,
        sortDescriptors: [NSSortDescriptor] = [
            NSSortDescriptor(key: "createdAt", ascending: false)
        ],
        sectionKeyPath: String? = nil,
        cacheName: String? = "UserListCache"
    ) {
        let fetchRequest: NSFetchRequest<User> = User.fetchRequest()
        fetchRequest.sortDescriptors = sortDescriptors
        fetchRequest.fetchBatchSize = 20  // Fetch in batches

        fetchedResultsController = NSFetchedResultsController(
            fetchRequest: fetchRequest,
            managedObjectContext: context,
            sectionNameKeyPath: sectionKeyPath,
            cacheName: cacheName
        )

        super.init()

        fetchedResultsController.delegate = self
    }

    func bind(to tableView: UITableView) throws {
        self.tableView = tableView
        try fetchedResultsController.performFetch()
        tableView.reloadData()
    }

    func object(at indexPath: IndexPath) -> User {
        fetchedResultsController.object(at: indexPath)
    }

    var sections: [NSFetchedResultsSectionInfo] {
        fetchedResultsController.sections ?? []
    }

    var numberOfSections: Int {
        sections.count
    }

    func numberOfRowsInSection(_ section: Int) -> Int {
        sections[section].numberOfObjects
    }
}

// MARK: - NSFetchedResultsControllerDelegate

extension UserListDataSource: NSFetchedResultsControllerDelegate {

    func controllerWillChangeContent(_ controller: NSFetchedResultsController<NSFetchRequestResult>) {
        tableView?.beginUpdates()
    }

    func controllerDidChangeContent(_ controller: NSFetchedResultsController<NSFetchRequestResult>) {
        tableView?.endUpdates()
    }

    func controller(
        _ controller: NSFetchedResultsController<NSFetchRequestResult>,
        didChange anObject: Any,
        at indexPath: IndexPath?,
        for type: NSFetchedResultsChangeType,
        newIndexPath: IndexPath?
    ) {
        guard let tableView = tableView else { return }

        switch type {
        case .insert:
            if let newIndexPath = newIndexPath {
                tableView.insertRows(at: [newIndexPath], with: .automatic)
            }
        case .delete:
            if let indexPath = indexPath {
                tableView.deleteRows(at: [indexPath], with: .automatic)
            }
        case .update:
            if let indexPath = indexPath,
               let cell = tableView.cellForRow(at: indexPath) as? UserCell {
                let user = controller.object(at: indexPath) as! User
                cell.configure(with: user)
            }
        case .move:
            if let indexPath = indexPath, let newIndexPath = newIndexPath {
                tableView.deleteRows(at: [indexPath], with: .automatic)
                tableView.insertRows(at: [newIndexPath], with: .automatic)
            }
        @unknown default:
            break
        }
    }

    func controller(
        _ controller: NSFetchedResultsController<NSFetchRequestResult>,
        didChange sectionInfo: NSFetchedResultsSectionInfo,
        atSectionIndex sectionIndex: Int,
        for type: NSFetchedResultsChangeType
    ) {
        guard let tableView = tableView else { return }

        switch type {
        case .insert:
            tableView.insertSections(IndexSet(integer: sectionIndex), with: .automatic)
        case .delete:
            tableView.deleteSections(IndexSet(integer: sectionIndex), with: .automatic)
        default:
            break
        }
    }
}
```

### Schema Migration — Production Discipline

**Model versioning workflow:**

1. Select `.xcdatamodeld` file in Xcode
2. Editor → Add Model Version → name it `AppModel_v2`
3. Select new version → File Inspector → Set Current Version
4. Make schema changes in new version
5. Enable lightweight migration (already configured in stack)

**Lightweight migration — automatic changes:**

| Change                         | Supported      | Notes                                  |
| ------------------------------ | -------------- | -------------------------------------- |
| Add attribute                  | ✅ Yes         | Default value required if non-optional |
| Remove attribute               | ✅ Yes         | Data lost                              |
| Rename attribute               | ✅ Yes         | Requires renaming identifier in model  |
| Add entity                     | ✅ Yes         |                                        |
| Remove entity                  | ✅ Yes         | Data lost                              |
| Add relationship               | ✅ Yes         |                                        |
| Remove relationship            | ✅ Yes         |                                        |
| Change optional → non-optional | ⚠️ Conditional | Requires default value                 |
| Change attribute type          | ❌ No          | Requires custom migration              |

**Custom migration policy:**

```swift
// When lightweight migration isn't sufficient
class UserV1ToV2MigrationPolicy: NSEntityMigrationPolicy {

    override func createDestinationInstances(
        forSource sInstance: NSManagedObject,
        in mapping: NSEntityMapping,
        manager: NSMigrationManager
    ) throws {
        // Create new instance
        let newEntityName = mapping.destinationEntityName!
        let dInstance = NSEntityDescription.insertNewObject(
            forEntityName: newEntityName,
            into: manager.destinationContext
        )

        // Copy attributes
        for key in sInstance.entity.attributesByName.keys {
            let value = sInstance.primitiveValue(forKey: key)
            dInstance.setPrimitiveValue(value, forKey: key)
        }

        // Transform: split fullName into firstName + lastName
        if let fullName = sInstance.primitiveValue(forKey: "fullName") as? String {
            let components = fullName.split(separator: " ", maxSplits: 1)
            dInstance.setPrimitiveValue(
                String(components.first ?? ""),
                forKey: "firstName"
            )
            dInstance.setPrimitiveValue(
                components.count > 1 ? String(components[1]) : "",
                forKey: "lastName"
            )
        }

        // Copy relationships
        for key in sInstance.entity.relationshipsByName.keys {
            let value = sInstance.primitiveValue(forKey: key)
            dInstance.setPrimitiveValue(value, forKey: key)
        }
    }
}
```

**Migration testing:**

```swift
import XCTest
import CoreData

final class MigrationTests: XCTestCase {

    func test_v1_to_v2_migration_preservesData() throws {
        // Create store at v1
        let v1ModelURL = Bundle.main.url(forResource: "AppModel", withExtension: "momd")!
            .appendingPathComponent("AppModel.mom")
        let v1Model = NSManagedObjectModel(contentsOf: v1ModelURL)!

        let v1Container = NSPersistentContainer(
            name: "AppModel",
            managedObjectModel: v1Model
        )
        v1Container.persistentStoreDescriptions.first?.url =
            FileManager.default.temporaryDirectory.appendingPathComponent("test_migration.sqlite")

        // Create test data at v1
        let v1Context = v1Container.viewContext
        let v1User = NSEntityDescription.insertNewObject(
            forEntityName: "User",
            into: v1Context
        ) as! NSManagedObject
        v1User.setValue("full_name", forKey: "fullName")
        v1User.setValue("user@test.com", forKey: "email")
        try v1Context.save()

        // Migrate to v2
        let v2ModelURL = Bundle.main.url(forResource: "AppModel", withExtension: "momd")!
        let v2Model = NSManagedObjectModel(contentsOf: v2ModelURL)!

        let v2Container = NSPersistentContainer(
            name: "AppModel",
            managedObjectModel: v2Model
        )
        v2Container.persistentStoreDescriptions.first?.url =
            v1Container.persistentStoreDescriptions.first?.url

        // This triggers migration
        v2Container.loadPersistentStores { _, error in
            XCTAssertNil(error, "Migration failed: \(String(describing: error))")
        }

        // Verify data preserved
        let v2Context = v2Container.viewContext
        let fetchRequest: NSFetchRequest<NSFetchRequestResult> = NSFetchRequest(entityName: "User")
        let results = try v2Context.fetch(fetchRequest) as! [NSManagedObject]

        XCTAssertEqual(results.count, 1)
        let migratedUser = results[0]
        XCTAssertEqual(migratedUser.value(forKey: "email") as? String, "user@test.com")
        // Verify fullName was split
        XCTAssertEqual(migratedUser.value(forKey: "firstName") as? String, "full")
        XCTAssertEqual(migratedUser.value(forKey: "lastName") as? String, "name")
    }
}
```

## Pipeline Integration

- **Stage 3 (Architecture):** ADRs define data persistence strategy (Core Data vs SQLite vs Realm). Schema design documented.
- **Stage 4 (Implementation Plan):** Core Data tasks include model design, stack setup, migration paths, and FRC integration.
- **Stage 5 (Development):** Primary skill for local data persistence. All Core Data entities, contexts, batch operations, and migrations.
- **Stage 6 (Code Review):** Core Data review: thread confinement, batch operation correctness, migration completeness, FRC delegate implementation.
- **Stage 7 (Automated Testing):** Migration tests, batch operation tests, data integrity tests, FRC integration tests.

## Quality Standards

- **Zero** Core Data access from wrong thread — strict context confinement enforced
- **100%** schema changes have migration paths — no `shouldMigrateStoreAutomatically = false`
- **Lightweight migration** enabled for all stores — automatic inference of mapping models
- Batch operations used for datasets **>100 records** — no individual saves for bulk operations
- `fetchBatchSize` set for all fetch requests returning **>20 records**
- **Zero** fault firing in loops — prefetch relationships with `setRelationshipKeyPathsForPrefetching`
- NSFetchedResultsController used for **all table view data sources** — no manual fetch-and-reload
- FRC cache invalidated on **model changes** — cache name nil during development
- Persistent history tracking enabled for **multi-context synchronization**
- View context `undoManager` disabled for performance (unless undo is a feature requirement)
- All Core Data migrations tested with **migration test suite** — data preservation verified
