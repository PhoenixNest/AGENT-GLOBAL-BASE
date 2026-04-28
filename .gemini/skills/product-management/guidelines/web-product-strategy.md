---
name: web-product-strategy
description: Specialized product strategy for web-based platforms, including architectural choices (PWA, SPA, SSR), accessibility (WCAG 2.1 AA), conversion funnel optimization, and cross-functional design partnerships. Use this skill when authoring Section 5 of a Web-focused PRD or when advising on web platform roadmap decisions.
---

# Web Product Strategy

Julia Thorne (VP Web) leads the web product strategy, ensuring that our web surfaces are performant, accessible, and optimized for growth. This skill defines the standards and decision frameworks for web product management.

---

## 1. Architectural Strategy: PWA vs. SPA vs. SSR

When defining a web product, the architectural choice must align with the product goals.

### Progressive Web Apps (PWA)

- **Use Case:** Mobile-first web experiences where offline capability, push notifications, and "installability" are critical.
- **PM Consideration:** Prioritize service worker implementation and manifest configuration. Ensure the "Add to Home Screen" prompt is timed to a high-intent user moment.

### Single Page Applications (SPA)

- **Use Case:** Highly interactive, app-like experiences (e.g., dashboards, editors) where state management is complex but SEO is secondary to interactivity.
- **PM Consideration:** Monitor initial bundle size and "Time to Interactive" (TTI). Ensure client-side routing handles deep-linking correctly.

### Server-Side Rendering (SSR)

- **Use Case:** Content-heavy sites where SEO, initial page load speed (First Contentful Paint), and social sharing (OpenGraph) are paramount.
- **PM Consideration:** Balance server load with performance gains. Ensure a "hydration" strategy that doesn't block interactivity.

---

## 2. Web Accessibility (WCAG 2.1 AA)

Accessibility is a non-negotiable requirement, not a post-launch polish.

- **Keyboard Navigability:** Every interactive element must be reachable and operable via keyboard.
- **Screen Reader Compatibility:** Proper use of semantic HTML (nav, main, section) and ARIA labels where native HTML falls short.
- **Color Contrast:** Maintain a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text.
- **Focus States:** Visible, high-contrast focus indicators for all interactive elements.

**PRD Requirement:** Every Web PRD must include an "Accessibility Checkpoint" in the edge case matrix.

---

## 3. Web Conversion Funnels

Optimizing the web funnel requires a deep understanding of browser behavior and user intent.

- **Performance as a Feature:** Every 100ms of latency can impact conversion by 7%. Core Web Vitals (LCP, FID, CLS) are product metrics, not just engineering ones.
- **Friction Reduction:** Minimize form fields, leverage browser auto-fill, and ensure "one-tap" auth (e.g., Sign in with Google) is prominent.
- **Mobile-Web Parity:** Ensure the mobile web experience isn't a "stripped-down" version but a "context-optimized" version of the desktop experience.

---

## 4. Design-Engineering Partnership

The "Web Handoff" is a critical junction in the pipeline.

- **Responsive Specs:** Designs must account for fluid layouts, not just fixed breakpoints (320px, 768px, 1024px, 1440px).
- **Design Tokens:** Utilize shared tokens for colors, typography, and spacing to ensure consistency between the prototype and the production codebase.
- **Fidelity Checkpoints:** Participate in the CDO-led Stage 2 and Stage 5 checkpoints to ensure the web implementation matches the intended interaction design.

---

## 5. Web-Specific PRD Extension (Section 5)

When authoring Section 5 for a Web PRD, document:

- **Target Browsers:** (e.g., Chrome/Safari/Firefox latest 2 versions).
- **Responsive Strategy:** (e.g., Mobile-first, desktop-first).
- **SEO Requirements:** (Meta tags, structured data, canonical URLs).
- **Analytics:** Specific web events (e.g., scroll depth, outbound link clicks).
