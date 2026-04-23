# React State Management

**Category:** Frontend Engineering / React Architecture
**Owner:** Frontend Engineer (Yuna Park)

## Overview

This skill enables the design, implementation, and maintenance of robust React state management architectures that scale from simple component state to complex application-wide data flows. It covers Context API for low-frequency global state, Zustand for lightweight client state, Redux Toolkit for complex state with middleware requirements, state normalization for relational data, async state management with React Query patterns, and optimistic update strategies with rollback guarantees. State management is the backbone of application correctness — poorly designed state leads to stale UI, race conditions, and unpredictable behavior that no amount of testing can fully cover.

## Competency Dimensions

| Dimension                  | Description                                                                              | Proficiency Indicators                                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **State Tool Selection**   | Right tool for the right job — Context API vs Zustand vs Redux vs server state libraries | Zero over-engineering (no Redux for 3 boolean flags); zero under-engineering (no prop drilling 8 levels deep) |
| **State Normalization**    | Normalizing relational data into flat lookup tables, eliminating duplication             | No nested data duplication; O(1) entity lookup by ID; consistent update patterns                              |
| **Async State Management** | Server state separation, caching, invalidation, background refetching                    | Server state managed by React Query/SWR; client state in Zustand; zero manual loading flags                   |
| **Optimistic Updates**     | UI updates before server confirmation with automatic rollback on failure                 | Optimistic updates with undo queue; rollback within 100ms of error; user notified of sync failures            |
| **State Colocation**       | Keeping state as close to where it's used as possible                                    | No global state for component-local concerns; minimal cross-component state sharing                           |
| **State Debugging**        | DevTools integration, state inspection, time-travel debugging, action logging            | Full state history traceable; reproduction steps for any state bug within 15 minutes                          |

## Execution Guidance

### State Management Selection Framework

**The state hierarchy** — choose the simplest tool that solves the problem:

```
┌─────────────────────────────────────────────────────────────┐
│                     STATE MANAGEMENT                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Component-local state (useState, useReducer)               │
│    └─ Form inputs, toggle states, local UI flags            │
│    └─ Scope: Single component                               │
│         ↓                                                   │
│  Shared component state (lifted useState, useContext)       │
│    └─ Theme, language preference, authenticated user info   │
│    └─ Scope: Component subtree                              │
│         ↓                                                   │
│  Client global state (Zustand)                              │
│    └─ UI state, feature flags, navigation state, selections │
│    └─ Scope: Entire application                             │
│         ↓                                                   │
│  Complex client state (Redux Toolkit)                       │
│    └─ Undo/redo, time-travel, complex middleware chains     │
│    └─ Scope: Entire application (only when complexity demands it) │
│         ↓                                                   │
│  Server state (React Query / SWR)                           │
│    └─ API data, caching, pagination, real-time updates      │
│    └─ Scope: Entire application                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Decision matrix:**

| State Type        | Tool                                                       | Rationale                                  | Anti-pattern                        |
| ----------------- | ---------------------------------------------------------- | ------------------------------------------ | ----------------------------------- |
| Form input value  | `useState`                                                 | Component-local, no sharing needed         | Storing form state in global store  |
| Theme toggle      | `useContext`                                               | Low-frequency updates, many consumers      | Redux for a single boolean          |
| Shopping cart     | `Zustand`                                                  | Shared across components, frequent updates | Prop drilling cart state 5 levels   |
| Undo/redo editor  | `Redux Toolkit`                                            | Needs time-travel, complex middleware      | Zustand without undo middleware     |
| API response data | `React Query`                                              | Caching, invalidation, background refetch  | Manual fetch + useState + useEffect |
| WebSocket stream  | `React Query` (infinite) or custom hook with Zustand cache | Deduplication, reconnection                | Raw WebSocket in useEffect          |

### Context API — Correct Usage Patterns

**Context is for dependency injection, not state management.** It re-renders ALL consumers when the value changes — use it for low-frequency updates only.

```tsx
// ✅ CORRECT: Context for dependency injection (stable values)
const ThemeContext = createContext({ theme: 'light', toggle: () => {} });

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  const toggle = useCallback(() => setTheme((t) => (t === 'light' ? 'dark' : 'light')), []);
  const value = useMemo(() => ({ theme, toggle }), [theme, toggle]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

// Consumer — only re-renders when theme changes (stable toggle reference)
function ThemedButton() {
  const { theme, toggle } = useContext(ThemeContext);
  return <button onClick={toggle}>{theme}</button>;
}

// ❌ WRONG: Context for high-frequency state (re-renders ALL consumers)
const DataContext = createContext({ items: [], addItem: () => {} });

function DataProvider({ children }) {
  const [items, setItems] = useState([]);
  // Every addItem call creates a new array → ALL consumers re-render
  const value = {
    items,
    addItem: (item) => setItems((prev) => [...prev, item]),
  };
  return <DataContext.Provider value={value}>{children}</DataContext.Provider>;
}

// ✅ FIX: Split context for high-frequency state — use Zustand instead
import { create } from 'zustand';

const useDataStore = create((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  // Consumers only subscribe to the slices they need
}));

