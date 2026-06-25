# Farbkontrastprüfung für NVDA

Tester der digitalen Barrierefreiheit müssen regelmäßig sicherstellen, dass Farbkontrastverhältnisse innerhalb der von den Web Content Accessibility Guidelines (WCAG) definierten Schwellenwerte liegen. Für blinde Tester war dies jedoch in der Vergangenheit schwierig, ohne auf sehende Kollegen oder automatisierte Lösungen angewiesen zu sein. Die meisten am Markt verfügbaren automatisierten Lösungen, darunter WAVE und axe DevTools, filtern Kontrastprobleme lediglich als „Vorschläge“, übersehen Dinge und untersuchen den Fokusindikator nicht.

Mit diesem Add-on können Sie den Kontrast des fokussierten Elements mit NVDA+F, des Elements unter dem NVDA-Cursor mit NVDA+Umschalt+F, des Fokusindikators mit NVDA+Umschalt+C prüfen sowie mit NVDA+Umschalt+Strg+F eine seitenweite Prüfung aller Textkontrastfehler durchführen.

| Aufgabe | Befehl | Umfang |
| --- | --- | --- |
| Kontrast des fokussierten Texts prüfen | **NVDA+F** | Formatierungsinformationen des fokussierten Elements, einschließlich Kontrastverhältnis |
| Kontrast des Texts am NVDA-Cursor prüfen | **NVDA+Umschalt+F** | Formatierungsinformationen an der Position des NVDA-Cursors, einschließlich Kontrastverhältnis |
| Kontrast des Fokusindikators prüfen | **NVDA+Umschalt+C** | Fokusring gegenüber dem umgebenden Hintergrund |
| Seitenweite Textprüfung durchführen | **NVDA+Umschalt+Strg+F** | Sichtbarer Text auf der aktuellen Seite, gruppiert nach WCAG-Kontrastschwelle |

## Textkontrast

Dieses Add-on erweitert die vorhandenen Befehle von NVDA zur Ausgabe von Formatierungsinformationen. Drücken Sie **NVDA+F** auf beliebigem Text, um Formatierungsinformationen einschließlich des Kontrastverhältnisses zu hören. Beispiel:

- Source Sans 3 ExtraLight
- 10.5pt
- schwarz auf weiß
- linksbündig
- `#000000 auf #FFFFFF, Kontrast 21.0:1`

Drücken Sie zweimal schnell für einen Dialog im Lesemodus. **NVDA+Umschalt+F** verwendet die Position des NVDA-Cursors anstelle des System-Cursors.

WCAG AA erfordert 4.5:1 für normalen Text und 3:1 für großen Text. WCAG AAA erfordert 7:1.

## Kontrast des Fokusindikators

Drücken Sie **NVDA+Umschalt+C** auf einem beliebigen fokussierten Element, um den Kontrast zwischen seinem Fokusring und dem umgebenden Hintergrund zu hören:

> `Fokusindikator: #000000 auf #FFFFFF, Kontrast 21.0:1`

WCAG bewertet Fokusindikatoren über zusammenhängende Anforderungen. Der Kontrast von Nicht-Text-Elementen erfordert, dass der visuelle Fokusindikator mindestens 3:1 Kontrast gegenüber benachbarten Farben aufweist, und das Fokus-Erscheinungsbild in WCAG 2.2 ergänzt Anforderungen an den Kontrast der Änderung und die Größe des Indikators. Dieses Add-on gibt die Kontrastmessung an; Tester sollten dennoch die vollständige Anforderung an das Fokus-Erscheinungsbild bewerten.

## Seitenweite Kontrastprüfung

Drücken Sie **NVDA+Umschalt+Strg+F**, um jeden Textabschnitt auf der aktuellen Seite auf einmal zu prüfen. Die Ergebnisse werden in einem Dialog im Lesemodus geöffnet, gruppiert nach Schweregrad:

- Unter 3:1 (großer Text)
- Unter 4.5:1 (normaler oder kleiner Text)
- Unter 7:1 (AAA-Textkontrast)

Text, der 7:1 oder besser erreicht, besteht alle WCAG-Schwellenwerte und wird ausgelassen. Wenn nichts fehlschlägt, gibt NVDA dies aus, anstatt den Dialog zu öffnen.

Bitte beachten Sie, dass dieser Befehl nur den im aktuellen Seitenzustand sichtbaren Text prüft. Sie müssen weiterhin andere Zustände wie Fokus, Mauszeigerkontakt, ein- oder ausgeklappte Inhalte, verzögert geladene Inhalte sowie benutzerdefiniert dargestellten oder bildbasierten Text einblenden und testen. Der Kontrast des Fokusrings wird separat mit **NVDA+Umschalt+C** geprüft.

## Installation

1. Laden Sie die neueste Version über [diesen Link](https://github.com/cartertemm/contrast-checker-nvda/releases/latest/) herunter.
2. Öffnen Sie die Datei .nvda-addon bei laufendem NVDA. NVDA fordert Sie zur Installation auf.

## Ausprobieren

Öffnen Sie `tests/test_contrast.html` lokal oder [die gerenderte Testseite](https://ctemm.me/files/test_contrast.html) in einem Browser bei laufendem NVDA.
Sie deckt verschiedene gängige Szenarien ab, etwa Textkontrast, Fokusringe mit bekannten Verhältnissen, fehlende Ringe, Ringe auf Basis von box-shadow, nicht weiße Hintergründe und verschiedene Elementtypen.

## Aus dem Quellcode erstellen

Erfordert Git, Python und SCons.

```
git clone https://github.com/cartertemm/contrast-checker-nvda/
cd contrast-checker-nvda
pip install scons
scons
```

Die erstellte Datei `.nvda-addon` erscheint im Stammverzeichnis des Projekts.

## Lizenz

GPL 2.0
