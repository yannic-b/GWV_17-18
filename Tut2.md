## GWV – Grundlagen der Wissensverarbeitung

### Tutorial 2: Search Spaces

Thomas Hofmann, Yannic Boysen



##### Class Exercise 2.1 : (Peg Solitaire)

-  Startzustand: Mitte: leer, überall sonst: Kugel
-  Zielzustand: Mitte: Kugel, überall sonst: leer




##### Class Exercise 2.2 : (Disease spreading)





##### Exercise 2.3 : (Search Space Construction 2)

Our search space would be formalised by tuples containing our current position, the number of available transport tickets and the distance to each of the detectives in tickets (a distance of 0 meaning the detective can reach our current position exactly on his next turn).

To find find the safe place, we just have to look for the place where the ticket distance to all detectives is greater than zero.



##### Exercise 2.4.1 : (Search Space Construction 3) - Furniture

- Search Space:
  - Tuples include position for each piece of furniture
- Goal:
  - Find Tuple where: 
    - chair positions near table positions
    - no position near door
    - all postions different from each other
    - all postions not null (all pieces inside flat)
- Properties:
  - cycling graph (reversible steps)
- Strategy:
  - Breadth-first search

##### Exercise 2.4.2 : (Search Space Construction 3) - Construction

- Search Space:
  - Tuples contain all the different parts with the respective current status (in construction etc.), list of people involved in construction of the part, the dependencies on other parts and the time
- Goal:
  - shortest path where each status is 'finished'
- Properties:
  - tree graph
- Strategy:
  - Breadth-first/ lowest-cost-first search

##### Exercise 2.4.3 : (Search Space Construction 3) - Elevator

- Search Space:
  - Tuple consisting of current floor, floors where button is pressed. direction of each button press and covered distance in floors
- Goal:
  - bring people to destination with smallest distance travelled
- Properties:
  - tree graph
- Strategy:
  - Lowest-cost-first search