// Selective subscription — only re-renders when items.length changes
function ItemCount() {
  const count = useDataStore((state) => state.items.length);
  return <span>{count} items</span>;
}
```

**Context splitting pattern** — separate frequently-changing state from stable state:

```tsx
// Split context by update frequency
const StableContext = createContext(null); // User profile — changes rarely
const DynamicContext = createContext(null); // Notifications — changes frequently

function AppProvider({ children }) {
  const [user, setUser] = useState(null); // Stable
  const [notifications, setNotifications] = useState([]); // Dynamic

  return (
    <StableContext.Provider value={user}>
      <DynamicContext.Provider value={notifications}>{children}</DynamicContext.Provider>
    </StableContext.Provider>
  );
}

// Consumer only subscribes to what it needs
function UserProfile() {
  const user = useContext(StableContext); // Only re-renders when user changes
  return <div>{user?.name}</div>;
}

function NotificationBadge() {
  const notifications = useContext(DynamicContext); // Only re-renders on notification changes
  return <span>{notifications.length}</span>;
}
```

### Zustand — Lightweight Global State

**Zustand is the preferred client state management tool** for most applications. It's lighter than Redux (~1KB), doesn't require a Provider, and supports selective subscriptions out of the box.

**Store architecture pattern:**

```ts
import { create } from 'zustand';
import { devtools, persist, subscribeWithSelector } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

// Define store interface for type safety
interface UIState {
  // State
  sidebar: { isOpen: boolean; activeTab: string };
  modal: { type: string | null; data: Record<string, unknown> | null };
  toast: { id: string; message: string; type: 'success' | 'error' | 'info' }[];

  // Actions
  toggleSidebar: () => void;
  setSidebarTab: (tab: string) => void;
  openModal: (type: string, data?: Record<string, unknown>) => void;
  closeModal: () => void;
  addToast: (message: string, type?: 'success' | 'error' | 'info') => void;
  removeToast: (id: string) => void;
}

