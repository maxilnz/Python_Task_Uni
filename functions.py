### Bibliotheken importieren

import sys
import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


### Variablen definieren

fehler = 'Bitte geben Sie einen gültigen Wert ein.' # Fehlermeldung
toleranzen = {'ptol': None, 'ntol': None}
daten = [] # Liste, in die die Daten geschrieben werden


### Main-Funktion

def main():

    while True:
        print('Wenn Sie die Eingabe abbrechen möchten, geben Sie "Exit" ein.') # Willkommensnachricht

        mw = get_numeric_input('Bitte geben Sie einen Messwert [mm] ein: ') # Messwert-Abfrage
        tol = get_numeric_input('Bitte geben Sie die dazugehörige Toleranz [mm] ein: ') # Toleranz-Abfrage

        plaus_mw_tol(mw, tol) # Plausibilitätsprüfung des Mittelwerts und der Toleranz bzgl. ihrem Verhältnis

        check_sym_tol(mw, tol) # Abfragen ob die Toleranz symmetrisch, negativ oder positiv angenommen werden soll

        gen_mw(mw, toleranzen) # 10000 Messwerte generieren und in eine Datei schreiben

        analyse_data(daten, mw, toleranzen) # Datenanalyse (Aufgabe d)


### Nur numerischen Input zulassen

def get_numeric_input(prompt):

    while True:
        user_input = get_input(prompt)

        try:
            if user_input != str(0):
                numeric_input = float(user_input) # Versuch den Input in einen Float umzuwandeln

                return abs(numeric_input)
            
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
    

### Plausibilität von Messwert und Toleranz prüfen

def plaus_mw_tol(mw, tol):
        
        while True:
            if abs(tol) * 100 >= abs(mw): # Wenn das Tausendfache des absoluten Wertes der Toleranz größer gleich dem Messwert ist
                    tgm = get_input('Achtung! Die von Ihnen eingegebene Toleranz ist verhältnismäßig groß. Möchten Sie trotzdem fortfahren [y/n]: ') # Warnung abfragen

                    if tgm.lower() == 'y':
                        print('Werte werden beibehalten.')

                        return # Funktion beenden

                    elif tgm.lower() == 'n':
                        print('Neue Eingabe wird gestartet.')

                        main() # Programm von vorne starten
                        return # Funktion beenden

                    else:
                        print(fehler)

            elif abs(tol) * 10000 <= abs(mw): # Wenn das Tausendfache des absoluten Wertes der Toleranz kleiner gleich dem Messwert ist
                tkm = get_input('Achtung! Die von Ihnen eingegebene Toleranz ist verhältnismäßig klein. Möchten Sie trotzdem fortfahren [y/n]: ') # Warnung abfragen

                if  tkm.lower() == 'y':
                    print('Werte werden beibehalten.')

                    return # Funktion beenden

                elif tkm.lower() == 'n':
                    print('Neue Eingabe wird gestartet.')

                    main() # Programm von vorne starten
                    return # Funktion beenden

                else:
                    print(fehler)

            else: # Falls keine Bedingung erfüllt ist
                break


### Symmetrische, negative oder positive Toleranz festlegen

