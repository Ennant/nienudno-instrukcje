# Instrukcje dla tabletów – Nienudno Robotyka

Z tego repozytorium tablety z aplikacją **Nienudno Robotyka** same pobierają instrukcje PDF
(wystarczy, że są podłączone do Wi‑Fi). Nic nie trzeba robić na tabletach.

## Jak dodać lub podmienić instrukcję

1. Wejdź do folderu [`instrukcje`](instrukcje) i otwórz folder kategorii (albo utwórz nowy – nazwa folderu = nazwa kategorii w aplikacji).
2. Kliknij **Add file → Upload files**, przeciągnij PDF i kliknij **Commit changes**.
3. Po ok. 1–2 minutach plik jest na serwerze. Tablety pobiorą go przy najbliższym połączeniu z Wi‑Fi
   (albo od razu po stuknięciu ikony odświeżania w ekranie „Instrukcje”). Nowe pliki mają plakietkę **NOWE**.

* **Nazwa pliku = tytuł w aplikacji.** Numer na początku ustala kolejność i jest ukrywany:
  `01 Robot-ślimak.pdf` → „Robot-ślimak”. Podkreślenia zamieniają się na spacje.
* **Numer na początku nazwy folderu** ustala kolejność kategorii: `01 Modele WeDo 2.0`.
* **Usunięcie pliku** z repozytorium usuwa go też z tabletów.
* Przez stronę GitHuba można wgrać plik do 25 MB. Większe pliki wgrywa się przez GitHub Desktop / git.

## Aktualizacja aplikacji

W folderze `aplikacja/` leży plik APK i `release.json` z numerem wersji. Po podmianie tablety pobiorą
nową wersję same i poproszą o jedno stuknięcie „Zainstaluj”.

Adres dla tabletów: `https://ennant.github.io/nienudno-instrukcje/manifest.json`
