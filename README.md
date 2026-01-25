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

```
W/S: Bewegen | A/D: Drehen | M: Karte | R: Neues Labyrinth | Q: Beenden
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓█ █ █████ █████ █ █▓
▓  @ █   █ █   █ █  ▓
▓█ █ █ █ █ █ █ █ █ █▓
▓█ █   █ █   █   █ █▓
▓█ █████ █████████ █▓
▓█ █   █ █       █ █▓
▓█ █ █ █ █ █████ █ █▓
▓█   █   █ █   █   █▓
▓█████████ █ █ █████▓
▓█       █   █     █▓
▓█ █████ █████████ █▓
▓█ █   █         █ █▓
▓█ █ █ █████████ █ █▓
▓█   █           █  ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

             ##########
            ############
           ##############
          ################
         ##################
        ####################
       ######################
      ########################
     ##########################
    ############################
   ##############################
  ################################
```

## Installation

### Voraussetzungen

* Python 3.x
* Terminal mit Unicode-Unterstützung (die meisten modernen Terminals)

### Einrichtung

1. Repository klonen:

```bash
git clone https://github.com/yourusername/3d-looker.git
cd 3d-looker
```

2. Spiel starten:

```bash
python 3DLooker.py
```

Keine zusätzlichen Abhängigkeiten notwendig – es wird nur die integrierte **curses**-Bibliothek von Python verwendet.

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

## Anpassungen

### Labyrinth-Größe ändern

In der `main()`-Funktion:

```python
maze_width = 21   # Muss eine ungerade Zahl sein
maze_height = 15  # Muss eine ungerade Zahl sein
```

### Sichtfeld (Field of View) ändern

```python
fov = math.pi / 3  # 60 Grad (π/3 Radiant)
```

### Bewegungsgeschwindigkeit anpassen

In der `Player`-Klasse:

```python
def move_forward(self, game_map):
    new_x = self.x + self.dir_x * 0.3  # Wert ändern, um Geschwindigkeit anzupassen
```

### Schattierung anpassen

In der Raycasting-Schleife:

```python
if distance < 2:
    char = "#"
elif distance < 4:
    char = "+"
elif distance < 8:
    char = "-"
# Weitere Stufen hinzufügen oder Zeichen ändern
```

## Technische Details

* **Sprache**: Python 3
* **Rendering**: ASCII-Zeichen mit der curses-Bibliothek
* **Rendering-Methode**: Spaltenbasiertes Raycasting
* **Bildrate**: ~60 FPS (16 ms Timeout)
* **Kollisionserkennung**: Gitterbasierte Abfrage
* **Kartenrepräsentation**: 2D-Array (1 = Wand, 0 = Gang)

## Fehlerbehebung

### Windows-Probleme

Falls es unter Windows zu Problemen kommt:

1. Windows Terminal für bessere Unicode-Unterstützung verwenden
2. Alternativ WSL (Windows Subsystem for Linux) nutzen
3. Oder das Paket `windows-curses` installieren:

```bash
pip install windows-curses
```

### Terminal-Größe

Falls die Anzeige fehlerhaft aussieht, stelle sicher, dass dein Terminal mindestens **80x24** Zeichen groß ist.

### Performance-Probleme

* `num_rays` reduzieren
* Labyrinth-Größe verkleinern
* `stdscr.timeout()` erhöhen

## Zukünftige Erweiterungen

* [ ] Texturierte Wände mit unterschiedlichen Zeichen/Farben
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

## Lizenz

Dieses Projekt steht unter der **MIT-Lizenz** – siehe die Datei [LICENSE](LICENSE) für Details.

## Danksagungen

* Inspiriert von klassischen Spielen wie *Wolfenstein 3D* und *Doom*
* Raycasting-Technik basierend auf dem Tutorial von Lode Vandevenne
* Labyrinth-Generierung mit klassischem rekursivem Backtracking

## Autor

Erstellt mit ❤️ von **[Dein Name]**

---

**Viel Spaß beim Erkunden der Labyrinthe! 🎮**
