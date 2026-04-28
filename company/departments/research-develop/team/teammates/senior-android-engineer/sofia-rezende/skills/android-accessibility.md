---
version: "1.0.0"
---

| Competency                      | Description                                                                                           | Quality Criteria                                                                                                                                               |
| ------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| WCAG 2.1 AA Compliance          | Understanding of perceivable, operable, understandable, robust (POUR) principles as applied to mobile | Every screen passes automated a11y scan; all interactive elements have meaningful labels; color contrast ratios meet 4.5:1 minimum                             |
| TalkBack & Screen Reader        | ContentDescription, accessibility traversal order, custom accessibility actions, state announcement   | TalkBack users can complete all core flows without sighted assistance; custom actions for complex gestures; live regions for dynamic content                   |
| Dynamic Font Scaling            | sp-based dimensions, ConstraintLayout chains, ScrollView fallbacks, maximum scale testing             | App remains usable at 200% font scale; no text truncation or overlap; horizontal scrolling only when semantically appropriate                                  |
| Accessibility Testing           | Accessibility Scanner, TalkBack manual testing, Espresso a11y checks, axe DevTools                    | Automated a11y checks in CI pipeline; manual TalkBack test script executed per release; accessibility defects tracked with same severity as functional defects |
| Touch Target & Focus Management | Minimum 48dp touch targets, focus ordering, touch delegation, clear focus indicators                  | All touch targets meet 48x48dp minimum (or have adequate spacing); logical focus order; visible focus state for keyboard/D-pad navigation                      |

## Execution Guidance

### WCAG 2.1 AA — Mobile Mapping

| WCAG Criterion               | Mobile Implementation                                                                         | Verification                                         |
| ---------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| 1.1.1 Non-text Content       | ContentDescription for all meaningful images; `importantForAccessibility="no"` for decorative | Accessibility Scanner; TalkBack test                 |
| 1.3.1 Info and Relationships | Semantic view hierarchy; heading structure; group related elements                            | TalkBack navigation by headings                      |
| 1.3.4 Orientation            | Supports both portrait and landscape; no orientation lock without justification               | Manual rotation test                                 |
| 1.4.3 Contrast (Minimum)     | 4.5:1 for normal text, 3:1 for large text (18pt or 14pt bold)                                 | Color contrast analyzer; automated scan              |
| 1.4.4 Resize Text            | Supports system font scaling up to 200% without loss of content                               | `adb shell settings put system font_scale 2.0`       |
| 2.1.1 Keyboard               | All functionality available via D-pad/keyboard; no gesture-only interactions                  | D-pad navigation test; external keyboard test        |
| 2.4.3 Focus Order            | Logical focus traversal matching visual reading order                                         | TalkBack swiping test; `nextFocusForward` attributes |
| 2.4.7 Focus Visible          | Visible focus indicator for all interactive elements                                          | Visual inspection with D-pad navigation              |
| 4.1.2 Name, Role, Value      | accessibilityLabel, accessibilityRole, accessibilityState set correctly                       | Accessibility Inspector; TalkBack announcement       |

### Compose Accessibility — Production Patterns

**ContentDescription and semantics:**

```kotlin
@Composable
fun UserAvatar(
    imageUrl: String,
    userName: String,
    isOnline: Boolean,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    Box(
        modifier = modifier
            .size(48.dp)  // Minimum touch target
            .clickable(
                onClickLabel = "Open profile for $userName",
                onClick = onClick
            )
            .semantics {
                contentDescription = "$userName profile picture${if (isOnline) ", online" else ", offline"}"
                role = Role.Button
                stateDescription = if (isOnline) "Online" else "Offline"
            }
    ) {
        AsyncImage(
            model = imageUrl,
            contentDescription = null, // Decorative — context provided by parent
            modifier = Modifier.fillMaxSize()
        )
        OnlineIndicator(isOnline)
    }
}
```

**Critical rule:** `contentDescription` should describe the **purpose and state**, not the visual appearance. "Add to cart button" not "Green plus icon."

**Custom accessibility actions for complex interactions:**

