import tkinter as tk


class SettingView(tk.Frame):

    def __init__(self, parent, parameter=None, symbol=None, summary=None):
        tk.Frame.__init__(self, parent)
        if not parameter:
            return

        # scrollbar = tk.Scrollbar(self)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.label1 = tk.Label(self, text="Time space:")
        self.label1.grid(row=0, column=0, pady=10)
        self.label2 = tk.Label(self, text=parameter.time_start + "-" + parameter.time_end)
        self.label2.grid(row=0, column=1, pady=10)

        self.label3 = tk.Label(self, text="Period:" + parameter.period_id)
        self.label3.grid(row=1, column=0, columnspan=2, pady=10, sticky=tk.W)

        self.label4 = tk.Label(self, text="From curr.:")
        self.label5 = tk.Label(self, text="To curr.:")
        self.label6 = tk.Label(self, text="Exchange:")
        self.label7 = tk.Label(self, text="Symbol:")
        self.label8 = tk.Label(self, text=summary)


    # TODO: Remove duplicate

    def update_view(self, parameter=None, symbols=None, summary=None):
        if hasattr(self, 'label1'):
            self.label1.destroy()
        if hasattr(self, 'label2'):
            self.label2.destroy()
        if hasattr(self, 'label3'):
            self.label3.destroy()
        if hasattr(self, 'label4'):
            self.label4.destroy()
        if hasattr(self, 'label5'):
            self.label5.destroy()
        if hasattr(self, 'label6'):
            self.label6.destroy()
        if hasattr(self, 'label7'):
            self.label7.destroy()
        if hasattr(self, 'label8'):
            self.label8.destroy()

        self.label1 = tk.Label(self, text="Time space:")
        self.label1.grid(row=0, column=0, pady=10)
        self.label2 = tk.Label(self, text=parameter.time_start + "-" + parameter.time_end)
        self.label2.grid(row=0, column=1, pady=10)

        self.label3 = tk.Label(self, text="Period:" + parameter.period_id)
        self.label3.grid(row=1, column=0, columnspan=2, pady=10, sticky=tk.W)

        # labels_groups_wscroll = tk.Frame(self)
        # scrollbar = tk.Scrollbar(labels_groups_wscroll)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        labels_groups = tk.Frame(self)
        if symbols:
            for symbol in symbols:
                self.label4 = tk.Label(labels_groups, text="From curr.:" + symbol.base_currency.name)
                self.label4.pack(fill=tk.X)
                self.label5 = tk.Label(labels_groups, text="To curr.:" + symbol.quote_currency.name)
                self.label5.pack(fill=tk.X)
                self.label6 = tk.Label(labels_groups, text="Exchange:" + symbol.mark.name)
                self.label6.pack(fill=tk.X)
                self.label7 = tk.Label(labels_groups, text="Symbol:" + symbol.symbol_global_id)
                self.label7.pack(fill=tk.X)
        labels_groups.grid(row=2, column=0, columnspan=2, pady=10, sticky=tk.W)
        # labels_groups.pack(fill=tk.BOTH)
        # labels_groups.config(yscrollcommand=scrollbar.set)
        # scrollbar.config(command=labels_groups.yview)
        if summary:
            self.label8 = tk.Label(self, text=summary)
            self.label8.grid(row=3, column=0, columnspan=2, pady=10)
