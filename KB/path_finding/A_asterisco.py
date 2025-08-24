from KB.path_finding.librerie.ricerca_generica import Arc, Search_problem, AStarsearch
from typing import List, Dict

"""
A_asterisco consiste in:
    * una lista o un insieme di nodi
    * una lista o un insieme di archi
    * un nodo iniziale
    * una lista o un insieme di nodi obiettivo
    * un dizionario che mappa ogni nodo nel suo valore euristico
    * un dizionario che mappa ogni nodo nella sua posizione (x,y)
"""

class Node:
    def _init_(self, name: str, coordinates: Dict[str, float]):
        self.name = name
        self.coordinates = coordinates

class SearchProblemHiddenGraph(Search_problem):
    def _init_(self, prolog=None, start=None, goal_build=None, positions={}):
        self.prolog = prolog
        self.start = start
        self.goals = set(goal_build) if goal_build else set()
        self.positions = positions

    def start_node(self):
        """return del nodo iniziale"""
        return self.start
    
    def is_goal(self, node):
        """restituisce True se il nodo e' un goal"""
        return node in self.goals

    def neighbors(self, node, seconds_from_start=0):
        """restituisce i vicini del nodo"""
        neigh = self.prolog.vicini_edificio(node)
        arcs = []
        for item in neigh:
            dist, tempo = self.prolog.distanza_nodi_tempo(node, item, seconds_from_start, True)
            arcs.append(Arc(node, item, tempo, dist, None))
        return arcs

    def heuristic(self, node):
        """Restituisce il valore euristico del nodo n.
        Restituisce 0 se non ha sovrascritto hmap."""
        return self.prolog.euristica_nodi(node)
        
    def AStarsearch(self):
        return AStarsearch(self)
    
