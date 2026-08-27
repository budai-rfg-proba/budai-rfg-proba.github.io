import { defineCollection, z } from 'astro:content';

// Elsődleges hírkategóriák — a specifikáció szerint rövid, véglegesnek tekintett lista.
// Ne bővítsük egyetlen hír kedvéért; a keresztkapcsolatokra a tags mező szolgál.
export const NEWS_CATEGORIES = [
  'Hivatalos tájékoztatók',
  'Tanév rendje',
  'Iskolai élet',
  'Versenyek és eredmények',
  'Közösségeink',
  'Felvételi',
  'Rákóczi Röplap',
] as const;

const news = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    excerpt: z.string(),
    category: z.enum(NEWS_CATEGORIES),
    tags: z.array(z.string()).default([]),
    pubDate: z.date(),
    expiryDate: z.date().optional(),
    status: z.enum(['vázlat', 'felülvizsgálatra küldve', 'publikált']).default('publikált'),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    author: z.string().optional(),
    relatedDocument: z.string().optional(),
    relatedLink: z.string().optional(),
    featured: z.boolean().default(false),
  }),
});

const events = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    startDate: z.date(),
    endDate: z.date().optional(),
    location: z.string(),
    description: z.string(),
    audience: z.enum(['diákok', 'szülők', 'mindenki']).default('mindenki'),
    relatedNews: z.string().optional(),
    relatedDocument: z.string().optional(),
    featured: z.boolean().default(false),
    status: z.enum(['vázlat', 'felülvizsgálatra küldve', 'publikált']).default('publikált'),
  }),
});

export const DOCUMENT_GROUPS = [
  'Alapdokumentumok',
  'Különös közzétételi lista',
  'Letölthető nyomtatványok, kérelmek',
] as const;

const documents = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    group: z.enum(DOCUMENT_GROUPS),
    description: z.string().optional(),
    validFrom: z.date().optional(),
    validUntil: z.date().optional(),
    file: z.string().optional(),
    archived: z.boolean().default(false),
    status: z.enum(['vázlat', 'felülvizsgálatra küldve', 'publikált']).default('publikált'),
  }),
});

// Egyedi, "singleton" jellegű szerkeszthető oldalak és tartalmi blokkok
// (főoldali kiemelt információ, felvételi oldal, kapcsolati adatok, rólunk).
const pages = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    updatedAt: z.date().optional(),
    // Kiemelt információs sáv
    highlightActive: z.boolean().optional(),
    highlightText: z.string().optional(),
    highlightLink: z.string().optional(),
    // Kapcsolati adatok
    address: z.string().optional(),
    phone: z.string().optional(),
    email: z.string().optional(),
    kretaUrl: z.string().optional(),
    officeHours: z.string().optional(),
  }),
});

export const collections = { news, events, documents, pages };
