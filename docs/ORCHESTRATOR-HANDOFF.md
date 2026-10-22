# Brain obsydian: podsumowanie projektu i handoff (stan: 22.10.2026, po migracji)

Projekt: przeniesienie osobistej bazy wiedzy (wiki) z Dysku Google na GitHuba, z automatycznym grafem notatek na stronie internetowej. Migracja jest ZAKOŃCZONA (etapy 0-5 zamknięte 22.10.2026). Ten plik zastępuje handoffy orkiestratora części 1 i 2. Szczegóły i dowody każdego etapu: `PLAN.md` (sekcje „Etap N: WYNIKI”). Repo jest publiczne: tu nie ma tytułów notatek, treści ani sekretów.

## 1. Jak to działa teraz
- **Notatki** (źródło prawdy): prywatne repo `simontg/Brain-Obsydian-NOTES`, katalog `wiki/`, jeden plik `.txt` na notatkę (UTF-8 z BOM, końce linii CRLF, nazwa pliku = tytuł; dwukropki w nazwach zostają). 67 plików w chwili przełączenia: 5 hubów, 3 pliki pomocnicze (HOT, INDEX, LOG) i 59 notatek (jedna należy do dwóch hubów).
- **Obsługa wiki**: skill konta `wiki-brain-git` w wersji 1.1, polecenia „wiki save”, „zapisz do wiki”, „wiki ask <pytanie>”, „wiki lint” (działają też z dopiskiem „git”). Działa w zwykłym czacie Claude (telefon) i w sesjach Claude Code. Czytanie: HOT, potem INDEX, potem hub, potem wyszukiwarka BM25, na końcu pojedyncze notatki. Zapis: jeden commit na polecenie, prosto na `main`, przed pushem `pull --rebase`, nigdy force-push, nigdy kasowanie (wycofanie notatki tylko przez przeniesienie do `archiwum/` na polecenie właściciela).
- **Stary skill** `wiki-brain` (Dysk): wyłączony w ustawieniach, nie skasowany.
- **Graf i indeks**: każdy push zmieniający `wiki/` uruchamia Action `generate-graph-index` w repo notatek. Action pobiera skrypty `tools/wiki_graph.py` i `tools/wiki_index.py` z tego repo (przypięte do konkretnego commitu, `TOOLS_REF`), zapisuje `graph/GRAPH-AUTO.json` i `graph/INDEX-AUTO.txt` w repo notatek, szyfruje graf i wypycha `graph/graph.enc.json` do tego repo. Workflow `pages` (plik `pilot-graph.yml`) publikuje stronę.
- **Strona grafu**: https://simontg.github.io/brain-obsydian/ . Graf zaszyfrowany (AES-256-GCM, PBKDF2-SHA256, 600 000 iteracji, losowa sól i IV), odszyfrowywany w przeglądarce hasłem. Hasło wpisuje się raz na kartę przeglądarki. Aktualizacja około 40-60 s po zapisie notatki. Przycisk „Otwórz na GitHubie” prowadzi do pliku notatki w prywatnym repo (wymaga zalogowania).
- **Dysk Google**: kopia zapasowa tylko do odczytu, zamrożona na stanie z 22.10.2026. Nic tam nie zapisywać i nic nie kasować.
- **Telefon (Termux)**: cron grafu i indeksu wyłączony (usunięte tylko 2 linie; kopia `~/crontab-backup-etap5.txt`, przywrócenie `crontab ~/crontab-backup-etap5.txt`). Klon repo notatek w `~/notes-git`, zalogowany tokenem tylko do repo notatek.

## 2. Sekrety i tokeny (wartości zna tylko właściciel)
- Token 1 (telefon, `~/notes-git`): fine-grained, tylko `Brain-Obsydian-NOTES`.
- Token 2: sekret Actions `PUBLIC_REPO_TOKEN` w repo notatek; fine-grained, tylko `brain-obsydian`, Contents: Read and write; bez daty wygaśnięcia. Pozwala zmienić także kod strony, więc przy podejrzeniu wycieku: unieważnić w ustawieniach GitHuba, wygenerować nowy, wpisać do sekretu.
- `GRAPH_PASSWORD`: sekret Actions w repo notatek, hasło do grafu (co najmniej 20 znaków; workflow odmawia publikacji krótszego). Zaszyfrowane wersje grafu zostają na zawsze w publicznej historii gita, więc bezpieczeństwo treści zależy wyłącznie od siły hasła.
- `PILOT_PASSWORD` (sekret z pilotażu): usunięty przez właściciela 22.10.2026.
- Agent nigdy nie widzi ani nie wypisuje wartości sekretów. Workflow ma tryb kontrolny `check_only` (ręczne uruchomienie), który sprawdza oba sekrety bez ich wypisywania.

