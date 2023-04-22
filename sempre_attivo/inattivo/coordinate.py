from pynput import mouse
import time
import os

class MouseCoordinates:


    def __init__(self, duration, nomeFileCoordinate, nomeFileVelocita):
        self.duration = duration
        self.nomeFileCoordinate = nomeFileCoordinate
        self.nomeFileVelocita = nomeFileVelocita
        self.coordinate_path = self.path_file_coordinate()
        self.velocita_path = self.path_file_velocita()
        print(f'ecco il path coordinate: {self.coordinate_path}e il path delle velocita: {self.velocita_path}####')
    
    def path_file_coordinate(self):
        """
        Restituisce il path corrente del file delle coordinate
        """
        return os.path.join((os.path.abspath(os.getcwd()) + "\\assets\\"), self.nomeFileCoordinate)

    def path_file_velocita(self):
        """
        Restituisce il path corrente del file delle velocità
        """
        return os.path.join((os.path.abspath(os.getcwd()) + "\\assets\\"), self.nomeFileVelocita)
        
    def get_coordinates_and_velocities(self):
        """
        Restituisce una lista di tuple contenenti le coordinate del mouse e la velocità durante
        l'arco di tempo specificato (in secondi).
        """
        coordinates = []
        velocities = []

        def on_move(x, y):
            coordinates.append((x, y))
            velocities.append((time.time(), x, y))

        with mouse.Listener(on_move=on_move) as listener:
            start_time = time.time()
            while time.time() - start_time < self.duration:
                pass

        listener.stop()

        return coordinates, velocities

    def save_coordinates(self, coordinates):
        """
        Salva le coordinate in un file di testo con il percorso specificato.
        """
        with open(self.coordinate_path, "w") as f:
            for x, y in coordinates:
                f.write(f"{x},{y}\n")
        num_lines = len(coordinates)
        print(f"Coordinate salvate in {self.coordinate_path}")
        return num_lines

    def save_velocities(self, velocities):
        """
        Salva le velocità in un file di testo con il percorso specificato.
        """
        with open(self.velocita_path, "w") as f:
         for timestamp, x, y in velocities:
            if len(velocities) > 1:
                prev_timestamp, prev_x, prev_y = velocities[velocities.index((timestamp, x, y)) - 1]
                elapsed_time = timestamp - prev_timestamp
                if elapsed_time > 0:
                    distance = ((x - prev_x) ** 2 + (y - prev_y) ** 2) ** 0.5
                    velocity = distance / elapsed_time
                    f.write(f"{velocity}\n")
        num_lines = len(velocities)
        print(f"Velocità salvate in {self.velocita_path}")
        return num_lines

    def check_files(self, coordinates_length, velocities_length):
        """
        Controlla se i file delle coordinate e delle velocità hanno lo stesso numero di righe
        nel caso contrario aggiunge le righe mancanti
        """
        print(f'coordinate totali : {coordinates_length} velocita totali :{velocities_length}')
        if coordinates_length == velocities_length:
            return
        elif coordinates_length > velocities_length:
            quantita_righe = coordinates_length - velocities_length
            cancella_righe_di_troppo(self.coordinate_path, quantita_righe)
            #self.aggiungi_righe_mancanti("V", quantita_righe)
        else:
            quantita_righe = velocities_length - coordinates_length
            cancella_righe_di_troppo(self.velocita_path, quantita_righe)
            #self.aggiungi_righe_mancanti("C", quantita_righe)
    
    def cancella_righe_di_troppo(self, file_to_open, righe_to_delete):
       
        righe = open(file_to_open, r).readlines()
        while righe_to_delete > 0:
            print(f'righe da cancellare: {righe_to_delete}')
            del righe[-1]
            righe_to_delete -= 1
        open(file_to_open, w).writelines(righe)
        
    def aggiungi_righe_mancanti(self, file_name, quantita_righe):
        """
        Aggiunge righe mancanti al file 
        """
        print(quantita_righe)
        if file_name == "V":
            with open(self.velocita_path, "r") as f:
                lines = f.readlines()
            last_lines = lines[-quantita_righe:]
            with open(self.velocita_path, "a") as f:
                for line in last_lines:
                    f.write(line)
        elif file_name == "C":
            with open(self.coordinate_path, "r") as f:
                lines = f.readlines()
            last_lines = lines[-quantita_righe:]
            with open(self.coordinate_path, "a") as f:
                for line in last_lines:
                    f.write(line)
