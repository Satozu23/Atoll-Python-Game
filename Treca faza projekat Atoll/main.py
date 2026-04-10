from tkinter import messagebox
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tabla
import mats
import ai

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 1000
HEX_SIZE = 30
CIRCLE_RADIUS = 12
OFFSET_X = 600
OFFSET_Y = 500

TABLA_PODACI = {}
CURRENT_PLAYER = ""
VELICINA_TABLE = 0

GAME_MODE = None
AI_COLOR = None  
START_COLOR = None

def check_game_over_and_reset(root, canvas):
    global TABLA_PODACI, CURRENT_PLAYER, VELICINA_TABLE, START_COLOR, GAME_MODE, AI_COLOR
    
    if tabla.check_win(TABLA_PODACI, CURRENT_PLAYER):
        canvas.update() 
        odgovor = messagebox.askyesno("Kraj igre", 
                                      f"Pobednik je {CURRENT_PLAYER} igrač!\n\n"
                                      "Da li želite da igrate ponovo?")
        if odgovor: 
            matrix = tabla.generate_atoll_matrix(VELICINA_TABLE)
            TABLA_PODACI = tabla.generate_polja(matrix, VELICINA_TABLE)
            tabla.draw_board(canvas, TABLA_PODACI, VELICINA_TABLE)
            
            CURRENT_PLAYER = START_COLOR 
            root.title(f"Atoll - {GAME_MODE} | Na potezu: {CURRENT_PLAYER}")
            
            if GAME_MODE == "PvE" and CURRENT_PLAYER == AI_COLOR:
                root.after(500, lambda: computer_move(root, canvas))
            return True
        else:
            create_main_menu(root)
            return True
    return False

def computer_move(root, canvas):
    global CURRENT_PLAYER, TABLA_PODACI, VELICINA_TABLE, AI_COLOR
    
    root.config(cursor="watch")
    canvas.update()

    try:
        best_move = ai.get_best_move(TABLA_PODACI, VELICINA_TABLE, AI_COLOR)
        
        if best_move:
            tabla.postavi_kamencic(TABLA_PODACI, best_move, AI_COLOR)
            tabla.draw_board(canvas, TABLA_PODACI, VELICINA_TABLE)
            
            if check_game_over_and_reset(root, canvas):
                root.config(cursor="")
                return

            if CURRENT_PLAYER == "crveni":
                CURRENT_PLAYER = "zeleni"
            else:
                CURRENT_PLAYER = "crveni"
                
            print(f"Sledeci je: {CURRENT_PLAYER} (Covek)")
            root.title(f"Atoll - {GAME_MODE} | Na potezu: {CURRENT_PLAYER}")
        else:
            print("AI nije nasao potez (mozda je tabla puna ili greska).")
            
    except Exception as e:
        print(f"AI Greska: {e}")
    finally:
        root.config(cursor="")

def handle_click(event, canvas):
    global CURRENT_PLAYER, TABLA_PODACI, VELICINA_TABLE, GAME_MODE, AI_COLOR
    
    if GAME_MODE == "PvE" and CURRENT_PLAYER == AI_COLOR:
        return

    klik_x, klik_y = event.x, event.y
    kliknuto_polje = mats.pixel_to_hex(klik_x, klik_y, TABLA_PODACI, VELICINA_TABLE)

    if kliknuto_polje:
        try:
            tabla.postavi_kamencic(TABLA_PODACI, kliknuto_polje, CURRENT_PLAYER)
            tabla.draw_board(canvas, TABLA_PODACI, VELICINA_TABLE)
            
            root = canvas.winfo_toplevel()

            if check_game_over_and_reset(root, canvas):
                return

            if CURRENT_PLAYER == "crveni":
                CURRENT_PLAYER = "zeleni"
            else:
                CURRENT_PLAYER = "crveni"

            print(f"Potez odigran! Sledeci je: {CURRENT_PLAYER}")
            root.title(f"Atoll - {GAME_MODE} | Na potezu: {CURRENT_PLAYER}")
            
            if GAME_MODE == "PvE" and CURRENT_PLAYER == AI_COLOR:
                root.after(100, lambda: computer_move(root, canvas))
            
        except Exception as e:
            print(f"Greska pri kliku: {e}")
            messagebox.showwarning("Greška", str(e))

