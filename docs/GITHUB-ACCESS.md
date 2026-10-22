# Jak sesja Claude pracuje na repozytoriach GitHub (zweryfikowane praktycznie 22.10.2026)

Kontekst: ten opis powstał w czacie z aplikacji mobilnej Claude (sesja z narzędziami chmurowymi). Zapis do prywatnego repo `simontg/Brain-Obsydian-NOTES` i do publicznego `simontg/brain-obsydian` przeszedł (commit, push, usunięcie pliku, weryfikacja na serwerze).

## Mechanizm (NIE jest to skill)
1. Narzędzia MCP serwera `claude-code-remote` (`mcp__claude-code-remote__*`):
   - `list_repos {query?}` — lista repo konta: `full_name`, `visibility`, `can_push`, `pushed_at`. To jeszcze nie jest dostęp z sesji.
   - `add_repo {owner, repo, access: "read"|"push"}` — dodaje repo do zakresu SESJI. Do zapisu użyj `access: "push"`. Odpowiedź zawiera polecenie klonowania i katalog docelowy `/home/claude/<repo>`. Jedno wywołanie = jedno repo; test z dwoma repo w jednej sesji przeszedł.
   - `register_repo_root {owner, repo, directory}` — wołaj PO udanym klonie; sesja wczyta CLAUDE.md, skille i pluginy z repo.
2. Zwykły `git` w powłoce. Ruch HTTPS idzie przez proxy sesji (`HTTPS_PROXY`, CA: `/root/.ccr/ca-bundle.crt`). Uwierzytelnienie robi proxy, tokenu w sesji nie widać i nie trzeba go podawać. Nie wyłączaj weryfikacji TLS. Dostępne są też `gh`, `gcloud`, `gsutil`, `bq` skonfigurowane pod proxy (`gh` nie był testowany).
3. Za tym stoi integracja GitHub w ustawieniach claude.ai (Settings → Connectors). Przy błędzie autoryzacji z `add_repo` właściciel musi tam połączyć GitHub lub nadać dostęp do repo. Szczegóły mechanizmu: nie wiem (wynika z opisu narzędzia, nie z testu).

## Przepis
1. `list_repos {query:"brain"}` — sprawdź `can_push: true` i `visibility`.
2. `add_repo {owner:"simontg", repo:"Brain-Obsydian-NOTES", access:"push"}`.
3. Klonuj JEDNYM poleceniem, inline, z dużym timeoutem (ok. 10 min): `git clone --depth 1 https://github.com/simontg/<repo> /home/claude/<repo>`.
   Nie klonuj równolegle: proxy dopuszcza max 2 równoległe operacje smart-HTTP na repo, kolejna daje HTTP 429 (odczekaj 10 s, ponów RAZ). Jeśli katalog już istnieje, nie usuwaj go odruchowo: `git -C <katalog> rev-parse HEAD`.
4. `register_repo_root {owner, repo, directory:"/home/claude/<repo>"}`.
5. Zapis: lokalnie `git config user.email` i `user.name`, potem `git add`, `git commit`, `git push origin main`. Przed pushem na niepustym repo zrób `git fetch origin main` (inaczej push ze starego płytkiego klona może dać HTTP 413). Dodawaj stopki commitów z przypomnienia systemowego sesji, jeśli się pojawiło.
6. Weryfikacja ZAWSZE: `git ls-remote origin main` i `git log --oneline`.
7. Usunięcie pliku = `git rm` + commit + push (historia zostaje).

## Zaobserwowane pułapki
- Świeże repo było puste ("cloned an empty repository"): to normalne, pierwszy push tworzy gałąź `main`.
- W pustym repo `git fetch` + `git merge --ff-only origin/main` kończy się błędem "not something we can merge" (brak zdalnej gałęzi). Pomiń to przy pierwszym commicie.
- Po zmianie wielkości liter w nazwie GitHub pisze "This repository moved". Push działa, ale używaj oryginalnej pisowni: `Brain-Obsydian-NOTES`.
- Zapis tylko do repo dodanych przez `add_repo` w tej sesji. W razie odmowy (polityka organizacji / brak aplikacji GitHub) przekaż właścicielowi dokładny komunikat i nie ponawiaj.
- `brain-obsydian` jest PUBLICZNE: nic osobistego tam nie commituj. Notatki tylko do prywatnego `Brain-Obsydian-NOTES`.

## Niezweryfikowane (sprawdź w etapie 0 planu)
- Czy zadanie Claude Code uruchamiane jako osobna sesja w chmurze (zaplanowane lub ręczne) ma te same narzędzia `claude-code-remote` i te same prawa. Test: `list_repos`, `add_repo` na prywatnym repo z `access:"push"`, commit syntetycznego pliku testowego, `ls-remote`, usunięcie pliku.
- Czy `gh` działa przez proxy tak samo jak `git`.
- Limity wielkości pushu i czas klonowania dużych repo (obecne repo są małe).
