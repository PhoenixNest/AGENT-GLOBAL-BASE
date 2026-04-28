---
name: react-testing-advanced
description: This skill establishes the React testing discipline that ensures component correctness, integration reliability, and user experience quality across all frontend deliverables.
---

# Advanced React Testing

**Category:** Frontend Engineering / Testing
**Owner:** Frontend Engineer (Yuna Park)

## Overview

This skill establishes the React testing discipline that ensures component correctness, integration reliability, and user experience quality across all frontend deliverables. It covers React Testing Library's user-centric testing philosophy, component testing patterns that test behavior over implementation, Mock Service Worker for API mocking at the network level, integration testing for multi-component workflows, and the testing infrastructure needed to support the Stage 7 Automated Testing gate. Tests are written from the user's perspective — if a test can't distinguish between a correct and incorrect implementation based on observable behavior, it's testing the wrong thing.

## Competency Dimensions

| Dimension                             | Description                                                                             | Proficiency Indicators                                                                              |
| ------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **React Testing Library Mastery**     | User-centric queries, event simulation, async testing, accessibility assertions         | Zero implementation-detail tests (no testing state variables, refs, or internal methods)            |
| **Component Testing Patterns**        | Testing props, state transitions, side effects, error boundaries, Suspense boundaries   | Every component has tests covering default render, props variants, error states, and loading states |
| **Mock Service Worker**               | Network-level API mocking, request matching, response handlers, MSW lifecycle           | All API interactions mocked at network level; zero fetch/axios mocking                              |
| **Integration Testing**               | Multi-component workflows, form submissions, navigation flows, state transitions        | End-to-end user flows tested with real component tree, not isolated mocks                           |
| **Test Infrastructure**               | Jest/Vitest configuration, custom render functions, test utilities, coverage thresholds | Shared test utilities in `test-utils.tsx`; coverage thresholds enforced in CI                       |
| **Testing Anti-patterns Recognition** | Identifying and eliminating shallow testing, implementation coupling, flaky tests       | Zero tests that break on refactoring; zero tests that pass for wrong reasons                        |

## Execution Guidance

### React Testing Library — User-Centric Testing Philosophy

**The guiding principle:** Test components the way users interact with them — through visible text, accessible labels, and observable behavior. Never test implementation details (state variables, method calls, internal component structure).

**Query priority** — use the most accessible query available:

```
1. getByRole — Best option (matches how screen readers see the page)
   └─ getByRole('button', { name: /submit/i })
   └─ getByRole('heading', { level: 1 })
   └─ getByRole('link', { name: /profile/i })
        ↓
2. getByLabelText — For form fields
   └─ getByLabelText('Email address')
   └─ getByPlaceholderText('Enter your email') — fallback if no label
        ↓
3. getByText — For non-interactive text content
   └─ getByText(/welcome back/i)
   └─ getByText('Hello, World') — exact match
        ↓
4. getByDisplayValue — For form input values
   └─ getByDisplayValue('user@email.com')
        ↓
5. getByTestId — LAST RESORT (no semantic meaning)
   └─ getByTestId('custom-element') — only when no other query works
```

**Async testing patterns:**

```tsx
import { render, screen, waitFor, findByRole } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// ✅ CORRECT: Using findBy* for async queries
test('displays user data after loading', async () => {
  render(<UserProfile userId="123" />);

  // findBy* automatically waits for element to appear
  const heading = await screen.findByRole('heading', { name: /alice/i });
  expect(heading).toBeInTheDocument();
});

// ✅ CORRECT: Using waitFor for async assertions
test('submits form and shows success message', async () => {
  const user = userEvent.setup();
  render(<ContactForm onSubmit={handleSubmit} />);

  await user.type(screen.getByLabelText('Email'), 'test@example.com');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  // waitFor retries assertion until it passes or times out (default 1000ms)
  await waitFor(() => {
    expect(screen.getByText(/message sent/i)).toBeInTheDocument();
  });
});

// ❌ WRONG: Using getBy* for async content
test('displays user data', () => {
  render(<UserProfile userId="123" />);
  // getBy* throws immediately if element not found — doesn't wait
  expect(screen.getByText('Alice')).toBeInTheDocument(); // Flaky!
});

// ❌ WRONG: Using arbitrary setTimeout
test('displays user data', async () => {
  render(<UserProfile userId="123" />);
  await new Promise((resolve) => setTimeout(resolve, 1000)); // Brittle — what if it takes 1001ms?
  expect(screen.getByText('Alice')).toBeInTheDocument();
});
```

