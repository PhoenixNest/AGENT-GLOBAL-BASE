---
name: frontend-web-react-react-testing
description: "Frontend Web skill: React Testing"
---

# React Testing

**Category:** Frontend Testing
**Owner:** Senior Frontend Engineer

## Overview

Comprehensive React testing discipline covering component unit testing, integration testing, custom hook validation, and end-to-end user flow verification. Emphasizes testing user behavior over implementation details, with production-grade patterns for async operations, API mocking, accessibility validation, and visual regression detection.

## Competency Dimensions

| Dimension                         | Description                                                               | Proficiency Indicators                                                                                                    |
| --------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **React Testing Library Mastery** | Querying, user-event simulation, and debugging RTL patterns               | Uses `getByRole` as primary query; never uses `getByTestId` without justification; writes tests that mirror user behavior |
| **Async Component Testing**       | Testing loading states, race conditions, error boundaries, and Suspense   | Correctly awaits `findBy*` queries; handles `waitFor` timeouts; tests Suspense fallbacks                                  |
| **Custom Hook Testing**           | Isolating and testing hook logic with `@testing-library/react-hooks`      | Uses `renderHook` with custom wrapper; tests all hook return paths including error states                                 |
| **API Mocking (MSW)**             | Service worker–based network interception for realistic integration tests | Configures MSW handlers at test setup; uses runtime handlers for per-test overrides; tests error responses                |
| **Context & Provider Testing**    | Testing components that depend on React Context, Redux, or Zustand        | Creates reusable test wrappers; isolates provider behavior from component logic                                           |
| **Snapshot Testing Discipline**   | Knowing when snapshots add value vs. when they create maintenance debt    | Uses snapshots for stable UI contracts only; never snapshots large component trees without intent                         |
| **Accessibility Testing**         | Automated a11y assertion integration with axe-core                        | Every component test includes `expect(container).toBeAccessible()`; tests keyboard navigation                             |
| **Visual Regression Testing**     | Pixel-diff detection with Storybook + Chromatic/Percy                     | Catches unintended visual changes; approves intentional design updates with design team sign-off                          |
| **CI Integration**                | Jest/Vitest configuration, coverage thresholds, parallel execution        | Tests run in <30s for full suite; coverage gates block merge; flaky test quarantine process                               |

## Execution Guidance

### 1. React Testing Library Best Practices

**Query Priority (always use the highest-priority query available):**

```
1. getByRole          → Most accessible, mirrors how users find elements
2. getByLabelText     → Form fields
3. getByPlaceholderText → Inputs (fallback)
4. getByText          → Non-interactive elements
5. getByDisplayValue  → Form elements with current value
6. getByAltText       → Images
7. getByTitle         → Elements with title attribute
8. getByTestId        → LAST RESORT, document justification
```

**Correct Pattern — Test User Behavior, Not Implementation:**

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CommentForm } from './CommentForm';

test('submits comment and shows success message', async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();

  render(<CommentForm onSubmit={onSubmit} />);

  // User sees the form
  expect(screen.getByRole('heading', { name: /leave a comment/i })).toBeInTheDocument();

  // User fills out the form
  await user.type(screen.getByRole('textbox', { name: /your comment/i }), 'Great post!');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  // User sees confirmation
  expect(await screen.findByText(/comment posted successfully/i)).toBeInTheDocument();
  expect(onSubmit).toHaveBeenCalledWith({ content: 'Great post!' });
});
```

**❌ Anti-Patterns to Never Use:**

```typescript
// WRONG: Testing implementation details (internal state, class names)
expect(component.state().isOpen).toBe(true);
expect(screen.getByTestId("submit-btn").classList.contains("active")).toBe(
  true,
);

// WRONG: Using act() manually — RTL handles this automatically
act(() => {
  fireEvent.click(button);
});

