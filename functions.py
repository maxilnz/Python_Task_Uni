### Bibliotheken importieren

import sys
import matplotlib.pyplot as plt
import numpy as np
import random


### Variablen definieren

fehler = 'Bitte geben Sie einen gültigen Wert ein.' # Fehlermeldung
fehler_500 = 'Die maximale Drehzahl muss mindestens 500 rpm betragen.' # Fehlermeldung Input maximale Drehzahl
fehler_05 = 'Die maximale Maschinenbelastung muss mindestens 0.5 kN betragen.' # Fehlermeldung Input maximale Maschinenbelastung
fehler_31 = 'Die Anzahl der Wartungen der Anlage darf maximal 31 betragen.' # Fehlermeldung Input Anzahl der Wartungen pro Monat

global drehzahl_daten
drehzahl_daten = []

global belastung_daten
belastung_daten = []

global dauer_daten
dauer_daten = []

global vorgang_daten
vorgang_daten = []


### Main-Funktion

def main():

    while True:
        print('Wenn Sie die Eingabe abbrechen möchten, geben Sie "Exit" ein.') # Willkommensnachricht

        n_max = get_numeric_input_500('Geben Sie bitte die maximale Drehzahl [rpm] ein: ') # Maximale Drehzahl abfragen
        f_max = get_numeric_input_05('Geben Sie bitte die maximale Belastung [kN] ein: ') # Maximale Belastung abfragen
        int_inst = get_numeric_input_31('Geben Sie bitte an, wie oft die Anlage pro Monat gewartet wird: ') # Instandhaltungsintervall abfragen

        sim_ablauf(n_max, f_max, int_inst) # Simuliert den gesamten Betrieb der Anlage für zwei Jahre

        analyse_data(drehzahl_daten, belastung_daten, dauer_daten, n_max, f_max) # erstellt die Plots für den gesamten Zeitraum
        analyse_data_100(drehzahl_daten[:100], belastung_daten[:100], dauer_daten[:100], n_max, f_max) # erstellt die Plots für die ersten 100 Daten
        analyse_data_1000(drehzahl_daten[:1000], belastung_daten[:1000], dauer_daten[:1000], n_max, f_max) # erstellt die Plots für die ersten 1000 Daten


        sys.exit()
        

### Nur numerischen Input für die maximale Drehzahl zulassen

def get_numeric_input_500(prompt):

    while True:
        user_input = get_input(prompt)

        try:
            numeric_input = int(user_input) # Versuch den Input in einen Integer umzuwandeln

            if numeric_input < 500: # Mindestwert Belastung
                print(fehler_500)
        
            else:
                return numeric_input

        except ValueError:
            print(fehler)


### Nur numerischen Input für die maximale Maschinenbelastung zulassen

def get_numeric_input_05(prompt):

    while True:
        user_input = get_input(prompt)

        try:
            numeric_input = float(user_input) # Versuch den Input in einen Float umzuwandeln

            if numeric_input < 0.5: # Mindestwert Belastung
                print(fehler_05)
        
            else:
                return numeric_input

        except ValueError:
            print(fehler)


### Nur numerischen Input für die Anzahl der Wartungen pro Monat zulassen

def get_numeric_input_31(prompt):

    while True:
        user_input = get_input(prompt)

        try:
            numeric_input = int(user_input) # Versuch den Input in einen Integer umzuwandeln

            if numeric_input < 32: # Mindestwert Belastung
                return numeric_input
        
            else:
                print(fehler_31)

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


### Ablauf-Funktion

def sim_ablauf(n_max, f_max, int_inst):

    dauer = 0

    while dauer < 730: # wird ausgeführt solange die Dauer kleiner als 730 Tage bzw. 2 Jahre ist

        dauer = sum(dauer_daten) # summiert die Dauer der Vorgänge bzw. Funktionen

        wahr_defekt = 0.2 * np.exp(-0.0475 * int_inst) + 0.005 # ermittelt die Wahrscheinlichkeit für einen Defekt in Abhängigkeit von der Anzahl der Wartungen pro Monat; max. 20%, min. 0,5% Wahrscheinlichkeit
        wahr_instand = int_inst / 31 # ermittelt die Wahrscheinlichkeit für eine Instandhaltung auf Basis der Anzahl der Wartungen pro Monat
        wahr_ruest = 0.05 # Annahme, dass die Wahrscheinlichkeit für Rüstzeit 5% beträgt
        wahr_betrieb = 1 - wahr_defekt - wahr_instand - wahr_ruest # ermittelt die Restwahrscheinlichkeit für den normalen Betrieb

        funktionen = [calc_betrieb(n_max, f_max), calc_defekt(), calc_instand(), calc_ruest()]
        wahrscheinlichkeiten = [wahr_betrieb, wahr_defekt, wahr_instand, wahr_ruest]

        gewaehlte_funktion = random.choices(funktionen, weights = wahrscheinlichkeiten, k = 1)[0] # wählt aus den Funktionen eine (k = 1) mit den entsprechenden Wahrscheinlichkeiten aus

        gewaehlte_funktion # führt die ausgewählte Funktion aus


### Normaler Betrieb

