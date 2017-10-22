## GWV – Grundlagen der Wissensverarbeitung

### Tutorial 1: Search Space design



##### Exercise 1.1 : (Search space properties)

-  Angenommen wir haben einen Roboter der sich über ein Feld mit Hindernissen zu einem Zielfeld bewegt.
- Der Roboter sieht nur das, was unmittelbar vor ihm steht. Würde er alles wissen, kˆnnte er gezielt
- Hindernissen ausweichen. Jedoch muss er nun nach jedem Schritt schauen, ob er einem Hindernis ausweichen muss.
- Somit hat er einen Teil der Umgebung als Information zur Verfügung und kann so mit Hilfe von Wahrscheinlichkeiten, die wir aufgrund einer diskreter Anzahl von Informationen (endliche Menge an Hindernissen und Feldern) seine nächste Aktion berechnen.



##### Exercise 1.2.1 : (Search Space 1) - Public Transport

Der Zustandsraum besteht aus:

- endliche Menge an Haltestellen
- endliche Menge an Übergängen zwischen Haltestellen
- Start Haltestelle
- End Haltestelle

Ein Knoten beschreibt eine Haltestelle und wird durch eine Kante mit anderen erreichbaren Haltestellen verbunden.
Somit sind im Zustandsraum alle Knoten, Kanten und Übergänge gegeben.



##### Exercise 1.2.2 : (Search Space 1) - Water Jugs

Model of state of two jugs: (x,y) - x,y representing amount of water in each jug

List of possible states:

| x (4-liter-jug) | y (3-liter-jug) |
| --------------- | --------------- |
| 0               | 0               |
| 0               | 1               |
| 0               | 2               |
| 0               | 3               |
| 1               | 0               |
| 1               | 1               |
| 1               | 2               |
| 1               | 3               |
| 2               | 0               |
| 2               | 1               |
| 2               | 2               |
| 2               | 3               |
| 3               | 0               |
| 3               | 1               |
| 3               | 2               |
| 3               | 3               |
| 4               | 0               |
| 4               | 1               |
| 4               | 2               |
| 4               | 3               |
|                 |                 |

**Start and goal states: (0,0) -> … -> (2,?)**

Possible Transisitions:

| start state | end states                       |
| ----------- | -------------------------------- |
| (0,0)       | (0,3) \| (4,0) \| (4,3)          |
| (0,3)       | (0,0) \| (3,0) \| (4,3)          |
| (4,0)       | (0,0) \| (1,3) \| (4,3)          |
| (4,3)       | (0,3) \| (4,0)                   |
| (3,0)       | (0,0) \| (0,3) \| (4,0) \| (3,3) |
| (1,3)       | (1,0) \| (0,3) \| (4,0) \| (4,3) |
| (1,0)       | (0,0) \| (0,1) \| (4,0) \| (1,3) |
| (0,1)       | (0,0) \| (1,0) \| (0,3) \| (4,1) |
| (4,1)       | (0,1) \| (4,0) \| (2,2) \| (4,3) |
| (2,2)       | (0,2) \| (2,0) \| (4,2) \| (2,3) |
|             |                                  |

Solution: (0,0) -> (4,0) -> (1,3) -> (1,0) -> (0,1) -> (4,1) -> (2,2)



(b) No, the solution requires the 3-liter-jug be emptied once.