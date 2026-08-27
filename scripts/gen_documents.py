#!/usr/bin/env python3
"""Egyszeri segédszkript: a dokumentumtár minta-frontmatter fájljainak legenerálása
a specifikáció 9. szakasza alapján. Nem kell buildkor futtatni, csak a 0. verzió
tartalmának előállításához használtuk."""
import re
import unicodedata
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "src" / "content" / "documents"
OUT.mkdir(parents=True, exist_ok=True)

def slugify(title: str) -> str:
    t = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t

GROUP_1 = "Alapdokumentumok"
GROUP_2 = "Különös közzétételi lista"
GROUP_3 = "Letölthető nyomtatványok, kérelmek"

# (title, group, description, has_placeholder_file, archived)
DOCS = [
    ("Belső vizsgaszabályzat", GROUP_1, "A tanulmányok alatti vizsgák belső rendjét meghatározó szabályzat.", True, False),
    ("Esélyegyenlőségi terv", GROUP_1, "Az intézmény esélyegyenlőségi intézkedéseit összefoglaló dokumentum.", False, False),
    ("Gyakornoki szabályzat", GROUP_1, "A gyakornoki idő és a mentorálás rendje.", False, False),
    ("Házirend", GROUP_1, "A tanulói és szülői jogokat és kötelezettségeket rögzítő házirend.", True, False),
    ("Iskolai sportkörök", GROUP_1, "A diáksport-egyesület és a sportkörök működési rendje.", False, False),
    ("Minőségirányítási program", GROUP_1, "Az intézmény minőségirányítási programja.", False, False),
    ("NOKS helyi értékelési szabályzat", GROUP_1, "A nevelő-oktató munkát segítő munkatársak helyi értékelési szabályzata.", False, False),
    ("Pedagógiai program", GROUP_1, "Az intézmény pedagógiai programja. Jelenleg fenntartói jóváhagyás alatt áll.", False, False),
    ("Szakmai alapdokumentum", GROUP_1, "Az intézmény hatályos szakmai alapdokumentuma.", False, False),
    ("Szakmai alapdokumentum módosítása – határozat", GROUP_1, "A szakmai alapdokumentum legutóbbi módosításáról szóló fenntartói határozat.", False, False),
    ("Szervezeti és működési szabályzat", GROUP_1, "Az intézmény szervezeti és működési szabályzata (SZMSZ).", True, False),
    ("Tanév rendje", GROUP_1, "A hatályos tanév rendjéről szóló miniszteri rendelet és az intézményi ütemezés.", False, False),
    ("Tanulmányi- és sportversenyek", GROUP_1, "Az intézmény által meghirdetett és támogatott versenyek listája.", False, False),
    ("Intézményi önértékelés 2024", GROUP_2, "Az intézményi önértékelési folyamat 2024. évi összefoglalója.", False, False),
    ("Tanfelügyeleti értékelés 2025", GROUP_2, "A 2025. évi külső tanfelügyeleti értékelés dokumentuma.", False, False),
    ("Intézkedési terv 2025–2030", GROUP_2, "Az intézmény középtávú fejlesztési és intézkedési terve.", False, False),
    ("Az érettségi vizsgák átlageredményei", GROUP_2, "Az érettségi vizsgák átlageredményei évenkénti bontásban.", False, False),
    ("Pedagógusok végzettsége és szakképzettsége", GROUP_2, "A pedagógusok iskolai végzettsége és szakképzettsége a helyi tanterv tantárgyfelosztásához rendelve.", False, False),
    ("Nevelő-oktató munkát segítők adatai", GROUP_2, "A nevelő és oktató munkát segítők száma, feladatköre, végzettsége és szakképzettsége.", False, False),
    ("Országos mérés-értékelés eredményei", GROUP_2, "Az országos kompetenciamérés eredményei évenkénti bontásban.", False, False),
    ("Lemorzsolódási és évismétlési mutatók", GROUP_2, "Az intézmény lemorzsolódási és évismétlési adatai.", False, False),
    ("Szakkörök és mindennapos testedzés", GROUP_2, "A szakkörök igénybevételének lehetősége és a mindennapos testedzés rendje.", False, False),
    ("Házi feladat és iskolai dolgozatok szabályai", GROUP_2, "A hétvégi házi feladat és az iskolai dolgozatok szabályozása.", True, False),
    ("Osztályok száma és létszáma", GROUP_2, "Az iskolai osztályok száma és az egyes osztályok tanulói létszáma.", False, False),
    ("Közzétételi lista (KIR)", GROUP_2, "A Köznevelési Információs Rendszerben (KIR) vezetett közzétételi lista.", False, False),
    ("Osztályozó vizsga követelményei", GROUP_2, "Az osztályozó vizsga tantárgyankénti, évfolyamonkénti követelményei és a vizsgák tervezett ideje.", False, False),
    ("Osztályozó vizsga iránti kérelem (DOCX)", GROUP_3, "Kitölthető kérelem osztályozó vizsga letételéhez, szerkeszthető formátumban.", True, False),
    ("Osztályozó vizsga iránti kérelem (PDF)", GROUP_3, "Kitölthető kérelem osztályozó vizsga letételéhez, nyomtatható formátumban.", True, False),
    ("Testnevelés felmentés kérelem (DOCX)", GROUP_3, "Kérelem testnevelés óra alóli felmentéshez, szerkeszthető formátumban.", False, False),
    ("Testnevelés felmentés kérelem (PDF)", GROUP_3, "Kérelem testnevelés óra alóli felmentéshez, nyomtatható formátumban.", False, False),
]

for title, group, desc, has_file, archived in DOCS:
    slug = slugify(title)
    ext = "docx" if "DOCX" in title else "pdf"
    file_field = f'\nfile: "/dokumentumok/{slug}.{ext}"' if has_file else ""
    content = f'''---
title: "{title}"
group: "{group}"
description: "{desc}"{file_field}
archived: {str(archived).lower()}
status: "publikált"
---
'''
    (OUT / f"{slug}.md").write_text(content, encoding="utf-8")

print(f"Legenerálva: {len(DOCS)} dokumentum-bejegyzés a {OUT} mappába.")
