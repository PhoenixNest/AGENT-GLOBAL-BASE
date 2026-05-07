---
name: virtualized-rendering
description: Implement virtualized list/grid rendering for large datasets, infinite scroll, skeleton loading, and perceived performance techniques for web applications.
version: "1.0.0"
---

# Virtualized Rendering and Perceived Performance

| Competency             | Description                                                    | Quality Criteria                                                                                                                           |
| ---------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Virtual Scrolling      | DOM windowing with `react-window` or `@tanstack/react-virtual` | Only visible rows + overscan rendered in DOM; no `key` collisions; scroll position preserved on data refresh; accessible with keyboard nav |
| Infinite Scroll        | IntersectionObserver sentinel pattern with async page fetching | Sentinel is last rendered item (not a fixed offset); loading state prevents duplicate fetches; error state has retry path                  |
| Skeleton Loading       | CSS-only shimmer animations for loading states                 | Skeleton matches rendered content layout precisely; animation paused via `prefers-reduced-motion`; no JS required for animation            |
| Optimistic UI          | Immediate local state mutation before server confirmation      | Rollback on server error with user-visible notification; mutation ID tracked to correlate server response; no double-update on success     |
| Image Lazy Loading     | Native `loading="lazy"` with IntersectionObserver fallback     | Images outside viewport not requested; LCP image has `loading="eager"` and `fetchpriority="high"`; correct `width`/`height` prevent CLS    |
| Content Visibility     | CSS `content-visibility: auto` for off-screen content sections | Applied only to large, independent content blocks (article cards, rows); `contain-intrinsic-size` set to prevent layout thrash             |
| Web Vitals Measurement | FCP, LCP, INP, CLS instrumentation and performance budgets     | Core Web Vitals reported to analytics; INP target < 200ms; LCP target < 2.5s; CLS target < 0.1; budget enforced as CI performance test     |

## Execution Guidance

### Virtual Scrolling Concepts

**The windowing model:** instead of rendering all N items, the virtual list renders only the items visible in the viewport plus a configurable `overscan` buffer above and below. Items outside the window are replaced by a single spacer element that maintains scroll height.

```
┌─────────────────────────────┐  ← Scroll container (fixed height)
│  [spacer: height = offset]  │
│  ┌─────────────────────┐    │
│  │  Item 40 (overscan) │    │
│  ├─────────────────────┤    │  ← Visible window
│  │  Item 41            │    │
│  │  Item 42            │    │  ← DOM contains only items 40-55
│  │  ...                │    │
│  │  Item 53            │    │
│  ├─────────────────────┤    │
│  │  Item 54 (overscan) │    │
│  └─────────────────────┘    │
│  [spacer: remaining height] │
└─────────────────────────────┘
```

### react-window: FixedSizeList and VariableSizeList

**FixedSizeList** — every row has the same height (most performant):

```tsx
import { FixedSizeList, ListChildComponentProps } from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";

interface Contact {
  id: string;
  name: string;
  email: string;
}

function ContactRow({
  index,
  style,
  data,
}: ListChildComponentProps<Contact[]>) {
  const contact = data[index];
  return (
    // style MUST be applied — it contains the absolute positioning
    <div style={style} className="contact-row" role="row">
      <span>{contact.name}</span>
      <span>{contact.email}</span>
    </div>
  );
}

function ContactList({ contacts }: { contacts: Contact[] }) {
  return (
    // AutoSizer fills parent container — use a sized parent div
    <div style={{ height: "600px" }}>
      <AutoSizer>
        {({ height, width }) => (
          <FixedSizeList
            height={height}
            width={width}
            itemCount={contacts.length}
            itemSize={60} // px — must match CSS exactly
            itemData={contacts}
            overscanCount={5}
          >
            {ContactRow}
          </FixedSizeList>
        )}
      </AutoSizer>
    </div>
  );
}
```

**VariableSizeList** — rows have different heights (requires size estimation):