// Create store with middleware
export const useUIStore = create<UIState>()(
  devtools( // Redux DevTools integration
    persist( // Persist to localStorage
      subscribeWithSelector( // Enable selective subscriptions
        immer((set) => ({ // Immer for mutable-style updates
          // Initial state
          sidebar: { isOpen: true, activeTab: 'dashboard' },
          modal: { type: null, data: null },
          toast: [],

          // Actions
          toggleSidebar: () => set((state) => {
            state.sidebar.isOpen = !state.sidebar.isOpen;
          }),

          setSidebarTab: (tab) => set((state) => {
            state.sidebar.activeTab = tab;
          }),

          openModal: (type, data) => set((state) => {
            state.modal.type = type;
            state.modal.data = data ?? null;
          }),

          closeModal: () => set((state) => {
            state.modal.type = null;
            state.modal.data = null;
          }),

          addToast: (message, type = 'info') => set((state) => {
            const id = crypto.randomUUID();
            state.toast.push({ id, message, type });
            // Auto-remove after 5 seconds
            setTimeout(() => {
              set((s) => {
                s.toast = s.toast.filter(t => t.id !== id);
              });
            }, 5000);
          }),

          removeToast: (id) => set((state) => {
            state.toast = state.toast.filter(t => t.id !== id);
          }),
        })),
      ),
      { name: 'ui-store' }, // localStorage key
    ),
    { name: 'UIStore' }, // DevTools name
  ),
);

// Selective subscriptions — component only re-renders when selected slice changes
function SidebarToggle() {
  // Only re-renders when sidebar.isOpen changes
  const isOpen = useUIStore(state => state.sidebar.isOpen);
  const toggle = useUIStore(state => state.toggleSidebar);

  return <button onClick={toggle}>{isOpen ? 'Close' : 'Open'}</button>;
}
```

**Store composition pattern** — split stores by domain, compose in consumers:

```ts
// stores/auth.ts
export const useAuthStore = create<AuthState>()(/* ... */);

// stores/cart.ts
export const useCartStore = create<CartState>()(/* ... */);

// stores/settings.ts
export const useSettingsStore = create<SettingsState>()(/* ... */);

// Consumers compose stores as needed
function CheckoutButton() {
  const cartItems = useCartStore(state => state.items);
  const isAuthenticated = useAuthStore(state => state.isAuthenticated);
  const currency = useSettingsStore(state => state.currency);

  return <button>{/* ... */}</button>;
}
```

### Redux Toolkit — When Complexity Demands It

**Use Redux Toolkit only when you need:**

- Time-travel debugging (complex multi-step workflows)
- Sophisticated middleware chains (thunks + sagas + custom middleware)
- Complex undo/redo functionality
- Large team with strict state change auditing requirements

**RTK Query for server state** — the Redux approach to async state:

```ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: '/api',
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) headers.set('authorization', `Bearer ${token}`);
      return headers;
    },
  }),
  tagTypes: ['User', 'Post', 'Comment'],
  endpoints: (builder) => ({
    getPosts: builder.query<Post[], { page: number; limit: number }>({
      query: ({ page, limit }) => `/posts?page=${page}&limit=${limit}`,
      providesTags: ['Post'],
    }),
    createPost: builder.mutation<Post, NewPost>({
      query: (body) => ({ url: '/posts', method: 'POST', body }),
      invalidatesTags: ['Post'], // Invalidate all Post queries
    }),
    updatePost: builder.mutation<Post, { id: string; body: Partial<Post> }>({
      query: ({ id, body }) => ({ url: `/posts/${id}`, method: 'PUT', body }),
      invalidatesTags: (result, error, { id }) => [{ type: 'Post', id }],
    }),
  }),
});

export const { useGetPostsQuery, useCreatePostMutation, useUpdatePostMutation } = api;

// Optimistic update with rollback
export const useOptimisticUpdatePost = () => {
  const [updatePost] = useUpdatePostMutation();

  return async (id: string, body: Partial<Post>) => {
    try {
      await updatePost(
        { id, body },
        {
          // Optimistic update
          fixedCacheKey: `post-${id}`,
        }
      ).unwrap();
    } catch (error) {
      // RTK Query automatically rolls back on error
      // Show error toast
      toast.error('Failed to update post');
      throw error;
    }
  };
};
```

### State Normalization

**Relational data should be normalized** — eliminate duplication, enable O(1) lookups:

```ts
// ❌ DENORMALIZED — duplication, inconsistency risk
const posts = [
  {
    id: '1',
    title: 'Hello World',
    author: { id: 'a1', name: 'Alice', avatar: '...' },
    comments: [
      {
        id: 'c1',
        text: 'Great!',
        author: { id: 'a2', name: 'Bob', avatar: '...' },
      },
      {
        id: 'c2',
        text: 'Thanks',
        author: { id: 'a1', name: 'Alice', avatar: '...' },
      },
    ],
  },
];
// Author data duplicated in multiple places. If Alice changes her name, update everywhere.