**Testing user interactions** — use `@testing-library/user-event`, not `fireEvent`:

```tsx
import userEvent from '@testing-library/user-event';

// ✅ CORRECT: userEvent simulates real user behavior (focus, keyboard events, etc.)
test('types in input field', async () => {
  const user = userEvent.setup();
  render(<input data-testid="name-input" />);

  await user.type(screen.getByTestId('name-input'), 'Hello World');
  expect(screen.getByTestId('name-input')).toHaveValue('Hello World');
});

// ❌ WRONG: fireEvent bypasses browser behavior (no focus, no keydown/keyup sequence)
import { fireEvent } from '@testing-library/react';

test('types in input field', () => {
  render(<input data-testid="name-input" />);
  fireEvent.change(screen.getByTestId('name-input'), {
    target: { value: 'Hello World' },
  });
  // This works but doesn't simulate real user behavior
});
```

### Component Testing Patterns

**Testing prop variants** — systematic coverage of all prop combinations:

```tsx
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  // Default rendering
  it('renders with default props', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  // Variant testing
  it.each([
    ['primary', 'bg-blue-500'],
    ['secondary', 'bg-gray-500'],
    ['danger', 'bg-red-500'],
  ])('renders with %s variant', (variant, expectedClass) => {
    render(<Button variant={variant as ButtonVariant}>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toHaveClass(expectedClass);
  });

  // Size testing
  it.each(['sm', 'md', 'lg'] as const)('renders with size %s', (size) => {
    render(<Button size={size}>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toHaveAttribute('data-size', size);
  });

  // Disabled state
  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeDisabled();
  });

  // Loading state
  it('shows spinner and is disabled when loading', () => {
    render(<Button loading>Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });
    expect(button).toBeDisabled();
    expect(screen.getByRole('status')).toBeInTheDocument(); // Spinner
  });

  // Icon with label
  it('renders icon when icon prop is provided', () => {
    render(<Button icon={<TrashIcon data-testid="trash-icon" />}>Delete</Button>);
    expect(screen.getByTestId('trash-icon')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /delete/i })).toBeInTheDocument();
  });
});
```

**Testing state transitions:**

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Accordion } from './Accordion';

describe('Accordion', () => {
  it('toggles open/closed state on click', async () => {
    const user = userEvent.setup();
    render(
      <Accordion title="Section 1">
        <p>Hidden content</p>
      </Accordion>
    );

    // Initially closed
    expect(screen.queryByText('Hidden content')).not.toBeInTheDocument();
    const trigger = screen.getByRole('button', { name: /section 1/i });
    expect(trigger).toHaveAttribute('aria-expanded', 'false');

    // Open
    await user.click(trigger);
    expect(screen.getByText('Hidden content')).toBeInTheDocument();
    expect(trigger).toHaveAttribute('aria-expanded', 'true');

    // Close
    await user.click(trigger);
    expect(screen.queryByText('Hidden content')).not.toBeInTheDocument();
    expect(trigger).toHaveAttribute('aria-expanded', 'false');
  });
});
```

**Testing error boundaries:**

```tsx
import { render, screen } from '@testing-library/react';
import { ErrorBoundary } from './ErrorBoundary';

// Component that throws on render
function BrokenComponent() {
  throw new Error('Something went wrong');
}

