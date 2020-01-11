import pickle
from tkinter import *
from tkinter import messagebox


class File:
    def __init__(self, filename):
        self.filename = filename
        self.data = None

    def open(self):
        try:
            with open(self.filename, 'rb') as file:
                self.data = pickle.load(file)
                print(self.data)
        except IOError as e:
            Tk().wm_withdraw()
            messagebox.showerror("Error!", "Błąd pliku " + str(e))

    def save(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)