def check_sym_tol(mw, tol):

    while True:

        if tol != 0: 
                pon = get_input(f'Im Moment wird die Toleranz als symmetrisch (+{abs(tol)}, -{abs(tol)}) angenommen. Falls Sie dies beibehalten möchten, geben Sie [sym] ein. Falls nicht, bestätigen Sie mit einem [+] oder einem [-], dass die Toleranz positiv oder negativ anzunehmen ist. ') # Art (symmetrisch, positiv oder negativ) der Toleranz abfragen

                if pon == '+':
                    toleranzen['ptol'] = abs(tol) # als positive Toleranz festlegen

                    print('Die Toleranz wird als positiv angenommen.')

                    ntoli = get_input('Möchten Sie eine negative Toleranz hinzufügen? [y/n]: ') # nach negativer Toleranz fragen

                    if ntoli.lower() == 'y':
                        toleranzen['ntol'] = get_numeric_input('Bitte geben Sie die gewünschte negative Toleranz [mm] ein: ') * -1 # als negative Toleranz festlegen

                        plaus_mw_tol(mw,toleranzen['ntol']) # Toleranz auf Plausibilität prüfen

                        print(f'Negative Toleranz {toleranzen['ntol']} hinzugefügt.')

                        return toleranzen # Funktion beenden

                    elif ntoli.lower() == 'n':
                        toleranzen['ntol'] = 0

                        print('Es wird keine negative Toleranz hinzugefügt.')

                        return toleranzen # Funktion beenden

                    else:
                        print(fehler)

                elif pon == '-':
                    toleranzen['ntol'] = abs(tol) * -1 # als negative Toleranz festlegen

                    print('Die Toleranz wird als negativ angenommen.')

                    ptoli = get_input('Möchten Sie eine positive Toleranz hinzufügen? [y/n]: ') # nach positiver Toleranz fragen

                    if ptoli.lower() == 'y':
                        toleranzen['ptol'] = get_numeric_input('Bitte geben Sie die gewünschte positive Toleranz [mm] ein: ') # als positive Toleranz festlegen

                        plaus_mw_tol(mw,toleranzen['ptol']) # Toleranz auf Plausibilität prüfen

                        print(f'Positive Toleranz {toleranzen['ptol']} hinzugefügt.')

                        return toleranzen # Funktion beenden

                    elif ptoli.lower() == 'n':
                        toleranzen['ptol'] = 0

                        print('Es wird keine positive Toleranz hinzugefügt.')

                        return toleranzen # Funktion beenden

                    else:
                        print(fehler)
                
                elif pon.lower() == 'sym':
                    print('Die Toleranz wird als symmetrisch angenommen.')

                    toleranzen['ptol'] = abs(tol)
                    toleranzen['ntol'] = abs(tol) * -1

                    return toleranzen # Funktion beenden

                else:
                    print(fehler)


### Messwerte generieren

def gen_mw(mw, toleranzen):
    global daten # Zugriff auf globale Variable
    daten = [] # Liste, in die die Daten geschrieben werden, leeren

    datei = open("Messwerte_a_d.txt", 'w')

    z = 0 # Zählvariable definieren

    for i in range(10000): # 10000 Messwerte der Liste hinzufügen
        wert = mw + ablese_fehler(toleranzen) + mw_ungenau_fehler(toleranzen) + fertigung_fehler(toleranzen)

        if z < 10: # Sicherstellen, dass Ausreiser nur in weniger als 0,1 % der Daten vorkommen
            ausreiser = ausreiser_fehler(toleranzen)

            if ausreiser: # nur wenn tatsächlich ein Ausreiser zurückgegeben wird
                wert += ausreiser

                z += 1

        wert = round(wert, 4)

        daten.append(wert) # zur Liste hinzufügen
        datei.write(str(wert) + '\n') # in Datei schreiben

    datei.close()

    print('Datei erfolgreich geschrieben.')

    return daten

### Ablesefehler

def ablese_fehler(toleranzen):
    ablese_f = random.uniform(toleranzen['ntol'], toleranzen['ptol']) * 0.2
    return ablese_f


### Messwertungenauigkeiten

def mw_ungenau_fehler(toleranzen):
    mw_ungenau_f = random.uniform(toleranzen['ntol'], toleranzen['ptol']) * 0.1
    return mw_ungenau_f


### Fertigungsfehler

def fertigung_fehler(toleranzen):
    fertigung_f = random.uniform(toleranzen['ntol'], toleranzen['ptol']) * 0.7
    return fertigung_f


### Ausreiser

def ausreiser_fehler(toleranzen):
    if random.randint(0, 1000) == 1: # Bedingung für einen Ausreiser
        ausreiser_f = random.randint(1,2) * random.uniform(toleranzen['ntol'], toleranzen['ptol'])
        return ausreiser_f
    
    else:
        return None


### Datenanalyse

