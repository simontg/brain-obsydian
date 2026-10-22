# PLAN: migracja "brain obsydian" z Dysku Google do GitHuba (etapowo, z punktami stopu)

## Kontekst (zweryfikowany)
- Repo kodu (PUBLICZNE): simontg/brain-obsydian. Zawiera graph/graf-wiki.html, README.md, CLAUDE.md, ten plik. Przeczytaj CLAUDE.md najpierw.
- Notatki żyją na Dysku Google (folder Wiki, ID 1gZ7LkfEBOfg0oY3FGf7HRkIGhADK_b2Z): 1 Google Doc = 1 notatka (67 węzłów wg stanu z 22.10.2026, w tym 5 hubów i HOT/INDEX/LOG jako meta; w chwili pisania planu było 57). Format: pierwsza linia = tytuł, potem Type:, Tags:, Summary:, fakty z tagami [stated]/[verified]/[unverified], linia Related: (tytuły rozdzielone średnikiem), [[Dokładny tytuł]]; wiersze huba: "- Tytuł | typ | opis | tagi | data".
- Dwa skrypty w Termuxie (telefon, cron): wiki_index.py (:07) buduje lokalny indeks wyszukiwania BM25 w SQLite FTS5 i wysyła INDEX-AUTO.txt; wiki_graph.py (:12) buduje GRAPH-AUTO.json (węzły, krawędzie, lint). Kopia wiki_graph.py na Dysku: ID 16L62fcMCjLgfsz0Yq6MkjbFpX7VET2lF. wiki_index.py jest tylko w Termuxie (poproś właściciela o kopię).
- Strona grafu jest artefaktem Claude i czyta GRAPH-AUTO.json z Dysku przez konektor. Nie czyta z GitHuba (nie wiadomo, czy mogłaby).
- Test z 21.10: zadanie w chmurze MA dostęp do Dysku przez konektor (Google Drive: get_file_metadata, download_file_content, read_file_content, create_file). Brak rclone w chmurze; curl do googleapis.com z powłoki = 403. Duże odpowiedzi konektora zapisują się do pliku (przetwarzaj jq/Pythonem, nie wczytuj do kontekstu).
- Handoff z pełnymi ID: dokument "HANDOFF-graf-brain.md" w folderze Obsidian-graf (ID folderu 1vyq6DNfJ4it8poszcPXRlkPlSaykyHEI), czytaj przez konektor Dysku.

## Dostęp do GitHuba
Zobacz docs/GITHUB-ACCESS.md. Zapis z czatu mobilnego do obu repo zweryfikowany 22.10.2026 (to odpowiada na punkt c etapu 1 i zadanie 5 etapu 1.5: działa przez narzędzia sesji add_repo + git, nie przez osobny konektor GitHuba).

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

## Etap 0: ZROBIONY (22.10.2026)
Dostęp do Dysku konektorem OK (GRAPH-AUTO.json, 57 węzłów), FTS5 w Pythonie OK (SQLite 3.45.1), skille na liście sesji: wiki-brain, write-to-gdrive, handoff, to-spec, grill-me (treści nie czytano). Brak kopii wiki_index.py: potrzebna od właściciela przed etapem 3.

## Etap 1: DECYZJE WŁAŚCICIELA (zatwierdzone 22.10.2026)
a) Dane: prywatne repo `simontg/Brain-Obsydian-NOTES` (istnieje, puste). Układ: `wiki/` (notatki), `sources/` (materiały źródłowe, bez dużych PDF-ów; zalecany limit repo 1 GB), `graph/` (wygenerowany graf). Publiczne `brain-obsydian` zostaje z samym kodem.
b) Panel: graf dostępny z repo, nie z Dysku. Publiczna strona na GitHub Pages z publicznego repo, dane grafu ZASZYFROWANE hasłem odszyfrowywanym w przeglądarce. Pages z prywatnego repo odpada (Free = Pages tylko w publicznych repo; prywatna publikacja wymaga Enterprise Cloud wg dokumentacji GitHub).
c) Konektor GitHuba z zapisem w czacie na telefonie: według właściciela jest (niezweryfikowane przez agenta; sprawdza etap 1.5).
d) Pilotaż (etap 1.5) PRZED etapem 2.
e) Organizacja pracy: jeden etap = jedno nowe okno projektu. Sesja orkiestratora tylko przyjmuje raport, sprawdza wynik i czeka na zgodę właściciela.

