# Sprawdzanie kontrastu kolorów dla NVDA

Testerzy dostępności cyfrowej muszą regularnie upewniać się, że współczynniki kontrastu kolorów mieszczą się w progach określonych przez Wytyczne dotyczące dostępności treści internetowych (WCAG). Jednak niewidomym testerom historycznie trudno było to robić bez polegania na widzących współpracownikach lub rozwiązaniach automatycznych. Większość dostępnych na rynku rozwiązań automatycznych, w tym WAVE i axe DevTools, jedynie oznacza problemy z kontrastem jako „sugestie”, pomija pewne rzeczy i nie sprawdza wskaźnika fokusu.

Ten dodatek pozwala sprawdzić kontrast elementu z fokusem za pomocą NVDA+F, elementu pod kursorem przeglądania za pomocą NVDA+Shift+F, wskaźnika fokusu za pomocą NVDA+Shift+C oraz uruchomić audyt całej strony pod kątem wszystkich błędów kontrastu tekstu za pomocą NVDA+Shift+Ctrl+F.

| Zadanie | Polecenie | Zakres |
| --- | --- | --- |
| Sprawdź kontrast tekstu z fokusem | **NVDA+F** | Informacje o formatowaniu elementu z fokusem, w tym współczynnik kontrastu |
| Sprawdź kontrast tekstu pod kursorem przeglądania | **NVDA+Shift+F** | Informacje o formatowaniu w pozycji kursora przeglądania, w tym współczynnik kontrastu |
| Sprawdź kontrast wskaźnika fokusu | **NVDA+Shift+C** | Obwódka fokusu względem otaczającego tła |
| Uruchom audyt tekstu dla całej strony | **NVDA+Shift+Ctrl+F** | Widoczny tekst na bieżącej stronie, pogrupowany według progu kontrastu WCAG |

## Kontrast tekstu

Ten dodatek rozszerza istniejące polecenia NVDA dotyczące informacji o formatowaniu. Naciśnij **NVDA+F** na dowolnym tekście, aby usłyszeć informacje o formatowaniu, w tym współczynnik kontrastu. Przykład:

- Source Sans 3 ExtraLight
- 10.5pt
- czarny na białym
- wyrównanie do lewej
- `#000000 na #FFFFFF, kontrast 21.0:1`

Naciśnij dwukrotnie szybko, aby otworzyć okno dialogowe w trybie przeglądania. **NVDA+Shift+F** używa pozycji kursora przeglądania zamiast karetki systemowej.

WCAG AA wymaga 4.5:1 dla zwykłego tekstu i 3:1 dla dużego tekstu. WCAG AAA wymaga 7:1.

## Kontrast wskaźnika fokusu

Naciśnij **NVDA+Shift+C** na dowolnym elemencie z fokusem, aby usłyszeć kontrast między jego obwódką fokusu a otaczającym tłem:

> `Wskaźnik fokusu: #000000 na #FFFFFF, kontrast 21.0:1`

WCAG ocenia wskaźniki fokusu poprzez powiązane wymagania. Kontrast elementów nietekstowych wymaga, aby wizualny wskaźnik fokusu miał co najmniej 3:1 kontrastu względem sąsiednich kolorów, a wygląd fokusu w WCAG 2.2 dodaje wymagania dotyczące kontrastu zmiany oraz rozmiaru wskaźnika. Ten dodatek podaje zmierzony kontrast; testerzy powinni jednak nadal oceniać pełne wymaganie dotyczące wyglądu fokusu.

## Audyt kontrastu całej strony

Naciśnij **NVDA+Shift+Ctrl+F**, aby za jednym razem przeskanować każdy fragment tekstu na bieżącej stronie. Wyniki otwierają się w oknie dialogowym w trybie przeglądania, pogrupowane według wagi:

- Poniżej 3:1 (duży tekst)
- Poniżej 4.5:1 (zwykły lub mały tekst)
- Poniżej 7:1 (kontrast tekstu AAA)

Tekst, który osiąga 7:1 lub lepiej, spełnia wszystkie progi WCAG i jest pomijany. Jeśli nic nie zawodzi, NVDA informuje o tym zamiast otwierać okno dialogowe.

Pamiętaj, że to polecenie sprawdza tylko tekst widoczny w bieżącym stanie strony. Nadal musisz odsłonić i przetestować inne stany, takie jak fokus, najechanie kursorem, rozwinięta lub zwinięta treść, treść ładowana z opóźnieniem oraz tekst renderowany niestandardowo lub oparty na obrazach. Kontrast obwódki fokusu sprawdza się osobno za pomocą **NVDA+Shift+C**.

## Instalacja

1. Pobierz najnowsze wydanie z [tego odnośnika](https://github.com/cartertemm/contrast-checker-nvda/releases/latest/).
2. Otwórz plik .nvda-addon przy uruchomionym NVDA. NVDA zaproponuje instalację.

## Wypróbuj

Otwórz `tests/test_contrast.html` lokalnie lub [wyrenderowaną stronę testową](https://ctemm.me/files/test_contrast.html) w przeglądarce przy uruchomionym NVDA.
Obejmuje ona różne typowe scenariusze, takie jak kontrast tekstu, obwódki fokusu o znanych współczynnikach, brakujące obwódki, obwódki oparte na box-shadow, niebiałe tła oraz różne typy elementów.

## Budowanie ze źródeł

Wymaga Git, Python oraz SCons.

```
git clone https://github.com/cartertemm/contrast-checker-nvda/
cd contrast-checker-nvda
pip install scons
scons
```

Zbudowany plik `.nvda-addon` pojawia się w katalogu głównym projektu.

## Licencja

GPL 2.0