```tsx
import { VariableSizeList } from "react-window";
import { useRef, useCallback } from "react";

function ExpandableList({ items }: { items: Item[] }) {
  const listRef = useRef<VariableSizeList>(null);
  const sizeMap = useRef<Record<number, number>>({});

  const setSize = useCallback((index: number, size: number) => {
    if (sizeMap.current[index] !== size) {
      sizeMap.current[index] = size;
      // Notify react-window to recalculate from this index
      listRef.current?.resetAfterIndex(index, false);
    }
  }, []);

  const getSize = useCallback(
    (index: number) => sizeMap.current[index] ?? 80, // default estimate
    [],
  );

  return (
    <VariableSizeList
      ref={listRef}
      height={600}
      width="100%"
      itemCount={items.length}
      itemSize={getSize}
      overscanCount={3}
    >
      {({ index, style }) => (
        <MeasuredRow
          style={style}
          item={items[index]}
          onMeasure={(size) => setSize(index, size)}
        />
      )}
    </VariableSizeList>
  );
}

// Measure row height after render
function MeasuredRow({ style, item, onMeasure }: MeasuredRowProps) {
  const rowRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (rowRef.current) {
      onMeasure(rowRef.current.getBoundingClientRect().height);
    }
  });

  return (
    <div style={style}>
      <div ref={rowRef} className="expandable-row">
        {/* variable-height content */}
      </div>
    </div>
  );
}
```

**FixedSizeGrid** for tabular data:

```tsx
import { FixedSizeGrid } from "react-window";

function DataGrid({ rows, columns }: { rows: Row[]; columns: Column[] }) {
  return (
    <FixedSizeGrid
      columnCount={columns.length}
      columnWidth={200}
      height={500}
      rowCount={rows.length}
      rowHeight={40}
      width={1000}
    >
      {({ columnIndex, rowIndex, style }) => (
        <div style={style} className="grid-cell">
          {rows[rowIndex][columns[columnIndex].key]}
        </div>
      )}
    </FixedSizeGrid>
  );
}
```

### @tanstack/react-virtual (Headless Alternative)

Use `@tanstack/react-virtual` when you need full layout control (e.g., CSS grid, masonry, custom scroll containers):

```tsx
import { useVirtualizer } from "@tanstack/react-virtual";
import { useRef } from "react";

function VirtualFeed({ posts }: { posts: Post[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: posts.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 120, // rough estimate; overrides after measurement
    overscan: 5,
  });

  return (
    <div ref={parentRef} style={{ height: "600px", overflow: "auto" }}>
      {/* Total size spacer — enables native scroll bar */}
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: "relative",
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            data-index={virtualItem.index}
            ref={virtualizer.measureElement} // auto-measures after render
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            <PostCard post={posts[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Infinite Scroll with IntersectionObserver

**Scroll sentinel pattern** — a zero-height div at the bottom of the list that triggers the next page load when it enters the viewport:

```tsx
import { useEffect, useRef, useCallback } from "react";

function useSentinel(onIntersect: () => void, enabled: boolean) {
  const sentinelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!enabled || !sentinelRef.current) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          onIntersect();
        }
      },
      { rootMargin: "200px" }, // trigger 200px before reaching bottom
    );

    observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [onIntersect, enabled]);

  return sentinelRef;
}

function InfinitePostList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isError,
    refetch,
  } = useInfiniteQuery({
    queryKey: ["posts"],
    queryFn: ({ pageParam }) => fetchPosts({ cursor: pageParam }),
    getNextPageParam: (lastPage) => lastPage.nextCursor ?? undefined,
    initialPageParam: undefined,
  });

  const posts = data?.pages.flatMap((p) => p.items) ?? [];

  const loadMore = useCallback(() => {
    if (!isFetchingNextPage) fetchNextPage();
  }, [fetchNextPage, isFetchingNextPage]);

  const sentinelRef = useSentinel(
    loadMore,
    !!hasNextPage && !isFetchingNextPage,
  );

  return (
    <>
      <div className="post-list">
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>

      {/* Sentinel — zero height, triggers load when visible */}
      <div ref={sentinelRef} aria-hidden="true" style={{ height: 1 }} />

      {isFetchingNextPage && <LoadingSpinner />}

      {isError && (
        <ErrorState
          message="Failed to load more posts"
          onRetry={() => refetch()}
        />
      )}

      {!hasNextPage && posts.length > 0 && (
        <p className="end-of-list">You've reached the end</p>
      )}
    </>
  );
}
```

### Skeleton Loading with CSS Shimmer

CSS-only shimmer: no JavaScript required, GPU-accelerated via `transform`, respects `prefers-reduced-motion`.

```css
/* Base skeleton styles */
.skeleton {
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

/* Shimmer animation via gradient sweep */
.skeleton::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.6) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite linear;
}