```kotlin
@Composable
fun SwipeableTaskItem(
    task: Task,
    onToggleComplete: () -> Unit,
    onDelete: () -> Unit,
    onSnooze: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .semantics {
                contentDescription = buildString {
                    append("Task: ${task.title}")
                    if (task.isCompleted) append(", completed")
                    append(", due ${task.dueDate}")
                    if (task.priority == Priority.HIGH) append(", high priority")
                }
                // Custom actions for TalkBack users who can't swipe
                customActions = listOf(
                    CustomAccessibilityAction(
                        label = if (task.isCompleted) "Mark incomplete" else "Mark complete",
                        action = { onToggleComplete(); true }
                    ),
                    CustomAccessibilityAction(
                        label = "Delete task",
                        action = { onDelete(); true }
                    ),
                    CustomAccessibilityAction(
                        label = "Snooze task",
                        action = { onSnooze(); true }
                    )
                )
            }
    ) {
        // Visual content
    }
}
```

**Live regions for dynamic content announcements:**

```kotlin
@Composable
fun CartBadge(itemCount: Int) {
    Box(
        modifier = Modifier.semantics {
            // Announce changes to screen reader users
            liveRegion = LiveRegionMode.Polite
            contentDescription = "Shopping cart, $itemCount item${if (itemCount != 1) "s" else ""}"
        }
    ) {
        Icon(Icons.Default.ShoppingCart, contentDescription = null)
        if (itemCount > 0) {
            Text(
                text = itemCount.toString(),
                modifier = Modifier.align(Alignment.TopEnd)
            )
        }
    }
}
```

### Dynamic Font Scaling — Resilient Layouts

**All text dimensions in `sp`, all layout dimensions in `dp`. Test at all font scale levels:**

```kotlin
@Composable
fun ArticleCard(
    title: String,
    summary: String,
    author: String,
    modifier: Modifier = Modifier
) {
    Card(modifier = modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier
                .padding(16.dp)
                .verticalScroll(rememberScrollState())  // Scrollable at large fonts
        ) {
            Text(
                text = title,
                style = MaterialTheme.typography.headlineSmall,
                modifier = Modifier.padding(bottom = 8.dp)
            )
            Text(
                text = summary,
                style = MaterialTheme.typography.bodyMedium,
                maxLines = 3,  // Prevent excessive expansion
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.padding(bottom = 8.dp)
            )
            Text(
                text = "By $author",
                style = MaterialTheme.typography.labelMedium
            )
        }
    }
}
```

**Font scale testing via ADB:**

```bash
# Test at different font scales
adb shell settings put system font_scale 1.0   # 100% (default)
adb shell settings put system font_scale 1.3   # 130%
adb shell settings put system font_scale 1.5   # 150%
adb shell settings put system font_scale 2.0   # 200%

# Reset to default
adb shell settings put system font_scale 1.0
```

**Maximum font scale detection and adaptation:**

```kotlin
@Composable
fun AdaptiveText(
    text: String,
    style: TextStyle,
    maxLinesAtLargeFont: Int = 2,
    modifier: Modifier = Modifier
) {
    val density = LocalDensity.current
    val fontScale = density.fontScale

    Text(
        text = text,
        style = style,
        maxLines = if (fontScale > 1.5) maxLinesAtLargeFont else Int.MAX_VALUE,
        overflow = if (fontScale > 1.5) TextOverflow.Ellipsis else TextOverflow.Clip,
        modifier = modifier
    )
}
```

### Touch Target Compliance

**WCAG 2.5.5 Target Size (Enhanced): minimum 44x44 CSS pixels (~48x48dp on Android).**

```kotlin
// Modifier to ensure minimum touch target
fun Modifier.minimumTouchTarget(): Modifier = this
    .then(
        Modifier
            .sizeIn(minWidth = 48.dp, minHeight = 48.dp)
            .padding(8.dp)  // 8dp spacing between adjacent targets
    )

// Usage
IconButton(
    onClick = { /* ... */ },
    modifier = Modifier.minimumTouchTarget()
) {
    Icon(Icons.Default.MoreVert, contentDescription = "More options")
}
```

