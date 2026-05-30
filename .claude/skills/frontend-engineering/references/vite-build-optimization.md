---
name: vite-build-optimization
description: Configure and optimize Vite for production: code splitting, tree shaking, HMR tuning, plugin development, and bundle analysis.
version: "1.0.0"
---

# Vite Build Optimization

| Competency         | Description                                                            | Quality Criteria                                                                                                                               |
| ------------------ | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Configuration      | `vite.config.ts` structure, plugin composition, environment handling   | Config is typed with `defineConfig`; plugins ordered correctly (transform order matters); environment variables validated at build time        |
| HMR Performance    | Hot Module Replacement boundary management and sub-100ms update cycles | HMR boundaries are explicit for stateful modules; no full-page reload for style changes; HMR time measured and kept under 100ms in development |
| Code Splitting     | Manual chunk strategy, route-level splitting, vendor separation        | Vendor chunks isolate stable third-party code; routes lazy-loaded via dynamic `import()`; no single chunk exceeds 250 kB gzipped               |
| Tree Shaking       | ESM-first imports, side-effect declarations, dead code elimination     | Named imports used exclusively (no namespace imports for large libs); `package.json` `sideEffects: false` validated; no dead exports in bundle |
| Production Build   | Minification, asset inlining thresholds, compression, source maps      | Terser/esbuild minification active; assets ≤ 4 kB inlined; Brotli+gzip pre-compressed; source maps excluded from deployment artifact           |
| Plugin Development | Custom Vite plugin hooks (`transform`, `resolveId`, `load`)            | Plugins use `enforce` when ordering matters; transform functions are pure and idempotent; plugins validated against Vite plugin test utilities |
| Bundle Analysis    | Rollup visualizer, size-limit gates, per-route budget enforcement      | `rollup-plugin-visualizer` runs in CI on every PR; size-limit thresholds enforced as CI failure; largest dependency identified and justified   |

## Execution Guidance

### vite.config.ts Structure

```typescript
import { defineConfig, splitVendorChunkPlugin } from "vite";
import react from "@vitejs/plugin-react";
import { visualizer } from "rollup-plugin-visualizer";
import { compression } from "vite-plugin-compression2";

export default defineConfig(({ command, mode }) => {
  const isProduction = mode === "production";

  return {
    plugins: [
      react(),
      splitVendorChunkPlugin(),
      compression({ algorithm: "brotliCompress", deleteOriginalAssets: false }),
      isProduction &&
        visualizer({
          filename: "dist/stats.html",
          gzipSize: true,
          brotliSize: true,
          open: false, // do not auto-open in CI
        }),
    ].filter(Boolean),

    build: {
      target: "es2020",
      minify: "terser",
      terserOptions: {
        compress: {
          drop_console: isProduction,
          drop_debugger: true,
          pure_funcs: ["console.log", "console.info"],
        },
      },
      rollupOptions: {
        output: {
          manualChunks: chunkStrategy,
          chunkFileNames: "assets/js/[name]-[hash].js",
          entryFileNames: "assets/js/[name]-[hash].js",
          assetFileNames: "assets/[ext]/[name]-[hash].[ext]",
        },
      },
      chunkSizeWarningLimit: 500, // kB, warn before the 250 kB gzipped target
      assetsInlineLimit: 4096, // 4 kB — inline small assets as base64
      sourcemap: isProduction ? "hidden" : true,
      reportCompressedSize: true,
    },

    resolve: {
      alias: {
        "@": "/src",
        "@components": "/src/components",
        "@features": "/src/features",
      },
    },

    server: {
      hmr: {
        overlay: true,
      },
    },
  };
});
```

### Manual Chunk Splitting Strategy

**The `manualChunks` function drives chunk topology.** Group by stability, not by directory:

```typescript
function chunkStrategy(id: string): string | undefined {
  // Vendor: stable, heavy libraries — change rarely
  if (id.includes("node_modules")) {
    // Charting library: large, isolated
    if (id.includes("recharts") || id.includes("d3")) return "vendor-charts";

    // Validation: used everywhere, stable
    if (id.includes("zod") || id.includes("yup")) return "vendor-validation";

    // Date manipulation: stable, used across features
    if (id.includes("date-fns") || id.includes("dayjs")) return "vendor-dates";

    // React ecosystem: always co-change
    if (
      id.includes("react/") ||
      id.includes("react-dom") ||
      id.includes("react-router")
    ) {
      return "vendor-react";
    }

    // Everything else in a single vendor chunk
    return "vendor";
  }

  // Feature-level splitting: lazy-loaded routes
  if (id.includes("/src/features/dashboard")) return "feature-dashboard";
  if (id.includes("/src/features/analytics")) return "feature-analytics";
  if (id.includes("/src/features/settings")) return "feature-settings";

  // Default: let Rollup decide (shared modules, entry points)
  return undefined;
}
```

