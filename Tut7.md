## 7.1 

### 1.

Jeder Buchstabe wird durch eine Variable mit der Domäne 0-9 (außer M, da der Übertrag maximal 1 ist)
beschrieben.

D1 = (0-9) für Buchstaben
D2 = (0-1) für Übertrag (U1-U3)

D + E = Y + U1
N + R + U1 = E + U2
E + O + U2 = N + U3
S + M + U3 = O + M -> M ist der Übertrag

### 2.

Man würde so vorgehen dass man ein Wort einsetzt,
sodass aus dem ersten, zweiten und dritten Buchstaben weitere Wörter
gewählt werden können. Das bedeutet man würde kein Wort wählen, das ein Buchstabe
beinhaltet mit dem wir kein weiteres Wort einsetzen können, wie z.B. "ask".
Sonst wäre das Kreuzworträtsel nicht lösbar. Dementsprechend würde man
per Ausschlussverfahren Wörter einsetzen.

### 3.

#### Domain Constraints:

Für D1 / A1 gilt jeder Buchstabe muss der Anfangsbuchstabe eines anderen Wortes sein
Für D2 / A2 gilt jeder Buchstabe muss der mittlere Buchstabe eines anderen Wortes sein
Für D3 / A3 gilt jeder Buchstabe muss der Endbuchstabe eines anderen Wortes sein

#### Arc Constraints:

A1(1) = D1(1)
A1(2) = D2(1)
A1(3) = D3(1)

A2(1) = D1(2)
A2(2) = D2(2)
A2(3) = D3(2)

A3(1) = D1(3)
A3(2) = D2(3)
A3(3) = D3(3)

A1 =\= A2 =\= A3 =\= D1 =\= D2 =\= D3

#### Domain Consistency

DOM(D1 & A1): {are,art,bat,bee,boa,ear,eel,eft,far,fat,oaf,rat,tar}
DOM(D2 & A2): {add, ado, age, ago, air,aid, and, any, ape,
​		are, awe, awl, aye, ear, far, oaf}
DOM(D3 & A3): {add, ado, age, ago, and, any, arc, are, ark, arm,
​		art, aye, ear, eel, eft, far, fat, lee, oaf, rat
​		tar}

#### Arc Consistency

to_do = {A1(1) = D1(1), A1(2) = D2(1), A1(3) = D3(1), A2(1) = D1(2),
 	A2(2) = D2(2), A2(3) = D3(2), A3(1) = D1(3), A3(2) = D2(3), 
​	A3(3) = D3(3), A1 =\= A2 =\= A3 =\= D1 =\= D2 =\= D3}

A1(1) = D1(1)
DOM(D1 & A1): {are,art,bat,bee,boa,ear,eel,eft,far,fat}

A2(2) = D2(2)
DOM(D2 & A2): {add, ado, age, ago, air,aid, and, any,
​		awe, awl, ear, far, oaf}

A3(3) = D3(3)
DOM(D3 & A3): {add, ado, age, ago, and, are,
​		art, aye, ear, eft, far, fat, lee, rat
​		tar}

A1(2) = D2(1)
DOM(D1 & A1): {bat,bee,boa,ear,eel,far,fat}
DOM(D2 & A2): {add, ado, age, ago, air,aid, and, any,
​		awe, awl, ear, oaf}

A1(3) = D3(1)
DOM(D1 & A1): {bat,bee,boa,ear,eel,far,fat}
DOM(D3 & A3): {add, ado, age, ago, and, are,
​		art, aye, ear, eft,lee, rat
​		tar}

A2(3) = D3(2)
DOM(D2 & A2): {add, age, air,aid, and, any,
​		awe, ear, oaf}
DOM(D3 & A3): {add, ado, are,
​		art, aye, eft,lee}

A3(1) = D1(3)
DOM(D1 & A1): {bee,boa,eel}
DOM(D3 & A3): {add, ado, are, art, aye, eft,lee}

A3(2) = D2(3)
DOM(D2 & A2): {add, air,aid, and, any, ear, oaf}
DOM(D3 & A3): {add, ado, are, art, aye, eft,lee}

#### Zwischenstand 

DOM(D1 & A1): {bee,boa,eel}
DOM(D2 & A2): {add, air,aid, and, any, ear, oaf}
DOM(D3 & A3): {add, ado, are, art, aye, eft,lee}

A1(1) = D1(1)
DOM(D1 & A1): {bee,boa}

A2(2) = D2(2)
DOM(D2 & A2): {air,aid, and, any, ear, oaf}

A3(3) = D3(3)
DOM(D3 & A3): {are, art, aye, eft,lee}

A1(2) = D2(1)
DOM(D1 & A1): {bee,boa}
DOM(D2 & A2): {ear, oaf}

A3(2) = D2(3)
DOM(D2 & A2): {ear, oaf}
DOM(D3 & A3): {are, art, eft}

A3(3) = D3(3)
DOM(D3 & A3): {art, eft}

#### Lösung ist also:

DOM(D1 & A1): {bee,boa}
DOM(D2 & A2): {ear, oaf}
DOM(D3 & A3): {art, eft}

