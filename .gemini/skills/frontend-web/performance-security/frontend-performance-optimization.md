---
name: frontend-performance-optimization
description: This skill provides deep React-specific performance engineering expertise, covering rendering optimization through memoization strategies, virtual scrolling for large datasets.
---

# Frontend Performance Optimization — React Specialization

**Category:** Frontend Engineering / Performance
**Owner:** Senior Frontend Engineer (Rafael Santos)

## Overview

This skill provides deep React-specific performance engineering expertise, covering rendering optimization through memoization strategies, virtual scrolling for large datasets, progressive loading with React.lazy and Suspense, bundle optimization at the component level, and the profiling methodology needed to identify and eliminate performance bottlenecks. React's declarative model makes it easy to write correct code but easy to write slow code — understanding the reconciliation algorithm, the conditions that trigger re-renders, and the cost of each render phase is essential for building applications that remain performant at scale. This skill applies from Stage 2 prototype validation through Stage 5 implementation and Stage 6 code review.

## Competency Dimensions

| Dimension                  | Description                                                                              | Proficiency Indicators                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **React Rendering Model**  | Deep understanding of reconciliation, commit phase, render phase, and bailout conditions | Can explain why a component re-renders; can predict render count from state update patterns   |
| **Memoization Strategies** | React.memo, useMemo, useCallback — when to use, when to avoid, measuring actual benefit  | Memoization applied only where profiling confirms benefit; zero premature optimization        |
| **Virtual Scrolling**      | react-window / react-virtualized for large lists/grids with constant memory footprint    | Lists of 10,000+ items render at 60fps; DOM node count stays constant regardless of data size |
| **Progressive Loading**    | React.lazy, Suspense boundaries, transition APIs, streaming SSR                          | Initial paint shows meaningful content within 1.5s; loading states are skeletal, not spinners |
| **Bundle Optimization**    | Route-level and component-level code splitting, dynamic imports, tree shaking analysis   | Every route is lazy-loaded; no chunk > 50KB gzipped without justification                     |
| **Performance Profiling**  | React DevTools Profiler, Chrome Performance tab, flame graphs, why-did-you-render        | Can identify the exact component and prop causing unnecessary re-renders within 5 minutes     |

## Execution Guidance

### React Rendering Model — Understanding the Cost

**The two-phase render process:**

```
Phase 1: Render Phase (JavaScript — can be interrupted)
  ├─ Component functions execute
  ├─ Virtual DOM tree is built
  ├─ Diffing against previous tree
  └─ Changes are calculated
       ↓
Phase 2: Commit Phase (DOM — cannot be interrupted)
  ├─ DOM mutations applied
  ├─ Layout effects fire (useLayoutEffect)
  ├─ Passive effects fire (useEffect)
  └─ Screen updates
```

**What triggers a re-render:**

```
State change (useState, useReducer)
  ├─ In the component → component + all children re-render
  ├─ In a parent → all descendants re-render (unless memoized)
  └─ In a sibling → NO re-render (independent state)
       ↓
Context value change
  ├─ ALL consumers re-render (regardless of which context property changed)
  └─ Mitigation: split contexts, memoize consumers, or use context selectors
       ↓
Parent re-render
  ├─ ALL children re-render by default
  └─ Mitigation: React.memo on children, lift content above state boundary
       ↓
Hook dependency change
  ├─ useEffect callback re-executes
  ├─ useMemo recomputes
  └─ useCallback returns new function reference
```

**The bailout conditions** — React skips re-rendering a component when:

1. **React.memo** — props are shallowly equal to previous render
2. **useState** — new state is `Object.is()` equal to current state
3. **useReducer** — dispatched value is `Object.is()` equal to current state
4. **Context** — component doesn't consume the changed context value

**Render cost measurement:**

```tsx
// Enable profiling in development
// React DevTools → Settings → "Record why each component rendered"

// In production, use the Profiler API
import { Profiler } from 'react';

function onRenderCallback(
  id,
  phase,
  actualDuration,
  baseDuration,
  startTime,
  commitTime,
  interactions
) {
  // actualDuration: time spent rendering this component + descendants
  // baseDuration: estimated time if no memoization was used
  // If actualDuration ≈ baseDuration, memoization is not helping
  if (actualDuration > 16) {
    // Exceeds frame budget
    console.warn(`Component ${id} took ${actualDuration.toFixed(1)}ms`);
  }
}

<Profiler id="ExpensiveComponent" onRender={onRenderCallback}>
  <ExpensiveComponent />
</Profiler>;
```

