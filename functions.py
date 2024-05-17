### Bibliotheken importieren

import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import truncnorm
from collections import Counter


### Variablen definieren

fehler = 'Bitte geben Sie einen Wert zwischen 1 und 6 ein.' # Fehlermeldung
anz = 1000 # Anzahl der Studenten


### Main-Funktion

def main():

    while True:
        print('Wenn Sie die Eingabe abbrechen möchten, geben Sie "Exit" ein.') # Willkommensnachricht

        ew = get_numeric_input('Geben Sie bitte die mittlere Note (Erwartungswert) ein: ') # Erwartungswert abfragen

        plot_diag(gen_noten(ew, choose_standardwert(ew), anz), ew) # Diagramm plotten (dazu werden erst die Noten generiert)


### Nur numerischen Input zulassen

def get_numeric_input(prompt):

    while True:
        user_input = get_input(prompt)

        try:
            numeric_input = float(user_input) # Versuch den Input in einen Float umzuwandeln

            if 1 <= numeric_input <= 6: # Notenbereich
                return numeric_input
        
            else:
                print(fehler)

        except ValueError:
            print(fehler)


### User-Input erfassen

def get_input(prompt):
    
    while True:
        user_input = input(prompt)

        if user_input.lower() == 'exit': # prüft bei jedem Input ob der User mit 'Exit' das Programm verlassen möchte
            sys.exit()

        elif user_input.strip(): # prüft, ob der User etwas eingegeben hat
            return user_input

        else:
            print(fehler)


### Standardabweichung in Abhängigkeit vom Erwartungswert wählen

def choose_standardwert(erwartungswert): # Wählt die Standardabweichung in Abhängigkeit des Erwartungswerts um eine realistische Verteilung darzustellen
    if erwartungswert >= 4:
        sa = 0.7

    elif erwartungswert >= 3:
        sa = 0.5

    else:
        sa = 0.3

    return sa


### Noten erzeugen

def gen_noten(erwartungswert, standardabweichung, anzahl):
    a, b = (1 - erwartungswert) / standardabweichung, (6 - erwartungswert) / standardabweichung # Bereich der Normalverteilung definieren, die zwischen 1 und 6 liegt
    trunc_normal = truncnorm(a, b, erwartungswert, standardabweichung) # trunkierte / gestutze Normalverteilung, da Noten von 1 bis 6 gehen und adernfalls bei einem Erwartungswert von z. B. 6 Noten > 6 errechnet werden
    
    noten = trunc_normal.rvs(anzahl) # Zufällige Noten aus der Normalverteilung generieren

    for i in range(len(noten)):
        noten[i] = round(noten[i], 1) # Noten auf eine Nachkommastelle runden

    noten_anzahl = Counter(noten) # erstellt Dictionary mit der Anzahl jeder Note
    noten_anzahl = dict(sorted(noten_anzahl.items())) # sortiert das Dictionary damit später ein Plot erzeugt werden kann

    return noten_anzahl # Noten in Dictionary zurückgeben


### Diagramm erzeugen

def plot_diag(noten, erwartungswert):
    plt.figure(figsize=(10,6)) # Größe des Diagramms festlegen

    # Balkendiagramm erzeugen
    x = list(noten.keys()) # Liste mit den Schlüsselwörtern (Noten) des Dictionarys erzeugen
    y = list(noten.values()) # Liste mit den Werten (Anzahl der Noten) des Dictionarys erzeugen
    
    plt.bar(x , y, 0.1, color='skyblue', edgecolor='black') # Plot mit 0.1 Balkenbreite
    plt.axvline(erwartungswert, color = 'black', linestyle = 'dashed', linewidth = 1, label = f'Erwartungswert: {erwartungswert:.2f}') # Erwartungswert einzeichnen (Formatierung float mit 2 Dezimalstellen hinter dem Punkt)
    
    # Polynom-Fit 
    p = np.poly1d(np.polyfit(x, y, 3)) # Funktion dritten Grades den Werten annähern
    plt.plot(x, p(x), color = 'red') # Funktion plotten
    
    plt.xticks(np.arange(1,7)) # X-Achsen-Skala auf 1 bis 6 setzen
    plt.xlim(1,6) # X-Achse genau von 1 bis 6 begrenzen
    plt.ylim(0) # Y-Achse nach unten hin wegen Polynom-Funktion begrenzen

    plt.xlabel('Note') # X-Achsen-Beschriftung
    plt.ylabel('Anzahl der Studierenden') # Y-Achsen-Beschriftung
    plt.title('Notenverteilung') # Titel 

    plt.legend()
    plt.show()
