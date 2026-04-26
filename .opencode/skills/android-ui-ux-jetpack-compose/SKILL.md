---
name: android-ui-ux-jetpack-compose
description: Jetpack Compose declarative UI development — state hoisting and unidirectional data flow, recomposition optimization with @Stable/@Immutable, Material 3 theming with design tokens, animation APIs (animate*AsState, Transition, SharedElement), and reduced motion support. Owned by Jan Kowalski (Android Engineer). Use during Stage 5 (Development) for Android UI implementation and Stage 6 (Code Review) for composable correctness and performance. Trigger: jetpack compose, compose UI, state hoisting, recomposition, material 3, theming, compose animation, shared element transition, declarative UI.
prerequisites:
  - android-language-core-kotlin-advanced

version: "1.0.0"
---

# Jetpack Compose

**Category:** Mobile Engineering — Android UI
**Owner:** Android Engineer (Jan Kowalski)

## Overview

This skill covers Jetpack Compose declarative UI development including state hoisting, recomposition optimization, theming with Material 3, and animation APIs. It applies to Stage 5 (Development) where all Android UI is built with Compose, Stage 6 (Code Review) where composables are reviewed for correctness and performance, and Stage 8 (Integrity Verification) where the CDO verifies IDS specifications are realized in Compose implementation.

## Competency Dimensions

| Dimension                  | Description                                                                                              | Proficiency Indicators                                                                                                             |
| -------------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Declarative UI             | Composable functions, composition lifecycle, slot APIs, mental model shift from imperative UI            | Composables are pure functions of state; no direct View manipulation; composition follows declarative mental model                 |
| State Hoisting             | State flow direction, unidirectional data flow, stateless vs stateful composables, event callbacks       | State hoisted to caller; composables accept state + events as parameters; zero internal mutable state in reusable components       |
| Recomposition Optimization | Stability, derivedStateOf, remember, recomposition scope, skippable composables                          | Minimal unnecessary recompositions; verified via Layout Inspector; uses `@Stable`/`@Immutable` annotations correctly               |
| Theming & Design Tokens    | MaterialTheme, color schemes, typography scale, shape system, dark theme support, dynamic color          | Theme follows IDS design tokens; dark theme fully supported; dynamic color (Material You) on Android 12+                           |
| Animations                 | animate\*AsState, Transition API, AnimatedContent, shared element transitions, gesture-driven animations | Animations are performant (60fps); interruptible; respect system animation scale settings; accessible to users with reduced motion |

## Execution Guidance

### Composable Function Design — Production Patterns

**Stateless composable (preferred pattern):**

```kotlin
@Composable
fun UserCard(
    user: UserDisplayModel,
    isExpanded: Boolean,
    onExpandToggle: () -> Unit,
    onDelete: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable(onClick = onExpandToggle),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                UserAvatar(
                    avatarUrl = user.avatarUrl,
                    userName = user.name,
                    modifier = Modifier.size(48.dp)
                )
                Column(modifier = Modifier.weight(1f).padding(start = 12.dp)) {
                    Text(
                        text = user.name,
                        style = MaterialTheme.typography.titleMedium
                    )
                    Text(
                        text = user.email,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                IconButton(onClick = onDelete) {
                    Icon(
                        Icons.Default.Delete,
                        contentDescription = "Delete ${user.name}"
                    )
                }
            }
            AnimatedVisibility(visible = isExpanded) {
                UserDetailSection(
                    bio = user.bio,
                    joinDate = user.joinDate,
                    modifier = Modifier.padding(top = 12.dp)
                )
            }
        }
    }
}
```

**Stateful wrapper (only when internal state is truly encapsulated):**

```kotlin
@Composable
fun SearchBar(
    onQueryChanged: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    // Internal state hoisted to this composable — caller doesn't need to manage it
    var query by remember { mutableStateOf("") }

    OutlinedTextField(
        value = query,
        onValueChange = {
            query = it
            onQueryChanged(it)
        },
        leadingIcon = {
            Icon(Icons.Default.Search, contentDescription = null)
        },
        trailingIcon = {
            if (query.isNotEmpty()) {
                IconButton(onClick = { query = "" }) {
                    Icon(Icons.Default.Clear, contentDescription = "Clear search")
                }
            }
        },
        placeholder = { Text("Search...") },
        singleLine = true,
        modifier = modifier.fillMaxWidth()
    )
}
```