## Etap 1.5 (pilotaż na danych SYNTETYCZNYCH, bez prawdziwych notatek)
Zadania i kryteria zaliczenia:
1. Syntetyczny graf (ok. 10 węzłów, format jak w README) generowany Actionem i szyfrowany hasłem (hasło w sekrecie repo, nie w kodzie). Zaliczone, gdy: plik w repo jest nieczytelny bez hasła.
2. Strona na GitHub Pages (publiczne repo) odszyfrowuje graf w przeglądarce (WebCrypto). Zaliczone, gdy: działa na telefonie i desktopie; błędne hasło daje czytelny komunikat.
3. Aktualizacja grafu: zmień dane, uruchom Action, odśwież stronę. Zaliczone, gdy: nowe dane widoczne, a hasła nie trzeba zmieniać. Zapisać, ile razy właściciel musi wpisać hasło.
4. Test, czy artefakt Claude może pobrać dane z GitHuba (publiczny URL i/lub konektor). Wynik zapisać wprost, także negatywny.
5. Test zapisu z telefonu do repo przez konektor GitHuba (właściciel). Wynik zapisać wprost.
6. Raport po polsku: co zrobione, co zweryfikowane, czego nie wiadomo. STOP do zgody właściciela.
Zasady: żadnych prawdziwych tytułów ani danych; hasła i tokeny nigdy w commitach ani w raporcie.

