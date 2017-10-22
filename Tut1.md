## GWV – Grundlagen der Wissensverarbeitung

### Tutorial 1: Search Space design



##### Exercise 1.1 : (Search space properties)

**Observability:** 

- Wenn etwas nur partially observable ist, muss man zum Beispiel altes Wissen über nicht mehr sichtbare Bereiche speichern

**Discreteness:** 

- Wichtig um die richtige Art Algorithmus auszusuchen, zum Beispiel Entscheidung ob Diskretisierung nötig ist oder der Algorithmus continous features unterstützt

**Determinism:** 

- In einer deterministicschen Welt sind mögliche zukünftige Weltzustände vollständig bekannt -> es gibt immer eine beste Entscheidung
- In einer stochastischen muss mit Wahrscheinlichkeiten gearbeitet werden und die beste Entscheidung garnatiert nicht das beste Ergebnis 



##### Exercise 1.2.1 : (Search Space 1) - Public Transport

State Space is the sum of all tuples of all possible combinations of places and times.

A node would be one specific place and time as a tuple.

The edges would represent the changes in place and time.



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