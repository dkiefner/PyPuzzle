from tkinter import ttk
import tkinter


class Application(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.grid(row=0, column=0)
        self.create_widgets()
        self.style = ttk.Style()
        self.style.configure("BW.TLabel", foreground="black", background="white", pady=100)

    def create_widgets(self):
        # self.view_start = ttk.Button(text="Start", style="BW.TButton")
        # self.view_start["command"] = self.start
        # self.view_start.grid(row=1, column=0)

        for tile in range(0, 15):
            view_tile = ttk.Label(text=str(tile + 1), style="BW.TLabel")
            view_tile.grid(column=tile % 4, row=int(tile / 4))

    def start(self):
        print("Start")


app = Application()
app.master.title("Pyzzle")
app.master.minsize(640, 480)
app.master.maxsize(640, 480)

app.mainloop()
