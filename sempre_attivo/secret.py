import sys
import os
from inattivo.coordinate import MouseCoordinate
from inattivo.movement_name_file_handler import MovementNameFileHandler
from inattivo.file_manager import FileManager
import math
import tkinter as tk
import threading
import time
import random
from pynput import mouse, keyboard
import pyautogui

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        path_attuale = os.getcwd()  #automaticamente il path di dove si trova il progetto
        sys.path.append(path_attuale)
        # Inizializzazione della finestra grafica
        self.title("Start/Stop Program")
        self.geometry("200x150")
        
        # Creazione dei pulsanti e loro disposizione
        self.btn_start = tk.Button(self, text="Start", command=self.start)
        self.btn_start.pack(pady=10)
        self.btn_stop = tk.Button(self, text="Stop", command=self.stop, state=tk.DISABLED)
        self.btn_stop.pack(pady=10)
        # self.btn_random = tk.Button(self, text="Random Move", command=self.move_random, state=tk.DISABLED)
        # self.btn_random.pack(pady=10)
        
        # Inizializzazione delle variabili di stato
        self.is_running = False
        self.thread = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.last_active_time = time.time()
        self.is_movement_user_paused = False

    def start(self):
        # Avvia il programma
        self.is_running = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        # self.btn_random.config(state=tk.NORMAL)
        self.mouse_listener = mouse.Listener(on_move=self.on_move)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        
        # Esegue il ciclo principale del programma
        fm = FileManager()
        fm.create_assets_folder()
        fm.create_coordinate_velocita_folders()
        fm.create_name_movements_file()
        fm.add_current_folder_to_path()

        
        movement = MovementNameFileHandler("nome_movimenti_mouse.txt")
        while True:       
            nome_movimento = input("Inserisci il nome del movimento: ")
            if movement.is_movement_name_available(nome_movimento):
                movement.add_movement_name(nome_movimento)
                break
            else:
                print("Il nome del movimento è già presente nel file. Riprova.")
                
        # nome_movimento = input("scrivi il nome che indentifica il movimento del mouse che farai : ")
        # # Gestisce il file con i nomi dei movimenti
        # movement = MovementNameFileHandler("nome_movimenti_mouse.txt")
        # while not movement.is_movement_name_available(nome_movimento):
            # nome_movimento = input("Il nome del movimento è già presente nel file! Scrivi un altro nome: ")
        # movement.add_movement_name(nome_movimento)
        


        

        #passi il nome del movimento
        mc = MouseCoordinate(10, "coordinate.txt", "velocita.txt", nome_movimento)
        
        coordinates, velocities = mc.get_coordinates_and_velocities()
        
        quantita_coordinate = mc.save_coordinates(coordinates)
        quantita_velocita = mc.save_velocities(velocities)
        mc.check_files(quantita_coordinate, quantita_velocita)
        while self.is_running:
            if self.check_timeout():
                velocitiesReaded = self.read_velocities(velocities, quantita_coordinate)
                self.move_to_coordinates(coordinates, velocitiesReaded)
            time.sleep(1)

    def stop(self):
        # Arresta il programma
        self.is_running = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        # self.btn_random.config(state=tk.DISABLED)
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.thread.join()

    def on_move(self, x, y):
        """ 
        Aggiorna il tempo dell'ultima attività dell'utente 
        e mette in pausa il movimento automatico quando il cursore si muove
        """
        self.last_active_time = time.time()
        self.is_movement_user_paused = True

    def on_press(self, key):
        """
        Aggiorna il tempo dell'ultima attività dell'utente 
        e mette in pausa il movimento automatico quando viene premuto un tasto
        """
        self.last_active_time = time.time()
        self.is_movement_user_paused = True  
   

    def check_timeout(self):
        """
        Metodo che controlla se l'utente è inattivo da più di 10 secondi.
        Se l'utente è inattivo, imposta la variabile is_movement_user_paused a False e restituisce True.
        Altrimenti, imposta la variabile is_movement_user_paused a True e restituisce False.
        """
        time_since_last_active = time.time() - self.last_active_time
        if time_since_last_active > 10:
            self.is_movement_user_paused = False
            return True
        else:
            self.is_movement_user_paused = True
            return False


    def read_velocities(self, lista_velocita, num_velocities):
        # Si assicura che ci siano abbastanza velocità
        if len(lista_velocita) < num_velocities:
            raise ValueError("Not enough velocities in file")
        # Converte le tuple di stringhe in float
        return [float() for v in lista_velocita[:num_velocities][:num_velocities]]
    


    def move_to_coordinates(self, coordinate, velocita):
        """
        Metodo che muove il cursore del mouse a tutte le coordinate nella lista coordinates.
        Se la variabile is_movement_user_paused è True, interrompe il movimento.
        """
        for i, (x, y) in enumerate(coordinate):
            if self.is_movement_user_paused:
                break
            pyautogui.moveTo(x, y, duration = velocita[i] / 100)

       
if __name__ == '__main__':
    app = App()
    app.mainloop()
