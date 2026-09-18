export const SCHOOL_NAME = 'Budapest II. Kerületi II. Rákóczi Ferenc Gimnázium';
export const SCHOOL_SHORT = 'II. Rákóczi Ferenc Gimnázium';

// Ideiglenes/generikus KRÉTA cél a 0. verzióban — lásd a specifikáció 10. szakaszát.
// Éles beüzemeléskor az intézményi rendszergazdától kapott stabil, intézményspecifikus
// belépési URL-re kell cserélni.
export const KRETA_URL = 'https://idp.e-kreta.hu/';

export const MAIN_NAV = [
  { label: 'Főoldal', href: '/' },
  { label: 'Hírek', href: '/hirek/' },
  { label: 'Események', href: '/esemenyek/' },
  { label: 'Iskolai élet', href: '/iskolai-elet/' },
  { label: 'Közösségeink', href: '/kozossegeink/' },
  { label: 'Felvételi', href: '/felveteli/' },
  { label: 'Dokumentumtár', href: '/dokumentumtar/' },
  { label: 'Rólunk', href: '/rolunk/' },
  { label: 'Kapcsolat', href: '/kapcsolat/' },
];

export const FOOTER_LEGAL_NAV = [
  { label: 'Adatvédelem', href: '/adatvedelem/' },
  { label: 'Impresszum', href: '/impresszum/' },
  { label: 'Akadálymentességi nyilatkozat', href: '/akadalymentesseg/' },
  { label: 'Fenntartó', href: '/fenntarto/' },
  { label: 'Kötelező közzétételi információk', href: '/dokumentumtar/#kulonos-kozzeteteli-lista' },
];

// GitHub Pages projekt-alútvonalon (pl. org.github.io/repo/) a base konfig miatt
// minden belső hivatkozást és statikus fájlt ezzel kell prefixelni, különben a
// linkek egyedi domainen működnek, de alútvonalon eltörnek.
export function withBase(path: string): string {
  // A teljes külső URL-eket, protokoll-relatív URL-eket és horgonyokat változatlanul hagyjuk.
  if (/^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test(path)) {
    return path;
  }

  const base = import.meta.env.BASE_URL || '/';
  const cleanBase = base.endsWith('/') ? base : `${base}/`;
  const cleanPath = path.startsWith('/') ? path.slice(1) : path;
  return `${cleanBase}${cleanPath}`;
}

export function slugify(input: string): string {
  return input
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

export function formatDateHu(date: Date, withTime = false): string {
  const d = new Intl.DateTimeFormat('hu-HU', { year: 'numeric', month: 'long', day: 'numeric' }).format(date);
  if (!withTime) return d;
  const t = new Intl.DateTimeFormat('hu-HU', { hour: '2-digit', minute: '2-digit' }).format(date);
  return `${d}, ${t}`;
}

export function formatDateShort(date: Date): string {
  return new Intl.DateTimeFormat('hu-HU', { year: 'numeric', month: '2-digit', day: '2-digit' }).format(date);
}