// WRONG: Testing mock function calls instead of user-visible outcomes
expect(mockApi).toHaveBeenCalledWith("/api/comments");
```

### 2. Custom Render Patterns

**Create a `test-utils.tsx` that wraps common providers — eliminates duplication and ensures consistent test environment:**

```typescript
// test-utils.tsx
import { render, type RenderOptions } from '@testing-library/react';
import { ThemeProvider } from '@/providers/theme';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { IntlProvider } from 'react-intl';
import type { ReactElement } from 'react';

const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });

interface CustomRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  route?: string;
  queryClient?: QueryClient;
  locale?: string;
}

function customRender(ui: ReactElement, options: CustomRenderOptions = {}) {
  const {
    route = '/',
    queryClient = createTestQueryClient(),
    locale = 'en',
    ...renderOptions
  } = options;

  window.history.pushState({}, '', route);

  const Wrapper = ({ children }: { children: React.ReactNode }) => (
    <BrowserRouter>
      <IntlProvider locale={locale}>
        <ThemeProvider>
          <QueryClientProvider client={queryClient}>
            {children}
          </QueryClientProvider>
        </ThemeProvider>
      </IntlProvider>
    </BrowserRouter>
  );

  return render(ui, { wrapper: Wrapper, ...renderOptions });
}

// Re-export everything from RTL plus our custom render
export * from '@testing-library/react';
export { customRender as render };
```

**Usage in tests:**

```typescript
import { render, screen } from '@/test-utils';
import { UserProfile } from './UserProfile';

test('displays user profile with translated labels', async () => {
  render(<UserProfile userId="123" />, { locale: 'pt-BR', route: '/profile/123' });
  expect(screen.getByText(/perfil do usuário/i)).toBeInTheDocument();
});
```

### 3. Mock Service Worker (MSW) for API Mocking

**MSW intercepts real network requests at the service worker level — tests exercise the same fetch/XHR code paths as production.**

**Setup (`src/mocks/handlers.ts`):**

```typescript
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/api/users/:id", ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: "Test User",
      email: "test@example.com",
    });
  }),

  http.post("/api/comments", async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      { id: "new-id", ...body, createdAt: new Date().toISOString() },
      { status: 201 },
    );
  }),

  http.get("/api/posts", () => {
    return HttpResponse.json({
      data: [
        { id: "1", title: "Post 1" },
        { id: "2", title: "Post 2" },
      ],
      meta: { total: 2 },
    });
  }),
];
```

**Test Setup (`src/mocks/setup.ts`):**

```typescript
import { setupServer } from "msw/node";
import { handlers } from "./handlers";
import { afterAll, afterEach, beforeAll } from "vitest";

export const server = setupServer(...handlers);

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => {
  server.resetHandlers(); // Reset to default handlers between tests
  vi.clearAllMocks();
});
afterAll(() => server.close());
```

**Runtime Handler Overrides (per-test scenarios):**

```typescript
import { http, HttpResponse } from 'msw';
import { server } from '@/mocks/setup';
import { render, screen } from '@/test-utils';
import { UserList } from './UserList';

test('displays error state when API returns 500', async () => {
  // Override the default handler for this test only
  server.use(
    http.get('/api/users/:id', () => {
      return HttpResponse.json(
        { error: 'Internal Server Error' },
        { status: 500 }
      );
    })
  );

  render(<UserList />);

  expect(await screen.findByRole('alert', { name: /error loading users/i }))
    .toBeInTheDocument();
  expect(screen.getByText(/please try again later/i)).toBeInTheDocument();
});

test('displays empty state when API returns no data', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json({ data: [], meta: { total: 0 } });
    })
  );

  render(<UserList />);

  expect(await screen.findByText(/no users found/i)).toBeInTheDocument();
});
```

**Testing Network Errors (not just HTTP errors):**

```typescript
import { http } from 'msw';
import { server } from '@/mocks/setup';