### Memoization Strategies — Decision Framework

**The memoization decision tree:**

```
Is the component re-rendering unnecessarily?
  ├─ Profile with React DevTools to confirm
  ├─ If NO → Don't memoize (premature optimization costs more than it saves)
  └─ If YES → Apply strategy based on cause:
      ├─ Parent re-rendering → React.memo on child
      ├─ Expensive computation → useMemo
      ├─ Function passed as prop → useCallback
      └─ Context causing mass re-renders → Split context or use selector pattern
```

**React.memo — when it helps and when it hurts:**

```tsx
// ✅ GOOD: Expensive component that rarely changes
const ExpensiveChart = React.memo(function ExpensiveChart({ data, config }) {
  // Complex rendering logic — costly to re-run
  return <canvas>{/* ... */}</canvas>;
});
// Benefit: Avoids expensive re-render when parent updates but data/config are the same

// ❌ BAD: Cheap component that always receives new props
const SimpleText = React.memo(function SimpleText({ text }) {
  return <span>{text}</span>;
});
// Cost: Shallow comparison on every render + allocation of memo wrapper
// Benefit: None — text changes every render anyway

// ❌ WORSE: Component with inline object/array props (shallow comparison always fails)
<ExpensiveChart data={[...items]} config={{ theme: 'dark' }} />;
// Every render creates new array and new object → React.memo is useless
// FIX: Lift data and config outside component or memoize them

// ✅ CORRECT: Stable props that enable React.memo to work
const chartData = useMemo(() => computeChartData(items), [items]);
const chartConfig = useMemo(() => ({ theme: 'dark' }), []);
<ExpensiveChart data={chartData} config={chartConfig} />;
```

**useMemo — correct usage patterns:**

```tsx
function Dashboard({ items, filter, sortBy }) {
  // ✅ CORRECT: Expensive computation that depends on changing values
  const filteredItems = useMemo(() => {
    return items.filter((item) => item.matches(filter)).sort((a, b) => a[sortBy] - b[sortBy]);
  }, [items, filter, sortBy]);

  // ✅ CORRECT: Creating a stable reference for child component
  const chartData = useMemo(
    () => ({
      labels: filteredItems.map((i) => i.name),
      values: filteredItems.map((i) => i.value),
    }),
    [filteredItems]
  );

  // ❌ WRONG: Memoizing primitive values (React already bails out on === equality)
  const count = useMemo(() => items.length, [items]); // Useless — just do: items.length

  // ❌ WRONG: Memoizing with empty deps when value should change
  const staticData = useMemo(() => computeInitialData(), []); // Only if truly static

  // ❌ WRONG: useMemo as a substitute for state
  const formData = useMemo(() => ({ name: '', email: '' }), []); // Use useState instead

  return (
    <div>
      <FilteredList items={filteredItems} />
      <Chart data={chartData} />
    </div>
  );
}
```

**useCallback — when function identity matters:**

```tsx
function Parent() {
  // ✅ CORRECT: Function passed to memoized child component
  const handleClick = useCallback((id) => {
    setSelectedId(id);
  }, []); // Stable reference — child won't re-render unnecessarily

  // ✅ CORRECT: Function in useEffect dependency array
  const fetchData = useCallback(async () => {
    const response = await api.get(`/items/${selectedId}`);
    setData(response.data);
  }, [selectedId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]); // Now fetchData is stable unless selectedId changes

  // ❌ WRONG: Callback not passed to any memoized component
  const handleClick = useCallback(() => {
    // ...
  }, []); // Useless — just define it normally
  // <button onClick={handleClick}> — button is not memoized

  return (
    <>
      <MemoizedChild onItemClick={handleClick} /> {/* memo benefit realized */}
      <NonMemoizedChild onClick={handleClick} /> {/* no memo benefit, but harmless */}
    </>
  );
}
```

**The Context Selector Pattern** — prevent mass re-renders from context updates:

