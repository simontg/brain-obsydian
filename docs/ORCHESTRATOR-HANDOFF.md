# Handoff orkiestratora: część 1 -> część 2 (stan: 22.10.2026)

Nowy orkiestrator: przeczytaj najpierw CLAUDE.md, PLAN.md, docs/GITHUB-ACCESS.md. Ten plik to tylko skrót stanu i rutyna pracy. Żadnych danych osobistych ani sekretów (repo jest publiczne).

## Rola
Orkiestrator nie wykonuje prac etapów. Przyjmuje raport okna etapu, sprawdza wynik NIEZALEŻNIE (nie ufa raportowi), scala PR-y z wynikami i przygotowuje następne okno: prompt do wklejenia, model, effort, oczekiwania, a gdy właściciel ma coś zrobić ręcznie (Termux) dokładny schemat kopiuj-wklej. Każdy etap = nowe okno.

## Stan etapów (wg PLAN.md na main)
- Etapy 0, 1, 1.5, 2, 3a, 3b, 3c, 4: zamknięte (2, 3, 4 "z uwagami"; wyniki w sekcjach "Etap N: WYNIKI").
- Etap 3d (graf z GitHuba na Pages, szyfrowany): DO ZROBIENIA, opisany w PLAN.md. Najpierw właściciel podejmuje D1 (hasło, długa losowa fraza) i D2 (token fine-grained tylko do brain-obsydian, Contents RW; sekrety zakłada właściciel sam, agent nigdy nie widzi wartości). Okno 3d: Opus 5.5, effort high (propozycja).
- Etap 5 (przełączenie, wyłączenie crona w Termuxie, Dysk jako kopia): dopiero po 3d, za zgodą właściciela. Blokują go O19 (zmiana opisu skilla na zwykłe "wiki ...") i O23 (synchronizacja Dysk -> repo w pracy równoległej).
- Ostatnie scalenia na main: #8 (3d w planie), #9 (wyniki etapu 4, e88585c).

## Najbliższe kroki
1. Właściciel instaluje skill `wiki-brain-git` kartą z pliku `.claude/skills/wiki-brain-git/SKILL.md` w prywatnym repo notatek (commit 2bbdfa8) i robi test akceptacyjny "wiki git ask" w nowej sesji (O20). Do tego czasu "wiki git save" na prawdziwych notatkach nie używać.
2. Właściciel sprawdza, czy Action w repo notatek uruchamia się po zmianie notatki (O17, filtr wiki/**); najprościej ręcznie "Run workflow" w aplikacji GitHub albo przy pierwszym prawdziwym zapisie.
3. Etap 3d (po D1 i D2).
4. Decyzje właściciela przed etapem 5: O18 (stara kopia wiki-brain 2.2 na Dysku), O19, O22 (poprawki lintu), O23, O7 (przycisk "Otwórz" na stronie), O10/O14 wg PLAN.md.

## Rutyna sprawdzania raportu etapu (kopiuj)
- Repo notatek (prywatne): klon w /home/user/brain-obsydian-notes, dołączone przez add_repo (read). `git fetch origin main` (w tym klonie czasem trzeba `git fetch origin main` bez `-q`, potem FETCH_HEAD). Sprawdź hash commitu, liczbę plików w wiki/ (stan: 67), `git diff --stat <commit> FETCH_HEAD -- wiki` (puste = notatki nietknięte), wielkość i nagłówek SKILL.md.
- PR: `pull_request_read` get_files; szukaj prawdziwych tytułów notatek, danych z grafu, tokenów (nie mają prawa być w publicznym repo); sprawdź, czy raport nie przypisuje właścicielowi decyzji, której nie podjął (przypadek z etapu 3: "Etap 4 pomijam, tak jak chcesz" było nieprawdą).
- Scalanie: oznacz PR jako gotowy (update_pull_request draft=false), potem merge_pull_request z PEŁNYM 40-znakowym expectedHeadSha. PR z commitem przypiętym w workflow (TOOLS_REF) scalaj zwykłym merge commitem, nie squashem. Błąd 502 jest przejściowy: najpierw sprawdź `git ls-remote origin refs/heads/main`, czy scalenie nie przeszło.
- Gałąź robocza orkiestratora: ccr-d454dec2-3pxl3a, po każdym scaleniu restart z origin/main (`git checkout -B ... origin/main`, push --force-with-lease). Okna etapów robią własne gałęzie.

## Preferencje i ustalenia właściciela
- Po polsku, zwięźle, bez zastrzeżeń; "nigdy nie zmyślaj, powiedz że nie wiesz"; oznaczaj zweryfikowane vs niezweryfikowane.
- Przy każdym nowym oknie: prompt, model, effort, oczekiwania. Zalecane modele: Haiku (mechaniczna walidacja), Sonnet 5.5 high (kod, porównania), Opus 5.5 high (projekt, bezpieczeństwo, skille).
- Zrzut do Termuxa: dokładny schemat kopiuj-wklej, po jednym kroku; właściciel odsyła wynik. Tokeny i hasła nigdy do czatu.
- Dysk Google: nic nie kasować; cron w Termuxie nie ruszać do etapu 5. Etap 4 (skille) nie jest pomijany (zrobiony).
- Skille konta zmienia tylko właściciel kartą propose_skills.
- Termux właściciela: klon repo notatek w ~/notes-git, dane logowania GitHub zapisane przez credential.helper store (token fine-grained tylko do Brain-Obsydian-NOTES; wartości nie znamy i nie potrzebujemy).
- Orkiestrator zmienia nazwę sesji na "Etap 0 - orkiestrator część N".

## Znane pułapki
- Narzędzia GitHub w sesji bywają chwilowo niedostępne (reconnect); ponów po chwili.
- add_repo zwraca nazwę repo małymi literami; klon i push działają.
- Pliki notatek mają BOM + CRLF i nazwy z dwukropkiem (zostają, decyzja właściciela).
