import os

class MovementNameFileHandler:
    def __init__(self, filename_):
        self.filename = os.path.join((os.path.abspath(os.getcwd()) + "\\assets\\"), filename_)

    def is_movement_name_available(self, movement_name):
        # Verifica se il file esiste se non esiste il nome può essere scritto
        if not os.path.isfile(self.filename):
            return True
        # Verifica se il nome del movimento è già presente nel file 
        # se non è presente il nome può essere scritto
        with open(self.filename, 'r') as f:
            return movement_name not in f.read()

    def add_movement_name(self, movement_name):
        # Aggiunge il nome del movimento al file
        with open(self.filename, 'a+') as f:
            f.write(movement_name + '\n')
        print("Il nome del movimento è stato aggiunto al file!")