## Etap 1.5: WYNIKI (22.10.2026)
Zaliczone (zweryfikowane):
1. Graf syntetyczny generowany Actionem (pilot/synthetic-graph.json, tools/pilot_build.py, .github/workflows/pilot-graph.yml), szyfrowany AES-256-GCM + PBKDF2, hasło w sekrecie PILOT_PASSWORD. Plik graph/graph.enc.json w repo nieczytelny (0 trafień na słowo "Synthetic"). Przebiegi Action na main: build + commit bota + deploy, zielone.
2. Strona na GitHub Pages (https://simontg.github.io/brain-obsydian/) odszyfrowuje graf w przeglądarce. Błędne hasło: komunikat "Błędne hasło lub uszkodzony plik" (sprawdzone na żywo przez agenta, 1280 i 392 px). Dobre hasło na komputerze i telefonie: potwierdził właściciel.
3. Aktualizacja: dodany węzeł (11 zamiast 10) przez PR i Action, hasło bez zmian, nowe dane widoczne (potwierdził właściciel). Hasło wpisywane raz na komputerze i raz na telefonie; odświeżenie strony ani "Odśwież" nie pytają ponownie (hasło w sessionStorage, tylko do zamknięcia karty). Po zamknięciu karty pytanie wraca (wg właściciela, zgodne z projektem).
4. Artefakt Claude NIE pobierze danych z GitHuba: fetch() z artefaktu do publicznego URL = "TypeError: Failed to fetch" (zrzut właściciela); konektor "GitHub" w artefakcie = "No matching connector found" (na koncie nie ma takiego konektora, sprawdzone listą konektorów). Artefakt-graf dalej czyta z Dysku.
Uwagi: każdy przebieg Action commituje nowy graph/graph.enc.json na main (losowa sól i IV), więc przed lokalną edycją trzeba zrobić git pull. Commit bota na main przeszedł (brak ochrony gałęzi).

5. Zapis do prywatnego repo Brain-Obsydian-NOTES: zaliczone, dwa niezależne testy. (a) Telefon właściciela: pilot-test.txt w repo (commit 42a8a09, syntetyczny). (b) Sesja agenta, za zgodą właściciela: add_repo z access "push", klon, commit i push syntetycznego pliku (2ace8f7), weryfikacja git ls-remote, usunięcie pliku (e7cbaa6, historia zostaje). Założenie 1c było błędne co do mechanizmu: zapis działa przez narzędzia chmurowej sesji claude-code-remote (docs/GITHUB-ACCESS.md), nie przez konektor GitHub z listy konektorów claude.ai. Pierwsza próba add_repo push została odrzucona przez system uprawnień sesji, druga (po wyraźnej zgodzie) przeszła. Uwaga: add_repo zwraca nazwę z małych liter (brain-obsydian-notes); klon i push działały z pisownią Brain-Obsydian-NOTES.

Źródło prawdy do końca migracji (Etap 5): Dysk Google. Strona na Pages z grafem syntetycznym działa równolegle jako pilotaż. Po potwierdzeniu migracji Dysk zostaje kopią zapasową.

## Etap 2 (eksport notatek do prywatnego repo)
Opcja A (rekomendowana, najtaniej w tokenach): właściciel na telefonie uruchamia istniejący rclone: `rclone copy "gdrive:Claude - skille i projekty/Wiki" ~/brain-notes --drive-export-formats txt`, potem git push do prywatnego repo. Ty tylko walidujesz wynik.
Opcja B: konektor Dysku, notatka po notatce (kosztowne w tokenach; zmierz najpierw 3 notatki).
Walidacja (skryptem): liczba plików = liczba węzłów w GRAPH-AUTO.json (22.10.2026: 67); tytuł w pierwszej linii = nazwa pliku; każda notatka ma Type:; nazwy plików bezpieczne (slug), tytuł zostaje w treści. Bez przepisywania treści i bez normalizacji, tylko eksport 1:1.

## Etap 2: WYNIKI (22.10.2026) — STATUS: ZAMKNIĘTY Z UWAGAMI
Eksport 1:1 z Dysku wypchnięty przez właściciela do prywatnego `Brain-Obsydian-NOTES` (commit 41b731d), po walidacji porządki w commicie 4fd8651. Stan: 67 plików w `wiki/`, wszystkie notatki; w katalogu głównym tylko `wiki/`.
Zweryfikowane (skryptem sesji walidującej i ponownie przez orkiestratora na klonie): 67 plików; `Type:` z wartością w 67/67; 67 węzłów w grafie z Dysku (22.10.2026) = 67 plików; lint grafu: 0 martwych linków, 0 niejednoznacznych tytułów, 0 osieroconych, 0 bez typu, 0 pustych.
Usunięte z repo notatek (za zgodą właściciela): `pilot-test.txt` (syntetyczny test zapisu) oraz `wiki/INDEX-AUTO.txt` (dane pochodne z `wiki_index.py`, w etapie 3 będą generowane Actionem).
Pozycje otwarte (nie blokują etapu 3, chyba że napisano inaczej):
- O1. 64 z 67 nazw plików ma dwukropek (niedozwolony w nazwach plików Windows). Decyzja właściciela: zostają, bez normalizacji. Do rozstrzygnięcia PRZED etapem 5; nie sprawdzono, jak radzą sobie rclone, Termux i Obsidian. Nie blokuje etapu 3.
- O2. Wszystkie 67 plików ma BOM i końce linii CRLF (z eksportu Dysku). Etap 3 musi to obsłużyć przy parsowaniu (utf-8-sig, normalizacja CRLF) bez zmieniania plików. BLOKUJE test `wiki_graph.py`.
- O3. Pierwsza linia `HOT.txt` ma sufiks ze stanem (data i godzina), więc nie równa się nazwie pliku; to jedyny taki plik (kontrola orkiestratora). Traktować jako wyjątek meta; w etapie 3 sprawdzić, jak tytuł HOT trafia do grafu.
- O4. Różnica 57 (w chwili pisania planu) wobec 67 (stan z 22.10): wyjaśnienie właściciela to przyrost notatek z innego projektu po pierwszym eksporcie. Niezweryfikowane. Nie blokuje.
- O5. Przyczyna, dla której `INDEX-AUTO.txt` znalazł się w eksporcie: zakładana (kopiowanie całego folderu `Wiki`), niepotwierdzona. Nie blokuje.

## Etap 3 (skrypty)
1. tools/wiki_graph.py: reużyj czystej funkcji build() z kopii na Dysku, wczytuj pliki z katalogu zamiast rclone. Test: wygeneruj graf z eksportu i porównaj z GRAPH-AUTO.json z Dysku (te same tytuły, te same krawędzie, ten sam lint; ID węzłów mogą się różnić).
2. tools/wiki_index.py: BM25 na SQLite FTS5 (stdlib), ten sam format INDEX-AUTO.txt. Test na danych syntetycznych + porównanie wyników zapytań ze starym indeksem na kilku zapytaniach.
3. GitHub Action w repo prywatnym: po pushu do wiki/ generuje graph/GRAPH-AUTO.json i INDEX-AUTO.txt (commit przez bota lub artefakt Action). Sekretów do Dysku NIE twórz bez zgody właściciela.
4. OTWARTE: jak strona-artefakt dostaje dane z GitHuba (nie wiadomo, czy może). Do rozstrzygnięcia w etapie 1/3; tymczasowo graf nadal produkuje telefon na Dysk.

## Etap 3a: WYNIKI (22.10.2026) — STATUS: ZAMKNIĘTY Z UWAGAMI
Zrobione: `tools/wiki_graph.py` (stdlib, `wiki_graph.py WIKI_DIR [-o OUT]`) i test `tools/tests/test_wiki_graph.py` (dane syntetyczne, `python3 tools/tests/test_wiki_graph.py`). Funkcje `norm/clean/strip_code/field/build` skopiowane bez zmian z kopii na Dysku (ID 16L62fcMCjLgfsz0Yq6MkjbFpX7VET2lF; kontrola: fragment kodu identyczny ze wzorcem, 6484 B = rozmiar z metadanych). Zmieniona tylko warstwa I/O: katalog zamiast rclone; ID i tytuł węzła = nazwa pliku bez `.txt` (jak we wzorcu); notatki sortowane po nazwie (determinizm); `modified` = data ostatniego commitu pliku w git, a poza git mtime.
Wejście: `Brain-Obsydian-NOTES`, `wiki/`, HEAD main 4fd8651. Porównanie z `GRAPH-AUTO.json` z Dysku (ID 1_8l49uTR8LomAfFyDEIjdE6KmneL4NqR, `generated_at` 2026-10-22T08:17:02Z, 76628 B).
Kryteria "Zaliczone gdy":
1. 67 węzłów z `wiki/` — ZWERYFIKOWANE (`count` = 67, 67 plików `*.txt`, wszystkie z BOM i CRLF, pliki niezmienione: sha256 przed/po identyczne, `git status` repo notatek czysty).
2. Porównanie z grafem z Dysku — ZWERYFIKOWANE: ten sam zbiór tytułów (67 wspólnych, 0 różnic); ten sam zbiór krawędzi (źródło, cel, rodzaj) po tytułach: 305 = 305, 0 różnic (related 232, hub 60, link 13); lint identyczny, wszystkie 5 list puste; klucze `nodes` i kolejność kluczy najwyższego poziomu identyczne. Różnice pól węzłów: jedynie `modified` (67/67). Klasyfikacja: oczekiwana, nie błąd — Drive podaje ModTime dokumentu (67 różnych wartości, 2026-10-07..2026-10-22), a eksport do gita go nie zachował; po pełnej historii wszystkie pliki mają datę commitu eksportu 41b731d (2026-10-22T08:14:43Z), w płytkim klonie datę HEAD (zweryfikowane oba warianty). Poza `modified` pozostałe pola węzłów (typ, tagi, summary, chars, verified/stated/unverified, incoming) zgodne we wszystkich 67. Tytuł HOT: jak we wzorcu tytuł = nazwa pliku (`HOT`), sufiks ze stanu z pierwszej linii NIE trafia do grafu; w grafie z Dysku też `HOT` (zweryfikowane). Polecenie zadania mówiło "tytuł z pierwszej linii", ale wzorzec bierze nazwę pliku; zachowano wzorzec (66/67 identyczne, HOT zgodny z grafem z Dysku).
3. Test syntetyczny — ZWERYFIKOWANE: 8 testów OK (BOM+CRLF, martwy link we wzorze `[[..]]`, w `Related:` i w wierszu huba, osierocona notatka, duplikat tytułu wykryty także bez uwzględnienia ogonków, brak typu, pusta notatka, link w code fence ignorowany, HOT z sufiksem, pominięcie INDEX-AUTO.txt, pliki wejściowe nie zmienione, uruchomienie z linii poleceń). Kontrola mutacyjna: usunięcie normalizacji CRLF oraz wyłączenie zapisu martwych linków powoduje czerwone testy.
4. Determinizm — ZWERYFIKOWANE: dwa uruchomienia na prawdziwych notatkach dają identyczny graf poza `generated_at` (porównanie bajtowe).
Środowisko testu: Python 3.13.16 w chmurze. Termux (inna wersja Pythona, system plików) — NIEZWERYFIKOWANE. Wynik z prawdziwych notatek nie jest w repo.
Pozycje otwarte:
- O6. `modified` z gita nie odtwarza dat z Dysku (patrz wyżej): widok "Czas" na grafie z gita byłby płaski (jedna data). Decyduje właściciel: zaakceptować, czy trzymać datę w nagłówku notatki (wymaga zmiany notatek i skilla). Nie blokuje 3b; blokuje przełączenie grafu na dane z gita (etap 5).
- O7. `id` węzła = nazwa pliku, nie ID Dokumentu Google. `graph/graf-wiki.html` buduje link "Otwórz" z `n.id` (`docUrl(n.id)`), więc dla grafu z gita link byłby błędny. Wymaga zmiany strony (np. link do pliku w repo prywatnym albo ukrycie przycisku) przed przełączeniem. Decyduje właściciel (zachowanie przycisku). Nie blokuje 3b.
- O8. Dla płytkiego klonu (`--depth 1`) `modified` = data HEAD. Akcja w etapie 3c powinna używać `fetch-depth: 0`, jeśli `modified` ma być datą ostatniej zmiany pliku. Nie blokuje 3b.
- O9. Nazwy plików z dwukropkiem (O1): skrypt działa na nich w Linuksie (64 pliki w teście); Windows niezweryfikowane. DECYZJA WŁAŚCICIELA (22.10.2026): ZAMKNIĘTE jako nieistotne, system ma działać niezależnie od platformy (Linux/Termux), Windows poza zakresem.
- Decyzja właściciela do O6 (22.10.2026): akceptuje jedną wspólną datę dla 67 notatek z eksportu; nowe i zmienione notatki mają mieć poprawne daty (data ostatniego commitu pliku). Zastrzeżenia: to data zapisu do gita, nie pisania; zbiorczy commit dotykający wszystkich plików spłaszczy oś; wymaga pełnej historii (O8). Zachowanie dla późniejszych edycji niezweryfikowane na prawdziwych danych. O7 (przycisk "Otwórz") bez decyzji, do rozstrzygnięcia przed etapem 5; propozycja: link do pliku w prywatnym repo (niesprawdzone, czy artefakt pozwoli otworzyć taki link).

## Etap 3b: WYNIKI (22.10.2026) — STATUS: ZAMKNIĘTY Z UWAGAMI
Zrobione: `tools/wiki_index.py` (stdlib + FTS5, `wiki_index.py {build,search,export} [zapytanie] [--root DIR] [--db PLIK] [--out PLIK]`, domyślnie `--root wiki`, `--db index.db`, `--out INDEX-AUTO.txt` w bieżącym katalogu) i test `tools/tests/test_wiki_index.py` (dane syntetyczne, `python3 tools/tests/test_wiki_index.py`). Wzorzec: kopia `wiki_index.py` z Termuxa przesłana przez właściciela na Dysk (ID 1iH6vH5tYojYdEQIcWLpBdNnPTFJvxm9l, 7149 B = rozmiar z metadanych). Funkcje `chunk`, `search`, `export` są bez zmian (diff: jedyna zmiana to nagłówek `root:` bez przedrostka rclone). Zmieniona tylko warstwa wejścia: katalog zamiast rclone, `modified` jak w `wiki_graph.py` (data ostatniego commitu pliku, poza gitem mtime), pliki `.txt`/`.md` rekurencyjnie, pomijane `_stary-*`, katalogi z kropką i `INDEX-AUTO.txt`. Świadomie usunięte: przyrost (baza przebudowywana od zera, 67 notatek to ułamek sekundy), `--full`, `upload` (w 3c Action zapisze INDEX-AUTO.txt do repo), `guard` (dotyczył folderu na Dysku). Domyślne `--db` i `--out` w bieżącym katalogu, żeby nie nadpisać `~/wiki_index/index.db` ani INDEX-AUTO.txt, których używa cron na telefonie; `*.db` dodano do `.gitignore`.
Wejście: `Brain-Obsydian-NOTES`, `wiki/`, HEAD main 4fd8651 (pełna historia pobrana do sprawdzenia dat). Stary indeks do porównania: `INDEX-AUTO.txt` z folderu Wiki na Dysku (ID 1dCuwb2gohyXDHPAeXxL_GNhQU0XnUSys, `generated-at` 2026-10-22T09:07:04Z, root = folder Wiki, 67 plików, ścieżki `<nazwa>.txt`). Stary skrypt nie może czytać z katalogu, więc oryginał uruchomiono na tych samych notatkach przez atrapę `rclone` (poza repo, tylko `lsjson` i `cat`), a jej wierność sprawdzono osobno (pkt 2a).
Kryteria (zdefiniowane w tej sesji, bo PLAN.md nie ma ich dla 3b):
1. Działa na `wiki/` z repo notatek: 67 plików — ZWERYFIKOWANE (`plikow: 67`; pliki notatek niezmienione: sha256 przed/po identyczne, `git status` repo notatek czysty).
2. Zgodność z indeksem z Dysku — ZWERYFIKOWANE:
   a) oryginalny skrypt na notatkach z gita (atrapa) vs prawdziwy INDEX-AUTO z Dysku: ten sam zbiór 67 ścieżek, ta sama kolejność, te same tytuły, `chars`, słowa kluczowe, `modified` (atrapa dostała daty z Dysku), liczby `linked-from` w 67/67 i linie ORPHANS/STALE (0 i 0). Jedyna różnica: lista do 5 nazw w `linked-from` — kolejność nazw różni się w 58 plikach, a zawartość listy w 24 (wszystkie z liczbą > 5; lista jest obcięta do pierwszych 5, które zależą od kolejności wstawiania do bazy, a ta od historii przyrostu). Wniosek: notatki w gicie = notatki użyte do starego indeksu, atrapa jest wierna.
   b) oryginał (atrapa) vs nowy skrypt: ta sama lista 67 ścieżek i kolejność, te same tytuły (w tym HOT z sufiksem ze stanem, bo ten skrypt bierze tytuł z pierwszej linii, inaczej niż graf), słowa kluczowe, liczby `linked-from`, ORPHANS (0) i STALE (0). Różnice sklasyfikowane: (i) `modified` w 53 z 67 plików: data commitu zamiast czasu modyfikacji dokumentu (O6, zaakceptowane); (ii) `chars` w 63 z 67: nowy skrypt normalizuje CRLF (O2); dowód: ten sam kod z wyłączoną normalizacją daje `chars`, tytuły i słowa kluczowe identyczne z oryginałem w 67/67; (iii) lista do 5 nazw w `linked-from`: kolejność różni się w 56 plikach, zawartość w tych samych 24 co wyżej; w nowym skrypcie jest deterministyczna (kolejność po ścieżce).