## 3. Przebieg migracji (22.10.2026)
- Etap 0: analiza tylko do odczytu.
- Etap 1: decyzje właściciela (GitHub zamiast Dysku, repo prywatne na notatki, publiczne na kod).
- Etap 1.5: pilotaż na danych syntetycznych: szyfrowany graf na Pages, zapis do repo z telefonu i z sesji. Wynik: artefakt Claude nie pobierze danych z GitHuba (stąd później strona na Pages).
- Etap 2: eksport 67 notatek z Dysku do repo notatek (rclone, bez zmian treści).
- Etap 3a-3c: skrypty grafu i indeksu BM25 (Python stdlib, testy), Action w repo notatek.
- Etap 3d: zaszyfrowany prawdziwy graf na Pages, test koniec-do-końca (sztuczna notatka dodana i usunięta).
- Etap 4: skill `wiki-brain-git` (wariant gitowy dotychczasowego `wiki-brain`), testy na repo syntetycznym i tylko do odczytu na prawdziwym.
- Etap 5: szybkie przełączenie (bez kilkudniowej pracy równoległej): kontrola zgodności Dysk = repo (67 = 67 tytułów, 305 = 305 powiązań, lint 0), testy zapisu w Claude Code i w czacie na telefonie, skill 1.1 reagujący na zwykłe „wiki …”, wyłączenie starego skilla i crona.

## 4. Sprawy otwarte (nic nie blokuje codziennego używania)
1. Pierwszy prawdziwy „wiki save” (bez słowa „git”): sprawdzić, że czat dołącza repo notatek, a nie Dysk; odpowiedź podaje skrót commitu; w repo pojawia się commit bota; licznik notatek na stronie rośnie, jeśli doszła notatka. Sprawdzone dotąd tylko „wiki ask” i „wiki git save”.
2. Widok „Czas” na stronie: czy nowe zapisy mają właściwe daty. Stare notatki mają jedną wspólną datę z eksportu (zaakceptowane, O6).
3. O22: porządki znalezione przez lint (2 wiersze INDEX zlepione w jedną linię, 7 notatek z więcej niż 5 wpisami `Related:`); tylko za zgodą właściciela, przez „wiki lint”.
4. O14: skrypty przypięte do konkretnego commitu (`TOOLS_REF`); przy zmianie skryptów najpierw przegląd, potem podbicie `TOOLS_REF` w workflow repo notatek.
5. Niezmierzone: koszt tokenów jednego „wiki save”.

## 5. Jak pracować dalej (dla następnej sesji)
- Zmiana kodu strony lub skryptów: w tym repo, przez gałąź i PR; dane testowe tylko syntetyczne; test strony Playwrightem (1280x780 i 392x820, jasny i ciemny, bez błędów strony). Przed kodem skill `lazy-senior` (zasada z CLAUDE.md).
- Zmiana skilla: nowy `SKILL.md` w repo notatek (`.claude/skills/wiki-brain-git/`), instalacja przez właściciela kartą w zwykłym czacie.
- Dostęp sesji do repo notatek: `add_repo` (docs/GITHUB-ACCESS.md). Klasyfikator uprawnień sesji zwykle odrzuca `add_repo` z zapisem (a czasem nawet z odczytem); właściciel musi wtedy napisać wyraźną zgodę w TEJ sesji. Najlepiej wpisać ją od razu na starcie okna, np. „Zgadzam się na add_repo simontg/Brain-Obsydian-NOTES z access push w tej sesji”.
- Praca etapami (gdyby wróciła): jedno okno na zadanie, raport po polsku w formacie z CLAUDE.md, orkiestrator sprawdza niezależnie i scala PR-y zwykłym merge commitem z pełnym `expectedHeadSha`. Okna mogą wysyłać orkiestratorowi wiadomości (`send_message`); orkiestrator może sam uruchomić okno (`create_session`).

## 6. Wnioski z przebiegu
- Pomyłka okien: zgoda wpisana w niewłaściwej sesji nie działa. Każde okno ma swoją nazwę i link; podawać je właścicielowi przy każdej prośbie.
- Pierwsza wartość `PUBLIC_REPO_TOKEN` była nieprawidłowa (GitHub odpowiadał 401); pomogło wygenerowanie tokenu od nowa i tryb `check_only`.
- Hasło z pilotażu i hasło prawdziwego grafu to dwa różne hasła; po publikacji prawdziwego grafu działa tylko `GRAPH_PASSWORD`.
- Narzędzie Edit zachowuje BOM i CRLF; Write zmienia końce linii na LF, dlatego skill używa Edit dla istniejących notatek i poprawki FIX dla nowych.
- Klasyfikator uprawnień potrafi zablokować także odczyt stanu repo po scaleniu PR; wtedy potwierdzenie przychodzi z narzędzia GitHuba albo od okna etapu.
