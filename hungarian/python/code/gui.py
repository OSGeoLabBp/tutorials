import tkinter as tk
import tkinter.filedialog as fd
from tkinter import ttk
import pandas as pd
from point import Point
from angle import Angle

class App(tk.Tk, object):
    def __init__(self):
        super(App, self).__init__()
        # variables assigned to widgets
        self.filename = tk.StringVar()
        self.sp = tk.StringVar()
        self.ep = tk.StringVar()
        self.bearing = tk.StringVar()
        self.dist = tk.StringVar()
        self.pnts = {}
        # size and position of window
        self.geometry("280x160+10+10")
        self.title("Bearing & distance")
        self.resizable(False, False)   # no resize of window
        # widgets
        self.btn_file = tk.Button(self, text="Choose file",
                             command=self.ChooseFile)
        self.fileentry = tk.Entry(self, textvariable=self.filename, state="disabled")
        self.startpoint = ttk.Combobox(textvariable=self.sp)
        self.endpoint = ttk.Combobox(textvariable=self.ep)
        self.btn_calculate = tk.Button(self, text="Calculate", command=self.Calc)
        self.b = tk.Label(textvariable=self.bearing)
        self.d = tk.Label(textvariable=self.dist)
        # place widget into window
        self.btn_file.pack()
        self.fileentry.pack()
        self.startpoint.pack()
        self.endpoint.pack()
        self.btn_calculate.pack()
        self.b.pack()
        self.d.pack()

    def CooReader(self, fname):
        """ read coordinates from csv/txt file """
        self.pnts = {}                   # reset dictionary for points
        try:
            df = pd.read_csv(fname)
        except (pd.parser.CParserError, IOError, KeyError):
            return False
        # check keys
        for c in ['id', 'x', 'y']:
            if c not in df:
                return False
        # convert data to dictionary of Point objects
        for i in range(df.shape[0]):
            self.pnts[str(df['id'][i])] = Point(df['x'][i], df['y'][i])
        return True

    def ChooseFile(self):
        """ select a file of coordinates """
        filetypes = (("Plain text files", "*.txt"),
                     ("CSV files", "*.csv"),
                     ("All files", "*"))
        fn = fd.askopenfilename(title="Open file", initialdir=".",
                                filetypes=filetypes)
        if fn:
            self.sp.set("") # clear start point
            self.ep.set("") # clear end point
            if self.CooReader(fn):
                self.filename.set(fn)
                # fill combo boxes with point ids
                self.startpoint['values'] = sorted(list(self.pnts.keys()))
                self.endpoint['values'] = sorted(list(self.pnts.keys()))
            else:
                # clear is reader failed
                self.filename.set("")
                self.startpoint['values'] = []
                self.endpoint['values'] = []

    def Calc(self):
        """ claculate bearing and distance """
        pid1 = self.startpoint.get()
        pid2 = self.endpoint.get()
        if len(pid1) and len(pid2) and pid1 != pid2 and \
            pid1 in self.pnts and pid2 in self.pnts:
            w = (self.pnts[pid2] - self.pnts[pid1]).polar()
            self.bearing.set(Angle(w[1]).GetAngle('DMS'))
            self.dist.set("{:.3f}".format(w[0]))
        else:
            # clear result if invalid point ids given
            self.bearing.set("")
            self.dist.set("")

if __name__ == "__main__":
    app = App()
    app.mainloop()