def calc_betrieb(n_max, f_max):

    drehzahl = random.randint(0, n_max) # Zufallszahl zwischen 0 und der Maximaldrehzahl
    belastung = round(random.uniform(0, f_max), 2) # Zufallszahl zwischen 0 und der Maximalbelastung
    dauer = round(random.uniform(0.1, 3), 2) # Dauer beträgt minimal 0.1 Tage und maximal 3 Tage

    drehzahl_daten.append(drehzahl) # fügt die Drehzahl der Liste hinzu
    belastung_daten.append(belastung) # fügt die Belastung der Liste hinzu
    dauer_daten.append(dauer) # fügt die Dauer der Liste hinzu
    vorgang_daten.append('B') # fügt den Vorgang der Liste hinzu


### Ausfallzeiten (aufgrund von Defekten)

def calc_defekt():

    drehzahl = 0
    belastung = 0
    dauer = round(random.uniform(0.01, 1), 2) # Dauer beträgt minimal 0.01 Tage und maximal 1 Tag

    drehzahl_daten.append(drehzahl) # fügt die Drehzahl der Liste hinzu
    belastung_daten.append(belastung) # fügt die Belastung der Liste hinzu
    dauer_daten.append(dauer) # fügt die Dauer der Liste hinzu
    vorgang_daten.append('D') # fügt den Vorgang der Liste hinzu


### Ausfallzeiten (aufgrund von Instandhaltungsarbeiten)

def calc_instand():

    drehzahl = 0
    belastung = 0
    dauer = round(random.uniform(0.05, 0.35), 2) # Dauer beträgt minimal 0.05 Tage und maximal 0,35 Tage

    drehzahl_daten.append(drehzahl) # fügt die Drehzahl der Liste hinzu
    belastung_daten.append(belastung) # fügt die Belastung der Liste hinzu
    dauer_daten.append(dauer) # fügt die Dauer der Liste hinzu
    vorgang_daten.append('I') # fügt den Vorgang der Liste hinzu


### Ausfallzeiten (aufgrund von Rüstzeit)

def calc_ruest():

    drehzahl = 0
    belastung = 0
    dauer = round(random.uniform(0.0075, 0.025), 2) # Dauer beträgt minimal 0.0075 Tage und maximal 0.025 Tage

    drehzahl_daten.append(drehzahl) # fügt die Drehzahl der Liste hinzu
    belastung_daten.append(belastung) # fügt die Belastung der Liste hinzu
    dauer_daten.append(dauer) # fügt die Dauer der Liste hinzu
    vorgang_daten.append('R') # fügt den Vorgang der Liste hinzu


### Daten über den gesamten Zeitraum von zwei Jahren analysieren und plotten

