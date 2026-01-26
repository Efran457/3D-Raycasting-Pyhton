# 3D-Raycasting-Python

Dies ist ein 3D-Raycasting-Programm, das die Python-Bibliothek **curses** verwendet. Curses macht es einfach, Text an bestimmten Koordinaten im Terminal darzustellen.

# 3D Looker

Ein terminalbasierter 3D-Labyrinth-Explorer mit ASCII-Raycasting-Rendering. Erkunde prozedural generierte Labyrinthe direkt in deiner Kommandozeile!

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)

## Features

* **3D-Raycasting-Renderer** – Klassisches Pseudo-3D-Rendering ähnlich wie *Wolfenstein 3D*
* **Prozedurale Labyrinth-Generierung** – Verwendet den rekursiven Backtracking-Algorithmus
* **Echtzeit-Navigation** – Flüssige Steuerung mit WASD oder Pfeiltasten
* **Interaktive Minimap** – Ein-/ausblendbare Übersicht mit Position und Blickrichtung
* **Distanzabhängige Schattierung** – Wände erscheinen dunkler, je näher sie sind (Tiefeneffekt)
* **Labyrinth neu generieren** – Drücke **R**, um ein neues zufälliges Labyrinth zu erzeugen
* **Einfach zu starten** – Einfach die `.exe` im 3DLooker-Ordner öffnen – super easy

## Screenshots

<img width="400" height="1040" alt="image" src="https://github.com/user-attachments/assets/ca6e4766-1c60-4a4a-8ad1-93aab876adbd" /> <img width="278" height="84" alt="image" src="https://github.com/user-attachments/assets/f6a6ecec-0d50-4c13-ad76-216a13848551" />
<img width="650"  alt="image" src="https://github.com/user-attachments/assets/2e5f21da-669f-45b2-9c12-e4cb5a2e54a0" /><img width="730" alt="image" src="https://github.com/user-attachments/assets/8da312f6-10f2-4716-869d-32ffb0574815" />





## Installation

### Voraussetzungen

* Windows
* Unziper (ist normall schon in Windows)

## Steuerung

| Taste     | Aktion                     |
| --------- | -------------------------- |
| `W` / `↑` | Vorwärts bewegen           |
| `S` / `↓` | Rückwärts bewegen          |
| `A` / `←` | Nach links drehen          |
| `D` / `→` | Nach rechts drehen         |
| `M`       | Minimap ein-/ausblenden    |
| `R`       | Neues Labyrinth generieren |
| `Q`       | Spiel beenden              |

## Funktionsweise

### Raycasting-Algorithmus

Der Renderer verwendet eine Raycasting-Technik:

1. Für jede Bildschirmspalte wird ein Strahl von der Spielerposition ausgesendet
2. Der Strahl bewegt sich vorwärts, bis er eine Wand trifft
3. Die Wandhöhe wird anhand der Distanz berechnet (näher = höher)
4. Fischaugen-Verzerrung wird durch Kosinus-Korrektur reduziert
5. Distanzabhängige Schattierung erzeugt einen Tiefeneffekt

### Labyrinth-Generierung

Die Labyrinthe werden mit dem **rekursiven Backtracking-Algorithmus** erzeugt:

1. Starte mit einem Gitter voller Wände
2. Wähle eine zufällige Startzelle und markiere sie als Gang
3. Solange es unbesuchte Nachbarn gibt:

   * Wähle einen zufälligen unbesuchten Nachbarn
   * Entferne die Wand zwischen den Zellen
   * Bewege dich zum Nachbarn und wiederhole
4. Wenn keine Nachbarn mehr vorhanden sind, gehe zurück, bis alle Zellen besucht sind

Das Ergebnis ist ein „perfektes Labyrinth“ – zwischen zwei Punkten existiert genau ein Weg.

## Technische Details

* **Sprache**: Python 3
* **Rendering**: ASCII-Zeichen mit der curses-Bibliothek
* **Rendering-Methode**: Spaltenbasiertes Raycasting
* **Bildrate**: ~60 FPS (16 ms Timeout)
* **Kollisionserkennung**: Gitterbasierte Abfrage
* **Kartenrepräsentation**: 2D-Array (1 = Wand, 0 = Gang)

## Fehlerbehebung

### Terminal-Größe

Es könnte sein dass es kaputt geht wenn sie dass fenster Fergrößern

## Zukünftige Erweiterungen

* [x] Wände mit unterschiedlichen Zeichen/Farben
* [ ] Mehrere Ebenen
* [ ] Gegner / Sammelobjekte
* [ ] Speichern/Laden von Labyrinthen
* [ ] Weitere Labyrinth-Algorithmen
* [ ] Soundeffekte (Terminal-Beep)
* [ ] Multiplayer-Unterstützung

## Mitwirken

Beiträge sind willkommen!

* Bugs melden
* Feature-Ideen vorschlagen
* Pull Requests einreichen
* Dokumentation verbessern

## Danksagungen

* Inspiriert von klassischen Spielen wie *Wolfenstein 3D* und *Doom*
* Raycasting-Technik basierend auf dem Tutorial von Lode Vandevenne
* Labyrinth-Generierung mit klassischem rekursivem Backtracking

## Autor

* Erstellt mit ❤️ von **Initys**
* Youtube📹 Kanal: [https://www.youtube.com/@Initys-unityGames]

---

**Viel Spaß beim Erkunden der Labyrinthe! 🎮**
