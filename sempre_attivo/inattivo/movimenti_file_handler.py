import os

class MovementFileHandler:
    def __init__(self, filename):
        self.filename = filename

    def check_movement_name(self, movement_name):
        # Verifica se il file esiste
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                # Verifica se il nome del movimento è già presente nel file
                if movement_name in f.read():
                    print("Il nome del movimento è già presente nel file!")
                    return False
                else:
                    return True
        else:
            return True

    def add_movement_name(self, movement_name):
        # Aggiunge il nome del movimento al file
        with open(self.filename, 'a+') as f:
            f.write(movement_name + '\n')
        print("Il nome del movimento è stato aggiunto al file!")