**For small icons where 48dp is too large visually, use padding to expand touch area:**

```kotlin
@Composable
fun SmallIconWithLargeTouchTarget(
    @DrawableRes icon: Int,
    contentDescription: String,
    onClick: () -> Unit
) {
    Box(
        modifier = Modifier
            .size(48.dp)
            .clickable(onClick = onClick)
    ) {
        Icon(
            painter = painterResource(icon),
            contentDescription = contentDescription,
            modifier = Modifier
                .size(24.dp)  // Visual size
                .align(Alignment.Center)
        )
    }
}
```

### Accessibility Testing — CI Integration

**Automated a11y checks in Espresso tests:**

```kotlin
@RunWith(AndroidJUnit4::class)
class AccessibilityTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)

    @Test
    fun allScreens_passAccessibilityChecks() {
        // Navigate through all screens
        onView(withId(R.id.nav_home)).perform(click())
        assertAccessibilityConformance()

        onView(withId(R.id.nav_profile)).perform(click())
        assertAccessibilityConformance()

        onView(withId(R.id.nav_settings)).perform(click())
        assertAccessibilityConformance()
    }

    private fun assertAccessibilityConformance() {
        val checkResult = AccessibilityChecker.checkRootViewWithResult()
        val issues = checkResult.runChecks()

        // Fail on any accessibility issues
        assertTrue(
            "Accessibility issues found:\n${issues.joinToString("\n") { it.getMessage() }}",
            issues.isEmpty()
        )
    }
}
```

**Compose semantics tree validation:**

```kotlin
@Test
fun userCard_hasCorrectSemantics() {
    composeTestRule.setContent {
        UserCard(user = testUser)
    }

    composeTestRule.onNode(hasContentDescription("John Doe, Premium member"))
        .assertExists()
        .assertIsSelectable()
}
```

### Accessibility Checklist per Screen

Before marking any screen as complete:

- [ ] All images have meaningful `contentDescription` (or `null` if decorative)
- [ ] All interactive elements have minimum 48x48dp touch target
- [ ] Color contrast ratios meet 4.5:1 (normal text) / 3:1 (large text)
- [ ] Content is readable at 200% font scale without horizontal scrolling
- [ ] TalkBack can navigate all elements in logical order
- [ ] Dynamic content changes are announced via live regions
- [ ] No information conveyed by color alone
- [ ] Form fields have associated labels
- [ ] Error messages are announced to screen readers
- [ ] Custom views implement `ExploreByTouchHelper`

## Pipeline Integration

- **Stage 2 (Design):** IDS specifies accessibility requirements (contrast ratios, touch target sizes, screen reader labels). This skill implements them.
- **Stage 5 (Development):** All UI components built with accessibility from the start. No retrofitting after visual completion.
- **Stage 6 (Code Review):** Accessibility audit: ContentDescription completeness, touch target sizing, font scale resilience, semantic structure.
- **Stage 7 (Automated Testing):** Automated accessibility checks in test suite; manual TalkBack test script execution.
- **Stage 8 (Integrity Verification):** CDO verifies IDS accessibility specifications are realized. Automated accessibility scan with zero issues.
- **Stage 10 (Release Readiness):** Accessibility conformance is item 2 on the release checklist (Design — all CDO/IDS specifications realized).

## Quality Standards

- **100%** WCAG 2.1 AA criteria met for all production screens
- **Zero** missing ContentDescription on meaningful images (automated scan)
- **100%** interactive elements have minimum 48x48dp touch target (or adequate spacing)
- App fully usable at **200% font scale** — no truncation, overlap, or horizontal scrolling
- **100%** TalkBack users can complete all core user flows without sighted assistance
- Color contrast ratio **≥4.5:1** for normal text, **≥3:1** for large text (verified by automated tool)
- Accessibility defects classified as P0/P1 (not cosmetic) — they block release
- Manual TalkBack test script executed and signed off before every release
- No gesture-only interactions — all functionality available via sequential navigation
- Custom accessibility actions provided for complex multi-touch interactions