// ✅ NORMALIZED — flat entities, references by ID
const entities = {
  posts: {
    '1': {
      id: '1',
      title: 'Hello World',
      authorId: 'a1',
      commentIds: ['c1', 'c2'],
    },
  },
  users: {
    a1: { id: 'a1', name: 'Alice', avatar: '...' },
    a2: { id: 'a2', name: 'Bob', avatar: '...' },
  },
  comments: {
    c1: { id: 'c1', text: 'Great!', authorId: 'a2', postId: '1' },
    c2: { id: 'c2', text: 'Thanks', authorId: 'a1', postId: '1' },
  },
};

// Selector — compose normalized data into denormalized view
const selectPostWithDetails = (postId: string) => (state: RootState) => {
  const post = state.entities.posts[postId];
  const author = state.entities.users[post.authorId];
  const comments = post.commentIds.map((id) => state.entities.comments[id]);
  const commentAuthors = comments.map((c) => state.entities.users[c.authorId]);

  return {
    ...post,
    author,
    comments: comments.map((c, i) => ({ ...c, author: commentAuthors[i] })),
  };
};
```

**Normalization utilities** — use `normalizr` for complex API responses:

```ts
import { normalize, schema } from 'normalizr';

// Define entity schemas
const userSchema = new schema.Entity('users');
const commentSchema = new schema.Entity('comments', { author: userSchema });
const postSchema = new schema.Entity('posts', {
  author: userSchema,
  comments: [commentSchema],
});

// Normalize API response
const response = await fetch('/api/posts/1').then((r) => r.json());
const normalized = normalize(response, postSchema);

