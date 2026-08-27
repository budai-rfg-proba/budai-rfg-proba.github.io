# Budapest II. Kerületi II. Rákóczi Ferenc Gimnázium — új honlap (0. verzió)

Ez a repó a `iskolai-honlap-0-verzio-specifikacio.md` alapján készült, **0. verziós, tesztcélú prototípus**. Célja, hogy bemutassa a hírvezérelt főoldalt, a tartalomtípusokat (hírek, események, dokumentumok), a szerkesztői munkafolyamatot és a technikai alapokat — **nem az élesben futó `budai-rfg.hu` honlap**, és jelenleg nem tartalmaz éles, valós intézményi adatot (a cím, telefonszám, KRÉTA-link stb. minta-/helyőrző értékek).

## Technológiai áttekintés

- **[Astro](https://astro.build/)** statikus site generátor, Content Collections-szel (`src/content/`) a hírek, események, dokumentumok és egyedi ("singleton") oldalak strukturált kezelésére.
- **[Sveltia CMS](https://github.com/sveltia/sveltia-cms)** mint Git-alapú, kulcs nélküli tartalomkezelő felület (`/admin`), amely a `main` ágra ír commitokat/pull requesteket.
- **GitHub Actions + GitHub Pages** az automatikus buildhez és publikáláshoz.
- Sima HTML/CSS/JS a kliens oldalon (nincs React/Vue-keretrendszer) — vanília JavaScript a szűrőkhöz, kereséshez és a sötét módhoz.

## Helyi fejlesztés

```bash
npm install       # függőségek telepítése
npm run dev        # fejlesztői szerver, alapértelmezetten http://localhost:4321
npm run build       # statikus build a dist/ mappába
npm run preview      # a build előnézete lokálisan
npm run check       # Astro/TypeScript ellenőrzés
```

> A `npm run build` sikeres lefutását ellenőriztük — 53 oldal generálódik hiba nélkül a minta tartalommal.

## GitHub Pages telepítés

1. Töltsd fel ezt a repót a saját (vagy az iskolai) GitHub szervezet alá.
2. A repó **Settings → Pages** menüjében válaszd a **"GitHub Actions"** forrást (Source).
3. A `.github/workflows/deploy.yml` minden `main` ágra történő push-nál automatikusan buildel és publikál.
   - A workflow a `BASE_PATH` és `SITE_URL` környezeti változókat a repó nevéből és tulajdonosából állítja be, így a projekt-alútvonalas cím (pl. `https://felhasznalonev.github.io/rfg-honlap/`) automatikusan működik — nincs szükség kézi módosításra az `astro.config.mjs`-ben.
4. Az első sikeres futás után a Pages URL megjelenik a workflow futás összefoglalójában és a repó Pages beállításai között.

### Saját domain beállítása (később, éles indításkor)

Amikor a `budai-rfg.hu` domain mögé kerül a honlap:

1. Állítsd be a domaint a GitHub Pages **Custom domain** mezőjében (ez létrehoz egy `CNAME` fájlt).
2. Módosítsd az `astro.config.mjs` `site` értékét `https://budai-rfg.hu`-ra, és a `base`-t `'/'`-re (vagy hagyd a `SITE_URL`/`BASE_PATH` környezeti változókat a workflow-ban ennek megfelelően beállítva).
3. Frissítsd a DNS-t a regisztrátornál (A/ALIAS/CNAME rekord a GitHub Pages felé).

## Tartalomkezelés (Sveltia CMS) beüzemelése

A `/admin` felület jelenleg **nincs bekötve** működő GitHub OAuth-hoz — ehhez a következő lépések szükségesek:

1. **GitHub OAuth App létrehozása** (a repó tulajdonos szervezet/felhasználó fiókjában: Settings → Developer settings → OAuth Apps → New OAuth App). Az "Authorization callback URL" a választott auth worker domainje lesz (lásd 2. pont).
2. **`sveltia-cms-auth` Cloudflare Worker telepítése** — ez hidalja át a GitHub OAuth folyamatot statikus site esetén (a Sveltia CMS dokumentációja szerint: [github.com/sveltia/sveltia-cms-auth](https://github.com/sveltia/sveltia-cms-auth)). A workerbe kerül az OAuth App Client ID/Secret.
3. **`public/admin/config.yml` frissítése**:
   - `backend.repo`: a tényleges `felhasznalonev/repo` érték.
   - `backend.base_url`: a telepített Cloudflare Worker URL-je.
   - `site_url` / `display_url`: az éles (vagy GitHub Pages) URL.
4. Commit + push — az `/admin` ezután a valós repóhoz és OAuth-hoz kapcsolódik.

**Szerkesztői munkafolyamat:** a `publish_mode: editorial_workflow` beállítás miatt minden új/módosított tartalom előbb vázlat (draft), majd felülvizsgálatra küldött állapotba kerül a CMS-en belül (Git branch + pull request formájában), és csak jóváhagyás után kerül a `main` ágra — ez felel meg a specifikáció vázlat → felülvizsgálatra küldve → publikált elvárásának. Jelenleg egyetlen szerkesztő (projektgazda) van; több szerkesztő/jóváhagyási lánc bevezetése a CMS jogosultsági beállításain és/vagy GitHub repó-jogosultságokon keresztül later bővíthető.

## Tartalom szerkesztése

### CMS-en keresztül (ajánlott, ha az OAuth már be van kötve)

Nyisd meg a `/admin` URL-t → az oldalsávban:

- **Hírek** → Új hír
- **Események** → Új esemény
- **Dokumentumtár** → Új dokumentum
- **Egyedi oldalak** → Főoldali kiemelt információ / Felvételi oldal / Kapcsolati adatok / Rólunk oldal szerkesztése

### Közvetlenül Markdown-fájlokkal (a CMS bekötése előtt is használható)

- Hír: hozz létre egy új `.md` fájlt a `src/content/news/` mappában, a meglévők frontmatter-mintáját követve (`title`, `excerpt`, `category`, `tags`, `pubDate`, `status`, opcionálisan `image`+`imageAlt` stb.).
- Esemény: `src/content/events/`.
- Dokumentum: `src/content/documents/`, a fájlt (jellemzően PDF) a `public/dokumentumok/` mappába töltve, a `file` mezőben a `/dokumentumok/fajlnev.pdf` útvonalra hivatkozva.
- A `category` és `group` mezők **kötött listák** (`src/content/config.ts` — `NEWS_CATEGORIES`, `DOCUMENT_GROUPS`); ne adj hozzá új kategóriát egyetlen bejegyzés kedvéért — a keresztkapcsolatokra a `tags` mező szolgál.
- **Kép elnevezési szabály:** kisbetűs, ékezet nélküli, kötőjeles fájlnév (pl. `2026-golyatabor-csoportkep.webp`), max. 1920px hosszú oldal, tartalmi kép esetén **kötelező** `imageAlt`.

### Automatikus viselkedés

- Egy publikált hír automatikusan megjelenik a főoldal legfrissebb hírei között, a saját kategórialistájában és a hozzá tartozó címke-archívumokban — nincs szükség kézi linkelésre.
- `featured: true` hír a főoldal kiemelt blokkjába kerül (a legfrissebb ilyen jelölésű hír jelenik meg).
- A jövőbeli események a főoldal "Közelgő események" blokkjában és az `/esemenyek/` oldal felső részén jelennek meg; a lezajlott események automatikusan (a dátum alapján) az eseményarchívumba kerülnek — **soha nem törlődnek**.
- A dokumentumok automatikusan a megfelelő csoport alatt jelennek meg a `/dokumentumtar/` oldalon; az `archived: true` dokumentumok külön "Archivált dokumentumok" szekcióban, de továbbra is elérhetők maradnak.
- `vázlat` és `felülvizsgálatra küldve` állapotú tartalom **nem jelenik meg** a publikus oldalakon — csak a `publikált` státuszú elemek épülnek be a buildbe.

## KRÉTA link cseréje

A KRÉTA bejelentkezési link jelenleg egy **általános, ideiglenes célra** mutat (`https://idp.e-kreta.hu/`) — lásd `src/lib/nav.ts` (`KRETA_URL` konstans) tetején a magyarázatot. A specifikáció szerint a KRÉTA session-kötött, hosszú belépési URL-je **nem kódolható be véglegesen**; amint az intézményi IT rendszergazda megadja a stabil intézményi belépési linket, cseréld ki ezt az egyetlen konstanst — minden, ahol a KRÉTA gomb megjelenik (fejléc, főoldal gyors elérés, Kapcsolat oldal), automatikusan frissül.

## Ismert korlátozások (0. verzió)

- A dokumentumtárban szereplő PDF-ek és a `.docx` mintafájl **helyőrzők**, nem valós, éles tartalmúak — cseréld ki őket a valós dokumentumokra feltöltés előtt.
- A cím, telefonszám, e-mail, ügyfélfogadási rend (Kapcsolat oldal, lábláb) minta-/helyőrző adat.
- A jogi lábláboldalak (Adatvédelem, Impresszum, Akadálymentességi nyilatkozat, Fenntartó) placeholder tartalommal indulnak — az Akadálymentességi nyilatkozat a specifikáció szerint is "később" véglegesítendő.
- A `/admin` Sveltia CMS felület jelen állapotban **nincs bekötve élő OAuth-hoz** — lásd a fenti beüzemelési lépéseket.
- Nincs kliens-oldali form-beküldés (pl. kapcsolatfelvételi űrlap) — statikus site, backend nélkül; a Kapcsolat oldal `mailto:` linket használ.

## Verziókövetés

A projekt Git-repóként lett inicializálva, kezdeti commit-tal — így a jövőbeli szerkesztések bármikor visszaállíthatók egy korábbi állapotra (`git log`, `git revert`, `git checkout <commit>`).
