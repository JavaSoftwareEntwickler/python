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
        
        fm = FileManager()
        fm.clean__pycache__only_for_develop()
        fm.create_assets_folder()
        fm.create_coordinate_velocita_folders()
        fm.create_name_movements_file()
        fm.add_current_folder_to_path()
        
        # Inizializzazione della finestra grafica
        self.title("Start/Stop Program")
        self.geometry("220x150")
        
        # Creazione dei pulsanti e loro disposizione
        self.btn_start = tk.Button(self, text="Crea", command=self.start)
        #self.btn_start.pack(pady=10)
        self.btn_start.place(x=10, y=10)
        
        self.btn_stop = tk.Button(self, text="Stop", command=self.stop, state=tk.DISABLED)
        #self.btn_stop.pack(pady=10)
        self.btn_stop.place(x=60, y=10)
        
        self.btn_read_movement = tk.Button(self, text="Leggi Movimento", command=self.read_movement)
        self.btn_read_movement.place(x=10, y=50)
        

        # self.btn_random = tk.Button(self, text="Random Move", command=self.move_random, state=tk.DISABLED)
        # self.btn_random.pack(pady=10)
        self.variable = tk.StringVar(self)
        self.variable.set("Seleziona movimento")
        self.drop_down = tk.OptionMenu(self, self.variable, *self.get_movement_names())
        self.drop_down.place(x=10, y=90)
        
        # Inizializzazione delle variabili di stato
        self.is_creating_movement = False
        self.is_reading_movement = False
        self.is_running = False
        self.thread = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.last_active_time = time.time()
        self.is_movement_user_active = False

    def start(self):
        # Avvia il programma
        self.is_creating_movement = True
        self.is_running = True
        self.btn_start.config(state=tk.DISABLED)
        self.drop_down.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        # self.btn_random.config(state=tk.NORMAL)
        self.btn_read_movement.config(state=tk.DISABLED)        
        self.mouse_listener = mouse.Listener(on_move=self.on_move)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        
    def read_movement(self):
        # Avvia il programma
        self.is_reading_movement = True
        self.is_running = True
        self.btn_read_movement.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        # self.btn_random.config(state=tk.NORMAL)
        self.btn_read_movement.config(state=tk.DISABLED)        
        self.mouse_listener = mouse.Listener(on_move=self.on_move)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        
        # Esegue il ciclo principale del programma
        movement = MovementNameFileHandler("nome_movimenti_mouse.txt")
        
        if self.is_creating_movement:
            while True:       
                nome_movimento = input("Inserisci il nome del movimento: ")
                if movement.is_movement_name_available(nome_movimento):
                    movement.add_movement_name(nome_movimento)
                    break
                else:
                    print("Il nome del movimento è già presente nel file. Riprova.")
            #passi il nome del movimento
            mc = MouseCoordinate(10, "coordinate.txt", "velocita.txt", nome_movimento) 
            coordinates, velocities = mc.get_coordinates_and_velocities()            
            quantita_coordinate = mc.save_coordinates(coordinates)
            quantita_velocita = mc.save_velocities(velocities)
            mc.check_files(quantita_coordinate, quantita_velocita)
            
            
        elif self.is_reading_movement:
            #leggo il movimeto 
            nome_movimento = self.variable.get()
            print(f'ecco il movimento selezionato :{nome_movimento}')
            
            
            #passi il nome del movimento
            mc = MouseCoordinate(10, "coordinate.txt", "velocita.txt", nome_movimento)
            coordinates, velocities = mc.get_movement_file()
            mc.check_files(len(coordinates), len(velocities))
            
            
            
        while self.is_running:
            if self.check_timeout():
                velocitiesReaded = self.read_velocities(velocities, len(coordinates))
                self.move_to_coordinates(coordinates, velocitiesReaded)
            time.sleep(1)
                
        

    def stop(self):
        # Arresta il programma
        self.is_running = False
        self.is_creating_movement = False
        self.is_reading_movement = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_read_movement.config(state=tk.NORMAL)
        self.drop_down.config(state=tk.NORMAL)
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
        self.is_movement_user_active = True

    def on_press(self, key):
        """
        Aggiorna il tempo dell'ultima attività dell'utente 
        e mette in pausa il movimento automatico quando viene premuto un tasto
        """
        self.last_active_time = time.time()
        self.is_movement_user_active = True  
   

    def check_timeout(self):
        """
        Metodo che controlla se l'utente è inattivo da più di 10 secondi.
        Se l'utente è inattivo, imposta la variabile is_movement_user_active a False e restituisce True.
        Altrimenti, imposta la variabile is_movement_user_active a True e restituisce False.
        """
        time_since_last_active = time.time() - self.last_active_time
        if time_since_last_active > 10:
            self.is_movement_user_active = False
            return True
        else:
            self.is_movement_user_active = True
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
        Se la variabile is_movement_user_active è True, interrompe il movimento.
        """
        print("#############sottole coordinate################") 
        print(type(coordinate))
        print(coordinate)
        print(type(coordinate[0]))
        print(f'coordinata di 0 : {coordinate[0]}')
        print("#############sotto le velocita################") 
        print(type(velocita))        
        print(velocita)
        for i, (x, y) in enumerate(coordinate):
            if self.is_movement_user_active:
                break
            pyautogui.moveTo(x, y, duration = velocita[i] / 100)
            
    
    def get_movement_names(self):
        nomi_movimenti = ["cerchi","infinito","veloce","ciccio","provaasdf","aaaaa","compila","okok","iooo","nuovomovimento","elisse","11112222","1234567","ioooooooooooooooo"]
        return nomi_movimenti

       
if __name__ == '__main__':
    app = App()
    app.mainloop()
