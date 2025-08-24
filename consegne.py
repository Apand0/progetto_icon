from msvcrt import kbhit
from os import path
from ontologie.osm_parser import carica_file
from KB.knowledge_base import KnowledgeBase
from KB.path_finding.A_asterisco import SearchProblemHiddenGraph
from KB.CSP.dd_CSP import DroneDeliveryCSP
from sklearn.externals import joblib
import pandas as pd

# search_problem = SearchProblemHiddenGraph(...)  
classification_model = joblib.load('modello_random_forest.sav')
# csp = DroneDeliveryCSP(kb, search_problem)  

print("\nProgetto ICON 24-25")
print("")
print("             DRONE INTELLIGENTE            ")
print("")
print("")

# Menu' principale
while True:
    print("Menu:")
    print("1. Carica file predefinito")
    print("2. Carica file XML")
    print("3. Esci")

    scelta = input("Inserisci il numero dell'opzione desiderata: ")

    if scelta == "1":
        carica_file(0)
    elif scelta == "2":
        carica_file(1)
    elif scelta == "3":
        quit()
    else:
        print("Scelta non valida. Riprova.")

# Implementa il codice per far partire il drone (ML)
scelta_nome = input("\nInserire Nome Drone: ")
scelta_vel = input("\nInserire Velocita' Drone: ")
scelta_batteria = input("\nInserire Durata Batteria: ")

# Richiedi il numero di pacchi da consegnare
numero_pacchi = int(input("Quanti pacchi ci sono da consegnare? "))

# Richiedi informazioni per ciascuna consegna
nuovi_dati = []
strada = []
for _ in range(numero_pacchi):
    strada = input("Inserire nome della strada della consegna: ")
    # Simula il valore delle precipitazioni per ciascuna consegna

drone=Drone(nome, scelta_batteria, speed)

# Inizializza la Knowledge Base e le altre componenti necessarie
kb = KnowledgeBase(strada, drone)

# Utilizza il modello di classificazione per fare previsioni sulle nuove consegne
previsioni = predizione_maltempo()

# Aggiungi le previsioni al DataFrame dei nuovi dati
nuovi_dati_df['predictions'] = previsioni

# Utilizza il CSP per pianificare le consegne
assegnazione_ottimale = csp.solve_csp()

# Visualizza le previsioni e l'assegnazione ottimale
print("\nPrevisioni per le nuove consegne:")
print(nuovi_dati_df[['strada', 'precipitazione', 'predictions']])
print("\nAssegnazione ottimale:")
print(assegnazione_ottimale)

effettuate, percorsi = drone.run(kb)

# Aggiorna la Knowledge Base con l'assegnazione ottimale e altri dati
# ...

punteggio = valutazione_efficacia(effettuate, percorsi)