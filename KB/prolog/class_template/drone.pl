% Fatto per rappresentare il drone

/* Classe drone
*
* Contiene i seguenti attributi:
* - nome: nome del drone
* - latitudine: indica la latitudine del drone
* - longitudine: indica la longitudine del drone
* - altitudine: indica l'altitudine del drone
* - velocita': velocita' massima drone
* - batteria: tempo di durata del drone
*/

drone(posizione(X, Y), altitudine(Z)).


% Regole per il movimento verticale del drone

salta(Drone, NuovaAltitudine) :-

    drone(Posizione, AltitudineAttuale),

    NuovaAltitudine is AltitudineAttuale + 1,

    retract(drone(Posizione, AltitudineAttuale)),

    assert(drone(Posizione, NuovaAltitudine)).


atterra(Drone) :-

    drone(Posizione, _),

    retract(drone(Posizione, _)),

    assert(drone(Posizione, 0)).


% Regola per il movimento orizzontale del drone

sposta(Drone, NuovaPosizione) :-

    drone(PosizioneAttuale, Altitudine),

    NuovaPosizione = posizione(X, Y),

    retract(drone(PosizioneAttuale, Altitudine)),

    assert(drone(NuovaPosizione, Altitudine)).