describe('ErrorBoundary', () => {
  // Suppress console.error for expected errors
  beforeEach(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('displays fallback when child throws', () => {
    render(
      <ErrorBoundary fallback={<div role="alert">Something went wrong</div>}>
        <BrokenComponent />
      </ErrorBoundary>
    );

    expect(screen.getByRole('alert')).toHaveTextContent('Something went wrong');
  });

  it('resets error state when reset button is clicked', async () => {
    const user = userEvent.setup();
    const onReset = jest.fn();

    render(
      <ErrorBoundary fallback={<button onClick={onReset}>Try again</button>}>
        <BrokenComponent />
      </ErrorBoundary>
    );

    await user.click(screen.getByRole('button', { name: /try again/i }));
    expect(onReset).toHaveBeenCalledTimes(1);
  });
});
```

**Testing Suspense boundaries:**

```tsx
import { render, screen, Suspense } from 'react';
import { lazy } from 'react';

// Mock the lazy component
jest.mock('./HeavyComponent', () => ({
  HeavyComponent: () => <div data-testid="heavy-component">Loaded</div>,
}));

describe('Suspense boundary', () => {
  it('shows fallback while component loads', async () => {
    // Simulate async loading
    const HeavyComponent = lazy(
      () =>
        new Promise((resolve) =>
          setTimeout(() => resolve({ default: () => <div data-testid="heavy">Loaded</div> }), 100)
        )
    );

    render(
      <Suspense fallback={<div data-testid="loading">Loading...</div>}>
        <HeavyComponent />
      </Suspense>
    );

    // Fallback shown initially
    expect(screen.getByTestId('loading')).toHaveTextContent('Loading...');

    // Component shown after loading
    expect(await screen.findByTestId('heavy')).toHaveTextContent('Loaded');
  });
});
```

### Mock Service Worker — Network-Level API Mocking

**MSW mocks at the network layer** — your components make real `fetch`/`axios` calls, and MSW intercepts them. This means your tests don't need to know about your HTTP client library.

**MSW setup:**

```ts
// test/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  // GET endpoint
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'Alice',
      email: 'alice@example.com',
    });
  }),

  // POST endpoint with request body validation
  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    if (!body.name || !body.email) {
      return HttpResponse.json({ error: 'Name and email are required' }, { status: 400 });
    }
    return HttpResponse.json(
      { id: 'new-user', name: body.name, email: body.email },
      { status: 201 }
    );
  }),

  // Simulate network error
  http.get('/api/users', () => {
    return HttpResponse.error(); // Network error (not HTTP error)
  }),

  // Simulate HTTP error
  http.get('/api/users/:id', ({ params }) => {
    if (params.id === '999') {
      return HttpResponse.json({ error: 'User not found' }, { status: 404 });
    }
    return HttpResponse.json({ id: params.id, name: 'Alice' });
  }),

  // Delayed response (for loading state testing)
  http.get('/api/slow-data', async () => {
    await new Promise((resolve) => setTimeout(resolve, 2000));
    return HttpResponse.json({ data: 'loaded' });
  }),
];

// test/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);

// test/setup.ts (Jest/Vitest setup file)
import { server } from './mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers()); // Reset handlers between tests
afterAll(() => server.close());
```

**Per-test handler override:**

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { server } from '../test/mocks/server';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('displays user data on success', async () => {
    // Override handler for this test
    server.use(
      http.get('/api/users/123', () => {
        return HttpResponse.json({
          id: '123',
          name: 'Bob',
          email: 'bob@example.com',
        });
      })
    );

    render(<UserProfile userId="123" />);

    expect(await screen.findByRole('heading', { name: /bob/i })).toBeInTheDocument();
    expect(screen.getByText('bob@example.com')).toBeInTheDocument();
  });

  it('displays error on API failure', async () => {
    server.use(
      http.get('/api/users/123', () => {
        return HttpResponse.json({ error: 'Not found' }, { status: 404 });
      })
    );

    render(<UserProfile userId="123" />);

    expect(await screen.findByText(/failed to load user/i)).toBeInTheDocument();
  });

  it('displays loading state while fetching', async () => {
    server.use(
      http.get('/api/users/123', async () => {
        await new Promise((resolve) => setTimeout(resolve, 100));
        return HttpResponse.json({ id: '123', name: 'Bob' });
      })
    );

    render(<UserProfile userId="123" />);

    // Loading state visible immediately
    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    // Data appears after loading
    expect(await screen.findByRole('heading', { name: /bob/i })).toBeInTheDocument();
  });
});
```