test('handles network failure gracefully', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.error(); // Simulates network-level failure
    })
  );

  render(<UserList />);

  expect(await screen.findByRole('alert', { name: /network error/i }))
    .toBeInTheDocument();
});
```

### 4. Component Integration Testing

**Test components working together — the sweet spot between unit and E2E:**

```typescript
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ProductCatalog } from './ProductCatalog';

test('filters products and updates URL search params', async () => {
  const user = userEvent.setup();

  render(<ProductCatalog />);

  // Verify initial state — all products shown
  const productList = screen.getByRole('list');
  expect(within(productList).getAllByRole('listitem')).toHaveLength(12);

  // Apply filter — category
  const categoryFilter = screen.getByRole('combobox', { name: /category/i });
  await user.selectOptions(categoryFilter, 'electronics');

  // Verify filtered results
  expect(await screen.findByText(/no products in clothing/i)).not.toBeInTheDocument();
  expect(within(productList).getAllByRole('listitem')).toHaveLength(5);

  // Verify URL updated (integration with routing)
  expect(window.location.search).toContain('category=electronics');
});
```

**Testing Form Integration with React Hook Form:**

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CheckoutForm } from './CheckoutForm';

test('validates form and shows field-level errors', async () => {
  const user = userEvent.setup();

  render(<CheckoutForm onSubmit={vi.fn()} />);

  // Submit empty form
  await user.click(screen.getByRole('button', { name: /place order/i }));

  // Validation errors appear
  expect(screen.getByText(/email is required/i)).toBeInTheDocument();
  expect(screen.getByText(/card number is invalid/i)).toBeInTheDocument();

  // Fill with invalid data
  await user.type(screen.getByRole('textbox', { name: /email/i }), 'not-an-email');
  await user.type(screen.getByRole('textbox', { name: /card number/i }), '1234');
  await user.click(screen.getByRole('button', { name: /place order/i }));

  // Specific validation messages
  expect(screen.getByText(/please enter a valid email/i)).toBeInTheDocument();
  expect(screen.getByText(/card number must be 16 digits/i)).toBeInTheDocument();
});
```

### 5. Snapshot Testing — Decision Framework

**When to USE snapshots:**

- ✅ Stable UI components with fixed markup (icons, badges, avatars)
- ✅ Error message components (ensure consistency)
- ✅ Component libraries where markup changes are breaking changes
- ✅ Serialized state objects for debugging

**When to AVOID snapshots:**

- ❌ Large component trees (>50 lines of snapshot output)
- ❌ Components with dynamic content (dates, IDs, randomized values)
- ❌ Components where you care about behavior, not markup
- ❌ As a substitute for meaningful assertions

**Correct snapshot usage:**

```typescript
import { render } from '@testing-library/react';
import { StatusBadge } from './StatusBadge';

test('status badge renders consistent markup for screen readers', () => {
  const { container } = render(<StatusBadge status="error" />);

  // Snapshot the accessible structure, not visual styling
  expect(container.querySelector('[role="status"]')).toMatchSnapshot();
});
```

**Updating snapshots:** `vitest -u` or `jest --updateSnapshot`. Always review diffs before committing — never blindly update.

### 6. Testing Async Components

**Patterns for Suspense, loading states, and race conditions:**

```typescript
import { render, screen, act } from '@testing-library/react';
import { Suspense } from 'react';
import { UserProfile } from './UserProfile';

test('shows loading skeleton while profile fetches', async () => {
  render(
    <Suspense fallback={<div data-testid="skeleton">Loading...</div>}>
      <UserProfile userId="123" />
    </Suspense>
  );

  // Loading state visible immediately
  expect(screen.getByTestId('skeleton')).toBeInTheDocument();

  // Resolved content replaces skeleton
  expect(await screen.findByRole('heading', { name: /test user/i })).toBeInTheDocument();
  expect(screen.queryByTestId('skeleton')).not.toBeInTheDocument();
});

test('handles slow network with timeout message', async () => {
  // Configure MSW to delay response
  server.use(
    http.get('/api/users/:id', async () => {
      await new Promise((r) => setTimeout(r, 5000)); // 5 second delay
      return HttpResponse.json({ id: '123', name: 'Test User' });
    })
  );

  vi.useFakeTimers();

  render(<UserProfile userId="123" />);

  // Advance past the 3-second timeout threshold
  vi.advanceTimersByTime(3000);

  expect(await screen.findByText(/request is taking longer/i)).toBeInTheDocument();

  vi.useRealTimers();
});
```