**Chunk budget targets:**

| Chunk             | Budget (gzipped) | Notes                                  |
| ----------------- | ---------------- | -------------------------------------- |
| Initial JS total  | < 150 kB         | What the user downloads on first visit |
| `vendor-react`    | < 45 kB          | React + ReactDOM + Router              |
| `vendor` (misc)   | < 80 kB          | Everything else stable                 |
| Per feature chunk | < 50 kB          | Lazy loaded on route entry             |
| CSS per route     | < 20 kB          | Extracted to separate file             |

### Route-Level Code Splitting

```tsx
// src/router.tsx — React Router v6 with lazy routes
import { lazy, Suspense } from "react";
import { createBrowserRouter } from "react-router-dom";
import { PageSkeleton } from "@components/PageSkeleton";

const Dashboard = lazy(() => import("@features/dashboard/DashboardPage"));
const Analytics = lazy(() => import("@features/analytics/AnalyticsPage"));
const Settings = lazy(() => import("@features/settings/SettingsPage"));

export const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <Suspense fallback={<PageSkeleton />}>
        <Dashboard />
      </Suspense>
    ),
  },
  {
    path: "/analytics",
    element: (
      <Suspense fallback={<PageSkeleton />}>
        <Analytics />
      </Suspense>
    ),
  },
  {
    path: "/settings",
    element: (
      <Suspense fallback={<PageSkeleton />}>
        <Settings />
      </Suspense>
    ),
  },
]);
```

**Preloading on hover** (reduces perceived navigation latency):

```tsx
// Preload on hover — triggers the lazy import 200ms before click
function NavLink({ to, label, preload }: NavLinkProps) {
  return (
    <Link
      to={to}
      onMouseEnter={() => {
        void preload(); // triggers dynamic import early
      }}
    >
      {label}
    </Link>
  );
}

// Usage
<NavLink
  to="/analytics"
  label="Analytics"
  preload={() => import("@features/analytics/AnalyticsPage")}
/>;
```

### Tree Shaking and ESM-First Architecture

**Do:**

```typescript
// Named imports from ESM packages — fully tree-shakeable
import { format, parseISO } from "date-fns";
import { z } from "zod";
import { clsx } from "clsx";
```

**Do not:**

```typescript
// Namespace import — imports entire library, prevents tree shaking
import * as dateFns from "date-fns"; // ❌
import _ from "lodash"; // ❌ use lodash-es with named imports instead
```

**Declare side-effect-free packages in `package.json`:**

```json
{
  "sideEffects": false
}
```

**For packages with CSS side effects:**

```json
{
  "sideEffects": ["*.css", "*.scss", "src/polyfills.ts"]
}
```

**Identify and replace heavy dependencies:**

| Problem Library | ESM Alternative        | Size Saving |
| --------------- | ---------------------- | ----------- |
| `lodash`        | `lodash-es` (named)    | ~70 kB      |
| `moment`        | `date-fns` or `dayjs`  | ~280 kB     |
| `axios`         | native `fetch` wrapper | ~15 kB      |
| `classnames`    | `clsx`                 | ~1 kB       |

### HMR Boundary Management

Vite's HMR propagates changes up the module graph until it finds an accepting boundary. Poor boundaries cause full-page reloads.

**Explicit HMR acceptance for stateful modules:**

```typescript
// src/store/themeStore.ts
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    // Replace module without losing application state
    if (newModule) {
      store.replaceReducer(newModule.themeReducer);
    }
  });

  import.meta.hot.dispose(() => {
    // Cleanup subscriptions before module is discarded
    store.unsubscribeAll();
  });
}
```

**Common HMR slow paths and fixes:**

| Symptom                            | Cause                                       | Fix                                              |
| ---------------------------------- | ------------------------------------------- | ------------------------------------------------ |
| Full reload on CSS change          | CSS imported in JS module without `?inline` | Use CSS Modules or Vite CSS extraction           |
| HMR > 500ms                        | Too many modules in a single chunk          | Split features into separate entry points        |
| HMR breaks React state             | Component not wrapped in `React.memo`       | Add `memo`; ensure hooks have stable keys        |
| HMR loop (accepts then re-applies) | Circular dependency between modules         | Resolve circular dep; use dependency graph audit |

**Measure HMR time in development:**

```typescript
// vite.config.ts — custom plugin for HMR timing
function hmrTimingPlugin(): Plugin {
  return {
    name: "hmr-timing",
    handleHotUpdate({ modules }) {
      const start = performance.now();
      return modules.map((mod) => {
        console.log(
          `[HMR] ${mod.id} → ${(performance.now() - start).toFixed(1)}ms`,
        );
        return mod;
      });
    },
  };
}
```

### Custom Vite Plugin Development

Plugin hooks run in Rollup order. `enforce: 'pre'` runs before Vite's built-in plugins; `enforce: 'post'` runs after.