3. Zapytania — ZWERYFIKOWANE (przed poprawką O11; po niej patrz O11): 17 zapytań (typowe słowa z notatek, nie wypisane w publicznym repo; 14 z wynikami, 3 bez wyniku) na bazie starego oryginału i nowej bazie: te same ścieżki, ta sama kolejność i te same wyniki BM25 we wszystkich. Różnica w treści snippetów: stary skrypt zostawiał w nich `\r`, nowy nie.
4. Test syntetyczny — ZWERYFIKOWANE: 7 testów OK (BOM+CRLF, wybór plików: `.md`, podkatalog, `_stary-*`, katalog z kropką, INDEX-AUTO.txt i nie-notatka pominięte; tytuł z pierwszej linii, `#` obcięte; wyszukiwanie z ogonkami i brak wyniku; format nagłówka eksportu, `linked-from`, ORPHANS; STALE; przebudowa usuwa skasowaną notatkę; CLI; pliki wejściowe niezmienione). Kontrola mutacyjna na kopii: wyłączenie pomijania INDEX-AUTO.txt, wyłączenie czyszczenia bazy i wyłączenie pomijania `_stary-*` dają czerwone testy. Testy 3a nadal przechodzą (8/8).
5. Determinizm — ZWERYFIKOWANE: dwa uruchomienia `build`+`export` na prawdziwych notatkach dają identyczny INDEX-AUTO.txt poza linią `generated-at`.
Środowisko: Python 3.13.16, SQLite 3.45.1 z FTS5 w chmurze. Termux (inne wersje) — NIEZWERYFIKOWANE. Wynik z prawdziwych notatek, atrapa i kopie indeksów zostały poza repo. Dysk, cron i repo notatek nietknięte (jedyna zmiana na Dysku to kopia `wiki_index.py` wgrana przez właściciela).
Pozycje otwarte:
- O10. Normalizacja CRLF w indeksie: skutkiem są mniejsze `chars` w INDEX-AUTO i brak `\r` w snippetach; wyniki wyszukiwania bez zmian (pkt 3). Jeśli właściciel chce INDEX-AUTO identyczny bajtowo co dotychczas, wystarczy pominąć `clean()` w `build()` (jedna linia). Rekomendacja: zostawić normalizację (niezależność od końców linii). Decyduje właściciel. Nie blokuje 3c.
- O11. ROZWIĄZANE na polecenie właściciela (22.10.2026): tokenizer FTS5 nie składał `ł` do `l` (`zrodlo` nic nie znajdowało, `źródło` tak; ogonki ó, ź, ń działały; ą, ę, ś, ć, ż nie sprawdzano osobno). Poprawka tylko po stronie zapytania: każde słowo jest rozwijane na wszystkie kombinacje `l`/`ł` (do 6 takich liter w słowie, powyżej tylko wersje all-l i all-ł); indeks, snippety i punktacja BM25 bez zmian. Zweryfikowane: test syntetyczny (warianty `zrodlo`, `ZRODLO`, `źródło`, `zródło` dają ten sam zestaw; słowo mieszane `lubil` znajduje `lubił`; zapytanie z 8 literami l/ł bez błędu), kontrola mutacyjna (wyłączenie rozwijania daje czerwony test), prawdziwe notatki: `zrodlo` 0 → 5 wyników, `zrodlo` i `źródło` dają te same ścieżki i wyniki; z 16 zapytań 15 identycznych z oryginalnym skryptem, jedno (`zrodla verified`) różni się zamierzenie: w top-5 jest jedna dodatkowa notatka zawierająca "źródła" (4 z 5 ścieżek wspólnych). Skutek uboczny: dwa różne polskie słowa różniące się tylko `l`/`ł` (np. `stal`/`stał`) są traktowane jako jedno.
- O12. `wiki_index.py` bierze tytuł z pierwszej linii (HOT ma więc w indeksie sufiks ze stanem), a `wiki_graph.py` z nazwy pliku (HOT = `HOT`). Zgodne ze starymi skryptami; wystarczy pamiętać przy etapie 4 (skill). Nie wymaga decyzji.
- O8 (3a) obowiązuje także tu: `modified` w Action wymaga `fetch-depth: 0`.