// normalized.result → '1' (post ID)
// normalized.entities.posts → { '1': { id: '1', title: '...', author: 'a1', comments: ['c1', 'c2'] } }
// normalized.entities.users → { 'a1': { id: 'a1', name: 'Alice' }, 'a2': { id: 'a2', name: 'Bob' } }
// normalized.entities.comments → { 'c1': { id: 'c1', text: '...', author: 'a2' }, ... }
```

### Optimistic Updates with Rollback

**Optimistic update pattern** — update UI immediately, rollback on failure:

```ts
// Zustand store with optimistic updates
interface TodoStore {
  todos: Todo[];
  undoStack: { todos: Todo[]; timestamp: number }[];
  addTodo: (title: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
}

export const useTodoStore = create<TodoStore>((set, get) => ({
  todos: [],
  undoStack: [],

  addTodo: async (title: string) => {
    const tempId = `temp-${Date.now()}`;
    const optimisticTodo: Todo = {
      id: tempId,
      title,
      completed: false,
      createdAt: new Date(),
    };

    // Save current state for rollback
    const previousTodos = get().todos;
    set((state) => ({
      todos: [...state.todos, optimisticTodo],
      undoStack: [...state.undoStack, { todos: previousTodos, timestamp: Date.now() }],
    }));

    try {
      // Send to server
      const response = await api.post('/todos', { title });
      const serverTodo = response.data;

      // Replace optimistic todo with server response
      set((state) => ({
        todos: state.todos.map((t) => (t.id === tempId ? serverTodo : t)),
      }));
    } catch (error) {
      // Rollback to previous state
      set((state) => ({
        todos: previousTodos,
        undoStack: state.undoStack.slice(0, -1),
      }));
      toast.error('Failed to add todo');
      throw error;
    }
  },

  deleteTodo: async (id: string) => {
    const previousTodos = get().todos;

    // Optimistic delete
    set((state) => ({
      todos: state.todos.filter((t) => t.id !== id),
      undoStack: [...state.undoStack, { todos: previousTodos, timestamp: Date.now() }],
    }));

    try {
      await api.delete(`/todos/${id}`);
      // Clean up undo stack entry after 30 seconds
      setTimeout(() => {
        set((state) => ({
          undoStack: state.undoStack.filter((u) => u.timestamp > Date.now() - 30000),
        }));
      }, 30000);
    } catch (error) {
      // Rollback
      set({ todos: previousTodos });
      toast.error('Failed to delete todo');
      throw error;
    }
  },
}));
```

**React Query optimistic updates:**

```ts
const queryClient = useQueryClient();

const mutation = useMutation({
  mutationFn: (newTodo) => api.post('/todos', newTodo),

  onMutate: async (newTodo) => {
    // Cancel outgoing refetches to avoid race condition
    await queryClient.cancelQueries({ queryKey: ['todos'] });

    // Snapshot current value
    const previousTodos = queryClient.getQueryData(['todos']);

    // Optimistically update
    queryClient.setQueryData(['todos'], (old: Todo[]) => [
      ...old,
      { ...newTodo, id: `temp-${Date.now()}`, status: 'pending' },
    ]);

    // Return context with snapshot for rollback
    return { previousTodos };
  },

  onError: (error, newTodo, context) => {
    // Rollback on error
    queryClient.setQueryData(['todos'], context.previousTodos);
  },

  onSettled: () => {
    // Refetch after success or error to sync with server
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                                          | Deliverable                                   |
| ------------------------------------ | --------------------------------------------------------------------------------------- | --------------------------------------------- |
| **Stage 2** (Web Prototype + IDS)    | Identify state requirements from IDS interactions; document state dependencies          | State requirements in IDS                     |
| **Stage 3** (Architecture)           | Define state management architecture in UML; register ADRs for state tool selection     | State management ADRs                         |
| **Stage 5** (Development)            | Implement state stores, async state management, optimistic updates, state normalization | Production state management code              |
| **Stage 6** (Code Review)            | Review state architecture, normalization, async patterns, rollback logic                | State architecture review in DEFECT-REPORT.md |
| **Stage 8** (Integrity Verification) | Verify state consistency across all user flows; test rollback scenarios                 | State integrity verification report           |

## Quality Standards

| Metric                         | Target                                                          | Enforcement                                                      |
| ------------------------------ | --------------------------------------------------------------- | ---------------------------------------------------------------- |
| **State colocation**           | State lives at the lowest common ancestor that needs it         | Code review; zero global state for component-local concerns      |
| **State tool appropriateness** | No over-engineering or under-engineering                        | Architecture review against decision matrix                      |
| **State normalization**        | No duplicated entity data in stores                             | Data shape audit; O(1) entity lookup verification                |
| **Async state separation**     | Server state managed by React Query/SWR, not manual useState    | Code review; zero manual fetch + useState patterns               |
| **Optimistic update coverage** | All user-facing mutations have optimistic updates with rollback | Code review; rollback test for each mutation                     |
| **Rollback reliability**       | 100% of failed mutations restore previous state                 | Unit tests for rollback scenarios                                |
| **State debugging**            | Full state traceable via DevTools                               | DevTools integration verified                                    |
| **Selective subscriptions**    | Components only subscribe to the state slices they need         | Zustand selector audit; zero `useStore(state => state)` patterns |
| **Context update frequency**   | Context consumers re-render < 5 times per user action           | React DevTools Profiler audit                                    |
| **State persistence**          | Persisted state is versioned and migrated safely                | Migration test for persisted state schema changes                |
| **Race condition prevention**  | No stale state from out-of-order async responses                | React Query cancellation or request ID validation                |
| **State test coverage**        | ≥ 90% of state management logic tested                          | Unit test coverage report                                        |
