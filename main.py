### Eigene Files importieren

import functions # Funktionen importieren

### Main-Funktion aufrufen

if __name__ == '__main__':
    try:
        functions.main() # Main-Funktion aufrufen

    except SystemExit:
        print('Das Programm wurde beendet')
