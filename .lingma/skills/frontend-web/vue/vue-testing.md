---
name: vue-testing
description: This skill establishes the comprehensive testing discipline for Vue 3 applications, covering unit testing with Vitest and Vue Test Utils.
---

# Vue Testing — Vitest, Vue Test Utils, and Cypress

**Category:** Frontend Engineering / Testing
**Owner:** Frontend Engineer (Lucas Silva)

## Overview

This skill establishes the comprehensive testing discipline for Vue 3 applications, covering unit testing with Vitest and Vue Test Utils, component testing patterns that validate behavior over implementation, E2E testing with Cypress for critical user journeys, and visual regression testing for design fidelity verification. Vue's reactivity system and SFC architecture require testing approaches that respect the Composition API's reactive semantics while ensuring that component behavior matches the CDO's IDS specifications. This skill supports Stage 6 Code Review through Stage 8 Integrity Verification by providing the testing infrastructure needed to guarantee component correctness, integration reliability, and visual consistency.

## Competency Dimensions

| Dimension                      | Description                                                                     | Proficiency Indicators                                                           |
| ------------------------------ | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Vitest Configuration**       | Test runner setup, globals, coverage, mocking, environment configuration        | Zero-config Vitest for Vue; coverage thresholds enforced; MSW integration        |
| **Vue Test Utils**             | Mounting strategies, reactive state testing, event simulation, slot testing     | Tests use `mount`/`shallowMount` appropriately; all reactive states verified     |
| **Component Testing Patterns** | Testing props, emits, slots, composables, async components, Suspense            | Every component tested for default render, props variants, emits, and edge cases |
| **Cypress E2E**                | End-to-end test architecture, network stubbing, custom commands, CI integration | All critical user flows have E2E tests; flaky test rate = 0                      |
| **Visual Regression**          | Pixel-perfect comparison, baseline management, CI integration, diff analysis    | Visual regression CI gate; baseline updates require CDO approval                 |
| **Composable Testing**         | Testing reactive state, side effects, lifecycle hooks, async operations         | All composables have unit tests; reactive state transitions verified             |

## Execution Guidance

### Vitest Configuration for Vue

**Vitest is the natural test runner for Vite-based Vue projects** — it shares the same configuration, uses the same plugin system, and provides instant test feedback through HMR.

```ts
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  test: {
    // Environment
    environment: 'jsdom',
    globals: true, // No need to import describe, it, expect

    // Setup
    setupFiles: ['./test/setup.ts'],

    // Coverage
    coverage: {
      provider: 'v8', // More accurate than istanbul
      reporter: ['text', 'json', 'html'],
      thresholds: {
        global: {
          branches: 80,
          functions: 90,
          lines: 85,
          statements: 85,
        },
      },
      exclude: [
        'node_modules/',
        'test/',
        '**/*.d.ts',
        '**/*.config.ts',
        'src/main.ts', // Entry point — hard to test
      ],
    },

    // Mocking
    server: {
      deps: {
        inline: ['vue'], // Don't transform Vue
      },
    },

    // Include/exclude
    include: ['src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'],
    exclude: ['node_modules', 'dist', '.idea', '.git', '.cache'],
  },
});
```

**Test setup file:**

```ts
// test/setup.ts
import { afterAll, afterEach, beforeAll, vi } from 'vitest';
import { cleanup } from '@testing-library/vue';
import { server } from './mocks/server';

// MSW server setup
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => {
  server.resetHandlers();
  cleanup(); // Clean up DOM between tests
});
afterAll(() => server.close());

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};
```

### Vue Test Utils — Component Testing

**Mounting strategies** — choose the right approach for the test:

```ts
import { mount, shallowMount, VueWrapper } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import TodoItem from '@/components/TodoItem.vue';

describe('TodoItem', () => {
  // ✅ mount — renders full component tree (children included)
  // Use when testing integration with child components
  it('renders full component tree', () => {
    const wrapper = mount(TodoItem, {
      props: {
        todo: { id: '1', title: 'Test todo', completed: false },
      },
    });

    expect(wrapper.text()).toContain('Test todo');
  });

  // ✅ shallowMount — stubs all child components
  // Use when testing parent component in isolation
  it('renders with stubbed children', () => {
    const wrapper = shallowMount(TodoItem, {
      props: {
        todo: { id: '1', title: 'Test todo', completed: false },
      },
    });

    // Child components are stubs
    expect(wrapper.findComponent({ name: 'TodoActions' }).exists()).toBe(true);
    expect(wrapper.findComponent({ name: 'TodoActions' }).vm).toBeDefined();
  });
});
```

