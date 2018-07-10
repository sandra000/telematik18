import tkinter as tk


class SettingView(tk.Frame):

    def __init__(self, parent, parameter=None, symbol=None):
        tk.Frame.__init__(self, parent)
        if not parameter:
            return

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.label1 = tk.Label(self, text="Time space:")
        self.label1.pack(side=tk.LEFT, fill=tk.X)
        self.label2 = tk.Label(self, text=parameter.time_start + "-" + parameter.time_end)
        self.label2.pack(side=tk.LEFT, fill=tk.X)

        self.label3 = tk.Label(self, text="Period:" + parameter.period_id)
        self.label3.pack(side=tk.LEFT, fill=tk.X)

        if symbol:
            self.label4 = tk.Label(self, text="From curr.:" + symbol.cryptocurrency.name)
            self.label4.pack(side=tk.LEFT, fill=tk.X)
            self.label5 = tk.Label(self, text="To curr.:" + symbol.cryptocurrency.name)
            self.label5.pack(side=tk.LEFT, fill=tk.X)
            self.label6 = tk.Label(self, text="Exchange:" + symbol.mark.name)
            self.label6.pack(side=tk.LEFT, fill=tk.X)
            self.label7 = tk.Label(self, text="Symbol:" + symbol.symbol_global_id)
            self.label7.pack(side=tk.LEFT, fill=tk.X)

    # TODO: Remove duplicate

    def update_view(self, parameter=None, symbol=None):
        self.label1 = tk.Label(self, text="Time space:")
        self.label1.pack(side=tk.LEFT, fill=tk.X)
        self.label2 = tk.Label(self, text=parameter.time_start + "-" + parameter.time_end)
        self.label2.pack(side=tk.LEFT, fill=tk.X)

        self.label3 = tk.Label(self, text="Period:" + parameter.period_id)
        self.label3.pack(side=tk.LEFT, fill=tk.X)

        if symbol:
            self.label4 = tk.Label(self, text="From curr.:" + symbol.cryptocurrency.name)
            self.label4.pack(side=tk.LEFT, fill=tk.X)
            self.label5 = tk.Label(self, text="   To curr.:" + symbol.cryptocurrency.name)
            self.label5.pack(side=tk.LEFT, fill=tk.X)
            self.label6 = tk.Label(self, text="Exchange:" + symbol.mark.name)
            self.label6.pack(side=tk.LEFT, fill=tk.X)
            self.label7 = tk.Label(self, text="Symbol:" + symbol.symbol_global_id)
            self.label7.pack(side=tk.LEFT, fill=tk.X)
