---
inclusion: manual
description: Frontend/Web architecture patterns and best practices
---

# Frontend Architecture Steering

This steering file provides frontend and web development guidance for the workspace. Activate manually when working on web UI code.

## Frontend Context

- **Frameworks:** React, Vue.js, Angular, Svelte
- **Languages:** TypeScript (preferred), JavaScript
- **Build Tools:** Vite, Webpack, esbuild
- **Package Manager:** npm, yarn, pnpm
- **CSS:** Tailwind CSS, CSS Modules, Styled Components

## Architecture Patterns

### 1. Component Architecture

- **Atomic Design:** Atoms → Molecules → Organisms → Templates → Pages
- **Component Composition:** Build complex UIs from simple components
- **Props vs State:** Props for data flow, state for local component state
- **Controlled Components:** Parent controls component state
- **Presentational vs Container:** Separate UI from logic

### 2. State Management

**React:**

- **Local State:** `useState`, `useReducer`
- **Global State:** Redux, Zustand, Jotai, Recoil
- **Server State:** React Query, SWR
- **Context API:** For theme, auth, i18n

**Vue:**

- **Local State:** `ref`, `reactive`
- **Global State:** Pinia (preferred), Vuex
- **Composables:** Reusable stateful logic

**Angular:**

- **Services:** Singleton services for shared state
- **RxJS:** Reactive state management
- **NgRx:** Redux-style state management

### 3. Routing

- **Client-Side Routing:** React Router, Vue Router, Angular Router
- **Code Splitting:** Lazy load routes for performance
- **Route Guards:** Protect routes with authentication
- **Nested Routes:** Organize complex navigation

### 4. Data Fetching

- **REST APIs:** Fetch, Axios
- **GraphQL:** Apollo Client, urql
- **Caching:** React Query, SWR for automatic caching
- **Optimistic Updates:** Update UI before server response
- **Error Handling:** Retry logic, error boundaries

### 5. Performance Optimization

- **Code Splitting:** Dynamic imports, lazy loading
- **Tree Shaking:** Remove unused code
- **Image Optimization:** WebP, lazy loading, responsive images
- **Memoization:** `React.memo`, `useMemo`, `useCallback`
- **Virtual Scrolling:** For long lists
- **Web Vitals:** Monitor LCP, FID, CLS

### 6. Accessibility (a11y)

- **Semantic HTML:** Use proper HTML elements
- **ARIA Labels:** Add labels for screen readers
- **Keyboard Navigation:** Support tab, enter, escape
- **Focus Management:** Manage focus for modals, dialogs
- **Color Contrast:** WCAG 2.1 AA compliance (4.5:1 ratio)
- **Screen Reader Testing:** Test with NVDA, JAWS, VoiceOver

### 7. Security

- **XSS Prevention:** Sanitize user input, use framework escaping
- **CSRF Protection:** Use CSRF tokens
- **Content Security Policy:** Restrict resource loading
- **HTTPS Only:** Enforce secure connections
- **Secure Storage:** Use httpOnly cookies for sensitive data
- **Input Validation:** Validate on client and server

### 8. Testing

- **Unit Tests:** Jest, Vitest
- **Component Tests:** React Testing Library, Vue Test Utils
- **E2E Tests:** Playwright, Cypress
- **Visual Regression:** Percy, Chromatic
- **Aim for 80%+ code coverage**

## React Best Practices

### 1. Hooks

```typescript
// Custom hook example
function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch user
  }, []);

  return { user, loading };
}
```

### 2. Component Structure

```typescript
// Functional component with TypeScript
interface Props {
  title: string;
  onSubmit: (data: FormData) => void;
}

export function MyComponent({ title, onSubmit }: Props) {
  const [value, setValue] = useState("");

  return (
    <div>
      <h1>{title}</h1>
      {/* Component JSX */}
    </div>
  );
}
```

### 3. Error Boundaries

```typescript
class ErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    // Log error
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

## Vue Best Practices

### 1. Composition API

```typescript
// Composable example
export function useCounter() {
  const count = ref(0);
  const increment = () => count.value++;

  return { count, increment };
}
```

### 2. Component Structure

```vue
<script setup lang="ts">
interface Props {
  title: string;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  submit: [data: FormData];
}>();
</script>

<template>
  <div>
    <h1>{{ title }}</h1>
  </div>
</template>
```

## Styling Best Practices

### 1. CSS Architecture

- **BEM Naming:** Block\_\_Element--Modifier
- **CSS Modules:** Scoped styles per component
- **Utility-First:** Tailwind CSS for rapid development
- **CSS-in-JS:** Styled Components, Emotion

### 2. Responsive Design

- **Mobile-First:** Design for mobile, enhance for desktop
- **Breakpoints:** sm (640px), md (768px), lg (1024px), xl (1280px)
- **Fluid Typography:** Use clamp() for responsive text
- **Container Queries:** Use for component-level responsiveness

## Related Resources

- **Company Architecture Standards:** `company/library/topics/architecture.md`
- **Company Testing Standards:** `company/library/topics/testing.md`
- **Frontend Engineering Skills:** `.kiro/skills/frontend-engineering/`
- **Web Pipeline:** `.kiro/steering/web-pipeline.md`

## When to Activate

Activate this steering file when:

- Building new frontend features
- Reviewing frontend architecture decisions
- Implementing UI components
- Debugging frontend performance issues
- Writing frontend tests