def start_game(root, mode, choosing_frame, size_val, who_starts, start_color):
    global GAME_MODE, VELICINA_TABLE, CURRENT_PLAYER, TABLA_PODACI, AI_COLOR, START_COLOR

    GAME_MODE = mode
    VELICINA_TABLE = size_val
    CURRENT_PLAYER = start_color 
    START_COLOR = start_color

    AI_COLOR = None
    if mode == "PvE":
        if who_starts == "computer":
            AI_COLOR = start_color
        else:
            AI_COLOR = "zeleni" if start_color == "crveni" else "crveni"

    print(f"Start igre: Mod={GAME_MODE}, Velicina={VELICINA_TABLE}")
    print(f"Prvi igra: {CURRENT_PLAYER}, AI je: {AI_COLOR}")

    choosing_frame.destroy()
    root.title(f"Atoll - {mode} | Na potezu: {CURRENT_PLAYER}")

    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
    canvas.pack()

    matrix = tabla.generate_atoll_matrix(VELICINA_TABLE)
    TABLA_PODACI = tabla.generate_polja(matrix, VELICINA_TABLE)

    tabla.draw_board(canvas, TABLA_PODACI, VELICINA_TABLE)

    canvas.bind("<Button-1>", lambda event: handle_click(event, canvas))

    if mode == "PvE" and CURRENT_PLAYER == AI_COLOR:
        root.after(500, lambda: computer_move(root, canvas))


def playing_first(root, mode, size_val):
    for widget in root.winfo_children():
        widget.destroy()

    who_starts_var = tk.StringVar(value="human")
    color_var = tk.StringVar(value="crveni")

    choosing_frame = tk.Frame(root, bg="#f0f0f0", padx=50, pady=20)
    choosing_frame.place(relx=0.5, rely=0.5, anchor="center")

    lbl_info = tk.Label(choosing_frame, text=f"Podesavanja za {size_val}x{size_val}", font=("Arial", 12), bg="#f0f0f0")
    lbl_info.pack(pady=5)

    if mode == "PvE":
        lbl_who = tk.Label(choosing_frame, text="Ko igra prvi?", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        lbl_who.pack(pady=(10, 5))
        
        r_human = ttk.Radiobutton(choosing_frame, text="Čovek", variable=who_starts_var, value="human")
        r_human.pack()
        r_comp = ttk.Radiobutton(choosing_frame, text="Računar", variable=who_starts_var, value="computer")
        r_comp.pack()

    lbl_color = tk.Label(choosing_frame, text="Boja prvog igrača", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
    lbl_color.pack(pady=(20, 5))
    
    r_red = ttk.Radiobutton(choosing_frame, text="Crveni", variable=color_var, value="crveni")
    r_red.pack()
    r_green = ttk.Radiobutton(choosing_frame, text="Zeleni", variable=color_var, value="zeleni")
    r_green.pack()

    btn_start = tk.Button(choosing_frame, text="Start", font=("Arial", 14), width=20, height=2,
                          bg="#4CAF50", fg="white", cursor="hand2",
                          command=lambda: start_game(root, mode, choosing_frame, size_val,
                                                     who_starts_var.get(), color_var.get()))
    btn_start.pack(pady=20)

    btn_back = tk.Button(choosing_frame, text="Nazad", font=("Arial", 12), width=15,
                         bg="#f44336", fg="white", cursor="hand2",
                         command=lambda: create_main_menu(root))
    btn_back.pack(pady=10)


def create_main_menu(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Atoll - Izbor Igre")

    menu_frame = tk.Frame(root, bg="#f0f0f0", padx=50, pady=20)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")

    options = [3, 5, 7, 9]
    style = ttk.Style()
    style.theme_use("clam")

    root.option_add('*TCombobox*Listbox.background', '#dcdad5')
    root.option_add('*TCombobox*Listbox.foreground', 'black')
    
    cb = ttk.Combobox(
        menu_frame,
        values=options,
        cursor="hand2",
        state="readonly",
        font=("Arial", 14),
        justify="center"
    )
    cb.config(width=19)
    cb.set("5")

    lbl_cb = tk.Label(menu_frame, text="Izaberite dužinu stranice (n):", bg="#f0f0f0", font=("Arial", 10))
    

    def validate_and_proceed(mode):
        val = cb.get()
        if val.isdigit():
            size = int(val)
            playing_first(root, mode, size)
        else:
            playing_first(root, mode, 5)

    lbl_title = tk.Label(menu_frame, text="Dobrodošli u Atoll", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
    lbl_title.pack(pady=20)

    btn_pvp = tk.Button(menu_frame, text="Čovek vs Čovek", font=("Arial", 14), width=20, height=2,
                        bg="#4CAF50", fg="white", cursor="hand2",
                        command=lambda: validate_and_proceed("PvP"))
    btn_pvp.pack(pady=10)

    btn_pve = tk.Button(menu_frame, text="Čovek vs Računar", font=("Arial", 14), width=20, height=2,
                        bg="#2196F3", fg="white", cursor="hand2",
                        command=lambda: validate_and_proceed("PvE"))
    btn_pve.pack(pady=10)

    lbl_cb.pack()
    cb.pack(pady=10)
    btn_exit = tk.Button(menu_frame, text="Izlaz", font=("Arial", 12), width=15,
                         bg="#f44336", fg="white", cursor="hand2",
                         command=root.quit)
    btn_exit.pack(pady=80)
    

def main():
    root = tk.Tk()
    root.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}")
    root.configure(bg="#e0e0e0") 

    create_main_menu(root)

    root.mainloop()

if __name__ == "__main__":
    main()