**Testing Error Boundaries:**

```typescript
import { render, screen } from '@testing-library/react';
import { ErrorBoundary } from './ErrorBoundary';
import { BrokenComponent } from './BrokenComponent';

test('error boundary catches and displays render error', () => {
  // Suppress console.error from React's expected error
  vi.spyOn(console, 'error').mockImplementation(() => {});

  render(
    <ErrorBoundary fallback={<div role="alert">Something went wrong</div>}>
      <BrokenComponent />
    </ErrorBoundary>
  );

  expect(screen.getByRole('alert')).toHaveTextContent('Something went wrong');
  expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument();
});
```

### 7. Testing Custom Hooks

**Use `renderHook` from `@testing-library/react` (v13+): **

```typescript
import { renderHook, waitFor } from "@testing-library/react";
import { useDebounce } from "./useDebounce";
import { useAuth } from "./useAuth";

test("useDebounce delays value updates", async () => {
  vi.useFakeTimers();

  const { result, rerender } = renderHook(
    ({ value }) => useDebounce(value, 300),
    { initialProps: { value: "hello" } },
  );

  expect(result.current).toBe("hello");

  // Update input — should not debounce immediately
  rerender({ value: "hello world" });
  expect(result.current).toBe("hello"); // Still old value

  // Advance past debounce delay
  vi.advanceTimersByTime(300);
  expect(result.current).toBe("hello world");

  vi.useRealTimers();
});

test("useAuth handles login flow with loading and error states", async () => {
  const { result } = renderHook(() => useAuth(), {
    wrapper: AuthProvider, // Provide necessary context
  });

  // Initial state
  expect(result.current.user).toBeNull();
  expect(result.current.isLoading).toBe(false);

  // Trigger login
  await act(async () => {
    await result.current.login("test@example.com", "password");
  });

  await waitFor(() => {
    expect(result.current.user).toEqual({
      id: "123",
      email: "test@example.com",
    });
    expect(result.current.isLoading).toBe(false);
  });
});

test("useAuth handles login failure", async () => {
  server.use(
    http.post("/api/auth/login", () => {
      return HttpResponse.json(
        { error: "Invalid credentials" },
        { status: 401 },
      );
    }),
  );

  const { result } = renderHook(() => useAuth(), {
    wrapper: AuthProvider,
  });

  await act(async () => {
    const response = await result.current.login("bad@example.com", "wrong");
    expect(response.ok).toBe(false);
    expect(response.error).toBe("Invalid credentials");
  });

  expect(result.current.user).toBeNull();
});
```

### 8. Accessibility Testing Integration (axe-core)

**Every component test should include accessibility assertions:**

```typescript
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { NavigationMenu } from './NavigationMenu';

expect.extend(toHaveNoViolations);

test('navigation menu has no accessibility violations', async () => {
  const { container } = render(<NavigationMenu items={menuItems} />);

  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

test('navigation menu supports keyboard navigation', async () => {
  const user = userEvent.setup();
  render(<NavigationMenu items={menuItems} />);

  const menu = screen.getByRole('menubar');
  menu.focus();

  // Arrow right moves focus to next menu item
  await user.keyboard('{ArrowRight}');
  expect(screen.getByRole('menuitem', { name: /about/i })).toHaveFocus();

  // Enter activates the menu item
  await user.keyboard('{Enter}');
  expect(window.location.pathname).toBe('/about');
});

test('modal traps focus and has correct ARIA attributes', async () => {
  const user = userEvent.setup();
  render(<Modal isOpen={true} onClose={vi.fn()}>
    <h2>Confirm Action</h2>
    <p>Are you sure?</p>
    <button onClick={vi.fn()}>Confirm</button>
  </Modal>);

  const dialog = screen.getByRole('dialog');

  // ARIA attributes
  expect(dialog).toHaveAttribute('aria-modal', 'true');
  expect(dialog).toHaveAttribute('aria-labelledby');
  expect(dialog).toHaveAttribute('aria-describedby');

  // Focus is trapped inside
  await user.keyboard('{Tab}{Tab}{Tab}');
  expect(within(dialog).getByRole('button', { name: /confirm/i })).toHaveFocus();

  // Escape closes
  await user.keyboard('{Escape}');
  // Verify onClose was called
});
```

