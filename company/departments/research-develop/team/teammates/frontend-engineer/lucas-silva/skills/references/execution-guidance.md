---
version: "1.0.0"
---

------------------------------ | ----------------------------- | ------------------------------------------------------ |
| **ESBuild minification** | `build.minify: 'esbuild'` | Fast minification, good compression |
| **Terser for advanced minification** | `build.minify: 'terser'` | Slower but better compression; supports `drop_console` |
| **Gzip/Brotli compression** | `vite-plugin-compression` | ~70% size reduction |
| **Image optimization** | `vite-plugin-imagemin` | ~30-50% image size reduction |
| **Font subsetting** | Custom plugin or build script | ~60% font size reduction |
| **CSS code splitting** | `build.cssCodeSplit: true` | Per-route CSS loading |
| **Preload directives** | `build.modulePreload` | Browser fetches critical chunks early |
| **Dynamic import preload** | `<link rel="modulepreload">` | Prefetch route chunks on navigation |
