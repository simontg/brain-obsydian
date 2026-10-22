# PLAN: migracja "brain obsydian" z Dysku Google do GitHuba (etapowo, z punktami stopu)

## Kontekst (zweryfikowany)
- Repo kodu (PUBLICZNE): simontg/brain-obsydian. Zawiera graph/graf-wiki.html, README.md, CLAUDE.md, ten plik. Przeczytaj CLAUDE.md najpierw.
- Notatki żyją na Dysku Google (folder Wiki, ID 1gZ7LkfEBOfg0oY3FGf7HRkIGhADK_b2Z): 1 Google Doc = 1 notatka (57 notatek, 5 hubów, HOT/INDEX/LOG jako meta). Format: pierwsza linia = tytuł, potem Type:, Tags:, Summary:, fakty z tagami [stated]/[verified]/[unverified], linia Related: (tytuły rozdzielone średnikiem), [[Dokładny tytuł]]; wiersze huba: "- Tytuł | typ | opis | tagi | data".
- Dwa skrypty w Termuxie (telefon, cron): wiki_index.py (:07) buduje lokalny indeks wyszukiwania BM25 w SQLite FTS5 i wysyła INDEX-AUTO.txt; wiki_graph.py (:12) buduje GRAPH-AUTO.json (węzły, krawędzie, lint). Kopia wiki_graph.py na Dysku: ID 16L62fcMCjLgfsz0Yq6MkjbFpX7VET2lF. wiki_index.py jest tylko w Termuxie (poproś właściciela o kopię).
- Strona grafu jest artefaktem Claude i czyta GRAPH-AUTO.json z Dysku przez konektor. Nie czyta z GitHuba (nie wiadomo, czy mogłaby).
- Test z 21.10: zadanie w chmurze MA dostęp do Dysku przez konektor (Google Drive: get_file_metadata, download_file_content, read_file_content, create_file). Brak rclone w chmurze; curl do googleapis.com z powłoki = 403. Duże odpowiedzi konektora zapisują się do pliku (przetwarzaj jq/Pythonem, nie wczytuj do kontekstu).
- Handoff z pełnymi ID: dokument "HANDOFF-graf-brain.md" w folderze Obsidian-graf (ID folderu 1vyq6DNfJ4it8poszcPXRlkPlSaykyHEI), czytaj przez konektor Dysku.

## Cel
Notatki w repo GitHub (prywatnym), generowanie grafu i indeksu przez GitHub Actions bez telefonu, skille dostępne dla Ciebie, wyszukiwanie BM25 zachowane. Dysk zostaje źródłem prawdy aż do etapu 5.

## Zasady twarde
- Nie zmyślaj. Jeśli czegoś nie wiesz lub nie sprawdziłeś: napisz "nie wiem" / "niezweryfikowane".
- Repo brain-obsydian jest PUBLICZNE: żadnych notatek, tytułów notatek, eksportów, GRAPH-AUTO.json, tokenów. Dane testowe tylko syntetyczne.
- Nigdy nie usuwaj plików na Dysku (przemianuj na "_stary-NAZWA (do usuniecia)" i zgłoś). Nie ruszaj crona w Termuxie ani folderu "Claude - wymiana z pracą".
- Skille konta zmienia tylko właściciel przez kartę propose_skills; ty możesz dodać kopie robocze do repo.
- Po KAŻDYM etapie: krótki raport po polsku (co zrobione, co zweryfikowane, co nie) i STOP do zgody właściciela.
- Oszczędność tokenów: skrypty zamiast ręcznego kopiowania; nie wczytuj całych notatek ani plików, jeśli wystarczy nagłówek/grep/jq; najpierw zmierz koszt na 3 notatkach (HOT ma ok. 65 tys. znaków, czytaj go tylko fragmentami); małe commity; do mechanicznych konwersji wystarczy tańszy model, droższy tylko do projektowania.

## Etap 0 (tylko odczyt, bez zapisów)
1. Przeczytaj CLAUDE.md, README.md, graph/graf-wiki.html (tylko nagłówek i funkcje).
2. Sprawdź, które skille masz dostępne (ListSkills): wiki-brain, write-to-gdrive, handoff, to-spec, grill-me. Jeśli któregoś brakuje w sesji chmurowej, zapisz to w raporcie.
3. Sprawdź dostęp do Dysku konektorem na jednym pliku (np. metadane GRAPH-AUTO.json).
4. Sprawdź, czy sqlite3 w Pythonie ma FTS5: `python3 -c "import sqlite3;c=sqlite3.connect(':memory:');c.execute('create virtual table t using fts5(x)')"`.
5. Raport + STOP.