### 9. Visual Regression Testing with Storybook

**Storybook + Chromatic/Percy for pixel-level diff detection:**

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "Components/Button",
  component: Button,
  parameters: {
    chromatic: { diffThreshold: 0.2, viewports: [320, 1280] },
  },
  argTypes: {
    variant: { control: "select", options: ["primary", "secondary", "ghost"] },
    size: { control: "select", options: ["sm", "md", "lg"] },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: { variant: "primary", children: "Click me" },
};
export const Secondary: Story = {
  args: { variant: "secondary", children: "Cancel" },
};
export const Loading: Story = {
  args: { loading: true, children: "Submitting" },
};
export const Disabled: Story = {
  args: { disabled: true, children: "Disabled" },
};
```

**CI Integration (GitHub Actions):**

```yaml
# .github/workflows/visual-regression.yml
name: Visual Regression
on:
  pull_request:
    paths: ["src/components/**", "**.stories.tsx"]

jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: npm ci
      - uses: chromaui/action@v10
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          buildScriptName: build-storybook
```

**Decision: When to use visual regression vs. RTL tests:**

| Scenario                         | Use RTL | Use Visual Regression |
| -------------------------------- | ------- | --------------------- |
| Testing user interactions        | ✅      | ❌                    |
| Testing accessible markup        | ✅      | ❌                    |
| Testing layout/pixel perfection  | ❌      | ✅                    |
| Testing color/typography changes | ❌      | ✅                    |
| Testing responsive breakpoints   | ❌      | ✅                    |
| Testing form validation logic    | ✅      | ❌                    |

### 10. Test Coverage Thresholds

**Enforce minimum coverage in Vitest/Jest config:**

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    coverage: {
      provider: "istanbul",
      reporter: ["text", "lcov", "html"],
      thresholds: {
        lines: 85,
        functions: 90,
        branches: 80,
        statements: 85,
      },
      exclude: [
        "**/*.stories.tsx", // Storybook stories
        "**/*.d.ts", // Type definitions
        "src/mocks/**", // MSW handlers
        "src/test-utils/**", // Test utilities
        "src/types/**", // Pure type files
        "src/index.ts", // Entry point barrel
      ],
    },
  },
});
```

**Coverage interpretation:**

| Metric     | Minimum | Target | Rationale                                    |
| ---------- | ------- | ------ | -------------------------------------------- |
| Functions  | 90%     | 95%    | Hook logic and event handlers must be tested |
| Lines      | 85%     | 90%    | Acceptable gap for error-only branches       |
| Branches   | 80%     | 85%    | Error paths and edge cases covered           |
| Statements | 85%     | 90%    | Overall code execution coverage              |

**⚠️ Coverage is a floor, not a ceiling.** 100% coverage does not mean 0 bugs. Focus on testing critical paths, error handling, and user-facing behavior. Do not write meaningless tests just to hit a number.

### 11. CI Integration — Jest vs. Vitest

**Vitest is recommended for new projects** (faster, native ESM, Vite-compatible). Jest for legacy codebases.