```tsx
// ❌ PROBLEM: All consumers re-render when ANY part of AuthContext changes
const AuthContext = createContext({
  user: null,
  token: null,
  isLoading: false,
});

function UserProfile() {
  const { user } = useContext(AuthContext); // Re-renders when token or isLoading change too
  return <div>{user?.name}</div>;
}

// ✅ SOLUTION: Split contexts by update frequency
const UserContext = createContext(null); // Changes rarely
const TokenContext = createContext(null); // Changes on login/logout
const LoadingContext = createContext(false); // Changes frequently

function UserProfile() {
  const user = useContext(UserContext); // Only re-renders when user changes
  return <div>{user?.name}</div>;
}

// ✅ ALTERNATIVE: Custom hook with selector (requires external library or custom implementation)
function useAuthSelector(selector) {
  const auth = useContext(AuthContext);
  return useMemo(() => selector(auth), [auth, selector]);
}

function UserProfile() {
  const user = useAuthSelector((state) => state.user); // Only re-renders when user reference changes
  return <div>{user?.name}</div>;
}
```

### Virtual Scrolling — Large Dataset Performance

**When to use virtual scrolling:**

- Lists with > 100 items that are visible simultaneously
- Grids with > 50 cells visible at once
- Any list/grid where rendering all items causes noticeable lag (> 16ms frame time)

**react-window implementation** — production pattern:

```tsx
import { FixedSizeList as List, FixedSizeGrid as Grid } from 'react-window';
import { memo, useCallback, useMemo } from 'react';

// Memoize individual row items — critical for virtual scroll performance
const MemoizedRow = memo(function RowItem({ item, index, style, onClick }) {
  return (
    <div style={style} onClick={() => onClick(item.id)}>
      <span>{item.name}</span>
      <span>{item.status}</span>
    </div>
  );
});

function VirtualList({ items, onItemClick }) {
  // Stable callback reference — prevents row re-renders
  const handleRowClick = useCallback((id) => onItemClick(id), [onItemClick]);

  // Row renderer — receives index and style from react-window
  const Row = useCallback(
    ({ index, style }) => {
      const item = items[index];
      return (
        <MemoizedRow
          item={item}
          index={index}
          style={style} // REQUIRED — positions the row
          onClick={handleRowClick}
        />
      );
    },
    [items, handleRowClick]
  );

  return (
    <List
      height={600} // Viewport height in pixels
      itemCount={items.length}
      itemSize={48} // Height of each row
      width="100%"
      overscanCount={5} // Render 5 items above/below viewport for smooth scrolling
    >
      {Row}
    </List>
  );
}
```

**Variable height items** — when rows have different heights:

```tsx
import { VariableSizeList } from 'react-window';

function VariableHeightList({ items }) {
  // Measure item heights (can be estimated initially, refined after render)
  const getItemSize = useCallback(
    (index) => {
      const item = items[index];
      if (item.type === 'header') return 64;
      if (item.type === 'detail') return 128;
      return 48; // default
    },
    [items]
  );

  return (
    <VariableSizeList
      height={600}
      itemCount={items.length}
      itemSize={getItemSize}
      width="100%"
      estimatedItemSize={64} // Initial estimate — refined as items render
    >
      {Row}
    </VariableSizeList>
  );
}
```

**Virtual scroll performance checklist:**

- [ ] Individual items are memoized with `React.memo`
- [ ] Callbacks passed to items use `useCallback` with stable references
- [ ] `itemSize` is a constant (FixedSizeList) or memoized function (VariableSizeList)
- [ ] `overscanCount` is set (3-5 is typical; higher = smoother scroll but more DOM nodes)
- [ ] No inline styles on items except the required `style` prop from react-window
- [ ] No heavy computation in the row renderer — pre-compute data outside the list

### Progressive Loading and Suspense

**Suspense boundary strategy:**

```tsx
// Route-level lazy loading with Suspense
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<AppSkeleton />}>
      {' '}
      {/* Top-level fallback for route transitions */}
      <Router>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Router>
    </Suspense>
  );
}

// Component-level Suspense — below-the-fold content
function Dashboard() {
  const Chart = lazy(() => import('./components/Chart'));
  const RecentActivity = lazy(() => import('./components/RecentActivity'));

  return (
    <div>
      {/* Above the fold — render immediately */}
      <DashboardHeader />
      <StatsCards />

      {/* Below the fold — lazy load */}
      <Suspense fallback={<ChartSkeleton />}>
        <Chart />
      </Suspense>
      <Suspense fallback={<ActivitySkeleton />}>
        <RecentActivity />
      </Suspense>
    </div>
  );
}
```

**React 18 useTransition for non-blocking updates:**

```tsx
import { useTransition, useState } from 'react';

function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  function handleSearch(input) {
    setQuery(input); // Urgent — update input immediately

    startTransition(() => {
      // Non-urgent — can be interrupted by more typing
      const filtered = expensiveFilter(allItems, input);
      setResults(filtered);
    });
  }

  return (
    <div>
      <input value={query} onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />} {/* Shows only when results are being computed */}
      <ResultsList results={results} />
    </div>
  );
}
```

