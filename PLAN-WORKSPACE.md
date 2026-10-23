# PLAN-WORKSPACE: wspólny „folder roboczy” na GitHubie (etapowo, z punktami stopu)

Kontynuacja migracji wiki (PLAN.md, etapy 0-5 zamknięte 22.10.2026). Repo jest PUBLICZNE: w tym pliku tylko liczby i nazwy techniczne, bez nazw projektów, tytułów, treści i identyfikatorów plików z Dysku.

## Cel
Projekty, źródła i materiały, które dziś leżą w folderze roboczym na Dysku Google (folder z projektami i skillami), mają trafić do prywatnego repo `simontg/Brain-Obsydian-NOTES` obok `wiki/`, w jednej strukturze dostępnej dla każdej sesji Claude (czat i Claude Code w chmurze) do odczytu i zapisu. Skille korzystające z Dysku dostają jasną zasadę: domyślnie repo, Dysk tylko na wyraźne polecenie.

## Decyzje właściciela (23.10.2026, z orkiestratorem)
- W1. Folder roboczy = repo notatek `Brain-Obsydian-NOTES` (nowe foldery obok `wiki/`), a nie osobne repo. Graf i Action czytają tylko `wiki/`, więc działają bez zmian.
- W2. Zakres przeniesienia: najpierw inwentaryzacja tylko do odczytu, potem właściciel wybiera, co idzie.
- W3. Po przeniesieniu GitHub jest źródłem prawdy, Dysk kopią tylko do odczytu (jak przy wiki). `write-to-gdrive` zostaje, używany tylko na wyraźne polecenie. Nic na Dysku nie kasować.
- W4. Skille: jeden nowy skill `write-to-github` (wspólny przepis zapisu i odczytu w repo) plus krótka zmiana w `read-whole`, `handoff`, `skill-suggestions` (domyślnie repo, Dysk na polecenie). Bez osobnych gitowych kopii każdego skilla.
- W5. Claude Code na komputerze właściciela (VS Code) zostaje bez dostępu do repo (decyzja „A” z 23.10.2026); lokalny `~/.claude/CLAUDE.md` odsyła do czatu albo chmury.

## Ustalone fakty o dostępie (dokumentacja środowiska, 23.10.2026)
- Sesja Claude Code w chmurze uruchomiona z wybranym repo ma je od startu (odczyt i zapis) bez `add_repo` i bez zgody wpisywanej w czacie.
- Zwykły czat dołącza repo przez `add_repo` (działa, etap 5 PLAN.md).
- Reguły zezwoleń w `.claude/settings.json` repo zmniejszają liczbę pytań; czyta je tylko sesja z jednym repo.

## Etapy (każdy = osobne okno; raport w formacie z CLAUDE.md; STOP do zgody właściciela)
### R0. Inwentaryzacja folderu roboczego na Dysku (tylko odczyt)
- Lista podfolderów i plików z typem (Dokument Google, PDF, obraz, inne), rozmiarem i datą zmiany; zapis listy w repo notatek (`projekty/_inwentaryzacja.md`, prywatnie). Do tego pliku w publicznym repo trafiają tylko liczby.
- Zaliczone gdy: liczby plików i rozmiary zsumowane per typ; wskazane pliki większe niż 50 MB; nic na Dysku nie zmienione.
- Właściciel zaznacza w liście, co przenosimy.
### R1. Struktura i konwencje repo
- Foldery: `projekty/<nazwa>/`, `zrodla/`, `skille/` (kopie SKILL.md), `archiwum/` (już jest), `wiki/` bez zmian. `README.md` repo z zasadami: nazwy plików, format (Markdown/tekst, UTF-8), duże pliki, zakaz kasowania (tylko `archiwum/`), jeden commit na zmianę, `pull --rebase`, bez force-push.
- `.claude/settings.json` z regułami zezwoleń dla gita w tym repo.
- Zaliczone gdy: struktura na `main`, Action grafu nie uruchomiony przez zmianę poza `wiki/` albo zielony, graf bez zmian (liczba węzłów).
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
