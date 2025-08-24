from os import name
import os
import xml.etree.cElementTree as ET
from tkinter import Tk, filedialog

def carica_file(locale=0):
    '''
    Metodo carica_file
    -------------------
    Dati di input
    --------------

      locale: lindica se il file xml da analizzare deve essree quello preimpostato o caricato dalla macchina locale

    -------------- 
    Dati di output
    -------------- 

      Genera i file delle clausole prolog per la nostra KB

    '''

    if locale == 1:
        root = Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        filename = filedialog.askopenfilename()
        tree = ET.parse(filename)
    else:
        tree = ET.parse('ontologie/mappa/molfetta.xml')

root = tree.getroot()
allnodes = root.findall('node')
lista_edifici = []

for node in allnodes:
    is_building = False
    building_name = ""
    for tag in node.findall('tag'):
        if tag.attrib['k'] == 'building':
            is_building = True
        elif tag.attrib['k'] == 'name':
            building_name = tag.attrib['v']

    if is_building:
        edificio = {
            "id": "nodo_" + node.get('id'),
            "lat": node.get('lat'),
            "lon": node.get('lon'),
            "name": building_name
        }
        lista_edifici.append(edificio)

for node in allnodes:
        for strade in lista_strade:
            if "nodo_"+node.attrib['id'] in strade["nodi"]:

                if node.get('id') in lista_id_semafori:
                    semaforo = node.get('id')
                else:
                    semaforo = ""
                nome_strada = strade["name"]
                nome_strada = pulisci_stringa(nome_strada)
                
                nodo_strada_i = {
                    "id": "nodo_"+node.get('id'),
                    "lat": node.get('lat'),
                    "lon": node.get('lon'),
                    "strade": [nome_strada],
                }

                if nodo_strada_i["id"] in lista_dati_nodi_strada:
                    old_nodo = lista_dati_nodi_strada[nodo_strada_i["id"]]
                    nodo_strada_i["strade"] = old_nodo["strade"] + nodo_strada_i["strade"]

                lista_dati_nodi_strada[nodo_strada_i["id"]] = nodo_strada_i


with open("KB/prolog/class_template/edificio.pl", "r") as f:
        contents = f.readlines()

# strada
        
strada = ""
for item in lista_strade:
    name = item["name"]
    highway = item["highway"]
    speed = item["speed"]
    lanes = item["lanes"]

# edificio
        
edificio=""
for item in lista_edifici:
     name = item["name"]
     height = item["height"]
     lat = item["lat"]
     lon = item["lon"]

if not os.path.exists("KB/prolog/class_template"):
        os.makedirs("KB/prolog/class_template")

with open("KB/prolog/class_template/edificio.pl", "w") as f:
        contents = "".join(contents)
        f.write(contents)