@keyframes shimmer {
  from {
    background-position: -200% center;
  }
  to {
    background-position: 200% center;
  }
}

/* Respect user preference — freeze animation, keep placeholder visible */
@media (prefers-reduced-motion: reduce) {
  .skeleton::after {
    animation: none;
    background: rgba(255, 255, 255, 0.3);
  }
}
```

```tsx
// Skeleton that mirrors the real content layout exactly
function PostCardSkeleton() {
  return (
    <article
      className="post-card post-card--skeleton"
      aria-busy="true"
      aria-label="Loading post"
    >
      <div
        className="skeleton"
        style={{ width: "100%", height: 200, borderRadius: 8 }}
      />
      <div
        style={{
          padding: "16px 0",
          display: "flex",
          flexDirection: "column",
          gap: 8,
        }}
      >
        <div className="skeleton" style={{ width: "80%", height: 20 }} />
        <div className="skeleton" style={{ width: "60%", height: 20 }} />
        <div
          className="skeleton"
          style={{ width: "40%", height: 16, marginTop: 8 }}
        />
      </div>
    </article>
  );
}

// Show skeletons during initial load only
function PostFeed() {
  const { data, isLoading } = useQuery({
    queryKey: ["posts"],
    queryFn: fetchPosts,
  });

  if (isLoading) {
    return (
      <div>
        {Array.from({ length: 6 }, (_, i) => (
          <PostCardSkeleton key={i} />
        ))}
      </div>
    );
  }

  return <PostList posts={data!} />;
}
```

### Optimistic UI Updates

```tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

function LikeButton({ postId, isLiked }: { postId: string; isLiked: boolean }) {
  const queryClient = useQueryClient();

  const { mutate: toggleLike } = useMutation({
    mutationFn: (liked: boolean) => updateLike(postId, liked),

    // Immediately update UI before server responds
    onMutate: async (newLiked) => {
      // Cancel in-flight refetches to avoid overwriting optimistic update
      await queryClient.cancelQueries({ queryKey: ["posts", postId] });

      // Snapshot current value for rollback
      const previous = queryClient.getQueryData<Post>(["posts", postId]);

      // Optimistically apply the change
      queryClient.setQueryData<Post>(["posts", postId], (old) =>
        old
          ? {
              ...old,
              isLiked: newLiked,
              likeCount: old.likeCount + (newLiked ? 1 : -1),
            }
          : old,
      );

      return { previous }; // context passed to onError
    },

    onError: (_err, _newLiked, context) => {
      // Roll back to previous value
      if (context?.previous) {
        queryClient.setQueryData(["posts", postId], context.previous);
      }
      toast.error("Failed to update like. Please try again.");
    },

    onSettled: () => {
      // Always sync with server after mutation settles
      queryClient.invalidateQueries({ queryKey: ["posts", postId] });
    },
  });

  return (
    <button onClick={() => toggleLike(!isLiked)} aria-pressed={isLiked}>
      {isLiked ? "Unlike" : "Like"}
    </button>
  );
}
```

### Image Lazy Loading

```tsx
// LCP hero image: eager + high priority — do not lazy-load above-the-fold
function HeroImage({ src, alt }: { src: string; alt: string }) {
  return (
    <img
      src={src}
      alt={alt}
      width={1200}
      height={600}
      loading="eager"
      fetchPriority="high"
      decoding="async"
    />
  );
}

// Below-fold images: native lazy loading
function ProductCard({ product }: { product: Product }) {
  return (
    <article>
      <img
        src={product.imageUrl}
        alt={product.name}
        width={400}
        height={300}
        loading="lazy"
        decoding="async"
      />
      <h3>{product.name}</h3>
    </article>
  );
}
```

**Width + height are mandatory** to reserve space before load — prevents CLS.

### Content Visibility CSS

```css
/* Apply to large, independent content blocks */
.article-card {
  content-visibility: auto;
  /* Hint to browser about the expected rendered size — prevents scroll jump */
  contain-intrinsic-size: auto 300px;
}

