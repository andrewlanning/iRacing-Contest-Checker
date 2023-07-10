from tkinter import *    # Carga módulo tk (widgets estándar)
from tkinter import ttk  # Carga ttk (para widgets nuevos 8.5+)

class Contest_Frame(ttk.Labelframe):
    def __init__(self, parent, name, contestId, eligibleRaces, draws):
        super().__init__(parent, text=name, width=150, height=100, borderwidth=30)
        super().grid_propagate(False)
        label_eligible = ttk.Label(self, text="Eligible Entries: ")
        data_elibible = ttk.Label(self, text=str(eligibleRaces))
        

        label_draws = ttk.Label(self, text="Draws: ")
        data_draws = ttk.Label(self, text=str(draws))

        label_eligible.grid(column=0, row=0, sticky=E)
        #super().grid_propagate(False)
        data_elibible.grid(column=1, row=0)
        #super().grid_propagate(False)

        label_draws.grid(column=0, row=1, sticky=E)
        #super().grid_propagate(False)
        data_draws.grid(column=1, row=1)
        




    