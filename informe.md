# Problema #2 de DAA

## Título: Tito el corrupto

## Descripción del problema

Tenemos una entrada de n ciudades y m posibles carreteras a construir entre ellas. Cada carretara nos aporta una cantidad $a_i$ de dinero y las ciudades que une consumen una cantidad $c_i$ de dinero.
Se necesita conocer las carreteras que vamos a construir para maximizar la ganancia de dinero.

## Solución Fuerza Bruta

### Pseudcódigo

    def Solve(streetName, streets, cityTake, cities, funds):
    if len(streets) == 0:
        return [], 0

    currentStreet = streetName[0]

    nTakePath, nTake = Solve(streetName[1:], streets[1:], , cities, funds)


    if not cityTake[cStreet[0]]:
        funds += cities[cStreet[0]]
        cityTake[cStreet[0]] = True

    if not cityCopy[cStreet[1]]:
        funds += cities[cStreet[1]]
        cityTake[cStreet[1]] = True

    gain = streets[0] - funds

    if gain >= 0:
        funds = 0
    else:
        funds -= streets[0]

    TakePath, Take = Solve(streetName[1:], streets[1:], cityCopy, cities, funds)
    TakePath.append(cStreet)
    Take += gain

    if Take > nTake:
        return TakePath, Take

    else:
        return nTakePath, nTake

### Explicación del algoritmo fuerza bruta

La idea se reduce a dado un conjunto de aristas(calles) decidir cuales se toman y cuales se desechan. En cada paso del algoritmo se calcula la ganancia si se decidiera tomar o desechar una arista(calle) teniendo en cuenta la pérdida generada por las ciudades, la combinación que más ganancias genera es dada como solución. La complejidad de este algoritmo es $2^{|E|}$ donde |E| representa cantidad de aristas(calles) del grafo,pues este problema es equivalente a hallar todas las permutaciones de tamaño |E| que se pueden que se pueden hacer con los números 1(tomo la calle) y 0(desecho la calle).

## Solución

### Modelación del grafo

La idea principal es cómo modelamos el grafo de forma tal que quede como una red de flujo. Partiendo de la idea que queremos encontrar la máxima ganancia que se puede transmitir entre los vértices de fuente y destino.

Viéndolo de esta manera nos damos cuenta que lo que queremos transmitir por nuestra red es el dinero y así quedarnos con el máximo posible.

En este momento encontramos el primer problema, pues las carreteras suman y las ciudades restan dinero. No supimos modelar ese concepto con una red de flujo.

Es fácil notar que la idea anterior es equivalente a tener todo el dinero otorgado por las carreteras y solo quedaría restar el dinero de las ciudades que conectamos y de las calles que no construimos.

Después de muchos intentos no llegamos muy lejos con estas ideas.

Siguiendo la línea de pensamiento inicial donde queríamos obtener la máxima ganancia de una red de flujo donde se transmite dinero, es obvio que la capacidad de las aristas fuese dinero.

De esta forma llegamos a la idea de que las carreteras eran como fuentes que daban dinero y las ciudades consumidores de ese dinero.

No es muy difícil modelar las carrteras como fuente pues consideramos las carreteras como nodos conectados a una fuente y las capacidades de esas aristas son las respectivas cantidades de dinero que obtenemos por construirlas.

Ahora solo era necesario modelar las ciudades como "consumidores" de dinero cosa que no encotramos nunca, pero estaba claro que las carreteras tenían que estar conectadas a las ciudades que unían.

Teniendo este modelado pensamos en poner la capacidad de esas aristas como el dinero que restan las ciudades al construir una carretera que llega a ella. Esto no tiene sentido pues si existían dos carreteras que llegaban a la misma ciudad
duplicábamos su costo.

A pesar de ser una idea equivocada nos ayudó mucho porque interpretamos los costos de las ciudades como aristas que limitan el flujo del dinero y así la ganancia sería la capacidad de las aristas que van de la fuente a las carreteras que no pudimos saturar, cosa que coincide con la fórmula inicial:

$\sum*{a_i \in A} a_i - \sum*{c_i \in C} c_i $

siendo A el conjunto de las carreteras construidas y C el conjunto de las ciudades que están unidas por esas carreteras.

Teniendo esto ya es muy fácil ver el flujo del dinero. Sale de la fuente hacia cada una de las carreteras con su costo respectivo y llega de las ciudades al destino con el costo respectivo de cada una de ellas.

El costo de las aristas que conectan a las carreteras con las ciudades es infinito. No tiene sentido restringir el dinero que pasa por ellas.

### Solución del prblema

Para resolver nuestro problema hallamos el valor del flujo máximo en la red de flujo creada anteriormente y tenemos que el dinero que pasa por las manos de Tito es el total que brinda el gobierno por construir cada carretara menos el valor del flujo del máximo. Las carreteras que tenemos que construir son las que petenecen al corte mínimo.

### Demostración de correctitud

El grafo $G = (V, E)$ que creamos es una red de flujo pues es un grafo orientado, conexo que tiene dos nodos distinguidos una fuente s, con grado de salida positivo, y un sumidero t, con grado de entrada positivo.

La capacidad de una red de flujo es una función $c : E \rightarrow \R^+$ .

La función de capacidad para esta red $G = (V, E)$ es el costo respectivo de las calles y las ciudades. Cada arista que sale de la fuente llega a un vértice que respresenta una calle y su capacidad es el dinero que aporta construir esa calle. Esos vértices calles tienen aristas hacia los vértices ciudad que conectan, la capacidad de esas aristas es infinito. Los vértices ciudad tienen aristas hacia el sumidero cuyos valores son el dinero que otorgan las ciudades al construir una calle que llegue a ellas. Por tanto cumple con la definición.

Sabemos que el valor del flujo es igual a la capacidad del corte mínimo y que las aristas que unen a los vértices que pertenecen a $S$ con los vértices que pertenecen a $V/S$ están saturadas.


Sea $S$ el corte mínimo.

Si dado el corte mínimo existe un nodo carretera $A_i$ tal que $C_i \in V/S$ esa carretera no será construida porque que esa arista esté saturada implica que el dinero que gana Tito al construir $A_i$ es menor o igual que el dinero que aportan las ciudades que conecta y por tanto Tito no ganaría nada.

Si dado el corte mínimo existe un nodo ciudad $C_i$ que pertenece a $S$ es necesario conectar esa ciudad, la artista entre $C_i$ y $T$ está saturada por el dinero de las carreteras, o sea, las calles que conectan a $C_i$ aportan más dinero del que resta $C_i$.

Por tanto la respuesta final será todo $Ci$ tal que $C_i \in S$.

### Pseudocódigo

    def SolvePushRelabel(graph):
        g = Graph(graph)
        g.getMaxFlow(0, len(g.ver) - 1)
        solution = []
        for i in range(len(g.streetsName)):
            if (g.edge[i].capacity - g.edge[i].flow > 0):
                sol.append(g.streetsName[i])
        return solution

La clase Graph contiene una implementación del algoritmo Push-Relabel para hallar flujo máximo. Al instanciarse se construye el grafo, al que se hallará el flujo, con la estructura anteriormente explicada.
Se calcula el flujo máximo de este grafo. En el grafo resultante de calcular el flujo,las  calles a las cuales se puede alcanzar propagándonos desde $S$ se toman como solución.
