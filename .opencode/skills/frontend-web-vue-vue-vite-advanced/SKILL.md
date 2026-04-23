---
name: frontend-web-vue-vue-vite-advanced
description: 'Frontend Web skill: Vue Vite Advanced'
---

# Vue 3 and Vite Advanced Patterns

**Category:** Frontend Engineering / Vue Ecosystem
**Owner:** Frontend Engineer (Lucas Silva)

## Overview

This skill provides advanced expertise in Vue 3 Composition API architecture, Vite plugin development and build optimization, Hot Module Replacement (HMR) tuning, code splitting strategies, tree shaking configuration, and the performance engineering needed to ship production-grade Vue applications. Vue 3's Composition API enables powerful patterns for logic reuse and type safety, while Vite provides near-instant development feedback and highly optimized production builds. This skill ensures that Vue-based platforms (whether web admin panels, cross-platform targets, or hybrid applications) meet the same performance, quality, and maintainability standards as React counterparts across all pipeline stages from Stage 2 prototype validation through Stage 6 code review.

## Competency Dimensions

| Dimension                        | Description                                                                    | Proficiency Indicators                                                                  |
| -------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| **Composition API Architecture** | Composables, reactive state patterns, provide/inject, lifecycle management     | Zero Options API in new code; composables are pure, testable, and type-safe             |
| **Vite Plugin Development**      | Custom plugin creation, transform hooks, resolve hooks, dev server middleware  | Custom plugins for domain-specific transforms; zero build-time workarounds              |
| **HMR Optimization**             | Fast refresh configuration, module graph optimization, HMR boundary management | HMR updates in < 100ms; no full page reloads during development                         |
| **Code Splitting**               | Route-level, component-level, and vendor splitting with dynamic imports        | All routes lazy-loaded; vendor chunks optimally split; preload/prefetch strategy        |
| **Tree Shaking**                 | ESM-first architecture, sideEffects configuration, dead code elimination       | Zero unused exports in production bundle; package.json sideEffects correctly configured |
| **Build Optimization**           | Minification, compression, asset optimization, bundle analysis                 | Production build < 170KB gzipped initial; all assets optimized                          |

## Execution Guidance

### Composition API — Production Architecture

**The Composition API is not just a syntax change** — it's a fundamental shift in how we structure component logic, enabling true logic reuse without mixins or higher-order components.

**Composable design patterns:**

```ts
// composables/useTodos.ts
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import type { Ref, ComputedRef } from 'vue';
import { api } from '@/lib/api';

interface Todo {
  id: string;
  title: string;
  completed: boolean;
  createdAt: Date;
}

interface UseTodosReturn {
  todos: Ref<Todo[]>;
  filteredTodos: ComputedRef<Todo[]>;
  isLoading: Ref<boolean>;
  error: Ref<string | null>;
  filter: Ref<string>;
  addTodo: (title: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
  refresh: () => Promise<void>;
}

export function useTodos(): UseTodosReturn {
  // Reactive state — these are the component's private state
  const todos = ref<Todo[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const filter = ref('');

  // Computed — derived state, auto-updates when dependencies change
  const filteredTodos = computed(() => {
    if (!filter.value) return todos.value;
    return todos.value.filter((todo) =>
      todo.title.toLowerCase().includes(filter.value.toLowerCase())
    );
  });

  // Methods — business logic
  async function fetchTodos() {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await api.get<Todo[]>('/todos');
      todos.value = response.data;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch todos';
    } finally {
      isLoading.value = false;
    }
  }

  async function addTodo(title: string) {
    try {
      const response = await api.post<Todo>('/todos', { title });
      todos.value.push(response.data);
    } catch (err) {
      error.value = 'Failed to add todo';
      throw err;
    }
  }

  async function toggleTodo(id: string) {
    const todo = todos.value.find((t) => t.id === id);
    if (!todo) return;

    // Optimistic update
    const previousCompleted = todo.completed;
    todo.completed = !todo.completed;

    try {
      await api.patch(`/todos/${id}`, { completed: todo.completed });
    } catch (err) {
      // Rollback
      todo.completed = previousCompleted;
      error.value = 'Failed to update todo';
      throw err;
    }
  }

  async function deleteTodo(id: string) {
    const index = todos.value.findIndex((t) => t.id === id);
    if (index === -1) return;

    // Optimistic update — save for rollback
    const removedTodo = todos.value.splice(index, 1)[0];

    try {
      await api.delete(`/todos/${id}`);
    } catch (err) {
      // Rollback
      todos.value.splice(index, 0, removedTodo);
      error.value = 'Failed to delete todo';
      throw err;
    }
  }

  // Lifecycle — fetch on mount
  onMounted(fetchTodos);

  // Watch — react to filter changes
  watch(filter, () => {
    // filter change triggers filteredTodos recomputation automatically
    // No need to refetch — filtering is client-side
  });

  // Cleanup — abort pending requests on unmount
  onUnmounted(() => {
    // AbortController cleanup if using fetch
  });

  return {
    todos,
    filteredTodos,
    isLoading,
    error,
    filter,
    addTodo,
    toggleTodo,
    deleteTodo,
    refresh: fetchTodos,
  };
}
```

