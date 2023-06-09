import os
import sys
import shutil

class FileManager:
    def __init__(self):
        self.filename = 'nome_movimenti_mouse.txt'
    
    def create_assets_folder(self):
        if not os.path.exists('assets'):
            os.makedirs('assets')

    def create_coordinate_velocita_folders(self):
        if not os.path.exists(os.path.join('assets', 'coordinate')):
            os.makedirs(os.path.join('assets', 'coordinate'))
        if not os.path.exists(os.path.join('assets', 'velocita')):
            os.makedirs(os.path.join('assets', 'velocita'))

    def create_name_movements_file(self):
        movements_file = os.path.join(os.getcwd(), 'assets', self.filename)
        print(movements_file)
        if not os.path.isfile(movements_file):
            with open(movements_file, 'w') as f:
                f.write('')
        return movements_file

    def add_current_folder_to_path(self):
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    def clean__pycache__only_for_develop(self):
        cartella = 'C:\\programmi\\script_python\\sempre_attivo\\inattivo\\__pycache__\\'
        # Cancella tutto nella cartella
        shutil.rmtree(cartella)





