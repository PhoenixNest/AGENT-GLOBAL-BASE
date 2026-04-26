---
name: ios-data-networking-core-data
description: "Core Data for iOS persistence — managed object contexts, batch operations, faulting, schema migration, NSFetchedResultsController, and performance optimization. Owned by Seo-Yeon Park (iOS Lead). Use during Stage 5 (Development) for local data storage and Stage 6 (Code Review) for migration safety audits. Trigger: core data, nsmanagedobjectcontext, batch insert, batch update, schema migration, lightweight migration, nsfetchedresultscontroller, faulting, persistent container."
prerequisites:
  - ios-infrastructure-ios-implementation

version: "1.0.0"
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

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