### Integration Testing — Multi-Component Workflows

**Integration tests verify that components work together** — they use the real component tree with real state management and mocked network layer.

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { server } from '../test/mocks/server';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { TodoApp } from './TodoApp';

// Custom render with providers
function renderWithProviders(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false }, // Disable retries for faster tests
      mutations: { retry: false },
    },
  });

  return render(<QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>);
}

describe('TodoApp — Integration', () => {
  it('completes a full todo workflow', async () => {
    const user = userEvent.setup();

    // Setup mock handlers
    server.use(
      http.get('/api/todos', () => {
        return HttpResponse.json([{ id: '1', title: 'Existing todo', completed: false }]);
      }),
      http.post('/api/todos', async ({ request }) => {
        const body = await request.json();
        return HttpResponse.json({ id: '2', title: body.title, completed: false }, { status: 201 });
      }),
      http.patch('/api/todos/:id', async ({ request }) => {
        const body = await request.json();
        return HttpResponse.json({
          id: '1',
          title: 'Existing todo',
          completed: body.completed,
        });
      }),
      http.delete('/api/todos/:id', () => {
        return new HttpResponse(null, { status: 204 });
      })
    );

    renderWithProviders(<TodoApp />);

    // 1. Load existing todos
    expect(await screen.findByText('Existing todo')).toBeInTheDocument();

    // 2. Add new todo
    const input = screen.getByPlaceholderText('Add a todo');
    await user.type(input, 'New todo');
    await user.click(screen.getByRole('button', { name: /add/i }));
    expect(await screen.findByText('New todo')).toBeInTheDocument();

    // 3. Mark todo as complete
    const checkbox = screen.getByRole('checkbox', { name: /existing todo/i });
    await user.click(checkbox);
    expect(checkbox).toBeChecked();

    // 4. Delete todo
    const deleteButton = screen.getByRole('button', {
      name: /delete.*new todo/i,
    });
    await user.click(deleteButton);
    await waitFor(() => {
      expect(screen.queryByText('New todo')).not.toBeInTheDocument();
    });
  });

  it('handles network error gracefully', async () => {
    const user = userEvent.setup();

    server.use(http.get('/api/todos', () => HttpResponse.error()));

    renderWithProviders(<TodoApp />);

    expect(await screen.findByText(/failed to load todos/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
  });
});
```

**Custom test utilities** — `test-utils.tsx`:

```tsx
// test/test-utils.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RouterProvider, createMemoryRouter } from 'react-router-dom';
import type { ReactElement } from 'react';

// Custom render with all providers
interface RenderOptions {
  route?: string;
  initialEntries?: string[];
  queryClient?: QueryClient;
}

function customRender(ui: ReactElement, options: RenderOptions = {}) {
  const { route = '/', initialEntries = [route], queryClient } = options;

  const router = createMemoryRouter([{ path: route, element: ui }], {
    initialEntries,
  });

  const qc =
    queryClient ||
    new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false },
      },
    });

  return {
    ...render(
      <QueryClientProvider client={qc}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    ),
    user: userEvent.setup(),
    router,
    queryClient: qc,
  };
}

// Re-export everything from RTL
export * from '@testing-library/react';
export { customRender as render };

// Custom assertions
export const expectLoading = () => {
  expect(screen.getByRole('status')).toBeInTheDocument();
};

export const expectError = (message: string | RegExp) => {
  expect(screen.getByRole('alert')).toHaveTextContent(message);
};

export const expectToast = async (message: string | RegExp) => {
  expect(await screen.findByText(message)).toBeInTheDocument();
};
```

### Testing Anti-Patterns — What NOT to Do

```tsx
// ❌ ANTI-PATTERN: Testing implementation details
test('updates state correctly', () => {
  const { container } = render(<Counter />);
  // Testing internal state — this is an implementation detail!
  expect((container as any)._currentElement.state.count).toBe(0);
});