### State Hoisting Pattern — Unidirectional Data Flow

```kotlin
// Screen-level composable owns state
@Composable
fun UserListScreen(
    viewModel: UserListViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    UserListContent(
        state = uiState,
        onRefresh = { viewModel.sendIntent(UserListIntent.Refresh) },
        onUserClick = { viewModel.sendIntent(UserListIntent.UserSelected(it)) },
        onDeleteUser = { viewModel.sendIntent(UserListIntent.DeleteUser(it)) }
    )
}

// Content composable is stateless — receives state and events
@Composable
private fun UserListContent(
    state: UserListUiState,
    onRefresh: () -> Unit,
    onUserClick: (String) -> Unit,
    onDeleteUser: (String) -> Unit
) {
    PullToRefreshBox(
        isRefreshing = state.isLoading,
        onRefresh = onRefresh
    ) {
        when {
            state.error != null -> ErrorView(
                message = state.error,
                onRetry = onRefresh
            )
            state.users.isEmpty() -> EmptyStateView()
            else -> LazyColumn {
                items(state.users, key = { it.id }) { user ->
                    UserCard(
                        user = user,
                        isExpanded = state.expandedUserIds.contains(user.id),
                        onExpandToggle = { onUserClick(user.id) },
                        onDelete = { onDeleteUser(user.id) }
                    )
                }
            }
        }
    }
}
```

### Recomposition Optimization

**Understanding stability:**

```kotlin
// UNSTABLE — causes unnecessary recompositions
data class User(var name: String, var age: Int)  // mutable var = unstable

// STABLE — safe for composition caching
data class User(val name: String, val age: Int)  // immutable val = stable

// EXPLICITLY STABLE — for classes Compose can't infer
@Stable
interface UiState {
    val isLoading: Boolean
    val users: List<UserDisplayModel>
}

// IMMUTABLE — no mutable properties at all
@Immutable
data class AppConfig(
    val apiBaseUrl: String,
    val featureFlags: Map<String, Boolean>
)
```

**Optimization with derivedStateOf:**

```kotlin
@Composable
fun ScrollableListWithFAB(
    items: List<Item>,
    modifier: Modifier = Modifier
) {
    val listState = rememberLazyListState()

    // Only recompose when the derived value actually changes
    val showFAB by remember {
        derivedStateOf {
            listState.firstVisibleItemIndex > 0 ||
                listState.firstVisibleItemScrollOffset > 100
        }
    }

    Box(modifier = modifier) {
        LazyColumn(state = listState) {
            items(items) { item ->
                ItemCard(item)
            }
        }
        AnimatedVisibility(
            visible = showFAB,
            enter = slideInVertically(initialOffsetY = { it }),
            exit = slideOutVertically(targetOffsetY = { it })
        ) {
            FloatingActionButton(
                onClick = { /* scroll to top */ },
                modifier = Modifier.align(Alignment.BottomEnd).padding(16.dp)
            ) {
                Icon(Icons.Default.ArrowUpward, contentDescription = "Scroll to top")
            }
        }
    }
}
```

**Verification via Layout Inspector:**

- Enable "Show Recomposition Counts" in Layout Inspector
- Blue highlight = composables recomposed once (expected)
- Purple highlight = composables recomposed multiple times (investigate)
- Target: <2 recompositions per frame during normal interaction

### Material 3 Theming — Design Token Mapping

```kotlin
// theme/Theme.kt
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = AppTypography,
        shapes = AppShapes,
        content = content
    )
}

// theme/Color.kt
val LightColorScheme = lightColorScheme(
    primary = Color(0xFF6750A4),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFEADDFF),
    onPrimaryContainer = Color(0xFF21005D),
    secondary = Color(0xFF625B71),
    surface = Color(0xFFFFFBFE),
    onSurface = Color(0xFF1C1B1F),
    error = Color(0xFFBA1A1A)
)

// theme/Type.kt
val AppTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 57.sp,
        lineHeight = 64.sp,
        letterSpacing = (-0.25).sp
    ),
    // ... other text styles mapped from IDS
)
```

