---
name: frontend-web-react-ssr-nextjs
description: Next.js server-side rendering — SSR/SSG/ISR hybrid rendering strategies, server-side data fetching, App Router patterns, and SEO optimization for React applications. Owned by Amira Voss (Frontend Chapter Lead). Use during Stage 3 (Architecture) for rendering strategy selection and Stage 5 (Development) for Next.js implementation. Trigger: nextjs, ssr react, server-side rendering, ssg, isr, nextjs app router, seo optimization, react ssr.
prerequisites:
  - frontend-web-overview

version: "1.0.0"
---

# SSR/Next.js

## Overview

This skill covers Next.js server-side rendering (SSR), server-side data fetching, hybrid rendering strategies (SSG, SSR, ISR), and SEO optimization for React web applications. It is used by frontend engineers during Stage 5 (Development) for web frontend implementation and Stage 6 (Code Review) for performance and SEO conformance.

## Rendering Strategies

| Strategy                                  | When to Use                             | Pros                            | Cons                                  |
| ----------------------------------------- | --------------------------------------- | ------------------------------- | ------------------------------------- |
| **SSG** (Static Site Generation)          | Content rarely changes, marketing pages | Fastest TTFB, CDN cacheable     | Stale data, rebuild required          |
| **SSR** (Server-Side Rendering)           | User-specific data, real-time content   | Always fresh, good SEO          | Slower TTFB, server costs             |
| **ISR** (Incremental Static Regeneration) | Content updates periodically            | SSG speed with periodic refresh | Stale data within revalidation window |
| **CSR** (Client-Side Rendering)           | Dashboards, authenticated apps          | Rich interactivity, no server   | Poor SEO, slow initial load           |

## Server-Side Data Fetching

```tsx
// getServerSideProps — runs on every request
export async function getServerSideProps(context) {
  const data = await fetchFromAPI(context.params.id);
  return { props: { data } };
}

// getStaticProps — runs at build time
export async function getStaticProps() {
  const data = await fetchFromAPI();
  return { props: { data }, revalidate: 60 }; // ISR: revalidate every 60s
}

// generateStaticParams — for dynamic routes
export function generateStaticParams() {
  return products.map((p) => ({ id: p.id.toString() }));
}
```

## Performance Optimization

- **Code splitting**: Automatic per-page, manual with `dynamic()` for heavy components.
- **Image optimization**: `next/image` with automatic format detection (WebP/AVIF), lazy loading, blur placeholders.
- **Font optimization**: `next/font` with zero layout shift, self-hosted Google Fonts.
- **Middleware**: Edge Functions for authentication, A/B testing, geolocation routing.

## SEO Best Practices

- `next/head` or `generateMetadata` for dynamic title, description, Open Graph tags.
- Sitemap generation via `sitemap.ts` (Next.js 14+).
- Robots.txt management via `robots.ts`.
- Structured data (JSON-LD) for rich search results.
