# GWV - Blatt 8

### Aufgabe 1

Knowledgebase = KB

##### Assumables:

Gardener : I have been working in the Garden all day. g_worked
Butler: I have been fixing the car in the garage all day. b_worked

##### Observations:

The Gardener has no dirts on his hands !g_dirty
Butler has dirt on his hands b_dirty

##### Rules:

If the gardener have worked in the garden all day, he has dirt
on his hands g_worked -> g_dirty

If the Butler worked in the garage all day, he has dirt on his hands
b_worked -> b_dirty

##### Integrity Constraints:

The gardener has either dirt on his hands or not
g_dirty V !g_dirty -> false
The butler has either dirt on his hands or not.
d_dirty V !d_dirty -> false

Wir haben nur zwei Verdächtige also ist der minimale Konflikt:
{g_worked, d_worked}. Daraus lässt sich schließen, dass
aus der Knowledgebase : KB |= !g_worked V !b_worked zu folgern ist.
Die Integrität Constraints geben vor dass man entweder dreckig oder saubere 
Hände hat.
Nach der Anwendung der Regeln ergibt sich deshalb welcher der Beiden
lügt: KB |= !g_dirty V !b_dirty. Da wir aus der KB wissen, dass 
der Gardener saubere Hände haben, können wir sagen er ist der Täter!

### Aufgabe 2

Assumables all pipes, cables, mechanical lines ok
bat_ok -> ign_ok 
bat_ok & ign_ok -> fureg_ok
ign_ok -> starter_ok
ign_ok -> fureg_ok
starter_ok -> eng_ok
eng_ok -> filter_ok
filter_ok & fureg_ok -> pump_ok
pump_ok -> tank_ok

starter, eng, pump

#### observations: no noises

Da starter nicht ok, ist auch engine nicht ok, da engine nicht ok
ist ign_key nicht ok und dann evtl auch bat nicht ok. Wenn bat oder
ign nicht ok kann auch die pumpe nicht ok sein, da die Bedinungen nicht
erfüllt sind.

#### observations 2: noise 1

starter ok also ign und bat ok. <- noise 1

wenn starter ok ist sollte eng ok sein -> noise 2
dies ist nicht so, also ist auch filter und pump etc
nicht ok -> also kein noise 3. Außerdem ist pump auch abhängig
von fureg heißt es könnte auch kaputt sein.

#### observations 3: noise 2

noise 2 geht, also ist die pumpe ok wie auch fureg, filter, bat und filter.

Da kein noise 1 und 3 heißt es die engine ist nicht ok, wie auch der starter.
Wir wissen fureg ist ok, also ist auch ign ok.
Daher schlussfolgern wir dass der Starter kaputt sein kann.

#### observations 4: noise 1 and 2

noise 3 geht nicht also ist die engine nicht ok, da noise 2 geht
heißt es dass der starter ok ist, also kann es nur an der engine
selbst liegen, dass sie kaputt ist.