**Using composables in components:**

```vue
<script setup lang="ts">
import { useTodos } from '@/composables/useTodos';

// Destructure — all refs maintain reactivity
const { filteredTodos, isLoading, error, filter, addTodo, toggleTodo, deleteTodo } = useTodos();

// Local state
const newTodoTitle = ref('');

async function handleAddTodo() {
  if (!newTodoTitle.value.trim()) return;
  await addTodo(newTodoTitle.value);
  newTodoTitle.value = '';
}
</script>

<template>
  <div class="todo-app">
    <form @submit.prevent="handleAddTodo">
      <input v-model="newTodoTitle" placeholder="Add a todo" />
      <button type="submit" :disabled="isLoading">Add</button>
    </form>

    <input v-model="filter" placeholder="Filter todos" />

    <div v-if="isLoading" role="status">Loading...</div>
    <div v-if="error" role="alert">{{ error }}</div>

    <ul>
      <li v-for="todo in filteredTodos" :key="todo.id">
        <input
          type="checkbox"
          :checked="todo.completed"
          @change="toggleTodo(todo.id)"
          :aria-label="todo.title"
        />
        <span :class="{ completed: todo.completed }">{{ todo.title }}</span>
        <button @click="deleteTodo(todo.id)" :aria-label="`Delete ${todo.title}`">✕</button>
      </li>
    </ul>
  </div>
</template>
```

**Composable composition pattern** — combining multiple composables:

```ts
// composables/useAuthenticatedTodos.ts
import { useAuth } from './useAuth';
import { useTodos } from './useTodos';
import { watch } from 'vue';

export function useAuthenticatedTodos() {
  const { isAuthenticated, user, login } = useAuth();
  const { todos, filteredTodos, isLoading, error, addTodo, toggleTodo, deleteTodo } = useTodos();

  // Watch auth state — refetch when user changes
  watch(user, (newUser, oldUser) => {
    if (newUser?.id !== oldUser?.id) {
      // User changed — todos composable will refetch via the watch
    }
  });

  return {
    isAuthenticated,
    user,
    login,
    todos,
    filteredTodos,
    isLoading,
    error,
    addTodo,
    toggleTodo,
    deleteTodo,
  };
}
```

**Provide/Inject for dependency injection:**

```ts
// App.vue — provide at root
import { provide, ref } from 'vue';

const theme = ref<'light' | 'dark'>('light');
provide('theme', theme);
provide('toggleTheme', () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
});

// Any descendant component — inject
const theme = inject<Ref<'light' | 'dark'>>('theme');
const toggleTheme = inject<() => void>('toggleTheme');

// ✅ Type-safe with injection keys
const ThemeKey = Symbol() as InjectionKey<Ref<'light' | 'dark'>>;
provide(ThemeKey, theme);
const theme = inject(ThemeKey); // Type-inferred
```

### Vite Plugin Development

**When to write a custom Vite plugin:**

- Transforming domain-specific file types (`.mdx`, `.graphql`, `.proto`)
- Injecting environment variables or configuration at build time
- Adding custom dev server middleware (mock API, proxy)
- Modifying the build pipeline (minification, asset processing)

**Plugin anatomy:**

```ts
// plugins/mdx-loader.ts
import type { Plugin } from 'vite';
import { compile } from '@mdx-js/mdx';

export function mdxLoader(): Plugin {
  return {
    name: 'mdx-loader',

    // Transform hook — runs on each module
    async transform(code, id) {
      if (!id.endsWith('.mdx')) return null;

      // Compile MDX to JSX
      const compiled = await compile(code, {
        jsx: true,
        jsxImportSource: 'react',
      });

      return {
        code: compiled.toString(),
        map: compiled.map,
      };
    },

    // Configure the plugin to handle .mdx files
    config(config) {
      return {
        esbuild: {
          include: /\.(mdx)$/,
        },
      };
    },

    // Dev server middleware
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        // Custom middleware logic
        next();
      });
    },

    // HMR handling
    handleHotUpdate({ file, server }) {
      if (file.endsWith('.mdx')) {
        // Invalidate and re-transform
        server.ws.send({
          type: 'full-reload',
          path: '*',
        });
      }
    },
  };
}
```

