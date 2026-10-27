# PLAN-WORKSPACE: wspólny „folder roboczy” na GitHubie (etapowo, z punktami stopu)

Kontynuacja migracji wiki (PLAN.md, etapy 0-5 zamknięte 22.10.2026). Repo jest PUBLICZNE: w tym pliku tylko liczby i nazwy techniczne, bez nazw projektów, tytułów, treści i identyfikatorów plików z Dysku.

## Cel
Projekty, źródła i materiały, które dziś leżą w folderze roboczym na Dysku Google (folder z projektami i skillami), mają trafić do prywatnego repo `simontg/Brain-Obsydian-NOTES` obok `wiki/`, w jednej strukturze dostępnej dla każdej sesji Claude (czat i Claude Code w chmurze) do odczytu i zapisu. Skille korzystające z Dysku dostają jasną zasadę: domyślnie repo, Dysk tylko na wyraźne polecenie.

## Decyzje właściciela (23.10.2026, z orkiestratorem)
- W1. Folder roboczy = repo notatek `Brain-Obsydian-NOTES` (nowe foldery obok `wiki/`), a nie osobne repo. Graf i Action czytają tylko `wiki/`, więc działają bez zmian.
- W2. Zakres przeniesienia: najpierw inwentaryzacja tylko do odczytu, potem właściciel wybiera, co idzie.
- W3. Po przeniesieniu GitHub jest źródłem prawdy, Dysk kopią tylko do odczytu (jak przy wiki). `write-to-gdrive` zostaje, używany tylko na wyraźne polecenie. Nic na Dysku nie kasować.
- W4. Skille: jeden nowy skill `write-to-github` (wspólny przepis zapisu i odczytu w repo) plus krótka zmiana w `read-whole`, `handoff`, `skill-suggestions` (domyślnie repo, Dysk na polecenie). Bez osobnych gitowych kopii każdego skilla.
- W5. (zmiana 23.10.2026, zastępuje decyzję „A”) Stały, swobodny dostęp do odczytu i zapisu dla agentów na koncie właściciela we WSZYSTKICH miejscach: Claude Code w chmurze, zwykły czat (telefon) i Claude Code na komputerze (VS Code). Jak najmniej pytań o zgodę. W zamian zabezpieczenie po stronie GitHuba: zakaz force-push i usuwania `main` w repo notatek (historia zostaje, każdą zmianę da się cofnąć). Uwaga: na obecnym planie GitHub tej blokady nie egzekwuje, patrz W14.
- W13. (23.10.2026; wcześniej w PR #21 jako „W6”; DO POTWIERDZENIA przez właściciela, który 23.10.2026 wstrzymał tryb komputera i nie jest pewien WSL) Komputer (Windows, VS Code): propozycja: Claude Code działa w WSL (Linux w Windows), nie natywnie w Windows. Powód: 66 z 69 plików w `wiki/` ma w nazwie dwukropek, którego Windows nie dopuszcza w nazwach plików, więc natywny klon na Windows nie wypakuje notatek; zmiany nazw notatek nie robimy. Właściciel potwierdził 23.10.2026, że komputer przez WSL już czyta i zapisuje repo notatek („wiki save” działa).
- W14. (23.10.2026, po R1) Ochrona `main` na GitHubie: ruleset (blokada force-push i usuwania) utworzony, ale GitHub go nie egzekwuje w prywatnym repo na obecnym planie (komunikat GitHuba wymaga konta organizacji Team). Decyzja właściciela: A, zostaje bez ochrony GitHuba. Zabezpieczenie: reguły `deny` w `.claude/settings.json` repo notatek (działają tylko w Claude Code: chmura i komputer; nie w czacie ani przy ręcznym gicie), zasada „nigdy nie kasuj, tylko `archiwum/`”, historia gita.

## Zrobione poza etapami (23.10.2026)
- Repo notatek: `.gitattributes` z `* -text` (commit 583981d): git nie zmienia końców linii w żadnym klonie (notatki zostają UTF-8 z BOM i CRLF). Przy dodaniu `git add --renormalize .` nie zmienił żadnego pliku.

## Ustalone fakty o dostępie (dokumentacja środowiska, 23.10.2026)
- Sesja Claude Code w chmurze uruchomiona z wybranym repo ma je od startu (odczyt i zapis) bez `add_repo` i bez zgody wpisywanej w czacie.
- Zwykły czat dołącza repo przez `add_repo` (działa, etap 5 PLAN.md).
- Reguły zezwoleń w `.claude/settings.json` repo zmniejszają liczbę pytań; czyta je tylko sesja z jednym repo.

## Etapy (każdy = osobne okno; raport w formacie z CLAUDE.md; STOP do zgody właściciela)
### R0. Inwentaryzacja folderu roboczego na Dysku (tylko odczyt)
- Lista podfolderów i plików z typem (Dokument Google, PDF, obraz, inne), rozmiarem i datą zmiany; zapis listy w repo notatek (`projekty/_inwentaryzacja.md`, prywatnie). Do tego pliku w publicznym repo trafiają tylko liczby.
- Zaliczone gdy: liczby plików i rozmiary zsumowane per typ; wskazane pliki większe niż 50 MB; nic na Dysku nie zmienione.
- Właściciel zaznacza w liście, co przenosimy.
### R1. Struktura, konwencje i dostęp
- Foldery: `projekty/<nazwa>/`, `zrodla/`, `skille/` (kopie SKILL.md), `archiwum/` (już jest), `wiki/` bez zmian. `README.md` repo z zasadami: nazwy plików, format (Markdown/tekst, UTF-8), duże pliki, zakaz kasowania (tylko `archiwum/`), jeden commit na zmianę, `pull --rebase`, bez force-push.
- `.claude/settings.json` z regułami zezwoleń dla gita w tym repo.
- Dostęp, trzy tryby, wspólne dla wszystkich skilli (opisane raz, w `write-to-github`):
  (a) Claude Code w chmurze: sesja startuje z repo notatek wybranym (bez `add_repo`); środowisko chmurowe z tym repo jako domyślnym, jeśli ustawienia na to pozwalają (do sprawdzenia);
  (b) zwykły czat: `add_repo` robi skill;
  (c) komputer: WSL (W13). Klon repo notatek w systemie plików Linuksa (`~/...`), NIE w `/mnt/c/...` (dwukropki); logowanie gita w WSL już działa (stan na 23.10.2026, ustawione przez właściciela); `python3` w WSL; reguły zezwoleń w `~/.claude/settings.json` w WSL. `~/.claude/CLAUDE.md` w WSL to inny plik niż w Windows. Skill `wiki-brain-git` (i `write-to-github`): gdy brak `add_repo`, a jest lokalny klon i działa git, praca na klonie (zawsze `pull --rebase` przed zmianą).
- Ochrona na GitHubie (właściciel, ustawienia repo notatek → Rules): blokada force-push i usuwania `main`. Wynik: nieegzekwowana na obecnym planie (W14); zamiast niej reguły `deny` w `.claude/settings.json`.
- Zaliczone gdy: struktura na `main`, Action grafu nie uruchomiony przez zmianę poza `wiki/` albo zielony, graf bez zmian (liczba węzłów); w każdym z trzech trybów nowa sesja czyta i zapisuje plik testowy w repo, a liczba pytań o zgodę jest zapisana (cel: zero w trybach a i c); reguły `deny` (force-push, usuwanie gałęzi, `git rm`) są w `.claude/settings.json` na `main` (zmiana 23.10.2026 zamiast „force-push odrzucony przez GitHub”, W14; próby force-push na `main` nie robimy).
### R2. Skill `write-to-github` i zmiany w trzech skillach
- `to-spec`, potem `lazy-senior`. Zasady jak w `wiki-brain-git` (Edit dla istniejących plików, znajdź przed utworzeniem, nigdy nie kasuj, jeden commit, `pull --rebase`, `ls-remote` = HEAD). Test na repo syntetycznym, potem jeden mały prawdziwy zapis.
- Nowe wersje `read-whole`, `handoff`, `skill-suggestions`: domyślnie repo, Dysk na wyraźne polecenie. Kopie wszystkich SKILL.md w `skille/`.
- Instalacja kartą przez właściciela w zwykłym czacie; test w czacie i w Claude Code w chmurze.
### R3. Przeniesienie wybranych materiałów
- Dokumenty Google jako tekst/Markdown (bez zmiany treści), pozostałe pliki bez zmian; pliki ponad 50 MB tylko po osobnej decyzji (historia gita trzyma je na zawsze; GitHub odrzuca pliki ponad 100 MB).
- Zaliczone gdy: liczby plików przeniesionych = zaznaczonych w R0; próbka porównana z oryginałem; nic na Dysku nie zmienione.
### R4. Przełączenie
- CLAUDE.md (tu i lokalny na komputerze), `docs/ORCHESTRATOR-HANDOFF.md`: repo źródłem prawdy dla projektów i źródeł, Dysk kopią. Test: nowa sesja czatu i Claude Code w chmurze czyta i zapisuje w `projekty/` bez Dysku.

## Ryzyka
- Historia gita jest trwała: nie wrzucać sekretów ani danych innych osób; usunięcie pliku nie usuwa go z historii.
- Duże pliki binarne powiększają repo na zawsze.
- Każdy nowy skill to kolejna instalacja kartą przez właściciela.
- Swobodny zapis dla wielu agentów: błąd agenta trafia prosto na `main`. Zabezpieczenie: historia gita, reguły `deny` w Claude Code, zasada „nigdy nie kasuj, tylko `archiwum/`”. GitHub nie blokuje force-push (W14), więc błąd w czacie lub przy ręcznym gicie może przepisać `main`; odtworzenie tylko z innego klonu.
- Niesprawdzone: czy reguły zezwoleń w repo wyłączają pytania systemu bezpieczeństwa sesji chmurowej (np. o scalanie PR); części tych pytań nie da się wyłączyć z poziomu repo.
- Zapisane logowanie na komputerze daje każdemu programowi z dostępem do tego konta Windows zapis do repo notatek.

## R0: WYNIKI

STATUS: ZAMKNIĘTY (data 2026-10-23; tylko odczyt Dysku; lista szczegółowa w prywatnym repo notatek).

Liczby (rozmiar = pole fileSize z API; dla Dokumentów i Arkuszy Google wartość raportowana, niezweryfikowana):

| Folder | Typ | Pliki | Suma rozmiarów (B) |
|---|---|---|---|
| folder A | Dokument Google | 16 | 106518 |
| folder A | Arkusz Google | 5 | 6949 |
| folder A | PDF | 1 | 142016 |
| folder A | obraz (PNG) | 101 | 23895212 |
| folder A | Markdown | 24 | 114593 |
| folder A | Python | 3 | 19959 |
| folder A | JSON | 1 | 76628 |
| folder A | HTML | 1 | 28062 |
| folder A | CSV | 2 | 931 |
| folder A | TXT | 1 | 167 |
| folder A razem | | 155 | 24391035 |
| folder B | PDF | 18 | 66152850 |
| folder B | EPUB | 2 | 16172978 |
| folder B | ZIP | 3 | 8661 |
| folder B | JSON | 1 | 2394 |
| folder B razem | | 24 | 82336883 |

- Plików > 50 MB: 0 (folder A: 0, folder B: 0).
- Podfolder Wiki (w A, bez szczegółów): 68 plików, 180831 B.
- Skróty (shortcuts): 0.
- Weryfikacja „nic nie zmienione”: zapytanie Drive o pliki zmienione lub utworzone po starcie okna R0 (2026-10-23T05:09Z): 0 wyników (sprawdził orkiestrator); drugi przebieg okna częściowy, w sprawdzonej części bez różnic.

## Decyzje właściciela po R0 (23.10.2026, z orkiestratorem, grill-me)
- W6. Źródła w folderze B (artykuły i książki): wszystkie 20 plików (PDF/EPUB, ok. 82 MB, największy ok. 19 MB) do `zrodla/`, bez zmian.
- W7. Aktywny projekt badawczy (folder A, 121 plików, codzienny obieg: telefon wrzuca obrazy na Dysk, ocena w osobnym projekcie czatu Claude zapisuje wyniki na Dysk, telefon je odbiera) ZOSTAJE NA DYSKU do końca badania (ok. 02.2027). To wyjątek od W3: dla tego projektu Dysk pozostaje źródłem prawdy i nic w nim nie przenosić ani nie zmieniać. W repo notatek tylko notka-wskaźnik `projekty/<nazwa>/README.md` (bez plików projektu).
- W8. R2: zmiana skilli na „domyślnie repo” nie może dotknąć projektu czatu używanego do oceny w badaniu (oceniający ma być „ślepy”: bez wiki i innych dokumentów; instrukcja oceny jest wskazana tam po ID pliku na Dysku).
- W9. Pliki oznaczone na Dysku jako przestarzałe lub do usunięcia (17): nie przenosić.
- W10. Stary projekt grafu (9 plików; aktualne wersje są w tym repo): nie przenosić.
- W11. `skille/`: kopie z aktualnie zainstalowanych skilli konta (nowsze niż kopia na Dysku, która nie ma `wiki-brain-git`); kopii skilli z Dysku nie przenosić.
- W12. Pozostałe drobne pliki: przenieść; Dokumenty Google jako Markdown, Arkusze Google jako CSV, reszta bez zmian.
- Zakres R3 wynikający z W6-W12: 28 plików (folder A: 4, folder B: 24) + notka-wskaźnik z W7; skille z W11 w R2. Na Dysku nic się nie zmienia (tylko kopiowanie).

## R1: WYNIKI

STATUS: ZAMKNIĘTY Z UWAGAMI (23.10.2026; decyzja właściciela Q10A: tryb komputera wydzielony do R1c, nie blokuje R2 i R3; wyniki zapisał orkiestrator, decyzja Q11A).

Zweryfikowane przez orkiestratora:
- Struktura na `main` repo notatek (merge 14864b6 z PR #3 tamże): `README.md` z zasadami, `.claude/settings.json` (allow dla gita; deny: force-push, `-f`, `--force-with-lease`, `+ref`, `--delete`, `git rm`), `zrodla/`, `skille/`, `archiwum/` (już istniało).
- Action grafu nie uruchomił się po 14864b6 (filtr `paths: wiki/**`); graf: 69 węzłów, bez zmian.
- Tryb (a) Claude Code w chmurze (nowa sesja z aplikacji, tylko repo notatek): zapis i push na `main` (17e0d9b), bez `add_repo`, 0 okienek ze zgodą (liczył właściciel).
- Tryb (b) zwykły czat na telefonie: `add_repo` (push), zapis i push na `main` (8cef64f), 0 okienek ze zgodą (liczył właściciel).
- Pliki testowe przeniesione do `archiwum/` (855d1e1).
- Ochrona GitHuba: W14 (nieegzekwowana, decyzja A); kryterium zastąpione obecnością reguł `deny`; próby force-push nie było.

Uwagi / pozycje otwarte:
- R1c: tryb (c) komputer (VS Code, WSL czy Windows, W13 do potwierdzenia); właściciel; nie blokuje R2 i R3. Pierwsza próba była nieważna (folder bez gita).
- W obu testach zgoda była wpisana w poleceniu; liczba pytań przy zwykłym poleceniu bez takiej zgody do sprawdzenia w R2 (skill `write-to-github`).
- Nie sprawdzono, czy reguły `deny` z `.claude/settings.json` faktycznie blokują polecenia w sesji chmurowej.

## R3: WYNIKI

STATUS: ZAMKNIĘTY Z UWAGAMI (27.10.2026; wyniki zapisało okno R3; do weryfikacji przez orkiestratora).

Zrobione (tylko liczby; Dysk tylko odczyt, nic na nim nie zmieniono):
- Przeniesione pliki wg mapowania: 28 = 4 (dokumenty Google -> Markdown, folder A) + 3 (ZIP) + 1 (JSON) + 20 (PDF/EPUB). Plus notka-wskaźnik W7 (1 plik README, bez plików projektu).
- 20 plików źródłowych: skopiowane rclone przez właściciela na telefonie, `main` repo notatek d0e364e. Suma rozmiarów 20 plików = 82325828 B (równa sumie z R0; 82336883 B z zadania = cały folder B, 24 pliki, w tym 4 małe po 11055 B).
- `rclone check --one-way` dla `zrodla/`: 0 różnic, 21 zgodnych, 1 hash niesprawdzalny (który plik: nie wiem).
- ZIP (3) i JSON (1): `rclone check --download`, 0 różnic (3 zgodne ZIP, 1 zgodny JSON), bajt w bajt. 2 ZIP skopiowane rclone na `main` (d0e364e); 1 ZIP, JSON, 4 Markdown i notka są w draft PR #4 w repo notatek (head c37c35d), nie scalone.
- Action grafu: brak runu po pushu d0e364e (ostatni run z 23.10.2026).

Uwagi / pozycje otwarte:
- R3-U1: w folderze źródeł na Dysku jest 21 plików, nie 20 (1 plik .docx spoza R0, 8973 B, pojawił się po inwentaryzacji); rclone skopiował go do `zrodla/` (razem 21 plików + .gitkeep). Zostawić czy `git mv` do `archiwum/`: decyduje właściciel z orkiestratorem; nie blokuje.
- R3-U2: 4 pliki Markdown z dokumentów Google (eksport konektorem, `\-`/`\#` z eksportu zostawione) nie mają porównania z Dyskiem sumą kontrolną; tylko podwójne niezależne przepisanie; nie blokuje.
- R3-U3: PR #4 w repo notatek (draft) czeka na scalenie przez orkiestratora.

## R2: zadania (zatwierdzone przez właściciela 27.10.2026, skill to-tickets)
Każde zadanie = osobne okno; raport w formacie z CLAUDE.md; scala orkiestrator. Kolejność: 1 i 2 równolegle; 3 po 2; 4 i 5 równolegle po 3; 6 po 1, 4, 5.
1. R2.1 Kopie skilli w repo. Czeka na: nic. Daje: w `skille/<nazwa>/` kopie skilli konta autorstwa właściciela lub przerobionych przez niego (W11); wbudowane skille Anthropic nie są kopiowane, tylko wypisane w raporcie. Zaliczone gdy: liczba kopii = liczba takich skilli; treść bajt w bajt jak w zainstalowanej wersji.
2. R2.2 Specyfikacja `write-to-github` (`to-spec`). Czeka na: nic. Daje: zatwierdzona przez właściciela specyfikacja: wyzwalacze, dostęp (chmura: repo w sesji; czat: `add_repo`; komputer: później, R1c), zasady zapisu (znajdź przed utworzeniem, Edit dla istniejących, nigdy nie kasuj, jeden commit, `pull --rebase`, sprawdzenie `ls-remote`), duże pliki, wyjątek W8. Ustala też, jakim narzędziem projekt oceny w badaniu zapisuje dziś na Dysk.
3. R2.3 Skill `write-to-github`: budowa, testy, instalacja. Czeka na: 2. Zaliczone gdy: test na repo syntetycznym i jeden mały prawdziwy zapis; zainstalowany kartą; test w czacie na telefonie bez zgody wpisanej w poleceniu (liczba okienek zapisana) i w sesji w chmurze; sprawdzone, czy reguły `deny` blokują polecenia w chmurze. Bez testów w projekcie oceny (W8).
4. R2.4 `read-whole` domyślnie na repo. Czeka na: 3. Daje: źródła z `zrodla/`, READING-LOG w repo jako Markdown (przeniesienie obecnego dziennika z Dysku, domyka R3-U1), Dysk tylko na wyraźne polecenie, wyjątek W8.
5. R2.5 `handoff` i `skill-suggestions` domyślnie na repo. Czeka na: 3. Daje: notatka przekazania w folderze projektu w repo; podpowiedź `write-to-github` zamiast `write-to-gdrive`; wyjątek W8.
6. R2.6 Domknięcie R2. Czeka na: 1, 4, 5. Daje: odświeżone kopie zmienionych skilli w `skille/`, sekcja „R2: WYNIKI”.