def analyse_data(drehzahl_daten, belastung_daten, dauer_daten, n_max, f_max):

    ## Dauer aus den einzelnen Vorgängen zur Gesamtzeit aufsummieren
    
    zeit = list(dauer_daten) # Liste dauer_daten in die Variable zeit kopieren
    
    for i in range(1, len(dauer_daten)):

        zeit[i] += zeit[i - 1] # Dauer eines Vorgangs mit dem vorherigen aufsummieren um die "Position" im Diagramm verwenden zu können

    x = list(zeit) # Liste zeit in die Variable x kopieren (für Diagramm)


    ## Zeiten aus einzelnen Vorgängen getrennt betrachten

    betriebs_zeit = list(zeit) # Liste zeit in die Variable betriebs_zeit kopieren
    letzte_betriebs_zeit = zeit[0] # Default-Wert für die letzte Betriebszeit

    ausfall_zeit = list(zeit) # Liste zeit in die Variable ausfall_zeit kopieren
    letzte_ausfall_zeit = zeit[0] # Default-Wert für die letzte Ausfallzeit

    defekt_zeit = list(zeit) # Liste zeit in die Variable defekt_zeit kopieren
    letzte_defekt_zeit = zeit[0] # Default-Wert für die letzte Rüstzeit

    instand_zeit = list(zeit) # Liste zeit in die Variable instand_zeit kopieren
    letzte_instand_zeit = zeit[0] # Default-Wert für die letzte Instandhaltungszeit

    ruest_zeit = list(zeit) # Liste zeit in die Variable ruest_zeit kopieren
    letzte_ruest_zeit = zeit[0] # Default-Wert für die letzte Rüstzeit

    n90_zeit = list(zeit) # Liste zeit in die Variable n90_zeit kopieren
    letzte_n90_zeit = zeit[0] # Default-Wert für die letzte Zeit mit Drehzahlen >= 0,9 * Maximaldrehzahl

    f90_zeit = list(zeit) # Liste zeit in die Variable f90_zeit kopieren
    letzte_f90_zeit = zeit[0] # Default-Wert für die letzte Zeit mit Belastungen >= 0,9 * Maximalbelastung

    for i in range(1, len(dauer_daten)):

        # Betriebszeit auslesen

        if drehzahl_daten[i] == 0: # wenn die Maschine nicht in Betrieb ist

            betriebs_zeit[i] = letzte_betriebs_zeit  # Wert betriebs_zeit bleibt auf dem Niveau der letzten Betriebszeit

        else:
            betriebs_zeit[i] = betriebs_zeit[i - 1] + dauer_daten[i] # aktuelle Betriebszeit setzt sich aus der vorherigen Betriebszeit und der Dauer der aktuellen Betriebsdauer zusammen
            letzte_betriebs_zeit = betriebs_zeit[i] # letzte Betriebszeit aktualisieren

        # Gesamte Ausfallzeit auslesen

        if vorgang_daten[i] == 'B': # wenn die Maschine in Betrieb ist

            ausfall_zeit[i] = letzte_ausfall_zeit # Wert ausfall_zeit bleibt auf dem Niveau der letzten Ausfallzeit

        else:
            ausfall_zeit[i] = ausfall_zeit[i - 1] + dauer_daten[i] # aktuelle Ausfallzeit setzt sich aus der vorherigen Ausfallzeit und der Dauer der aktuellen Betriebsdauer zusammen
            letzte_ausfall_zeit = ausfall_zeit[i] # letzte Ausfallzeit aktualisieren

        # Ausfallzeit durch Defekte auslesen

        if vorgang_daten[i] == 'D': # wenn die Maschine defekt ist

            defekt_zeit[i] = defekt_zeit[i - 1] + dauer_daten[i] # aktuelle Ausfallzeit durch Defekte setzt sich aus der vorherigen Ausfallzeit durch Defekt und der Dauer der aktuellen Ausfallzeit durch Defekte zusammen
            letzte_defekt_zeit = defekt_zeit[i] # letzte Ausfallzeit durch Defekte aktualisieren

        else:
            defekt_zeit[i] = letzte_defekt_zeit # Wert defekt_zeit bleibt auf dem Niveau der letzten Ausfallzeit durch Defekte

        # Ausfallzeit durch Instandhaltung auslesen

        if vorgang_daten[i] == 'I': # wenn die Maschine instandgehalten wird

            instand_zeit[i] = instand_zeit[i - 1] + dauer_daten[i] # aktuelle Ausfallzeit durch Instandhaltung setzt sich aus der vorherigen Ausfallzeit durch Instandhaltung und der Dauer der aktuellen Ausfallzeit durch Instandhaltung zusammen
            letzte_instand_zeit = instand_zeit[i] # letzte Ausfallzeit durch Instandhaltung aktualisieren

        else:
            instand_zeit[i] = letzte_instand_zeit # Wert instand_zeit bleibt auf dem Niveau der letzten Ausfallzeit durch Instandhaltung

        # Ausfallzeit durch Rüstzeit auslesen

        if vorgang_daten[i] == 'R': # wenn die Maschine gerüstet wird

            ruest_zeit[i] = ruest_zeit[i - 1] + dauer_daten[i] # aktuelle Ausfallzeit durch Rüsten setzt sich aus der vorherigen Ausfallzeit durch Rüsten und der Dauer der aktuellen Ausfallzeit durch Rüsten zusammen
            letzte_ruest_zeit = ruest_zeit[i] # letzte Ausfallzeit durch Rüsten aktualisieren

        else:
            ruest_zeit[i] = letzte_ruest_zeit # Wert ruest_zeit bleibt auf dem Niveau der letzten Ausfallzeit durch Rüsten

        # Zeit mit Drehzahlen >= 0,9 * Maximaldrehzahl

        if drehzahl_daten[i]  >= 0.9 * n_max: # wenn Drehzahl >= 0,9 * Maximaldrehzahl

            n90_zeit[i] = n90_zeit[i - 1] + dauer_daten[i] # aktuelle Zeit, in der Drehzahlen >= 0,9 * Maximaldrehzahl gilt, setzt sich aus der vorherigen Zeit und der aktuellen Dauer zusammen
            letzte_n90_zeit = n90_zeit[i] # letzte Zeit, in der Drehzahlen >= 0,9 * Maximaldrehzahl gilt, aktualisieren

        else:
            n90_zeit[i] = letzte_n90_zeit # Wert n90_zeit bleibt auf dem Niveau der letzten Zeit, in der Umdrehungen >= 0,9 * Maximaldrehzahl gilt

        # Zeit mit Belastungen >= 0,9 * Maximalbelastung

        if belastung_daten[i]  >= 0.9 * f_max: # wenn Belastungen >= 0,9 * Maximalbelastung

            f90_zeit[i] = f90_zeit[i - 1] + dauer_daten[i] # aktuelle Zeit, in der Belastungen >= 0,9 * Maximalbelastung gilt, setzt sich aus der vorherigen Zeit und der aktuellen Dauer zusammen
            letzte_f90_zeit = f90_zeit[i] # letzte Zeit, in der Belastungen >= 0,9 * Maximalbelastung gilt, aktualisieren

        else:
            f90_zeit[i] = letzte_f90_zeit # Wert f90_zeit bleibt auf dem Niveau der letzten Zeit, in der Belastungen >= 0,9 * Maximalbelastung gilt


    ## Gesamte Daten über die Zeit plotten

    fig, ax1 = plt.subplots()

    # Erster Graph

    ax1.set_xlabel('Tage')
    ax1.set_ylabel('Drehzahl [rpm]')
    ax1.plot(x, drehzahl_daten, drawstyle = 'steps', color = 'blue', label = 'Drehzahl [rpm]')
    ax1.tick_params(axis = 'y') # legt Standardparameter für y-Achse des ersten Graphen fest
    
    ax1.axhline(n_max, color = 'black', linestyle = 'dashed', linewidth = 1, label = f'Maximaldrehzahl: {n_max} rpm, Maximalbelastung: {f_max} kN') # Horizontale Linie zur Kenntlichmachung der Maximalwerte; da aufgrund der Skalierung beide Maximalwerte auf einer Höhe liegen, werden beide mit einer einzelnen Linie dargestellt
    ax1.legend(loc = 'upper right', bbox_to_anchor=(1, 1.1)) # Legende einfügen und positionieren

    # Zweiter Graph

    ax2 = ax1.twinx() # erstellt eine zweite Achse (für unterschiedliche Skalierung der beiden Achsen erforderlich)
    ax2.set_ylabel('Belastung [kN]')
    ax2.plot(x, belastung_daten, drawstyle = 'steps', color = 'red', label = 'Belastung [kN]')
    ax2.tick_params(axis = 'y') # legt Standardparameter für y-Achse des zweiten Graphen fest
    
    #ax2.axhline(f_max, color = 'red', linestyle = 'dashed', linewidth = 1, label = f'Maximalbelastung: {f_max}')
    ax2.legend(loc = 'upper right', bbox_to_anchor=(1, 1.1)) # Legende einfügen und positionieren

    plt.xlim(0, 750) # Begrenzung für die x-Achse
    plt.title('Drehzahl und Belastung')
    plt.show()


    ## Gesamte "Zeiten" über die Zeit plotten

    fig, ax3 = plt.subplots()
    ax3.set_xlabel('Zeit in Tagen')
    ax3.set_ylabel('Zeit in Tagen')

    # Betriebszeit
    
    ax3.plot(zeit, betriebs_zeit, drawstyle = 'steps', label = 'Gesamte Betriebszeit')

    # Gesamte Ausfallzeit

    ax3.plot(zeit, ausfall_zeit, drawstyle = 'steps', color = 'red', label = 'Gesamte Ausfallzeit')

    # Ausfallzeit durch Defekt

    ax3.plot(zeit, defekt_zeit, drawstyle = 'steps', color = 'orange', label = 'Ausfallzeit durch Defekte')

    # Ausfallzeit durch Instandhaltungsarbeiten

    ax3.plot(zeit, instand_zeit, drawstyle = 'steps', color = 'grey', label = 'Ausfallzeit durch Instandhaltung')

    # Ausfallzeit durch Rüsten

    ax3.plot(zeit, ruest_zeit, drawstyle = 'steps', color = 'purple', label = 'Ausfallzeit durch Rüsten')
    
    ax3.legend(loc = 'upper right', bbox_to_anchor=(0.25, 1)) # Legende einfügen und positionieren
    plt.xlim(0, 750) # Begrenzung für die x-Achse
    plt.title('Zustände der Maschine über die Zeit')
    plt.grid(True) # aktiviert das Raster
    plt.show()


    ## Gesamte "Zeiten", denen mind. 90% der Maximalwerte erreicht werden, über die Zeit plotten

    fig, ax4 = plt.subplots()
    ax4.set_xlabel('Zeit in Tagen')
    ax4.set_ylabel('Zeit in Tagen')

    # Drehzahlen >= 0.9 * Maximaldrehzahl

    ax4.plot(zeit, n90_zeit, drawstyle = 'steps', label = 'Drehzahl >= 90% der Maximaldrehzahl')

    # Belastungen >= 0.9 * Maximalbelastung

    ax4.plot(zeit, f90_zeit, drawstyle = 'steps', color = 'red', label = 'Maschinenbelastung >= 90% der Maximalbelastung')

    ax4.legend(loc = 'upper right', bbox_to_anchor=(0.4, 1)) # Legende einfügen und positionieren
    plt.xlim(0, 750) # Begrenzung für die x-Achse
    plt.title('Zeiten, in denen die Maschine mindestens 90% ihrer Maximaldrehzahl & -belastung erreicht')
    plt.grid(True) # aktiviert das Raster
    plt.show()


