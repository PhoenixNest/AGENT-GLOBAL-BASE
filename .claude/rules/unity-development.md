---
paths:
  - "**/unity-project/**"
  - "**/*.unity"
  - "**/*.prefab"
  - "**/*.asset"
  - "**/*.cs"
description: Unity 6.3 LTS development patterns and best practices
---

# Unity 6.3 LTS Development Patterns

**Applies To:** All Unity development in the Casual Games Studio

---

## C# Naming Conventions

| Element            | Convention                                   |
| ------------------ | -------------------------------------------- |
| Classes/Structs    | PascalCase (`PlayerController`)              |
| Methods/Properties | PascalCase (`MovePlayer`)                    |
| Private fields     | camelCase with underscore (`_currentHealth`) |
| Constants          | UPPER_SNAKE_CASE (`MAX_PLAYERS`)             |
| Interfaces         | PascalCase with I prefix (`IPoolable`)       |

---

## Key Performance Practices

- Cache component references in `Awake()`/`Start()` — never call `GetComponent` in `Update()`
- Use `ObjectPool` for frequently instantiated/destroyed objects
- Use `StringBuilder` for string concatenation in loops
- Use `Addressables` for asset management, not `Resources.Load`
- Use Assembly Definitions to reduce compilation time

---

## Mobile Performance Targets

- **Frame Rate:** 60 FPS on mid-range devices
- **Memory:** < 1GB RAM usage
- **Build Size:** < 150MB initial download

---

## Dependency Injection

Use Zenject or VContainer. Never use static singletons for shared state.

---

## Testing

- **Unit tests:** NUnit in Edit Mode
- **Play Mode tests:** `UnityTest` attribute with `IEnumerator`
- **Coverage target:** > 70% on business logic scripts

---

## Git LFS

Use Git LFS for: `*.psd`, `*.png`, `*.jpg`, `*.fbx`, `*.unity`, `*.asset`, `*.prefab`