**Using plugins in vite.config.ts:**

```ts
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';
import { mdxLoader } from './plugins/mdx-loader';

export default defineConfig({
  plugins: [vue(), vueJsx(), mdxLoader()],

  // Build optimization
  build: {
    target: 'es2020',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          charts: ['chart.js'],
          utils: ['lodash-es', 'date-fns'],
        },
      },
    },
    chunkSizeWarningLimit: 500, // Warn if any chunk > 500KB
  },

  // Development server
  server: {
    port: 3000,
    hmr: {
      overlay: true, // Show error overlay
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },

  // CSS optimization
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: '@import "@/styles/variables";',
      },
    },
    postcss: {
      plugins: [
        // autoprefixer, cssnano, etc.
      ],
    },
  },

  // Resolve aliases
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@/composables': path.resolve(__dirname, 'src/composables'),
      '@/components': path.resolve(__dirname, 'src/components'),
    },
  },
});
```

### HMR Optimization

**HMR should be instant** — if you're seeing full page reloads during development, something is misconfigured.

**Common HMR issues and fixes:**

```ts
// ❌ PROBLEM: Full page reload on any change
// Cause: Importing a non-HMR-compatible module (e.g., CSS-in-JS without HMR support)

// ✅ FIX: Ensure all dependencies support HMR
// Use vite-plugin-vue for Vue SFCs — HMR is built-in

// ❌ PROBLEM: HMR doesn't update component state
// Cause: State is in module scope (not component scope)

// ✅ FIX: Move state into composables or component setup
// Module-scope state persists across HMR, which can cause stale state
const moduleState = ref(0); // ❌ Persists across HMR

function useLocalState() {
  return ref(0); // ✅ Fresh on each HMR update
}

// ❌ PROBLEM: HMR triggers on unrelated file changes
// Cause: Overly broad file watching

// ✅ FIX: Configure Vite's server.watch to exclude unnecessary directories
export default defineConfig({
  server: {
    watch: {
      ignored: ['**/node_modules/**', '**/.git/**', '**/dist/**', '**/coverage/**', '**/.turbo/**'],
    },
  },
});

// HMR boundary — control what triggers re-render
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    if (!newModule) return;
    // Custom HMR handling
    // For example, update a store without re-rendering the entire app
  });
}
```

**Vue SFC HMR** — Vue's official plugin handles HMR automatically for `.vue` files:

```
Template changes → HMR updates template only (state preserved)
<script> changes → HMR re-runs setup function (state reset)
<style> changes → HMR injects new styles (no re-render)
<style scoped> changes → HMR updates scoped styles (no flash)
```

### Code Splitting in Vue

**Route-level code splitting:**

```ts
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/HomePage.vue'), // Dynamic import → code split
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/pages/DashboardPage.vue'),
    children: [
      {
        path: 'analytics',
        component: () => import('@/pages/DashboardAnalytics.vue'),
      },
      {
        path: 'settings',
        component: () => import('@/pages/DashboardSettings.vue'),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  // Prefetch routes on hover
  scrollBehavior: (to, from, savedPosition) => {
    // Prefetch the target route's components
    to.matched.forEach((record) => {
      if (typeof record.components?.default === 'function') {
        record.components.default(); // Trigger dynamic import
      }
    });
    return savedPosition || { top: 0 };
  },
});

export default router;
```

**Component-level code splitting:**

```vue
<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

// Async component with loading and error states
const HeavyChart = defineAsyncComponent({
  loader: () => import('@/components/HeavyChart.vue'),
  loadingComponent: ChartSkeleton,
  errorComponent: ChartError,
  delay: 200, // Wait 200ms before showing loading component
  timeout: 10000, // Timeout after 10 seconds
});

// Async component with retry
const ExternalWidget = defineAsyncComponent({
  loader: () => import('@/components/ExternalWidget.vue'),
  onError(error, retry, fail, attempts) {
    if (attempts <= 3) {
      retry(); // Retry up to 3 times
    } else {
      fail(); // Give up
    }
  },
});
</script>

<template>
  <Suspense>
    <template #default>
      <HeavyChart :data="chartData" />
    </template>
    <template #fallback>
      <ChartSkeleton />
    </template>
  </Suspense>
</template>
```

**Manual chunk splitting** in Vite:

```ts
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          // Vendor chunks
          if (id.includes('node_modules')) {
            if (id.includes('vue') || id.includes('pinia')) return 'vendor-vue';
            if (id.includes('lodash')) return 'vendor-lodash';
            if (id.includes('chart.js')) return 'vendor-charts';
            return 'vendor-other';
          }

          // Feature chunks
          if (id.includes('/features/analytics/')) return 'feature-analytics';
          if (id.includes('/features/settings/')) return 'feature-settings';
        },
      },
    },
  },
});
```

### Tree Shaking — Eliminating Dead Code

**Vue 3 is tree-shakeable** — unused APIs are eliminated from the bundle:

```ts
// ✅ Tree-shakeable — only used APIs are included
import { ref, computed, watch } from 'vue';

// ❌ Not tree-shakeable — imports entire Vue
import Vue from 'vue';

// Ensure package.json has sideEffects flag
// package.json:
// {
//   "sideEffects": ["*.vue", "*.css", "*.scss"]
// }
```

**Composable tree shaking** — composables should be pure functions:

```ts
// ✅ Pure composable — tree-shakeable if unused
export function useFeatureA() {
  const state = ref(0);
  return { state };
}

// ❌ Impure composable — side effects prevent tree shaking
export function useFeatureB() {
  window.__featureB__ = {}; // Side effect
  const state = ref(0);
  return { state };
}
```

**Build-time tree shaking verification:**

```bash
# Analyze bundle
npx vite-bundle-visualizer

# Check for unused exports
npx rollup --config --silent --failAfterWarnings

# Verify tree shaking
# Look for modules that are included but have 0 bytes (fully shaken)
```

### Build Optimization Checklist

| Optimization                         | Configuration                 | Impact                                                 |
| ------------------------------------ | ----------------------------- | ------------------------------------------------------ |
| **ESBuild minification**             | `build.minify: 'esbuild'`     | Fast minification, good compression                    |
| **Terser for advanced minification** | `build.minify: 'terser'`      | Slower but better compression; supports `drop_console` |
| **Gzip/Brotli compression**          | `vite-plugin-compression`     | ~70% size reduction                                    |
| **Image optimization**               | `vite-plugin-imagemin`        | ~30-50% image size reduction                           |
| **Font subsetting**                  | Custom plugin or build script | ~60% font size reduction                               |
| **CSS code splitting**               | `build.cssCodeSplit: true`    | Per-route CSS loading                                  |
| **Preload directives**               | `build.modulePreload`         | Browser fetches critical chunks early                  |
| **Dynamic import preload**           | `<link rel="modulepreload">`  | Prefetch route chunks on navigation                    |

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                                 | Deliverable                                 |
| ------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------- |
| **Stage 2** (Web Prototype + IDS)    | Validate Vue-based prototype against IDS; document component architecture      | Vue prototype, component architecture notes |
| **Stage 3** (Architecture)           | Define Vue architecture in UML; register ADRs for state management and routing | Vue architecture ADRs                       |
| **Stage 5** (Development)            | Implement Vue components, composables, Vite build configuration                | Production Vue codebase                     |
| **Stage 6** (Code Review)            | Review Composition API patterns, Vite config, code splitting, tree shaking     | Vue architecture review in DEFECT-REPORT.md |
| **Stage 8** (Integrity Verification) | Verify Vue build meets performance budgets; validate all components match IDS  | Vue integrity verification report           |

## Quality Standards

| Metric                        | Target                                                   | Enforcement                                  |
| ----------------------------- | -------------------------------------------------------- | -------------------------------------------- |
| **Composition API adoption**  | 100% of new components use `<script setup>`              | Code review; zero Options API in new code    |
| **Composable quality**        | All composables are pure, type-safe, and testable        | Code review; unit test coverage              |
| **Code splitting**            | 100% of routes lazy-loaded                               | Import audit; zero synchronous route imports |
| **Tree shaking**              | Zero unused exports in production bundle                 | Bundle analyzer; sideEffects audit           |
| **HMR performance**           | HMR updates in < 100ms                                   | Manual measurement during development        |
| **Build size**                | Initial bundle < 170KB gzipped                           | CI gate via bundle analyzer                  |
| **Type safety**               | 100% of composables and components are type-safe         | `vue-tsc --noEmit` in CI                     |
| **Provide/Inject usage**      | Only for cross-cutting concerns (theme, auth, i18n)      | Code review; no over-use of provide/inject   |
| **Lifecycle cleanup**         | All subscriptions and timers cleaned up in `onUnmounted` | Code review                                  |
| **Vite plugin quality**       | Custom plugins have tests and documentation              | Code review; plugin test coverage            |
| **Vendor chunk optimization** | No vendor chunk > 100KB without justification            | Bundle analyzer review                       |
| **CSS optimization**          | No unused CSS in production                              | PurgeCSS or similar audit                    |