### Animation APIs — Production Patterns

**Simple state-driven animation:**

```kotlin
@Composable
fun AnimatedCounter(count: Int) {
    val animatedCount by animateIntAsState(
        targetValue = count,
        animationSpec = tween(durationMillis = 300, easing = FastOutSlowInEasing),
        label = "counter"  // Required for Android Studio animation inspector
    )

    Text(
        text = animatedCount.toString(),
        style = MaterialTheme.typography.headlineMedium
    )
}
```

**Complex multi-property animation with Transition:**

```kotlin
@Composable
fun CardExpandAnimation(
    isExpanded: Boolean,
    content: @Composable () -> Unit
) {
    val transition = updateTransition(targetState = isExpanded, label = "card_expand")

    val cardElevation by transition.animateDp(
        transitionSpec = { tween(durationMillis = 250) },
        label = "elevation"
    ) { expanded ->
        if (expanded) 8.dp else 2.dp
    }

    val cardPadding by transition.animateDp(
        transitionSpec = { tween(durationMillis = 250) },
        label = "padding"
    ) { expanded ->
        if (expanded) 24.dp else 16.dp
    }

    Card(elevation = CardDefaults.cardElevation(cardElevation)) {
        Column(modifier = Modifier.padding(cardPadding)) {
            content()
        }
    }
}
```

**Shared element transitions (Compose 1.7+):**

```kotlin
@OptIn(ExperimentalSharedTransitionApi::class)
@Composable
fun UserListToDetailTransition(
    users: List<User>,
    selectedUser: User?,
    onUserSelected: (User) -> Unit,
    onBack: () -> Unit
) {
    SharedTransitionLayout {
        AnimatedContent(targetState = selectedUser, label = "user_detail") { user ->
            if (user == null) {
                UserList(users, onUserSelected)
            } else {
                UserDetail(
                    user = user,
                    onBack = onBack,
                    sharedTransitionScope = this@SharedTransitionLayout
                )
            }
        }
    }
}
```

### Respecting Reduced Motion

```kotlin
@Composable
fun RespectReducedMotionAnimation(
    targetValue: Boolean,
    content: @Composable (Boolean) -> Unit
) {
    val accessibilityManager = LocalAccessibilityManager.current
    val animationSpec: AnimationSpec<Boolean> = if (accessibilityManager?.animationScale == 0f) {
        // User has disabled animations — snap immediately
        snap()
    } else {
        tween(durationMillis = 300)
    }

    val animatedValue by animateBoolAsState(
        targetValue = targetValue,
        animationSpec = animationSpec,
        label = "reduced_motion_respectful"
    )

    content(animatedValue)
}
```

## Pipeline Integration

- **Stage 2 (Design):** IDS specifies visual design, interaction patterns, and animation behaviors. This skill translates IDS into Compose implementation.
- **Stage 3 (Architecture):** ADRs establish Compose as the UI framework. UML component diagrams define composable hierarchy and state flow.
- **Stage 5 (Development):** Primary skill for Android UI development. All screens built as Composable functions following stateless/stateful patterns.
- **Stage 6 (Code Review):** Compose review checklist: state hoisting correctness, recomposition optimization, theming conformance, animation performance, accessibility semantics.
- **Stage 8 (Integrity Verification):** CDO verifies all IDS visual and interaction specifications are realized. Layout Inspector used to verify recomposition efficiency.

## Quality Standards

- **100%** composables follow stateless pattern (state hoisted to caller) except for truly encapsulated internal state
- Recomposition count **<2 per frame** during normal interaction (verified via Layout Inspector)
- **100%** text styles use MaterialTheme typography — no hardcoded text sizes
- **100%** colors sourced from MaterialTheme colorScheme — no hardcoded color values
- Dark theme **fully functional** on all screens — no visibility or contrast issues
- Dynamic color (Material You) supported on Android 12+ devices
- All animations specify `label` parameter for debugging
- Animations respect system animation scale — snap behavior when animations disabled
- ContentDescription provided for all meaningful Compose UI elements
- All composables accept `modifier: Modifier = Modifier` as first optional parameter
- No direct View interop (`AndroidView`) unless wrapping a third-party SDK with no Compose equivalent