```typescript
// Example: plugin that injects build metadata into the bundle
import type { Plugin } from "vite";

export function buildMetaPlugin(): Plugin {
  let viteConfig: ResolvedConfig;

  return {
    name: "build-meta",
    enforce: "post",

    configResolved(config) {
      viteConfig = config;
    },

    // transform: called for every module — keep this fast
    transform(code, id) {
      if (!id.endsWith("src/version.ts")) return null;

      return {
        code: code.replace(
          "__BUILD_META__",
          JSON.stringify({
            timestamp: new Date().toISOString(),
            mode: viteConfig.mode,
            hash: process.env.GIT_SHA ?? "dev",
          }),
        ),
        map: null,
      };
    },

    // generateBundle: called once, post-build — safe for slow operations
    generateBundle(options, bundle) {
      const totalSize = Object.values(bundle).reduce(
        (acc, chunk) =>
          chunk.type === "chunk" ? acc + chunk.code.length : acc,
        0,
      );
      this.emitFile({
        type: "asset",
        fileName: "build-meta.json",
        source: JSON.stringify({
          totalSize,
          chunks: Object.keys(bundle).length,
        }),
      });
    },
  };
}
```

**Plugin hook execution order for a module:**

```
resolveId  → load  → transform  → (build)  → generateBundle  → writeBundle
```

### Bundle Analysis and Size-Limit Gates

**Run visualizer in CI:**

```typescript
// vite.config.ts (production only)
visualizer({
  filename: "dist/stats.html",
  template: "treemap", // "sunburst" | "treemap" | "network"
  gzipSize: true,
  brotliSize: true,
});
```

**`size-limit` configuration (`.size-limit.json`):**

```json
[
  {
    "name": "Initial JS",
    "path": "dist/assets/js/index-*.js",
    "limit": "150 kB",
    "gzip": true
  },
  {
    "name": "Vendor React",
    "path": "dist/assets/js/vendor-react-*.js",
    "limit": "50 kB",
    "gzip": true
  },
  {
    "name": "CSS",
    "path": "dist/assets/css/*.css",
    "limit": "30 kB",
    "gzip": true
  }
]
```

**CI integration (GitHub Actions):**

```yaml
- name: Build
  run: npm run build

- name: Check bundle size
  run: npx size-limit --json > size-report.json
  # Fails with exit code 1 if any limit is exceeded

- name: Upload stats
  uses: actions/upload-artifact@v4
  with:
    name: bundle-stats
    path: |
      dist/stats.html
      size-report.json
```

### Environment Variables and Define Configuration

**`import.meta.env` is the Vite-native approach.** Use `define` for compile-time constants that Terser can constant-fold:

```typescript
// vite.config.ts
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  return {
    define: {
      // Compile-time constants — Terser eliminates dead branches
      __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
      __FEATURE_FLAG_ANALYTICS__: env.VITE_ANALYTICS_ENABLED === "true",
    },
    // Validate required env vars at build time
    plugins: [
      {
        name: "env-validation",
        buildStart() {
          const required = ["VITE_API_URL", "VITE_APP_ENV"];
          for (const key of required) {
            if (!env[key]) {
              this.error(`Missing required environment variable: ${key}`);
            }
          }
        },
      },
    ],
  };
});
```

**TypeScript type augmentation for `import.meta.env`:**

```typescript
// src/env.d.ts
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_APP_ENV: "development" | "staging" | "production";
  readonly VITE_ANALYTICS_ENABLED?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

## Pipeline Integration

**Stage 5 (Development):** `vite.config.ts` committed at project scaffold. Manual chunk strategy documented as an architectural note. Size-limit thresholds agreed with product and engineering leads before implementation begins.

**Stage 6 (Architecture & Conformance Review):** Bundle analysis report reviewed — no single initial chunk exceeds 250 kB gzipped. `manualChunks` strategy reviewed for correctness. Environment variable validation plugin active. Tree-shaking audit: no namespace imports of large libraries.

**CI Size-Limit Gates:** Enforced from first PR. Budget breaches block merge. Exceptions require tech lead approval and an ADR addendum explaining the trade-off.

## Quality Standards

| Metric                         | Target         | Measurement                          |
| ------------------------------ | -------------- | ------------------------------------ |
| Initial JS (gzipped)           | < 150 kB       | `size-limit` CI gate                 |
| HMR update time                | < 100ms        | Vite HMR timing plugin               |
| Largest single chunk (gzipped) | < 250 kB       | `rollup-plugin-visualizer` report    |
| Tree-shaking dead code         | 0 dead exports | `rollup-plugin-unused-exports` audit |
| Build time (cold, CI)          | < 60s          | CI build step timing                 |
| Brotli compression ratio       | > 70%          | `dist/build-meta.json` report        |
| Spectral / plugin lint errors  | 0              | `vite build` exit code               |
