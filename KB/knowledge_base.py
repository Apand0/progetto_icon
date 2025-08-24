import datetime
from symbol import atom
from unittest.mock import patch
from winreg import QueryInfoKey
from pyswip import Prolog
from math import atan2, cos, dist, radians, sin, sqrt
from KB.path_finding.A_asterisco import SearchProblemHiddenGraph
from KB.CSP.dd_CSP import DroneDeliveryCSP
from apprendimento_supervisionato.classification import random_forest
from drone_phython import Drone
import random
import pickle

class knowledge_base():
    def iniz(self, istanza_drone, consegne):
        self.prolog = Prolog()
        self.prolog.consult("KB/prolog/knowledge_base.pl",catcherrors=False)
        with open('apprendimento_supervisionato/modelli/classification.sav', 'rb') as pickle_file:
            self.classification = pickle.load(pickle_file)
        self.drone = istanza_drone
        self.package_destinations = consegne
        edifici=[]
        query_edificio="prop(Edificio, nodo, 1)"
        for atom in self.prolog.query(query_edificio):
            edifici.append(atom["Edifici"])
        csp=DroneDeliveryCSP(self, istanza_drone.max_battery, 5)
        assegnazione_ottimale=csp.solve_csp()

    def traccia_percorso(self):
        self.Search_problem=SearchProblemHiddenGraph(self.package_destinations, self)
        self.nodo_goal = self.package_destinations
        path=[]
        risoluzione=False
        query="prob("+self.package_destinations+",type,edificio)"
        for atom in self.prolog.query(query):
            risoluzione=True

        if not risoluzione:
            return path,0
        path,tempo=self.Search_problem.a_star_search()
        path.reverse()
        return path, tempo

    def salta(self):
        # Regola per il movimento verticale del drone
        query = "lat_lon("+self+", Latitudine, Longitudine)"
        lat, lon = self.prolog.query(query)
        lat = lat + 1
        lon = lon + 1
        # per renderlo piu' perfomante si potrebbe controllare in che verso si sta muovendo il drone, 
        # dato che in questo caso si sta controllando solo la latitudine, ho fatto cosi' perche' ho ipotizzato 
        # che un edificio sara' sempre abbastanza grande da poterlo prendere aumentando la latitudine e la longitudine di 1
        query="ritorno_altezza_edifici("+lat+lon+", Altezza)"
        altezza=self.prolog.query(query)
        query = "controllo_altitudine(Altitudine, "+altezza+")"
        self.prolog.query(query)

    def atterra(self, i):
        # Regola per atterrare il drone
        for atom in self.package_destinations:
            query = "controllo_arrivo("+self+", "+atom+")"
            self.prolog.query(query)
        for atom in self.prolog.query(query):
            risoluzione=True
        if risoluzione==True:
            self.move_down()
            i=i+1
        return i

    def sposta(self, nuova_posizione):
        # Regola per il movimento orizzontale del drone
        effettuate = 0
        query = f"sposta(Drone, {nuova_posizione}), drone(Drone, Altitudine)"
        self.prolog.query(query)
        for atom in self.prolog.query(query):
            risoluzione=True
        if risoluzione==True:
            # c'e' da fare controllo su come si muove (andare a dx o sx) oppure avanti e indietro
            self.move_forward()
            effettuate = self.atterra(effettuate)
            self.salta()
        
        

    def distanza_nodi_tempo(self, X, Y, tempo_partenza=0, in_tempo=True):
        '''
        Metodo distanza_nodi
        -------------------
        Dati di input
        --------------
        X: primo nodo
        Y: secondo nodo
        tempo_partenza: tempo trascorso dall'inizio del percorso
        in_tempo: se True aggiunge il tempo al drone

        Dati di output
        -------------- 
        distanza: distanza tra i due nodi
        '''
        distanza = 0
        velocita = self.velocita
        radius = 6371

        query = "lat_lon("+X+", L, G)"
        for atom in self.prolog.query(query):
            lat1 = atom["L"]
            lon1 = atom["G"]

        query = "lat_lon("+Y+", L, G)"
        for atom in self.prolog.query(query):
            lat2 = atom["L"]
            lon2 = atom["G"]


        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = (sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2))
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distanza = radius * c * 1000


        # converte km in secondi
        m_s = velocita / 3.6
        tempo = distanza / m_s

        distanza = self.total_delivery_time_within_battery(tempo, in_tempo)

        seconds_from_start += tempo

        if in_tempo:
            return distanza, tempo
        else:
            in_tempo = False 
            return distanza, 0

    def euristica_nodi(self, X):
        '''
        Metodo euristica_nodi
        -------------------
        Dati di input
        --------------
        X: nodo di cui si vuole conoscere l'euristica(distanza dal nodo di arrivo)

        Dati di output
        -------------- 
        euristica: euristica del nodo passato in input
        '''
        dist, tempo = self.distanza_nodi_tempo(X, self.nodo_goal, 0, False)
        return dist

    def lista_strade(self):
        '''
        Metodo lista_strade
        -------------------
        Dati di output
        -------------- 
        strade: lista contenente tutte le strade presenti nella KB
        '''
        strade = []

        query = "prop(X, type, strada)"
        for atom in self.prolog.query(query):
            if(isinstance(atom["X"], str)):
                strade.append(atom["X"])

        return strade
    

    def valutazione_efficacia(self, percorsi_effettuati, consegne_raggiunte):
    
        '''
        Valuta l'efficacia del drone in base ai percorsi effettuati e alle consegne raggiunte.

        :percorsi_effettuati: Numero totale di percorsi effettuati dal drone.
        :consegne_raggiunte: Numero totale di consegne raggiunte con successo.
        :return: Un punteggio che rappresenta l'efficacia del drone.
    
        '''

        # Assicurati che i valori siano non negativi
        percorsi_effettuati = max(0, percorsi_effettuati)
        consegne_raggiunte = max(0, consegne_raggiunte)

        # I coefficienti possono essere regolati in base all'importanza relativa dei due parametri
        coefficiente_percorsi = 0.7
        coefficiente_consegne = 0.3

        # Calcola il punteggio totale
        punteggio = (coefficiente_percorsi * percorsi_effettuati) + (coefficiente_consegne * consegne_raggiunte)

        return punteggio


    def predizione_maltempo(self):
        # Ottieni la data locale
        data = datetime.datetime.now()        

        # Costruisci il vettore di input
        X = [data.day, data.month, data.hour]

        # Normalizza il vettore di input
        X = self.scaler.transform(X)

        # Esegui la predizione con il modello Random Forest
        predizione = self.random_forest(X)

        return predizione