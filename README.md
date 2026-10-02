# TMDT-Thesisvorlage

LaTeX-Vorlage für Bachelor- und Masterarbeiten am Lehrstuhl für Technologien
und Management der Digitalen Transformation (TMDT) der Bergischen Universität
Wuppertal.

Das TMDT gehört zur Fakultät für Elektrotechnik, Informationstechnik und
Medientechnologie. Die Vorlage verwendet deshalb das Corporate Design der
Bergischen Universität und die Farbpalette des TMDT.

## Schnellstart

1. In `Einstellungen.tex` alle Pflichtangaben ersetzen.
2. Eigene Kapitel in `Kapitel/` anlegen und in `Thesis.tex` einbinden.
3. Literatur in `Verzeichnisse/Literatur.bib` pflegen.
4. Die Thesis mit `python build.py` bauen.

Benötigt werden Python 3 sowie eine LaTeX-Installation mit `pdflatex` und
`bibtex8` oder `bibtex`.

Mit `python release.py` wird nach einem erfolgreichen Build zusätzlich ein
datiertes Archiv `TMDT-Thesisvorlage_JJJJ-MM-TT.zip` erzeugt.

## Offizielle Dokumente

Aufgabenstellung, Verlängerung, eidesstattliche Versicherung und Sperrvermerk
werden nicht mitgeliefert. Verwendet werden müssen die jeweils aktuellen
Dokumente des zuständigen Prüfungsamts beziehungsweise des Studiengangs.

- [TMDT: Bachelor- und Masterarbeiten](https://www.tmdt.uni-wuppertal.de/de/studium-und-lehre/bachelor-und-masterarbeiten/)
- [Zentrales Prüfungsamt der BUW](https://zpa.uni-wuppertal.de/)

Die PDFs werden in `Medien/` abgelegt und anschließend in
`Einstellungen.tex` aktiviert:

```latex
\setbool{aufgabenstellung}{true}
\setbool{eidesstattlicheVersicherung}{true}
```

Die Dateinamen können dort ebenfalls angepasst werden.

## Generative KI

Am Ende des Anhangs steht standardmäßig eine ausfüllbare Seite zur
tabellarischen Dokumentation der KI- und Hilfsmittelverwendung im Querformat.
Die Angaben und Tabellenzeilen werden in `Kapitel/DeclarationGenerativeAI.tex`
bearbeitet. Name und Matrikelnummer werden aus `Einstellungen.tex` übernommen;
Datum, Unterschrift und beide Auswahlkästchen sind zunächst leer. Das zutreffende
Kästchen lässt sich dort mit `\kiAngekreuzt` statt `\kiKaestchen` markieren.

Die Tabelle enthält deutsche Beispieltexte direkt in den Zellen sowie
Werkzeugauswahlkästchen für ChatGPT, Claude, Gemini und ein
Freifeld „Andere“. Die Auswahl wird im Quelltext mit
`\kiAngekreuzt` statt `\kiKaestchen` vorgenommen oder im Ausdruck markiert.
Die Texte müssen an die tatsächliche Nutzung angepasst werden;
ungenutzte Einträge entfernen und Modell, Version oder URL ergänzen.

Bei Bedarf lässt sich die Seite in `Einstellungen.tex` deaktivieren:

```latex
\setbool{kiErklaerung}{false}
```

Die jeweils gültige Erklärung an Eides statt bleibt unabhängig davon
maßgeblich.

Aktuelle Hinweise bietet der
[UniService Digitalisierung Lehre](https://uniservice-dl.uni-wuppertal.de/de/services/ki-handreichung-fuer-studierende/).

## Projektstruktur

```text
Thesis.tex                 Hauptdatei
Einstellungen.tex          Persönliche Angaben und Optionen
Kapitel/                   Inhalt der Arbeit
Medien/                    Abbildungen und offizielle PDFs
Verzeichnisse/             Literatur und Glossareinträge
Vorlage/                   Layout und Titelei
build.py                   Plattformunabhängiger Build
```

## Hinweis

Diese technische Vorlage ersetzt keine Vorgaben des TMDT, des Studiengangs,
des Prüfungsausschusses oder des Zentralen Prüfungsamts. Im Zweifel gelten die
jeweils aktuellen offiziellen Vorgaben.
