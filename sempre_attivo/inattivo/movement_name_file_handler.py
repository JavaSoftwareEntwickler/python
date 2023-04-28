import os
from os.path import exists

class MovementNameFileHandler:
    def __init__(self, filename_):
        self.path=os.path.abspath((os.getcwd()) + "\\assets")
        self.filename = self.path + "\\" +filename_
        print(self.filename)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            f = open(self.filename, 'w+')
            f.close()
            

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
    
    def get_path_file_name(self):
        return self.filename;