## Etap 1 (decyzje właściciela, nie rób nic przed odpowiedzią)
a) Gdzie dane: REKOMENDACJA = osobne PRYWATNE repo na notatki (np. brain-obsydian-notes), a brain-obsydian zostaje publiczne z samym kodem. Alternatywa: zrobić brain-obsydian prywatnym i zrezygnować z publicznej witryny.
b) Panel: GitHub Pages z prywatnych danych nie działa na darmowym koncie (prywatna publikacja wymaga Enterprise Cloud). Opcje: zostać przy artefakcie Claude albo publiczna strona z zaszyfrowanym plikiem grafu odszyfrowywanym hasłem w przeglądarce (niesprawdzone).
c) Czy czat na telefonie ma konektor GitHuba z zapisem (niezweryfikowane). Bez tego "wiki save" z telefonu nie zadziała po migracji.

## Etap 2 (eksport notatek do prywatnego repo)
Opcja A (rekomendowana, najtaniej w tokenach): właściciel na telefonie uruchamia istniejący rclone: `rclone copy "gdrive:Claude - skille i projekty/Wiki" ~/brain-notes --drive-export-formats txt`, potem git push do prywatnego repo. Ty tylko walidujesz wynik.
Opcja B: konektor Dysku, notatka po notatce (kosztowne w tokenach; zmierz najpierw 3 notatki).
Walidacja (skryptem): liczba plików = 57 (+/- zmiany); tytuł w pierwszej linii = nazwa pliku; każda notatka ma Type:; nazwy plików bezpieczne (slug), tytuł zostaje w treści. Bez przepisywania treści i bez normalizacji, tylko eksport 1:1.

## Etap 3 (skrypty)
1. tools/wiki_graph.py: reużyj czystej funkcji build() z kopii na Dysku, wczytuj pliki z katalogu zamiast rclone. Test: wygeneruj graf z eksportu i porównaj z GRAPH-AUTO.json z Dysku (te same tytuły, te same krawędzie, ten sam lint; ID węzłów mogą się różnić).
2. tools/wiki_index.py: BM25 na SQLite FTS5 (stdlib), ten sam format INDEX-AUTO.txt. Test na danych syntetycznych + porównanie wyników zapytań ze starym indeksem na kilku zapytaniach.
3. GitHub Action w repo prywatnym: po pushu do wiki/ generuje graph/GRAPH-AUTO.json i INDEX-AUTO.txt (commit przez bota lub artefakt Action). Sekretów do Dysku NIE twórz bez zgody właściciela.
4. OTWARTE: jak strona-artefakt dostaje dane z GitHuba (nie wiadomo, czy może). Do rozstrzygnięcia w etapie 1/3; tymczasowo graf nadal produkuje telefon na Dysk.

## Etap 4 (skille)
- Przygotuj w repo prywatnym .claude/skills/ wariant gitowy wiki-brain (np. wiki-brain-git): te same komendy (wiki save / ask / lint), te same zasady (jeden fakt w jednej notatce, Related z dokładnymi tytułami, HOT jako router z linią Related do wszystkich hubów, tagi [stated]/[verified]/[unverified], nie kasować), ale operacje na plikach i commitach zamiast Dysku. Oryginalnego skilla na Dysku nie ruszaj.
- Skill ma wskazywać, że czytanie zaczyna się od HOT, potem INDEX, potem hub, potem wyszukiwanie BM25 (mniej tokenów niż czytanie wielu notatek).
- Propozycję zmian skilli konta zgłoś właścicielowi jako gotowy SKILL.md do zapisania kartą.

## Etap 5 (przełączenie, tylko za zgodą)
- Praca równoległa Dysk + GitHub min. kilka dni; kryterium: wynik grafu i lintu identyczny, "wiki ask" z obu źródeł daje te same odpowiedzi na zestawie pytań testowych.
- Dysk zostaje jako kopia zapasowa. Nic nie kasować.
- Zaktualizuj CLAUDE.md i README (bez danych osobistych).

## Do zweryfikowania przed etapem 5
Konektor GitHuba w czacie telefonu, sposób zasilania artefaktu danymi, koszt tokenów jednego "wiki save" w nowym układzie, czy FTS5 działa w środowisku chmurowym i na Termuxie.