**Vitest CI Configuration:**

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/mocks/setup.ts", "./src/test-setup.ts"],
    include: ["src/**/*.{test,spec}.{ts,tsx}"],
    exclude: ["src/**/*.stories.{ts,tsx}", "src/mocks/**"],
    reporters: ["default", "junit"],
    outputFile: {
      junit: "./test-results/junit.xml",
    },
    sequence: {
      shuffle: true, // Catch order-dependent tests
    },
    retry: 2, // Retry flaky tests up to 2 times
    maxConcurrency: 5, // Parallelize describe.concurrent blocks
  },
});
```

**GitHub Actions — Test Pipeline:**

```yaml
# .github/workflows/test.yml
name: Test Suite
on:
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"
      - run: npm ci
      - run: npm run typecheck
      - run: npm run lint
      - run: npm test -- --coverage --run
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage/lcov.info
          fail_ci_if_error: true
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: ./test-results/
```

**Flaky Test Management Protocol:**

1. **Detect:** CI marks tests that pass on retry but fail on first run
2. **Quarantine:** Add `.skip` or move to `flaky-tests/` directory with tracking issue
3. **Root Cause:** Common causes — unawaited promises, shared mutable state, time-dependent logic, network timing
4. **Fix:** Use `vi.useFakeTimers()`, isolate test state, properly await async operations
5. **Re-enable:** Remove skip after fix is verified in 5+ consecutive CI runs

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                           |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 5 — Development**            | Tests are written alongside component development (TDD/ATDD). Platform Lead ensures all new components have corresponding test files. |
| **Stage 6 — Code Review**            | Test coverage and quality are reviewed. Defect Report includes missing tests for critical paths as P2 defects.                        |
| **Stage 7 — Automated Testing**      | Full test suite execution. This skill defines the test architecture that Stage 7 runs. Test Lead validates test suite completeness.   |
| **Stage 8 — Integrity Verification** | Accessibility test results verified. Visual regression baselines confirmed. Test coverage thresholds enforced.                        |
| **Stage 10 — Release Readiness**     | Test results contribute to Item 5 (100% automated test pass rate). Any P0/P1 test failures block release.                             |

## Quality Standards

| Standard                                   | Metric                                    | Enforcement                                               |
| ------------------------------------------ | ----------------------------------------- | --------------------------------------------------------- |
| **Test Pass Rate**                         | 100%                                      | CI blocks merge on any failure                            |
| **Function Coverage**                      | ≥90%                                      | Vitest/Jest threshold gates                               |
| **Branch Coverage**                        | ≥80%                                      | Coverage report reviewed at Stage 6                       |
| **Flaky Test Rate**                        | <1%                                       | Monitored in CI; quarantined immediately                  |
| **Accessibility**                          | 0 axe-core violations                     | Every component test includes a11y assertion              |
| **Visual Regression**                      | 0 unapproved diffs                        | Chromatic/Percy blocks PR on unexpected changes           |
| **Test Execution Time**                    | <30s (full suite)                         | CI performance monitoring; parallelization required       |
| **No `getByTestId` Without Justification** | Documented exceptions only                | Code review check                                         |
| **No `any` in Test Files**                 | TypeScript strict mode                    | ESLint `@typescript-eslint/no-explicit-any` in test files |
| **Every Error Path Tested**                | All catch blocks and error states covered | Branch coverage metric                                    |

**Defect Classification for Test Failures:**

| Scenario                                          | Severity | Rationale                                                  |
| ------------------------------------------------- | -------- | ---------------------------------------------------------- |
| Test passes locally but fails in CI               | P1       | Indicates environment-dependent behavior — production risk |
| Missing tests for critical user flow              | P2       | Gap in safety net, but not a broken feature                |
| Flaky test (>5% failure rate)                     | P1       | Erodes trust in test suite; blocks reliable CI             |
| Coverage below threshold                          | P2       | Technical debt, not a functional defect                    |
| Accessibility violations in production components | P0       | Legal/compliance risk; blocks release                      |
| Snapshot update without design team approval      | P1       | Potential unapproved visual regression                     |