### Ersten 100 Daten analysieren und plotten

def analyse_data_100(drehzahl_daten, belastung_daten, dauer_daten, n_max, f_max):

    ## Dauer aus den einzelnen Vorgängen zur Gesamtzeit aufsummieren
    
    zeit = list(dauer_daten) # Liste dauer_daten in die Variable zeit kopieren
    
    for i in range(1, len(dauer_daten)):

        zeit[i] += zeit[i - 1] # Dauer eines Vorgangs mit dem vorherigen aufsummieren um die "Position" im Diagramm verwenden zu können

    x = list(zeit) # Liste zeit in die Variable x kopieren (für Diagramm)


    ## Zeiten aus einzelnen Vorgängen getrennt betrachten

    betriebs_zeit = list(zeit) # Liste zeit in die Variable betriebs_zeit kopieren
    letzte_betriebs_zeit = zeit[0] # Default-Wert für die letzte Betriebszeit

    ausfall_zeit = list(zeit) # Liste zeit in die Variable ausfall_zeit kopieren
    letzte_ausfall_zeit = zeit[0] # Default-Wert für die letzte Ausfallzeit

    defekt_zeit = list(zeit) # Liste zeit in die Variable defekt_zeit kopieren
    letzte_defekt_zeit = zeit[0] # Default-Wert für die letzte Rüstzeit

    instand_zeit = list(zeit) # Liste zeit in die Variable instand_zeit kopieren
    letzte_instand_zeit = zeit[0] # Default-Wert für die letzte Instandhaltungszeit

    ruest_zeit = list(zeit) # Liste zeit in die Variable ruest_zeit kopieren
    letzte_ruest_zeit = zeit[0] # Default-Wert für die letzte Rüstzeit

    n90_zeit = list(zeit) # Liste zeit in die Variable n90_zeit kopieren
    letzte_n90_zeit = zeit[0] # Default-Wert für die letzte Zeit mit Drehzahlen >= 0,9 * Maximaldrehzahl

    f90_zeit = list(zeit) # Liste zeit in die Variable f90_zeit kopieren
    letzte_f90_zeit = zeit[0] # Default-Wert für die letzte Zeit mit Belastungen >= 0,9 * Maximalbelastung

    for i in range(1, len(dauer_daten)):

        # Betriebszeit auslesen

        if drehzahl_daten[i] == 0: # wenn die Maschine nicht in Betrieb ist

            betriebs_zeit[i] = letzte_betriebs_zeit  # Wert betriebs_zeit bleibt auf dem Niveau der letzten Betriebszeit

        else:
            betriebs_zeit[i] = betriebs_zeit[i - 1] + dauer_daten[i] # aktuelle Betriebszeit setzt sich aus der vorherigen Betriebszeit und der Dauer der aktuellen Betriebsdauer zusammen
            letzte_betriebs_zeit = betriebs_zeit[i] # letzte Betriebszeit aktualisieren

        # Gesamte Ausfallzeit auslesen

        if vorgang_daten[i] == 'B': # wenn die Maschine in Betrieb ist

            ausfall_zeit[i] = letzte_ausfall_zeit # Wert ausfall_zeit bleibt auf dem Niveau der letzten Ausfallzeit

        else:
            ausfall_zeit[i] = ausfall_zeit[i - 1] + dauer_daten[i] # aktuelle Ausfallzeit setzt sich aus der vorherigen Ausfallzeit und der Dauer der aktuellen Betriebsdauer zusammen
            letzte_ausfall_zeit = ausfall_zeit[i] # letzte Ausfallzeit aktualisieren

        # Ausfallzeit durch Defekte auslesen

        if vorgang_daten[i] == 'D': # wenn die Maschine defekt ist

            defekt_zeit[i] = defekt_zeit[i - 1] + dauer_daten[i] # aktuelle Ausfallzeit durch Defekte setzt sich aus der vorherigen Ausfallzeit durch Defekt und der Dauer der aktuellen Ausfallzeit durch Defekte zusammen
            letzte_defekt_zeit = defekt_zeit[i] # letzte Ausfallzeit durch Defekte aktualisieren

        else:
            defekt_zeit[i] = letzte_defekt_zeit # Wert defekt_zeit bleibt auf dem Niveau der letzten Ausfallzeit durch Defekte

        # Ausfallzeit durch Instandhaltung auslesen

        if vorgang_daten[i] == 'I': # wenn die Maschine instandgehalten wird

            instand_zeit[i] = instand_zeit[i - 1] + dauer_daten[i] # aktuelle Ausfallzeit durch Instandhaltung setzt sich aus der vorherigen Ausfallzeit durch Instandhaltung und der Dauer der aktuellen Ausfallzeit durch Instandhaltung zusammen
            letzte_instand_zeit = instand_zeit[i] # letzte Ausfallzeit durch Instandhaltung aktualisieren

        else:
            instand_zeit[i] = letzte_instand_zeit # Wert instand_zeit bleibt auf dem Niveau der letzten Ausfallzeit durch Instandhaltung

        # Ausfallzeit durch Rüstzeit auslesen

        if vorgang_daten[i] == 'R': # wenn die Maschine gerüstet wird

            ruest_zeit[i] = ruest_zeit[i - 1] + dauer_daten[i] # aktuelle Ausfallzeit durch Rüsten setzt sich aus der vorherigen Ausfallzeit durch Rüsten und der Dauer der aktuellen Ausfallzeit durch Rüsten zusammen
            letzte_ruest_zeit = ruest_zeit[i] # letzte Ausfallzeit durch Rüsten aktualisieren

        else:
            ruest_zeit[i] = letzte_ruest_zeit # Wert ruest_zeit bleibt auf dem Niveau der letzten Ausfallzeit durch Rüsten

        # Zeit mit Drehzahlen >= 0,9 * Maximaldrehzahl

        if drehzahl_daten[i]  >= 0.9 * n_max: # wenn Drehzahl >= 0,9 * Maximaldrehzahl

            n90_zeit[i] = n90_zeit[i - 1] + dauer_daten[i] # aktuelle Zeit, in der Drehzahlen >= 0,9 * Maximaldrehzahl gilt, setzt sich aus der vorherigen Zeit und der aktuellen Dauer zusammen
            letzte_n90_zeit = n90_zeit[i] # letzte Zeit, in der Drehzahlen >= 0,9 * Maximaldrehzahl gilt, aktualisieren

        else:
            n90_zeit[i] = letzte_n90_zeit # Wert n90_zeit bleibt auf dem Niveau der letzten Zeit, in der Umdrehungen >= 0,9 * Maximaldrehzahl gilt

        # Zeit mit Belastungen >= 0,9 * Maximalbelastung

        if belastung_daten[i]  >= 0.9 * f_max: # wenn Belastungen >= 0,9 * Maximalbelastung

            f90_zeit[i] = f90_zeit[i - 1] + dauer_daten[i] # aktuelle Zeit, in der Belastungen >= 0,9 * Maximalbelastung gilt, setzt sich aus der vorherigen Zeit und der aktuellen Dauer zusammen
            letzte_f90_zeit = f90_zeit[i] # letzte Zeit, in der Belastungen >= 0,9 * Maximalbelastung gilt, aktualisieren

        else:
            f90_zeit[i] = letzte_f90_zeit # Wert f90_zeit bleibt auf dem Niveau der letzten Zeit, in der Belastungen >= 0,9 * Maximalbelastung gilt


    ## Gesamte Daten über die Zeit plotten

    fig, (ax1, ax3, ax4) = plt.subplots(3, 1, figsize = (10,15))

    # Erster Graph

    ax1.set_xlabel('Tage')
    ax1.set_ylabel('Drehzahl [rpm]')
    ax1.plot(x, drehzahl_daten, drawstyle = 'steps', color = 'blue', label = 'Drehzahl [rpm]')
    ax1.tick_params(axis = 'y') # legt Standardparameter für y-Achse des ersten Graphen fest
    
    ax1.axhline(n_max, color = 'black', linestyle = 'dashed', linewidth = 1, label = f'Maximaldrehzahl: {n_max} rpm, Maximalbelastung: {f_max} kN') # Horizontale Linie zur Kenntlichmachung der Maximalwerte; da aufgrund der Skalierung beide Maximalwerte auf einer Höhe liegen, werden beide mit einer einzelnen Linie dargestellt
    ax1.legend(loc = 'upper right', bbox_to_anchor=(1, 1.1)) # Legende einfügen und positionieren

    # Zweiter Graph

    ax2 = ax1.twinx() # erstellt eine zweite Achse (für unterschiedliche Skalierung der beiden Achsen erforderlich)
    ax2.set_ylabel('Belastung [kN]')
    ax2.plot(x, belastung_daten, drawstyle = 'steps', color = 'red', label = 'Belastung [kN]')
    ax2.tick_params(axis = 'y') # legt Standardparameter für y-Achse des zweiten Graphen fest
    
    #ax2.axhline(f_max, color = 'red', linestyle = 'dashed', linewidth = 1, label = f'Maximalbelastung: {f_max}')
    ax2.legend(loc = 'upper right', bbox_to_anchor=(1, 1.1)) # Legende einfügen und positionieren

    #ax1.xlim(0) # Begrenzung für die x-Achse
    ax1.set_title('Drehzahl und Belastung')


    ## Gesamte "Zeiten" über die Zeit plotten

    ax3.set_xlabel('Zeit in Tagen')
    ax3.set_ylabel('Zeit in Tagen')

    # Betriebszeit
    
    ax3.plot(zeit, betriebs_zeit, drawstyle = 'steps', label = 'Gesamte Betriebszeit')

    # Gesamte Ausfallzeit

    ax3.plot(zeit, ausfall_zeit, drawstyle = 'steps', color = 'red', label = 'Gesamte Ausfallzeit')

    # Ausfallzeit durch Defekt

    ax3.plot(zeit, defekt_zeit, drawstyle = 'steps', color = 'orange', label = 'Ausfallzeit durch Defekte')

    # Ausfallzeit durch Instandhaltungsarbeiten

    ax3.plot(zeit, instand_zeit, drawstyle = 'steps', color = 'grey', label = 'Ausfallzeit durch Instandhaltung')

    # Ausfallzeit durch Rüsten

    ax3.plot(zeit, ruest_zeit, drawstyle = 'steps', color = 'purple', label = 'Ausfallzeit durch Rüsten')
    
    ax3.legend(loc = 'upper right', bbox_to_anchor=(0.25, 1)) # Legende einfügen und positionieren
    #ax3.set_xlim(0) # Begrenzung für die x-Achse
    ax3.set_title('Zustände der Maschine über die Zeit')
    ax3.grid(True) # aktiviert das Raster


    ## Gesamte "Zeiten", denen mind. 90% der Maximalwerte erreicht werden, über die Zeit plotten

    ax4.set_xlabel('Zeit in Tagen')
    ax4.set_ylabel('Zeit in Tagen')

    # Drehzahlen >= 0.9 * Maximaldrehzahl

    ax4.plot(zeit, n90_zeit, drawstyle = 'steps', label = 'Drehzahl >= 90% der Maximaldrehzahl')

    # Belastungen >= 0.9 * Maximalbelastung

    ax4.plot(zeit, f90_zeit, drawstyle = 'steps', color = 'red', label = 'Maschinenbelastung >= 90% der Maximalbelastung')

    ax4.legend(loc = 'upper right', bbox_to_anchor=(0.4, 1)) # Legende einfügen und positionieren
    #ax4.set_xlim(0) # Begrenzung für die x-Achse
    ax4.set_title('Zeiten, in denen die Maschine mindestens 90% ihrer Maximaldrehzahl & -belastung erreicht')
    ax4.grid(True) # aktiviert das Raster

    plt.tight_layout() # damit sich nichts überschneidet
    plt.savefig('Maschinenanalyse_100.png') # Analyse speichern
    print('Bild gespeichert')
    plt.show() # Multiplot anzeigen
    