// ✅ CORRECT: Testing observable behavior
test('displays correct count', async () => {
  const user = userEvent.setup();
  render(<Counter />);
  expect(screen.getByText('Count: 0')).toBeInTheDocument();
  await user.click(screen.getByRole('button', { name: /increment/i }));
  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});

// ❌ ANTI-PATTERN: Shallow rendering (enzyme)
// Tests component in isolation, missing integration issues
shallow(<MyComponent />)
  .find('ChildComponent')
  .prop('onClick')();

// ✅ CORRECT: Full DOM rendering
render(<MyComponent />);
await user.click(screen.getByRole('button'));
expect(screen.getByText('Result')).toBeInTheDocument();

// ❌ ANTI-PATTERN: Mocking child components
jest.mock('./ChildComponent', () => () => <div>Mocked child</div>);
// Hides integration issues between parent and child

// ✅ CORRECT: Real child components (mock only network/external deps)
render(<ParentComponent />);
// ChildComponent renders for real

// ❌ ANTI-PATTERN: Testing by className
expect(screen.getByTestId('submit-btn').className).toContain('bg-blue');

// ✅ CORRECT: Testing by role and accessible name
const button = screen.getByRole('button', { name: /submit/i });
expect(button).toHaveAttribute('data-variant', 'primary');

// ❌ ANTI-PATTERN: Flaky tests with arbitrary timeouts
await new Promise((resolve) => setTimeout(resolve, 500));

// ✅ CORRECT: waitFor for async assertions
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});
```

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                     | Deliverable                          |
| ------------------------------------ | ------------------------------------------------------------------ | ------------------------------------ |
| **Stage 2** (Web Prototype + IDS)    | Identify testable behaviors from IDS specifications                | Test requirements in IDS             |
| **Stage 3** (Architecture)           | Define testing architecture; register ADRs for test tool selection | Testing ADRs                         |
| **Stage 5** (Development)            | Write component tests, integration tests, MSW handlers             | Test suite alongside production code |
| **Stage 6** (Code Review)            | Review test quality, coverage, anti-patterns                       | Testing section in DEFECT-REPORT.md  |
| **Stage 7** (Automated Testing)      | Execute full test suite; meet coverage thresholds; fix defects     | Test results report                  |
| **Stage 8** (Integrity Verification) | Verify tests cover all IDS-specified behaviors                     | Test integrity verification          |
| **Stage 10** (Release Readiness)     | Confirm testing sign-off (Item 5: "100% automated test pass rate") | Testing compliance contribution      |

## Quality Standards

| Metric                        | Target                                                                      | Enforcement                                |
| ----------------------------- | --------------------------------------------------------------------------- | ------------------------------------------ |
| **Test coverage**             | ≥ 80% lines, ≥ 90% branches                                                 | CI gate via Istanbul/Vitest coverage       |
| **Component coverage**        | 100% of components have at least one test                                   | Test file audit                            |
| **RTL query discipline**      | 100% of queries use role/label/text (zero getByTestId unless documented)    | Code review; eslint rule                   |
| **No implementation testing** | Zero tests that access component state, refs, or internal methods           | Code review                                |
| **MSW coverage**              | 100% of API calls mocked at network level                                   | Test audit; zero fetch/axios mocks         |
| **Integration test coverage** | All critical user flows have integration tests                              | Test audit against user journey map        |
| **Flaky test rate**           | Zero flaky tests in CI                                                      | CI retry analysis; flaky tests quarantined |
| **Test execution time**       | Full test suite completes in < 60 seconds                                   | CI timing metrics                          |
| **Accessibility testing**     | All component tests include accessibility assertions                        | RTL `jest-axe` integration                 |
| **Error path coverage**       | All error states tested (network errors, validation errors, boundary cases) | Code review; mutation testing              |
| **Custom render usage**       | All tests use shared `render` function with providers                       | Code review                                |
| **Test readability**          | Tests follow AAA pattern (Arrange, Act, Assert)                             | Code review                                |
