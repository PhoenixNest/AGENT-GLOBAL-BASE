---
inclusion: fileMatch
fileMatchPattern: "**/unity-project/**,**/*.unity,**/*.prefab,**/*.asset,**/*.cs"
description: Unity 6.3 LTS development patterns and best practices
version: "1.0.0"
---

# Unity 6.3 LTS Development Patterns

**Authority:** Casual Games Studio technical standards  
**Applies To:** All Unity development in the Casual Games Studio

---

## Unity Version

**Engine:** Unity 6.3 LTS (Long Term Support)

## Project Structure

### Recommended Folder Organization

```
Assets/
├── _Project/                  # Project-specific assets
│   ├── Art/
│   │   ├── Characters/
│   │   ├── Environment/
│   │   ├── UI/
│   │   └── VFX/
│   ├── Audio/
│   │   ├── Music/
│   │   ├── SFX/
│   │   └── Mixers/
│   ├── Prefabs/
│   ├── Scenes/
│   ├── Scripts/
│   │   ├── Gameplay/
│   │   ├── UI/
│   │   ├── Systems/
│   │   └── Utilities/
│   └── Settings/
├── Plugins/                   # Third-party plugins
├── Resources/                 # Runtime-loaded assets (use sparingly)
└── StreamingAssets/           # Platform-specific assets
```

### Assembly Definitions

Use Assembly Definitions to modularize code and reduce compilation time:

```
Assets/_Project/Scripts/
├── Gameplay/
│   └── Gameplay.asmdef
├── UI/
│   └── UI.asmdef
├── Systems/
│   └── Systems.asmdef
└── Utilities/
    └── Utilities.asmdef
```

## C# Coding Standards

### Naming Conventions

- **Classes/Structs:** PascalCase (`PlayerController`, `GameManager`)
- **Methods:** PascalCase (`MovePlayer`, `CalculateScore`)
- **Properties:** PascalCase (`Health`, `MaxSpeed`)
- **Fields (private):** camelCase with underscore (`_currentHealth`, `_playerTransform`)
- **Fields (public):** PascalCase (`PlayerName`, `MaxHealth`)
- **Constants:** UPPER_SNAKE_CASE (`MAX_PLAYERS`, `DEFAULT_SPEED`)
- **Interfaces:** PascalCase with I prefix (`IPoolable`, `IDamageable`)

### Code Organization

```csharp
using System;
using UnityEngine;

namespace ProjectName.Gameplay
{
    /// <summary>
    /// Handles player movement and input.
    /// </summary>
    public class PlayerController : MonoBehaviour
    {
        #region Serialized Fields
        [SerializeField] private float _moveSpeed = 5f;
        [SerializeField] private Rigidbody2D _rigidbody;
        #endregion

        #region Private Fields
        private Vector2 _moveInput;
        private bool _isMoving;
        #endregion

        #region Unity Lifecycle
        private void Awake()
        {
            // Initialize components
        }

        private void Update()
        {
            // Handle input
        }

        private void FixedUpdate()
        {
            // Handle physics
        }
        #endregion

        #region Public Methods
        public void SetMoveSpeed(float speed)
        {
            _moveSpeed = speed;
        }
        #endregion

        #region Private Methods
        private void HandleMovement()
        {
            // Movement logic
        }
        #endregion
    }
}
```

## Performance Best Practices

### Object Pooling

Implement object pooling for frequently instantiated/destroyed objects:

```csharp
public class ObjectPool : MonoBehaviour
{
    [SerializeField] private GameObject _prefab;
    [SerializeField] private int _initialSize = 10;

    private Queue<GameObject> _pool = new Queue<GameObject>();

    private void Awake()
    {
        for (int i = 0; i < _initialSize; i++)
        {
            GameObject obj = Instantiate(_prefab);
            obj.SetActive(false);
            _pool.Enqueue(obj);
        }
    }

    public GameObject Get()
    {
        if (_pool.Count > 0)
        {
            GameObject obj = _pool.Dequeue();
            obj.SetActive(true);
            return obj;
        }
        return Instantiate(_prefab);
    }

    public void Return(GameObject obj)
    {
        obj.SetActive(false);
        _pool.Enqueue(obj);
    }
}
```

### Avoid GetComponent in Update

Cache component references in Awake/Start:

```csharp
// Bad
private void Update()
{
    GetComponent<Rigidbody2D>().velocity = Vector2.zero;
}

// Good
private Rigidbody2D _rigidbody;

private void Awake()
{
    _rigidbody = GetComponent<Rigidbody2D>();
}

private void Update()
{
    _rigidbody.velocity = Vector2.zero;
}
```

### Use StringBuilder for String Concatenation

```csharp
// Bad
string result = "";
for (int i = 0; i < 100; i++)
{
    result += i.ToString();
}

// Good
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 100; i++)
{
    sb.Append(i);
}
string result = sb.ToString();
```

## Addressables System

Use Addressables for efficient asset management:

```csharp
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

public class AssetLoader : MonoBehaviour
{
    [SerializeField] private AssetReference _assetReference;

    private async void Start()
    {
        AsyncOperationHandle<GameObject> handle = _assetReference.LoadAssetAsync<GameObject>();
        await handle.Task;

        if (handle.Status == AsyncOperationStatus.Succeeded)
        {
            GameObject obj = handle.Result;
            Instantiate(obj);
        }
    }
}
```

## Dependency Injection

Use a DI framework (Zenject or VContainer) for better code architecture:

```csharp
// VContainer example
public class GameInstaller : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        builder.Register<IPlayerService, PlayerService>(Lifetime.Singleton);
        builder.RegisterComponentInHierarchy<PlayerController>();
    }
}

public class PlayerController : MonoBehaviour
{
    private IPlayerService _playerService;

    [Inject]
    public void Construct(IPlayerService playerService)
    {
        _playerService = playerService;
    }
}
```

## UI Best Practices

### Canvas Setup

- Use multiple canvases for different update frequencies
- Static UI: Canvas with "Screen Space - Overlay"
- Dynamic UI: Separate canvas with "Screen Space - Camera"
- World space UI: Canvas with "World Space"

### UI Optimization

- Use Canvas Groups for batch enabling/disabling
- Disable raycast target on non-interactive elements
- Use sprite atlases to reduce draw calls
- Implement UI object pooling for dynamic lists

## Mobile Optimization

### Target Performance

- **Frame Rate:** 60 FPS on mid-range devices
- **Memory:** < 1GB RAM usage
- **Build Size:** < 150MB initial download
- **Battery:** Minimal battery drain

### Optimization Techniques

- Use texture compression (ASTC for mobile)
- Implement LOD (Level of Detail) for 3D models
- Use occlusion culling
- Optimize physics (reduce collider complexity)
- Use static batching for static objects
- Use GPU instancing for repeated objects

## Testing in Unity

### Unit Testing

```csharp
using NUnit.Framework;
using UnityEngine;

public class PlayerTests
{
    [Test]
    public void PlayerHealth_DecreasesOnDamage()
    {
        // Arrange
        GameObject playerObj = new GameObject();
        Player player = playerObj.AddComponent<Player>();
        player.Health = 100;

        // Act
        player.TakeDamage(20);

        // Assert
        Assert.AreEqual(80, player.Health);
    }
}
```

### Play Mode Testing

```csharp
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using System.Collections;

public class GameplayTests
{
    [UnityTest]
    public IEnumerator Player_MovesForward()
    {
        // Arrange
        GameObject playerObj = new GameObject();
        PlayerController player = playerObj.AddComponent<PlayerController>();
        Vector3 startPos = player.transform.position;

        // Act
        player.MoveForward();
        yield return new WaitForSeconds(1f);

        // Assert
        Assert.Greater(player.transform.position.z, startPos.z);
    }
}
```

## Version Control

### .gitignore for Unity

```
# Unity generated
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uild/
[Bb]uilds/
[Ll]ogs/
[Uu]ser[Ss]ettings/

# Visual Studio cache
.vs/

# Rider cache
.idea/

# OS generated
.DS_Store
Thumbs.db
```

### Git LFS

Use Git LFS for large binary files:

```
*.psd
*.png
*.jpg
*.fbx
*.unity
*.asset
*.prefab
```

## Related Steering Files

- `casual-games-pipeline.md` — Studio pipeline overview
- `game-design.md` — Game design patterns

## Resources

- Unity Documentation: https://docs.unity3d.com/
- Unity Best Practices: https://unity.com/how-to/best-practices
- Unity Performance Optimization: https://docs.unity3d.com/Manual/BestPracticeUnderstandingPerformanceInUnity.html
