import tkinter as tk
from matplotlib import pyplot as plt
from controllers import HistoryController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ui.components import SymbolList


class DARCHFrameChanging(tk.Frame):
    figureCorrelation = plt.figure()
    valor = tk.StringVar()
    test_var = tk.IntVar()
    symbol_selected = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Set the grid size
        col = 0
        while col < 12:
            self.columnconfigure(col, weight=1)
            col += 1
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        label = tk.Label(self, text="Price changing mean", font=controller.LARGE_FONT)
        label.grid(row=0, columnspan=12)

        self.a = self.figureCorrelation.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figureCorrelation, self)
        self.canvas.get_tk_widget().grid(row=1, rowspan=3, columnspan=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history()
        self.symbol_list = SymbolList(self, self.symbol_data)
        self.symbol_list.grid(row=1, column=10, rowspan=3, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.symbol_list.config(relief=tk.GROOVE, bd=2)

        btn_update_selected = tk.Button(self, text="Update", command=self.renew)
        btn_update_selected.grid(row=4, column=11)

    def on_show(self):
        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history()
        self.symbol_list = SymbolList(self, self.symbol_data)
        self.symbol_list.grid(row=1, column=10, rowspan=3, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.symbol_list.config(relief=tk.GROOVE, bd=2)
        self.update()

    def update(self):
        self.a.cla()  # which clears data but not axes
        symbol_selected = self.symbol_selected
        history = HistoryController.History()
        if len(symbol_selected):
            for item in symbol_selected:
                current_history_data = history.get_by_symbol_id(item.id)
                current_prices = 100 * current_history_data.ask_price.pct_change(12).dropna()
                self.a.plot(current_prices, label=item.symbol_global_id)
        else:
            bitcoin_name = "BITSTAMP_SPOT_BTC_USD"
            bitcoin_symbol = list(filter(lambda x: x.symbol_global_id == bitcoin_name, self.symbol_data))[0]
            history_data = history.get_by_symbol_id(bitcoin_symbol.id)
            current_prices = 100 * history_data.ask_price.pct_change(12).dropna()
            if current_prices.size == 0:
                return
            self.a.plot(current_prices, color='red', label=bitcoin_name)

        self.a.legend()
        self.canvas.draw()

        toolbar_frame = tk.Frame(master=self)
        toolbar_frame.grid(row=4, columnspan=10, sticky=tk.W)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        return True

    def renew(self):
        self.symbol_selected = self.symbol_list.get_selection()
        self.update()