**Testing props and reactive state:**

```ts
import { mount } from '@vue/test-utils';
import { ref, nextTick } from 'vue';
import Counter from '@/components/Counter.vue';

describe('Counter', () => {
  it('displays initial count from props', () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 5 },
    });

    expect(wrapper.text()).toContain('Count: 5');
  });

  it('increments count on button click', async () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 0 },
    });

    expect(wrapper.text()).toContain('Count: 0');

    // Trigger event
    await wrapper.find('button.increment').trigger('click');

    // Wait for Vue to update DOM
    await nextTick();

    expect(wrapper.text()).toContain('Count: 1');
  });

  it('reacts to prop changes', async () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 0 },
    });

    expect(wrapper.text()).toContain('Count: 0');

    // Update props
    await wrapper.setProps({ initialCount: 10 });
    await nextTick();

    expect(wrapper.text()).toContain('Count: 10');
  });

  it('emits event on count change', async () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 0 },
    });

    await wrapper.find('button.increment').trigger('click');
    await nextTick();

    // Check emitted events
    expect(wrapper.emitted('count-changed')).toBeTruthy();
    expect(wrapper.emitted('count-changed')?.[0]).toEqual([1]);
  });
});
```

**Testing slots:**

```ts
import { mount } from '@vue/test-utils';
import Modal from '@/components/Modal.vue';

describe('Modal', () => {
  it('renders default slot content', () => {
    const wrapper = mount(Modal, {
      slots: {
        default: '<p>Slot content</p>',
      },
    });

    expect(wrapper.find('p').text()).toBe('Slot content');
  });

  it('renders named slots', () => {
    const wrapper = mount(Modal, {
      slots: {
        header: '<h1>Modal Title</h1>',
        footer: '<button>Close</button>',
        default: '<p>Body content</p>',
      },
    });

    expect(wrapper.find('h1').text()).toBe('Modal Title');
    expect(wrapper.find('button').text()).toBe('Close');
    expect(wrapper.find('p').text()).toBe('Body content');
  });

  it('renders scoped slots', () => {
    const wrapper = mount(Modal, {
      slots: {
        default: `<template #default="{ isOpen }">
          <span>{{ isOpen ? 'Open' : 'Closed' }}</span>
        </template>`,
      },
      data() {
        return { isOpen: true };
      },
    });

    expect(wrapper.find('span').text()).toBe('Open');
  });
});
```

**Testing async components and Suspense:**

```ts
import { mount, flushPromises } from '@vue/test-utils';
import AsyncWrapper from '@/components/AsyncWrapper.vue';

describe('AsyncWrapper', () => {
  it('shows loading state then content', async () => {
    const wrapper = mount(AsyncWrapper);

    // Initial loading state
    expect(wrapper.find('.loading').exists()).toBe(true);

    // Wait for async component to resolve
    await flushPromises();
    await wrapper.vm.$nextTick();

    // Content rendered
    expect(wrapper.find('.content').exists()).toBe(true);
    expect(wrapper.find('.loading').exists()).toBe(false);
  });

  it('shows error state on failure', async () => {
    // Mock the API to fail
    vi.spyOn(api, 'fetchData').mockRejectedValue(new Error('Network error'));

    const wrapper = mount(AsyncWrapper);

    await flushPromises();
    await wrapper.vm.$nextTick();

    expect(wrapper.find('.error').exists()).toBe(true);
    expect(wrapper.find('.error').text()).toContain('Network error');
  });
});
```

### Composable Testing

**Testing composables in isolation** — composables are pure functions, so they're straightforward to test:

```ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useCounter } from '@/composables/useCounter';
import { nextTick } from 'vue';

describe('useCounter', () => {
  // Reset Vue's reactivity system between tests
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('initializes with default count of 0', () => {
    const { count } = useCounter();
    expect(count.value).toBe(0);
  });

  it('initializes with custom count', () => {
    const { count } = useCounter({ initialCount: 10 });
    expect(count.value).toBe(10);
  });

  it('increments count', async () => {
    const { count, increment } = useCounter();

    increment();
    await nextTick(); // Wait for reactive update

    expect(count.value).toBe(1);
  });

  it('decrements count', async () => {
    const { count, decrement } = useCounter({ initialCount: 5 });

    decrement();
    await nextTick();

    expect(count.value).toBe(4);
  });

  it('emits count-changed event', async () => {
    const onCountChange = vi.fn();
    const { increment, on } = useCounter();

    on('count-changed', onCountChange);
    increment();
    await nextTick();

    expect(onCountChange).toHaveBeenCalledWith(1);
  });

  it('respects max limit', async () => {
    const { count, increment } = useCounter({ max: 3, initialCount: 2 });

    increment();
    await nextTick();
    expect(count.value).toBe(3);

    increment(); // Should not exceed max
    await nextTick();
    expect(count.value).toBe(3);
  });

  it('respects min limit', async () => {
    const { count, decrement } = useCounter({ min: 0, initialCount: 0 });

    decrement(); // Should not go below min
    await nextTick();
    expect(count.value).toBe(0);
  });

  it('async operation with loading state', async () => {
    vi.spyOn(api, 'saveCount').mockResolvedValue({ success: true });

    const { count, isLoading, save } = useCounter();

    const savePromise = save();
    await nextTick();
    expect(isLoading.value).toBe(true);

    await savePromise;
    await nextTick();
    expect(isLoading.value).toBe(false);
  });
});
```

**Testing composables with dependencies:**

```ts
import { useAuthenticatedTodos } from '@/composables/useAuthenticatedTodos';
import * as useAuthModule from '@/composables/useAuth';
import * as useTodosModule from '@/composables/useTodos';

describe('useAuthenticatedTodos', () => {
  it('combines auth and todos composables', () => {
    // Mock dependencies
    vi.spyOn(useAuthModule, 'useAuth').mockReturnValue({
      isAuthenticated: ref(true),
      user: ref({ id: '1', name: 'Alice' }),
      login: vi.fn(),
    });

    vi.spyOn(useTodosModule, 'useTodos').mockReturnValue({
      todos: ref([{ id: '1', title: 'Test', completed: false }]),
      filteredTodos: computed(() => [{ id: '1', title: 'Test', completed: false }]),
      isLoading: ref(false),
      error: ref(null),
      filter: ref(''),
      addTodo: vi.fn(),
      toggleTodo: vi.fn(),
      deleteTodo: vi.fn(),
      refresh: vi.fn(),
    });

    const result = useAuthenticatedTodos();

    expect(result.isAuthenticated.value).toBe(true);
    expect(result.user.value?.name).toBe('Alice');
    expect(result.todos.value).toHaveLength(1);
  });
});
```

### Cypress E2E Testing

**Cypress architecture for Vue applications:**

```ts
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5173', // Vite dev server
    setupNodeEvents(on, config) {
      // Plugin setup
    },
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false, // Disable video recording for faster CI
    screenshotOnRunFailure: true,
    retries: {
      runMode: 2, // Retry failed tests in CI
      openMode: 0, // No retry in interactive mode
    },
  },
  component: {
    devServer: {
      framework: 'vue',
      bundler: 'vite',
    },
  },
});
```

**Custom commands:**

```ts
// cypress/support/commands.ts

// Login command
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.intercept('POST', '/api/auth/login', {
    statusCode: 200,
    body: { token: 'mock-token', user: { id: '1', name: 'Test User' } },
  }).as('loginRequest');

  cy.visit('/login');
  cy.get('[data-testid="email-input"]').type(email);
  cy.get('[data-testid="password-input"]').type(password);
  cy.get('[data-testid="login-button"]').click();
  cy.wait('@loginRequest');
  cy.url().should('include', '/dashboard');
});

// Create todo command
Cypress.Commands.add('createTodo', (title: string) => {
  cy.intercept('POST', '/api/todos', {
    statusCode: 201,
    body: { id: Cypress._.uniqueId('todo-'), title, completed: false },
  }).as('createTodo');

  cy.get('[data-testid="todo-input"]').type(`${title}{enter}`);
  cy.wait('@createTodo');
  cy.contains(title).should('be.visible');
});

declare global {
  namespace Cypress {
    interface Chainable {
      login(email: string, password: string): Chainable<void>;
      createTodo(title: string): Chainable<void>;
    }
  }
}
```