## Etap 3c: WYNIKI (22.10.2026) — STATUS: ZAMKNIĘTY Z UWAGAMI
Zrobione: workflow `generate-graph-index`, wersjonowany w tym repo jako `tools/notes-repo/generate-graph-index.yml` i wgrany do prywatnego `Brain-Obsydian-NOTES` jako `.github/workflows/generate-graph-index.yml` (commit f7c445c na `main`, za wyraźną zgodą właściciela po wcześniejszej odmowie klasyfikatora uprawnień sesji; wdrożony plik jest identyczny z szablonem). Wyzwalacze: push do `main` zmieniający `wiki/**` lub sam plik workflow, oraz ręczne uruchomienie. Kroki: pełna historia gita (`fetch-depth: 0`, dla `modified`), narzędzia z publicznego repo przypięte do SHA 549449d (PR #7 jeszcze niescalony), `wiki_graph.py` + `wiki_index.py` (build, export), kontrola `count > 0`, w logu tylko liczby (żadnych tytułów), commit bota `graph/GRAPH-AUTO.json` i `graph/INDEX-AUTO.txt` WYŁĄCZNIE gdy zmieniła się treść (samo `generated_at` / `generated-at` nie liczy się), `git pull --rebase` przed pushem. Sekretów nie utworzono, Dysku nie dotykano. Zakładam rekomendację z O10 (normalizacja CRLF zostaje); właściciel nie odpowiedział wprost.
Zweryfikowane na GitHubie (przebieg 1 = push z workflow, przebieg 2 = ręczne uruchomienie, oba zielone, ok. 8-11 s):
1. Actions jest włączone, workflow aktywny, push zmieniający plik workflow uruchomił przebieg (sprawdza ścieżkę pliku workflow w filtrze `paths`, nie `wiki/**`, patrz niżej).
2. Pobranie publicznego repo po SHA z niescalonego PR-a zadziałało; Python runnera ma FTS5; `contents: write` wystarczyło do pushu bota na `main` (commit 2ab37fd, autor github-actions[bot], 2 pliki, brak ochrony gałęzi).
3. Wynik na GitHubie: 67 węzłów, 305 krawędzi, lint 0/0/0/0/0, 67 plików w indeksie. Porównanie z grafem z Dysku: te same tytuły (67/67), te same krawędzie (305/305), ten sam lint; jedyna różnica to `modified` (jedna wspólna data, O6). Graf z GitHuba identyczny z wynikiem lokalnym z 3a poza `generated_at`; INDEX-AUTO identyczny z lokalnym poza pierwszą linią.
4. Idempotencja: przebieg 2 na tych samych danych: "no content change, nothing to commit", brak nowego commita.
5. Brak pętli: po commicie bota nie uruchomił się żaden dodatkowy przebieg (w historii tylko przebiegi 1 i 2).
6. `wiki/` nietknięte (diff `wiki/` między 4fd8651 a `main` pusty); logi obu przebiegów przejrzane: tylko liczby i polecenia, bez tytułów.
Zweryfikowane lokalnie (symulacja przed wdrożeniem): po zmianie jednej notatki commit zmienia dokładnie 1 węzeł i jego datę, pozostałe 66 bez zmian; przy pustym `wiki/` job kończy się błędem bez commita. Na GitHubie niesprawdzone.
NIEZWERYFIKOWANE: (a) filtr `paths: wiki/**` dla zmiany notatek (nie wolno mi zmieniać notatek; do sprawdzenia po pierwszym prawdziwym pushu notatek: czy pojawia się nowy przebieg); (b) zachowanie przy pushu właściciela w trakcie przebiegu (kod ma `pull --rebase`, niesprawdzone na GitHubie); (c) daty `modified` po późniejszych edycjach na GitHubie; (d) pobranie narzędzi po scaleniu PR #7 i ewentualnym usunięciu gałęzi (O14). Log zawiera ostrzeżenie GitHuba o wycofywaniu Node 20 dla `actions/checkout@v4` (tylko ostrzeżenie).
Pozycje otwarte:
- O13. ROZWIĄZANE: zapis do prywatnego repo uzyskany za zgodą właściciela (droga A), workflow wgrany i uruchomiony.
- O14. Przypięcie do SHA 549449d zamiast `main`: po scaleniu PR #7 zostawić (bezpieczniej) lub przepiąć na SHA ze scalenia. Decyduje właściciel. Nie blokuje.
- O15. Miejsce wyników: `graph/GRAPH-AUTO.json` (zgodnie z etapem 1) i `graph/INDEX-AUTO.txt` (domyślna decyzja, plan nie wskazuje miejsca). Do uzgodnienia przy etapie 4. Nie blokuje.
- O16. (pkt 4 etapu 3) Strona-artefakt nadal nie odczyta `GRAPH-AUTO.json` z GitHuba (wynik etapu 1.5); graf dla strony nadal produkuje telefon na Dysk, cron zostaje. Graf z GitHuba jest na razie kopią, nie źródłem dla strony.
- O17. Do sprawdzenia przy pierwszym prawdziwym pushu notatek (niezweryfikowane a-c powyżej) przez właściciela lub orkiestratora. Nie blokuje etapu 4.

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