/* Do NOT apply to: headers, nav, above-fold content, interactive elements */
/* DO apply to: long article lists, comment threads, product grids */
```

**Browser support check before adoption:**

```typescript
const supportsContentVisibility = CSS.supports("content-visibility", "auto");
```

### Measuring Core Web Vitals

```typescript
// src/lib/vitals.ts — report to analytics
import { onCLS, onFCP, onINP, onLCP, onTTFB } from "web-vitals";

type MetricHandler = (metric: Metric) => void;

function sendToAnalytics(metric: Metric) {
  // Use `sendBeacon` to avoid blocking page unload
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating, // "good" | "needs-improvement" | "poor"
    delta: metric.delta,
    id: metric.id,
    navigationType: metric.navigationType,
    url: window.location.pathname,
  });

  if (navigator.sendBeacon) {
    navigator.sendBeacon("/api/metrics", body);
  } else {
    fetch("/api/metrics", { method: "POST", body, keepalive: true });
  }
}

export function initVitals() {
  onCLS(sendToAnalytics);
  onFCP(sendToAnalytics);
  onINP(sendToAnalytics); // replaces FID as of 2024
  onLCP(sendToAnalytics);
  onTTFB(sendToAnalytics);
}
```

**Core Web Vitals thresholds:**

| Metric | Good    | Needs Improvement | Poor    | Description                                  |
| ------ | ------- | ----------------- | ------- | -------------------------------------------- |
| LCP    | ≤ 2.5s  | 2.5s – 4.0s       | > 4.0s  | When largest visible content element loads   |
| INP    | ≤ 200ms | 200ms – 500ms     | > 500ms | Worst interaction latency over page lifetime |
| CLS    | ≤ 0.1   | 0.1 – 0.25        | > 0.25  | Cumulative unexpected layout shift score     |
| FCP    | ≤ 1.8s  | 1.8s – 3.0s       | > 3.0s  | When first content pixel is painted          |
| TTFB   | ≤ 800ms | 800ms – 1.8s      | > 1.8s  | Server response time                         |

**Common CLS causes and fixes:**

| Cause                            | Fix                                                  |
| -------------------------------- | ---------------------------------------------------- |
| Images without dimensions        | Always set `width` and `height` attributes           |
| Fonts causing FOUT               | `font-display: optional` or `size-adjust` descriptor |
| Dynamic banners / ads injected   | Reserve space with `min-height` before content loads |
| Late-loading embeds (video, map) | Set explicit aspect-ratio container                  |

## Pipeline Integration

**Stage 5 (Development):** Virtual scrolling implemented from the first iteration when list length > 500 items is expected. Skeleton components created in parallel with real components — they must match layout exactly. `web-vitals` library integrated at app entry point before first screen is implemented.

**Stage 6 (Architecture & Conformance Review):** Core Web Vitals review — Lighthouse CI run against staging environment. LCP, INP, CLS checked against thresholds. Review checklist — (1) No above-fold image uses `loading="lazy"`; (2) LCP image has `fetchpriority="high"`; (3) All images have explicit `width`/`height`; (4) Skeleton layout matches real content layout; (5) Skeleton animation paused on `prefers-reduced-motion`; (6) Virtual list overscan ≥ 3; (7) Optimistic mutations have rollback path tested.

**Lighthouse CI configuration (`.lighthouserc.json`):**

```json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "first-contentful-paint": ["error", { "maxNumericValue": 1800 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "interactive": ["warn", { "maxNumericValue": 3800 }]
      }
    }
  }
}
```

## Quality Standards

| Metric                        | Target                              | Measurement                              |
| ----------------------------- | ----------------------------------- | ---------------------------------------- |
| LCP (mobile, 4G)              | ≤ 2.5s                              | Lighthouse CI + real-user web-vitals     |
| INP                           | ≤ 200ms                             | web-vitals library → analytics           |
| CLS                           | ≤ 0.1                               | Lighthouse CI                            |
| DOM nodes at idle (long list) | < 1,500                             | Chrome DevTools Memory snapshot          |
| Scroll FPS (virtual list)     | 60 fps                              | Chrome DevTools Performance panel        |
| Skeleton-to-content CLS       | 0.0                                 | No layout shift when skeleton replaces   |
| Image requests (below fold)   | 0 on load                           | Network waterfall — lazy images deferred |
| Optimistic rollback coverage  | 100% of mutations with side effects | Code review + mutation tests             |
