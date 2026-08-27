import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

// Build-időben legenerált keresési index a hírekhez.
// A spec 12. szakasza szerint a keresés legalább a cím, a rövid bevezető,
// a kategória és a címkék mezőkben kell működjen.
export const GET: APIRoute = async () => {
  const news = await getCollection('news', ({ data }) => data.status === 'publikált');
  const index = news.map((entry) => ({
    title: entry.data.title,
    excerpt: entry.data.excerpt,
    category: entry.data.category,
    tags: entry.data.tags,
    slug: entry.slug,
    url: `/hirek/${entry.slug}/`,
    pubDate: entry.data.pubDate.toISOString(),
  }));
  return new Response(JSON.stringify(index), {
    headers: { 'Content-Type': 'application/json' },
  });
};