**E2E test — full user journey:**

```ts
// cypress/e2e/todo-workflow.cy.ts

describe('Todo Application — Full Workflow', () => {
  beforeEach(() => {
    // Setup API mocks
    cy.intercept('GET', '/api/todos', {
      statusCode: 200,
      body: [
        { id: '1', title: 'Existing todo', completed: false },
        { id: '2', title: 'Another todo', completed: true },
      ],
    }).as('getTodos');
  });

  it('completes a full todo workflow', () => {
    // 1. Login
    cy.login('test@example.com', 'password123');

    // 2. View existing todos
    cy.wait('@getTodos');
    cy.contains('Existing todo').should('be.visible');
    cy.contains('Another todo').should('be.visible');

    // 3. Add new todo
    cy.createTodo('New todo from E2E test');

    // 4. Toggle todo completion
    cy.intercept('PATCH', '/api/todos/1', {
      statusCode: 200,
      body: { id: '1', title: 'Existing todo', completed: true },
    }).as('toggleTodo');

    cy.get('[data-testid="todo-checkbox-1"]').click();
    cy.wait('@toggleTodo');
    cy.get('[data-testid="todo-checkbox-1"]').should('be.checked');

    // 5. Filter todos
    cy.get('[data-testid="filter-input"]').type('New');
    cy.contains('Existing todo').should('not.be.visible');
    cy.contains('New todo from E2E test').should('be.visible');

    // 6. Delete todo
    cy.intercept('DELETE', '/api/todos/*', { statusCode: 204 }).as('deleteTodo');

    cy.get('[data-testid="delete-todo-New todo from E2E test"]').click();
    cy.wait('@deleteTodo');
    cy.contains('New todo from E2E test').should('not.exist');
  });

  it('handles network errors gracefully', () => {
    cy.login('test@example.com', 'password123');

    // Simulate network failure
    cy.intercept('POST', '/api/todos', {
      statusCode: 500,
      body: { error: 'Internal server error' },
    }).as('createTodoFail');

    cy.get('[data-testid="todo-input"]').type('This will fail{enter}');
    cy.wait('@createTodoFail');

    // Error message displayed
    cy.get('[role="alert"]').should('contain.text', 'Failed to add todo');

    // Todo was not added
    cy.contains('This will fail').should('not.exist');
  });

  it('persists todos across page refresh', () => {
    cy.login('test@example.com', 'password123');
    cy.createTodo('Persistent todo');

    // Refresh page
    cy.reload();
    cy.wait('@getTodos');

    // Todo still exists
    cy.contains('Persistent todo').should('be.visible');
  });
});
```

### Visual Regression Testing

**Visual regression testing ensures that UI changes don't introduce unintended visual differences.** This is critical for maintaining design fidelity against the CDO's IDS specifications.

**Cypress Image Snapshot:**

```ts
// cypress/e2e/visual-regression.cy.ts

describe('Visual Regression — Design Fidelity', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'password123');
  });

  it('Dashboard matches design baseline', () => {
    cy.visit('/dashboard');
    cy.wait('@getTodos');

    // Wait for all content to render
    cy.get('[data-testid="dashboard-content"]').should('be.visible');

    // Take screenshot and compare with baseline
    cy.compareSnapshot('dashboard', {
      errorThreshold: 0.01, // 1% pixel difference allowed
      capture: 'fullPage',
    });
  });

  it('TodoItem matches design baseline in all states', () => {
    cy.visit('/dashboard');

    // Default state
    cy.get('[data-testid="todo-item-1"]').then(($el) => {
      cy.wrap($el).compareSnapshot('todo-item-default');
    });

    // Completed state
    cy.get('[data-testid="todo-checkbox-1"]').click();
    cy.get('[data-testid="todo-item-1"]').then(($el) => {
      cy.wrap($el).compareSnapshot('todo-item-completed');
    });

    // Hover state
    cy.get('[data-testid="todo-item-1"]').trigger('mouseover');
    cy.get('[data-testid="todo-item-1"]').then(($el) => {
      cy.wrap($el).compareSnapshot('todo-item-hover');
    });

    // Loading state
    cy.intercept('GET', '/api/todos', { delay: 5000 }).as('slowTodos');
    cy.reload();
    cy.get('[data-testid="todo-item-skeleton"]').then(($el) => {
      cy.wrap($el).compareSnapshot('todo-item-loading');
    });
  });

  it('Responsive design — mobile viewport', () => {
    cy.viewport('iphone-6');
    cy.visit('/dashboard');

    cy.compareSnapshot('dashboard-mobile', {
      errorThreshold: 0.02, // Slightly higher threshold for mobile
      capture: 'fullPage',
    });
  });

  it('Dark mode matches design baseline', () => {
    cy.visit('/dashboard');
    cy.get('[data-testid="theme-toggle"]').click();

    cy.compareSnapshot('dashboard-dark', {
      errorThreshold: 0.01,
      capture: 'fullPage',
    });
  });
});
```

