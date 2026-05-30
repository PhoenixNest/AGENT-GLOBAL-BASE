---
name: ssr-nextjs
description: Build server-side rendered web applications with Next.js App Router — implementing Server Components, streaming, route handlers, and ISR (Incremental Static Regeneration) — achieving Core Web Vitals scores that meet the company's SEO and performance requirements.
version: "1.0.0"
---

# SSR Nextjs

| Competency        | Description                                                      | Quality Criteria                                                                                                                     |
| ----------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| App Router        | Build features using Next.js App Router with file-system routing | Correct use of `layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx`; no Pages Router patterns in App Router code                     |
| Server Components | Use React Server Components for data-fetching pages              | Data fetching happens in Server Components; no `useEffect` for initial data; client boundary minimized to interactive parts          |
| Streaming         | Implement Suspense-based streaming for improved TTFB             | `<Suspense>` wraps slow data-fetching sections; skeleton loaders shown during streaming; no full-page loading states                 |
| ISR / Caching     | Configure appropriate caching for each route                     | Static routes use `revalidate` for ISR; dynamic routes use `force-dynamic` only when necessary; cache tags for granular invalidation |

## Execution Guidance

### Server vs. Client Component Decision

| Needs                         | Component Type |
| ----------------------------- | -------------- |
| Data fetching from DB/API     | Server         |
| Access to `window`/`document` | Client         |
| `useState`, `useEffect`       | Client         |
| Interactive event handlers    | Client         |
| Static content rendering      | Server         |
| `cookies()`, `headers()`      | Server         |

### Streaming Pattern

```tsx
// page.tsx
export default function ProductPage() {
  return (
    <main>
      <StaticHeader />
      <Suspense fallback={<ProductDetailSkeleton />}>
        <ProductDetail /> {/* Fetches from DB — streams in */}
      </Suspense>
      <Suspense fallback={<ReviewsSkeleton />}>
        <ReviewsList /> {/* Slower query — streams separately */}
      </Suspense>
    </main>
  );
}
```

### Core Web Vitals Targets

| Metric  | Target  | Measurement           |
| ------- | ------- | --------------------- |
| LCP     | < 2.5s  | Real user data (CrUX) |
| FID/INP | < 200ms | Real user data (CrUX) |
| CLS     | < 0.1   | Real user data (CrUX) |
| TTFB    | < 800ms | Lab (Lighthouse CI)   |
