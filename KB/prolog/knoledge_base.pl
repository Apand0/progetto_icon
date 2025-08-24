% Importazione delle classi
:- include('setup.pl').

%%  Regole della base di conoscenza


/**
 * Calcola la distanza tra due nodi X e Y
 *
 * @param X: primo nodo
 * @param Y: secondo nodo
 * @param S: distanza tra i due nodi (viene restituito il risultato)
 */
distanza_nodi(X, Y, S) :- prop(X, latitudine, L1), prop(Y, latitudine, L2), 
                       prop(X, longitudine, G1), prop(Y, longitudine, G2), 
                       S is abs(L1 - L2 + G1 - G2).


/**
 * Restituisce la latitudine e longitudine di un nodo passato in input
 *
 * @param X: nodo di cui si vogliono conoscere le coordinate
 * @param L: latitudine 
 * @param G: latitudine 
 * 
 */
lat_lon(X, Latitudine, Longitudine) :- prop(X, latitudine, Latitudine), 
                                       prop(X, longitudine, Longitudine).

/** 
* Controlla che l'altezza dell'edificio non sia superiore all'altitudine del drone
* @param Altitudine: attuale altitudine del nodo
* @param Altezza: altezza dell'edificio
*/
controllo_altitudine(Altitudine, Altezza):- regola_and(Altitudine, Altezza), salta(drone, Altezza).

/*
* Controlla se il drone e' arrivato alla posizione di arrivo, se si il drone attera in quel punto
* @param X: posizione drone
* @param Y: posizione di arrivo
*/
controllo_arrivo(X, Y):- lat_lon(X, Latitudine, Longitudine),
                         lat_lon(Y, latitudine, longitudine), 
                         Latitudine=latitudine, Longitudine=longitudine,
                         atterra(drone).



/**
 * Restituisce gli edifici immediatamente vicini dell'edificio passato in input.
 * Due edifici sono immediatamente vicini se collegati dalla strada in input.
 *
 * @param Edificio: Edificio di cui si vogliono conoscere i vicini
 * @param Vicini: lista di edifici vicini (viene restituito il risultato)
 */
vicini_edificio(Edificio, Vicini) :- prop(Edificio, type, edificio), 
                                     prop(Edificio, strade, Strade), 
                                     vicini_strade_edificio(Edificio, Strade, Vicini).

vicini_strade_edificio(Edificio, [], Vicini) :- prop(Edificio, type, edificio), Vicini = [].
vicini_strade_edificio(Edificio, [S1|S2], Vicini) :- prop(S1, nodi, N1),
                                                     vicini_strade_edificio(Edificio, S2, Vicini3),
                                                     append(Vicini3, [Vicino1|Vicino2], Vicini).

/**
* Restituisce l'altezza dell'edificio passato in input.
* Verifichiamo se quello passato e' un edificio.
* 
* @param Edificio: identifica il nodo che vogliamo controllare e di cui vogliamo sapere l'altezza nel caso.
* @param Altezza: identifica l'altezza dell'edificio che vogliamo restituire.
*/
ritorno_altezza_edifici(Edificio, Altezza):- lat_lon(Edificio, Latitudine, Longitudine), 
                                             prop(Edificio, type, edificio),
                                             prop(Edificio, altezza, Altezza).

/**
* Metodo usato per ottenere una lista di edifici.
* 
* @param build_list: lista degli edifici.
*/

get_building_list(build_list):- find_all(Edificio, edificio(Edificio), build_list).