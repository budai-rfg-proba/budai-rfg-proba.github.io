import { defineConfig } from 'astro/config';

// A 0. verzió (prototípus) GitHub Pages-en fut, saját teszt-alútvonalon.
// A build workflow (.github/workflows/deploy.yml) a repó nevéből automatikusan
// beállítja a BASE_PATH környezeti változót, így ha a repót átnevezik, nem kell
// kézzel módosítani ezt a fájlt.
//
// Éles domain (budai-rfg.hu) beállításakor:
//   - site: 'https://budai-rfg.hu'
//   - base: '/'
const basePath = process.env.BASE_PATH || '/';
const siteUrl = process.env.SITE_URL || 'https://example.github.io';

export default defineConfig({
  site: siteUrl,
  base: basePath,
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
});
