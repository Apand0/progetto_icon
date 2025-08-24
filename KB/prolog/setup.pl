% Importazione delle classi
:- include('class_template/edificio.pl')
:- include('class_template/drone.pl')

% Definizione relazione di tipo e sottoclasse
prop(X, type, C) :- prop(S, subClassOf, C), prop(X, type, S).

% Clausole di supporto (librerie)

position(_, [], _) :-
    !, fail.
position(Elem, [Elem|_], 1).
position(Elem, [_|Tail], Position) :- position(Elem, Tail, Position1), Position is Position1 + 1.


delete(_, [], []) :- !.
delete(Elem, [Elem|Tail], Result) :- !, delete(Elem, Tail, Result).
delete(Elem, [Head|Tail], [Head|Result]) :- \+ unify_with_occurs_check(Elem, Head), delete(Elem, Tail, Result).


get_first([], First) :- First = [].
get_first([S1|_], First) :- First = [S1].


inverti(Lista, Invertita) :- inverti(Lista, [], Invertita).
inverti([], Acc, Acc).
inverti([H|T], Acc, Invertita) :- inverti(T, [H|Acc], Invertita).

regola_and(X, Y):- X<Y, X=Y. 

% Rappresenta la connessione tra due nodi
connected(X, Y).

% Predicato che verifica se due edifici sono collegati 
are_connected(X, Y):- connected(X, Y); connected(Y, X).