### Bundle Optimization — Component Level

**Dynamic import patterns:**

```tsx
// Conditional loading — feature flag controlled
async function loadFeature() {
  if (featureFlags.isEnabled('new-editor')) {
    return import('./features/NewEditor');
  }
  return import('./features/LegacyEditor');
}

// Preloading — start loading before user navigates
function Navigation() {
  function handleHover() {
    // Start loading the module so it's ready when clicked
    import('./pages/Settings');
  }

  return (
    <nav>
      <Link to="/settings" onMouseEnter={handleHover}>
        Settings
      </Link>
    </nav>
  );
}

// Error boundary for lazy components
import { ErrorBoundary } from 'react-error-boundary';

function SafeLazyComponent() {
  const HeavyComponent = lazy(() => import('./HeavyComponent'));

  return (
    <ErrorBoundary
      fallback={
        <div>
          Failed to load component. <button onClick={() => window.location.reload()}>Reload</button>
        </div>
      }
      onError={(error) => logger.error('Lazy component failed to load', error)}
    >
      <Suspense fallback={<ComponentSkeleton />}>
        <HeavyComponent />
      </Suspense>
    </ErrorBoundary>
  );
}
```

**Tree shaking verification:**

```js
// Verify that unused exports are eliminated
// Use rollup-plugin-visualizer or vite-bundle-visualizer

// Common tree-shaking failures:
// ❌ Side-effectful imports
import './side-effect-module'; // Prevents tree shaking of the entire module

// ❌ Mutating exports
export const config = {};
config.value = 42; // Module has side effects — can't be tree-shaken

// ✅ Pure exports (tree-shakeable)
export const getValue = () => 42;
export const Config = Object.freeze({ value: 42 });

// ✅ Package.json sideEffects flag
// "sideEffects": false // or ["*.css"] if CSS imports have side effects
```

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                                                  | Deliverable                            |
| ------------------------------------ | ----------------------------------------------------------------------------------------------- | -------------------------------------- |
| **Stage 2** (Web Prototype + IDS)    | Identify performance-sensitive components in IDS; establish rendering budgets                   | Performance notes in IDS               |
| **Stage 4** (Implementation Plan)    | Define performance optimization tasks in implementation plan and Gantt                          | Performance milestones in GANTT.md     |
| **Stage 5** (Development)            | Implement React rendering optimizations, virtual scrolling, code splitting, Suspense boundaries | Optimized React codebase               |
| **Stage 6** (Code Review)            | Review rendering patterns, memoization usage, bundle sizes, lazy loading coverage               | Performance review in DEFECT-REPORT.md |
| **Stage 8** (Integrity Verification) | Verify performance budgets met; run profiling against production build                          | Performance integrity report           |

## Quality Standards

| Metric                        | Target                                                                      | Enforcement                                      |
| ----------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------ |
| **Re-render optimization**    | No component re-renders more than once per user action (unless intentional) | React DevTools Profiler audit                    |
| **Memoization ROI**           | All memo() calls provide measurable performance benefit                     | Profiler confirms bailout on memoized components |
| **Virtual scroll**            | Lists > 100 items use virtualization                                        | Code review; audit of List/FlatList usage        |
| **Lazy loading coverage**     | 100% of routes lazy-loaded; all below-the-fold components lazy-loaded       | Import audit: zero synchronous route imports     |
| **Suspense boundaries**       | Every lazy() call wrapped in Suspense with meaningful fallback              | Code review                                      |
| **Bundle size per route**     | < 50KB gzipped per route chunk                                              | Bundle analyzer; CI gate                         |
| **Frame rate**                | ≥ 60fps for all user interactions (scroll, input, animation)                | Chrome Performance tab audit                     |
| **Memory usage**              | No memory leaks detected after 10-minute interaction session                | Chrome Memory Profiler                           |
| **useTransition usage**       | All expensive computations wrapped in startTransition                       | Code review for search/filter operations         |
| **Error boundaries**          | Every lazy-loaded component has an ErrorBoundary                            | Code review                                      |
| **Tree shaking**              | Zero unused exports in production bundle                                    | Bundle analyzer; dead code elimination audit     |
| **Context re-render control** | No component re-renders due to unrelated context changes                    | Context consumption audit                        |
