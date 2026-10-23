# PLAN-WORKSPACE: wspólny „folder roboczy” na GitHubie (etapowo, z punktami stopu)

Kontynuacja migracji wiki (PLAN.md, etapy 0-5 zamknięte 22.10.2026). Repo jest PUBLICZNE: w tym pliku tylko liczby i nazwy techniczne, bez nazw projektów, tytułów, treści i identyfikatorów plików z Dysku.

## Cel
Projekty, źródła i materiały, które dziś leżą w folderze roboczym na Dysku Google (folder z projektami i skillami), mają trafić do prywatnego repo `simontg/Brain-Obsydian-NOTES` obok `wiki/`, w jednej strukturze dostępnej dla każdej sesji Claude (czat i Claude Code w chmurze) do odczytu i zapisu. Skille korzystające z Dysku dostają jasną zasadę: domyślnie repo, Dysk tylko na wyraźne polecenie.

## Decyzje właściciela (23.10.2026, z orkiestratorem)
- W1. Folder roboczy = repo notatek `Brain-Obsydian-NOTES` (nowe foldery obok `wiki/`), a nie osobne repo. Graf i Action czytają tylko `wiki/`, więc działają bez zmian.
- W2. Zakres przeniesienia: najpierw inwentaryzacja tylko do odczytu, potem właściciel wybiera, co idzie.
- W3. Po przeniesieniu GitHub jest źródłem prawdy, Dysk kopią tylko do odczytu (jak przy wiki). `write-to-gdrive` zostaje, używany tylko na wyraźne polecenie. Nic na Dysku nie kasować.
- W4. Skille: jeden nowy skill `write-to-github` (wspólny przepis zapisu i odczytu w repo) plus krótka zmiana w `read-whole`, `handoff`, `skill-suggestions` (domyślnie repo, Dysk na polecenie). Bez osobnych gitowych kopii każdego skilla.
- W5. (zmiana 23.10.2026, zastępuje decyzję „A”) Stały, swobodny dostęp do odczytu i zapisu dla agentów na koncie właściciela we WSZYSTKICH miejscach: Claude Code w chmurze, zwykły czat (telefon) i Claude Code na komputerze (VS Code). Jak najmniej pytań o zgodę. W zamian zabezpieczenie po stronie GitHuba: zakaz force-push i usuwania `main` w repo notatek (historia zostaje, każdą zmianę da się cofnąć).

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
  (c) komputer (VS Code): lokalny klon repo z zapisanym logowaniem (Git Credential Manager albo token fine-grained tylko do repo notatek), prawdziwy Python, reguły zezwoleń w `~/.claude/settings.json` właściciela; skille wykrywają lokalny klon, gdy brak `add_repo`. Lokalny `~/.claude/CLAUDE.md` przestaje odsyłać do chmury.
- Ochrona na GitHubie (właściciel, ustawienia repo notatek → Rules): blokada force-push i usuwania `main`.
- Zaliczone gdy: struktura na `main`, Action grafu nie uruchomiony przez zmianę poza `wiki/` albo zielony, graf bez zmian (liczba węzłów); w każdym z trzech trybów nowa sesja czyta i zapisuje plik testowy w repo, a liczba pytań o zgodę jest zapisana (cel: zero w trybach a i c); próba force-push na `main` odrzucona przez GitHub.
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
- Swobodny zapis dla wielu agentów: błąd agenta trafia prosto na `main`. Zabezpieczenie: historia gita, zakaz force-push i usuwania `main`, zasada „nigdy nie kasuj, tylko `archiwum/`”.
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
