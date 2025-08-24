from constraint import Problem, AllDifferentConstraint
from KB.CSP.lib.CSP_problem import Variable
from KB.CSP.lib.CSP_SLS import SLSearcher
from datetime import datetime

"""
Una classe che si occupa di controllare i vincoli del CSP
* Vincoli hard: riuscire a consegnare i pacchi nel tempo massimo prefissato di batteria
* Vincoli hard: andare una sola volta nel luogo di consegna
* Vincoli soft: massimizzare il numero delle consegne
"""

class DroneDeliveryCSP:

    def _init_(self, max_deliveries_per_day):
        self.max_battery = self.scelta_batteria
        self.max_deliveries_per_day = max_deliveries_per_day
        self.buildings = list(self.prolog.get_building_list())
        self.problem = Problem()
        self.build_csp()

    def build_csp(self):
        # Definizione delle variabili decisionali
        for building in self.buildings:
            self.problem.addVariable(building, self.package_destinations)

        # Definizione del dominio per ogni variabile (1 per consegnato, 0 altrimenti)
        self.problem.addConstraint(AllDifferentConstraint())

        # Vincoli hard
        self.problem.addConstraint(self.at_most_one_delivery, self.buildings)
        self.problem.addConstraint(self.total_delivery_time_within_battery, self.buildings)

        # Vincoli soft
        self.problem.addConstraint(self.one_delivery_per_building, self.buildings)

        self.problem.addConstraint(self.delivery_time_constraint, self.buildings)

    # Vincoli soft, massimizzare il numero delle consegne
    def maximize_deliveries(*args, self):
            # La logica per valutare l'efficacia delle consegne
            return sum(1 for building in args if building != "undelivered")

    self.problem.addConstraint(maximize_deliveries, self.buildings)
            
    def at_most_one_delivery(self, *args):
        # Vincolo hard: Ad ogni edificio puo' essere consegnato un pacco al massimo una volta
        return sum(args) <= 1

    def total_delivery_time_within_battery(self, tempo, in_tempo):
        # Vincolo hard: Tempo totale di consegna (e ritorno) non deve superare la batteria del drone
        if in_tempo:
            tempo_batteria = self.batteria_rimanente - tempo
            if tempo_batteria < 0:
                return float('inf'), tempo  # Batteria insufficiente, restituisci una distanza infinita
            else:
                self.batteria_rimanente = tempo_batteria

    def one_delivery_per_building(self, *args):
        # Vincolo soft: Ad ogni edificio va fatta una consegna alla volta
        return sum(args) == 1

    def delivery_time_constraint(self, *args):
        # Vincolo: Se l'orario e' compreso tra l'1:00 e le 8:00, non consegnare
        current_hour = datetime.now().hour
        if 1 <= current_hour <= 8:
            return sum(args) == 0  # Non consegnare se l'orario e' tra l'1:00 e le 8:00
        else:
            return True

    def solve_csp(self):
        csp = self.create_csp()
        solutions = csp.getSolutions()
        # Sceglie la scelta migliore basata sul criterio di ottimizzazione
        best_solution = max(solutions, key=lambda x: x['_objective'])
        return best_solution