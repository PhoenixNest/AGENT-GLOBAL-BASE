---
version: "1.0.0"
---

------------------------ | -------------- | -------------------------------------- |
| Add attribute | ✅ Yes | Default value required if non-optional |
| Remove attribute | ✅ Yes | Data lost |
| Rename attribute | ✅ Yes | Requires renaming identifier in model |
| Add entity | ✅ Yes | |
| Remove entity | ✅ Yes | Data lost |
| Add relationship | ✅ Yes | |
| Remove relationship | ✅ Yes | |
| Change optional → non-optional | ⚠️ Conditional | Requires default value |
| Change attribute type | ❌ No | Requires custom migration |

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