def analyse_data(daten, mw, toleranzen):
    durchschnitt = np.mean(daten) # Durschnitt berechnen
    print(f'Durchschnittswert: {durchschnitt}')

    standardabw = np.std(daten) # Standardabweichung berechnen
    print(f'Standardabweichung: {standardabw}')

    max = np.max(daten) # Maximalwert berechnen
    print(f'Maximalwert: {max}')

    min = np.min(daten) # Minimalwert berechnen
    print(f'Minimalwert: {min}')

    # Plot von jedem Wert mit Durchschnittslinie und Markierung von Maximial- und Minimalwert
    plt.figure(figsize=(10, 5)) # Größe festlegen
    plt.plot(daten, label='Messdaten') # Plot

    plt.axhline(durchschnitt, color='red', linestyle='dashed', linewidth=1, label=f'Durchschnitt: {durchschnitt:.2f}') # Durchschnittslinie (Formatierung float mit 2 Dezimalstellen hinter dem Punkt)
    plt.axvspan(daten.index(max) - 250, daten.index(max) + 250, color = 'red', alpha = 0.5, label = 'Bereich Maximalwert') # Markiert den Bereich des Maximalwerts
    plt.axvspan(daten.index(min) - 250, daten.index(min) + 250, color = 'blue', alpha = 0.5, label = 'Bereich Minimalwert') # Markiert den Bereich des Minimalwerts
    plt.axhspan(mw + toleranzen['ntol'], mw + toleranzen['ptol'], color = 'brown', alpha = 0.5, label = 'Toleranzbereich') # Toleranzbereich farbig hinterlegen

    plt.title('Messdaten mit Durchschnittslinie') # Titel
    plt.xlabel('Datenpunkt') # x-Achsen-Bezeichnung
    plt.ylabel('Messwert [mm]') # y-Achsen-Bezeichnung
    plt.xlim(0, 10000) # Bereich der X-Achse formatieren
    plt.legend(loc = 'upper right', bbox_to_anchor=(1.1, 1.15)) # Legende einfügen und postionieren
    plt.show()

    ### Analysebogen

    ## Die ersten 100 Daten auswählen

    daten_100 = daten[1:100]

    ## Subplots erzeugen

    plt.figure(figsize=(20, 6)) # Größe festlegen

    # Histogramm
    plt.subplot(1, 2, 1) # erzeugt 1x2 Subplot (Histogramm an erster Stelle)

    plt.hist(daten_100, bins=30, color='skyblue', edgecolor='black') # erzeugt Histogramm mit 30 Balken

    plt.title('Histogramm') # Titel
    plt.xlabel('Messwert [mm]') # x-Achsen-Bezeichnung
    plt.ylabel('Anzahl der Datenpunkte') # y-Achsen-Bezeichnung

    # Poly-Fit
    plt.subplot(1, 2, 2) # erzeugt 1x2 Subplot (Poly-Fit an zweiter Stelle)

    x_100 = np.linspace(1,len(daten_100), len(daten_100)) # x-Werte, die für Annäherung benötigt werden
    p_100 = np.poly1d(np.polyfit(x_100, daten_100, 6)) # Annäherung mit Funktion sechsten Grades
    plt.plot(x_100, p_100(x_100), '-')

    plt.title('Verlauf des IST-Wertes') # Titel
    plt.xlabel('Datenpunkt / zeitlicher Verlauf') # x-Achsen-Bezeichnung
    plt.ylabel('Messwert [mm]') # y-Achsen-Bezeichnung    
    plt.grid(True) # fügt ein Raster hinzu

    plt.savefig('Analysebogen_QS_100.png') # Analysebogen als Bild speichern
    print('Bild gespeichert')

    ## Die ersten 1000 Daten auswählen

    daten_1000 = daten[1:1000]

    ## Subplots erzeugen

    plt.figure(figsize=(20, 6)) # Größe festlegen

    # Histogramm
    plt.subplot(1, 2, 1) # erzeugt 1x2 Subplot (Histogramm an erster Stelle)

    plt.hist(daten_1000, bins=30, color='skyblue', edgecolor='black') # erzeugt Histogramm mit 30 Balken

    plt.title('Histogramm') # Titel
    plt.xlabel('Messwert [mm]') # x-Achsen-Bezeichnung
    plt.ylabel('Anzahl der Datenpunkte') # y-Achsen-Bezeichnung

    # Poly-Fit
    plt.subplot(1, 2, 2) # erzeugt 1x2 Subplot (Poly-Fit an zweiter Stelle)

    x_1000 = np.linspace(1,len(daten_1000), len(daten_1000)) # x-Werte, die für Annäherung benötigt werden
    p_1000 = np.poly1d(np.polyfit(x_1000, daten_1000, 6)) # Annäherung mit Funktion sechsten Grades
    plt.plot(x_1000, p_1000(x_1000), '-')

    plt.title('Verlauf des IST-Wertes') # Titel
    plt.xlabel('Datenpunkt / zeitlicher Verlauf') # x-Achsen-Bezeichnung
    plt.ylabel('Messwert [mm]') # y-Achsen-Bezeichnung    
    plt.grid(True) # fügt ein Raster hinzu
    
    plt.savefig('Analysebogen_QS_1000.png') # Analysebogen als Bild speichern
    print('Bild gespeichert')