**Baseline management workflow:**

```
1. Baseline Creation (Initial Run)
   └─ Run visual regression tests
   └─ All screenshots become baselines
   └─ Commit baselines to git
        ↓
2. Change Detection (Subsequent Runs)
   └─ Run tests against new code
   └─ Compare with baselines
   └─ If diff > threshold → test fails
        ↓
3. Review and Update
   └─ Review diff images
   └─ If change is intentional → update baseline (requires CDO approval)
   └─ If change is unintentional → fix the code
        ↓
4. CI Integration
   └─ Visual regression runs on every PR
   └─ Fails build if unexpected diffs detected
   └─ Diff images uploaded as PR artifacts
```

**CI configuration for visual regression:**

```yaml
# .github/workflows/visual-regression.yml
name: Visual Regression
on: [pull_request]
jobs:
  visual-regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cypress-io/github-action@v6
        with:
          start: npm run dev
          wait-on: 'http://localhost:5173'
          command: npx cypress run --spec 'cypress/e2e/visual-regression.cy.ts'
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: visual-diffs
          path: cypress/snapshots/diff/
```

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                        | Deliverable                                    |
| ------------------------------------ | --------------------------------------------------------------------- | ---------------------------------------------- |
| **Stage 2** (Web Prototype + IDS)    | Identify testable behaviors and visual baselines from IDS             | Test requirements in IDS, visual baseline plan |
| **Stage 5** (Development)            | Write unit tests, component tests, E2E tests, visual regression tests | Test suite alongside Vue codebase              |
| **Stage 6** (Code Review)            | Review test quality, coverage, E2E flow completeness                  | Testing section in DEFECT-REPORT.md            |
| **Stage 7** (Automated Testing)      | Execute full test suite; meet coverage thresholds                     | Test results report                            |
| **Stage 8** (Integrity Verification) | Run visual regression against baselines; verify IDS fidelity          | Visual integrity verification report           |

## Quality Standards

| Metric                     | Target                                                  | Enforcement                         |
| -------------------------- | ------------------------------------------------------- | ----------------------------------- |
| **Unit test coverage**     | ≥ 80% lines, ≥ 90% branches                             | CI gate via Vitest coverage         |
| **Component coverage**     | 100% of components have tests                           | Test file audit                     |
| **Composable coverage**    | 100% of composables have tests                          | Test file audit                     |
| **E2E coverage**           | All critical user flows have E2E tests                  | Test audit against user journey map |
| **Visual regression**      | All key screens have visual baselines                   | Visual test audit                   |
| **Flaky test rate**        | Zero flaky tests in CI                                  | CI retry analysis                   |
| **Test execution time**    | Unit tests < 30s, E2E < 5 minutes                       | CI timing metrics                   |
| **MSW coverage**           | 100% of API calls mocked in unit/component tests        | Test audit                          |
| **Reactive state testing** | All reactive state transitions verified                 | Code review                         |
| **Emit testing**           | All component emits have tests                          | Code review                         |
| **Slot testing**           | All slot variants tested                                | Code review                         |
| **Baseline management**    | Visual baselines updated only with CDO approval         | PR review process                   |
| **Error path coverage**    | All error states tested (network, validation, boundary) | Code review; mutation testing       |
