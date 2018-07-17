import tkinter as tk
from tkinter import ttk     # widget(Style) for tkinter
from tkinter import messagebox
from matplotlib import pyplot as plt
import models
import api
from ui import CorrelationFrame
from ui import HistoryDataFrame
from ui import CryptocurrencyDataFrame
from ui import NeuronalesNetzFrame
from ui import ExchangeDataFrame
from ui import ImportHistoryFrame
from ui import SymbolDataFrame
from ui import CorrelationGraphFrame
from ui import AutocorrelationGraphFrame
from ui import OhlcGraphFrame
from ui import GARCHFrameChanging
from ui import GARCHFrame
from ui import LinearRegressionGraphFrame

session = models.Session()
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)

def popupmsg(msg):
    popup = tk.Tk() #creates an empty window
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text= "OK", command= lambda: popup.destroy())
    B1.pack()
    popup.mainloop()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Cryptocurrencies", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        label_text = tk.Label(self, text="This program is free to use under MIT license. "
                                         "This programmed was developed by student of FU Berlin "
                                         "only for research purpose.", font=NORM_FONT)
        label_text.pack(pady=10, padx=10)
        self.valor = tk.StringVar()
        self.valor.set("Hola Manejando datos") # ?????? why we need this
        tk.Label(self, textvariable=self.valor).pack()


class MainForm(tk.Tk):  # MainForm is the main class. It inherits from tk.Tk
    # main controller
    # figure for old graph(live course)
    f = plt.figure()
    LARGE_FONT = ("Verdana", 12)
    NORM_FONT = ("Verdana", 10)
    SMALL_FONT = ("Verdana", 8)
    import_api = api.MainImport()

    def run_main_import(self):
        self.import_api.update_exchanges()
        self.import_api.update_currencies()
        self.import_api.update_symbols()
        result = self.import_api.update_all_ohcl_histories()
        if result:
            messagebox.showinfo("Result", "Import is completed")

    def run_import_exchanges(self):
        result = self.import_api.update_exchanges()
        if result:
            messagebox.showinfo("Result", "Import is completed")

    def run_import_currencies(self):
        result = self.import_api.update_currencies()
        if result:
            messagebox.showinfo("Result", "Import is completed")

    def run_import_symbols(self):
        result = self.import_api.update_symbols()
        if result:
            messagebox.showinfo("Result", "Import is completed")

    def run_import_history_data(self):
        result = self.import_api.update_all_ohcl_histories()
        if result:
            messagebox.showinfo("Result", "Import is completed")

    def __init__(self, *args, **kwargs):
        # *args is any number of variables
        # **kwargs keyword arguments; we are passing through dictionaries
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Cryptocurrencies analyzer")
        container = tk.Frame(self)
        # container is the basis of every Tkinter GUI.
        # Frame is the edges of the basic window
        container.pack(side="top", fill="both", expand=True)
        # pack shoves elements in the window, side="top" means we are placing the element on the top of the window;
        # fill="both" means it fills the limits we set; expand=True means if there is space left,
        # the element should expand and occupy it
        # grid does the same, but we are able to better organize the elemts inside the window
        container.grid_rowconfigure(0, weight=1)
        # 0 is the minimum size, weight=1 means priority equals 1
        container.grid_columnconfigure(0, weight=1)
        # 1. We define what a menubar is (backend)
        # puts the menubar inside the container
        # puts the File submenu inside the menubar; tearoff means you can detach the menu
        menubar = tk.Menu(container)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        api_menu = tk.Menu(menubar, tearoff=1)
        api_menu.add_command(label="Import exchanges", command=lambda: self.run_import_exchanges())
        api_menu.add_command(label="Import currencies", command=lambda: self.run_import_currencies())
        api_menu.add_command(label="Import symbols", command=lambda: self.run_import_symbols())
        api_menu.add_command(label="Import history data", command=lambda: self.run_import_history_data())
        api_menu.add_command(label="Import History Form", command=lambda: self.show_frame(ImportHistoryFrame))
        api_menu.add_command(label="Import all", command=lambda: self.run_main_import())
        menubar.add_cascade(label="API", menu=api_menu)

        correlation_menu = tk.Menu(menubar, tearoff=1)
        correlation_menu.add_command(label="Correlation", command=lambda: self.show_frame(CorrelationFrame))
        correlation_menu.add_command(label="Correlation chart", command=lambda: self.show_frame(CorrelationGraphFrame))
        correlation_menu.add_command(label="Autocorrelation chart", command=lambda: self.show_frame(AutocorrelationGraphFrame))
        correlation_menu.add_command(label="Candlestick chart", command=lambda: self.show_frame(OhlcGraphFrame))
        correlation_menu.add_command(label="Neuronal Forecast", command=lambda: self.show_frame(NeuronalesNetzFrame))
        correlation_menu.add_command(label="Linear Regression Prediction Charts", command=lambda: self.show_frame(LinearRegressionGraphFrame))
        menubar.add_cascade(label="Windows", menu=correlation_menu)

        darch_menu = tk.Menu(menubar, tearoff=1)
        darch_menu.add_command(label="Price changing mean", command=lambda: self.show_frame(GARCHFrameChanging))
        darch_menu.add_command(label="Garch volatility", command=lambda: self.show_frame(GARCHFrame))
        menubar.add_cascade(label="GARCH", menu=darch_menu)

        data_menu = tk.Menu(menubar, tearoff=1)
        data_menu.add_command(label="Markets", command=lambda: self.show_frame(ExchangeDataFrame))
        data_menu.add_command(label="Currencies", command=lambda: self.show_frame(CryptocurrencyDataFrame))
        data_menu.add_command(label="Symbols", command=lambda: self.show_frame(SymbolDataFrame))
        data_menu.add_command(label="History", command=lambda: self.show_frame(HistoryDataFrame))    
        menubar.add_cascade(label="Show data", menu=data_menu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Tutorial")
        menubar.add_cascade(label="Help", menu=helpmenu)

        # set menubar
        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        # each frame in frames (dictionary) is a different window in our application.
        # If a certain page is not in self.frames, we cant display it
        # when we want to show a specific window, we run code to change the frame in frames

        # packing each page into frames:

        # with grid, we place the frame in the specified row and column
        # sticky=W would align the element to the left edge of the cell,
        # sticky='ew' would stretch the element to west and east (centering and stretching it);
        # sticky="nsew" stretches the element to the size of the window
        # if you dont use a row, default is the first unused row in the grid
        # http://effbot.org/tkinterbook/grid.htm for more grid() options

        for F in (StartPage, CorrelationFrame, HistoryDataFrame, CryptocurrencyDataFrame, ExchangeDataFrame, SymbolDataFrame,
                  GARCHFrameChanging, CorrelationGraphFrame, ImportHistoryFrame, AutocorrelationGraphFrame,
                  GARCHFrame, OhlcGraphFrame, LinearRegressionGraphFrame, NeuronalesNetzFrame):

            frame = F(container, self)  # main page
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        a = self.f.add_subplot(111)
        self.f.canvas.draw()
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        if "on_show" in dir(frame):
            frame.on_show()
        frame.tkraise()