### Ersten 1000 Daten analysieren und plotten

def analyse_data_1000(drehzahl_daten, belastung_daten, dauer_daten, n_max, f_max):

    ## Dauer aus den einzelnen Vorgängen zur Gesamtzeit aufsummieren
    
    zeit = list(dauer_daten) # Liste dauer_daten in die Variable zeit kopieren
    
    for i in range(1, len(dauer_daten)):

        zeit[i] += zeit[i - 1] # Dauer eines Vorgangs mit dem vorherigen aufsummieren um die "Position" im Diagramm verwenden zu können

    x = list(zeit) # Liste zeit in die Variable x kopieren (für Diagramm)


    ## Zeiten aus einzelnen Vorgängen getrennt betrachten

    betriebs_zeit = list(zeit) # Liste zeit in die Variable betriebs_zeit kopieren
    letzte_betriebs_zeit = zeit[0] # Default-Wert für die letzte Betriebszeit

    ausfall_zeit = list(zeit) # Liste zeit in die Variable ausfall_zeit kopieren
    letzte_ausfall_zeit = zeit[0] # Default-Wert für die letzte Ausfallzeit

    defekt_zeit = list(zeit) # Liste zeit in die Variable defekt_zeit kopieren
    letzte_defekt_zeit = zeit[0] # Default-Wert für die letzte Rüstzeit

    instand_zeit = list(zeit) # Liste zeit in die Variable instand_zeit kopieren
    letzte_instand_zeit = zeit[0] # Default-Wert für die letzte Instandhaltungszeit

    ruest_zeit = list(zeit) # Liste zeit in die Variable ruest_zeit kopieren
    letzte_ruest_zeit = zeit[0] # Default-Wert für die letzte Rüstzeit

    n90_zeit = list(zeit) # Liste zeit in die Variable n90_zeit kopieren
    letzte_n90_zeit = zeit[0] # Default-Wert für die letzte Zeit mit Drehzahlen >= 0,9 * Maximaldrehzahl

    f90_zeit = list(zeit) # Liste zeit in die Variable f90_zeit kopieren
    letzte_f90_zeit = zeit[0] # Default-Wert für die letzte Zeit mit Belastungen >= 0,9 * Maximalbelastung

    for i in range(1, len(dauer_daten)):

        # Betriebszeit auslesen

        if drehzahl_daten[i] == 0: # wenn die Maschine nicht in Betrieb ist

            betriebs_zeit[i] = letzte_betriebs_zeit  # Wert betriebs_zeit bleibt auf dem Niveau der letzten Betriebszeit

        else:
            betriebs_zeit[i] = betriebs_zeit[i - 1] + dauer_daten[i] # aktuelle Betriebszeit setzt sich aus der vorherigen Betriebszeit und der Dauer der aktuellen Betriebsdauer zusammen
            letzte_betriebs_zeit = betriebs_zeit[i] # letzte Betriebszeit aktualisieren

        # Gesamte Ausfallzeit auslesen

        if vorgang_daten[i] == 'B': # wenn die Maschine in Betrieb ist

            ausfall_zeit[i] = letzte_ausfall_zeit # Wert ausfall_zeit bleibt auf dem Niveau der letzten Ausfallzeit

        else:
            ausfall_zeit[i] = ausfall_zeit[i - 1] + dauer_daten[i] # aktuelle Ausfallzeit setzt sich aus der vorherigen Ausfallzeit und der Dauer der aktuellen Betriebsdauer zusammen
            letzte_ausfall_zeit = ausfall_zeit[i] # letzte Ausfallzeit aktualisieren

        # Ausfallzeit durch Defekte auslesen

        if vorgang_daten[i] == 'D': # wenn die Maschine defekt ist

            defekt_zeit[i] = defekt_zeit[i - 1] + dauer_daten[i] # aktuelle Ausfallzeit durch Defekte setzt sich aus der vorherigen Ausfallzeit durch Defekt und der Dauer der aktuellen Ausfallzeit durch Defekte zusammen
            letzte_defekt_zeit = defekt_zeit[i] # letzte Ausfallzeit durch Defekte aktualisieren

        else:
            defekt_zeit[i] = letzte_defekt_zeit # Wert defekt_zeit bleibt auf dem Niveau der letzten Ausfallzeit durch Defekte

        # Ausfallzeit durch Instandhaltung auslesen

        if vorgang_daten[i] == 'I': # wenn die Maschine instandgehalten wird

            instand_zeit[i] = instand_zeit[i - 1] + dauer_daten[i] # aktuelle Ausfallzeit durch Instandhaltung setzt sich aus der vorherigen Ausfallzeit durch Instandhaltung und der Dauer der aktuellen Ausfallzeit durch Instandhaltung zusammen
            letzte_instand_zeit = instand_zeit[i] # letzte Ausfallzeit durch Instandhaltung aktualisieren

        else:
            instand_zeit[i] = letzte_instand_zeit # Wert instand_zeit bleibt auf dem Niveau der letzten Ausfallzeit durch Instandhaltung

        # Ausfallzeit durch Rüstzeit auslesen

        if vorgang_daten[i] == 'R': # wenn die Maschine gerüstet wird

            ruest_zeit[i] = ruest_zeit[i - 1] + dauer_daten[i] # aktuelle Ausfallzeit durch Rüsten setzt sich aus der vorherigen Ausfallzeit durch Rüsten und der Dauer der aktuellen Ausfallzeit durch Rüsten zusammen
            letzte_ruest_zeit = ruest_zeit[i] # letzte Ausfallzeit durch Rüsten aktualisieren

        else:
            ruest_zeit[i] = letzte_ruest_zeit # Wert ruest_zeit bleibt auf dem Niveau der letzten Ausfallzeit durch Rüsten

        # Zeit mit Drehzahlen >= 0,9 * Maximaldrehzahl

        if drehzahl_daten[i]  >= 0.9 * n_max: # wenn Drehzahl >= 0,9 * Maximaldrehzahl

            n90_zeit[i] = n90_zeit[i - 1] + dauer_daten[i] # aktuelle Zeit, in der Drehzahlen >= 0,9 * Maximaldrehzahl gilt, setzt sich aus der vorherigen Zeit und der aktuellen Dauer zusammen
            letzte_n90_zeit = n90_zeit[i] # letzte Zeit, in der Drehzahlen >= 0,9 * Maximaldrehzahl gilt, aktualisieren

        else:
            n90_zeit[i] = letzte_n90_zeit # Wert n90_zeit bleibt auf dem Niveau der letzten Zeit, in der Umdrehungen >= 0,9 * Maximaldrehzahl gilt

        # Zeit mit Belastungen >= 0,9 * Maximalbelastung

        if belastung_daten[i]  >= 0.9 * f_max: # wenn Belastungen >= 0,9 * Maximalbelastung

            f90_zeit[i] = f90_zeit[i - 1] + dauer_daten[i] # aktuelle Zeit, in der Belastungen >= 0,9 * Maximalbelastung gilt, setzt sich aus der vorherigen Zeit und der aktuellen Dauer zusammen
            letzte_f90_zeit = f90_zeit[i] # letzte Zeit, in der Belastungen >= 0,9 * Maximalbelastung gilt, aktualisieren

        else:
            f90_zeit[i] = letzte_f90_zeit # Wert f90_zeit bleibt auf dem Niveau der letzten Zeit, in der Belastungen >= 0,9 * Maximalbelastung gilt


    ## Gesamte Daten über die Zeit plotten

    fig, (ax1, ax3, ax4) = plt.subplots(3, 1, figsize = (10,15))

    # Erster Graph

    ax1.set_xlabel('Tage')
    ax1.set_ylabel('Drehzahl [rpm]')
    ax1.plot(x, drehzahl_daten, drawstyle = 'steps', color = 'blue', label = 'Drehzahl [rpm]')
    ax1.tick_params(axis = 'y') # legt Standardparameter für y-Achse des ersten Graphen fest
    
    ax1.axhline(n_max, color = 'black', linestyle = 'dashed', linewidth = 1, label = f'Maximaldrehzahl: {n_max} rpm, Maximalbelastung: {f_max} kN') # Horizontale Linie zur Kenntlichmachung der Maximalwerte; da aufgrund der Skalierung beide Maximalwerte auf einer Höhe liegen, werden beide mit einer einzelnen Linie dargestellt
    ax1.legend(loc = 'upper right', bbox_to_anchor=(1, 1.1)) # Legende einfügen und positionieren

    # Zweiter Graph

    ax2 = ax1.twinx() # erstellt eine zweite Achse (für unterschiedliche Skalierung der beiden Achsen erforderlich)
    ax2.set_ylabel('Belastung [kN]')
    ax2.plot(x, belastung_daten, drawstyle = 'steps', color = 'red', label = 'Belastung [kN]')
    ax2.tick_params(axis = 'y') # legt Standardparameter für y-Achse des zweiten Graphen fest
    
    #ax2.axhline(f_max, color = 'red', linestyle = 'dashed', linewidth = 1, label = f'Maximalbelastung: {f_max}')
    ax2.legend(loc = 'upper right', bbox_to_anchor=(1, 1.1)) # Legende einfügen und positionieren

    #ax1.xlim(0) # Begrenzung für die x-Achse
    ax1.set_title('Drehzahl und Belastung')


    ## Gesamte "Zeiten" über die Zeit plotten

    ax3.set_xlabel('Zeit in Tagen')
    ax3.set_ylabel('Zeit in Tagen')

    # Betriebszeit
    
    ax3.plot(zeit, betriebs_zeit, drawstyle = 'steps', label = 'Gesamte Betriebszeit')

    # Gesamte Ausfallzeit

    ax3.plot(zeit, ausfall_zeit, drawstyle = 'steps', color = 'red', label = 'Gesamte Ausfallzeit')

    # Ausfallzeit durch Defekt

    ax3.plot(zeit, defekt_zeit, drawstyle = 'steps', color = 'orange', label = 'Ausfallzeit durch Defekte')

    # Ausfallzeit durch Instandhaltungsarbeiten

    ax3.plot(zeit, instand_zeit, drawstyle = 'steps', color = 'grey', label = 'Ausfallzeit durch Instandhaltung')

    # Ausfallzeit durch Rüsten

    ax3.plot(zeit, ruest_zeit, drawstyle = 'steps', color = 'purple', label = 'Ausfallzeit durch Rüsten')
    
    ax3.legend(loc = 'upper right', bbox_to_anchor=(0.25, 1)) # Legende einfügen und positionieren
    #ax3.set_xlim(0) # Begrenzung für die x-Achse
    ax3.set_title('Zustände der Maschine über die Zeit')
    ax3.grid(True) # aktiviert das Raster


    ## Gesamte "Zeiten", denen mind. 90% der Maximalwerte erreicht werden, über die Zeit plotten

    ax4.set_xlabel('Zeit in Tagen')
    ax4.set_ylabel('Zeit in Tagen')

    # Drehzahlen >= 0.9 * Maximaldrehzahl

    ax4.plot(zeit, n90_zeit, drawstyle = 'steps', label = 'Drehzahl >= 90% der Maximaldrehzahl')

    # Belastungen >= 0.9 * Maximalbelastung

    ax4.plot(zeit, f90_zeit, drawstyle = 'steps', color = 'red', label = 'Maschinenbelastung >= 90% der Maximalbelastung')

    ax4.legend(loc = 'upper right', bbox_to_anchor=(0.4, 1)) # Legende einfügen und positionieren
    #ax4.set_xlim(0) # Begrenzung für die x-Achse
    ax4.set_title('Zeiten, in denen die Maschine mindestens 90% ihrer Maximaldrehzahl & -belastung erreicht')
    ax4.grid(True) # aktiviert das Raster

    plt.tight_layout() # damit sich nichts überschneidet
    plt.savefig('Maschinenanalyse_1000.png') # Analyse speichern
    print('Bild gespeichert')
    plt.show() # Multiplot anzeigen
    