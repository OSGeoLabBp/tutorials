import tkinter as tk
import tkinter.messagebox as mb

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello világ\n(kattints ide)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="Vége", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        mb.showinfo("Hello", "Üdvözöllek a tkinter világában")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
