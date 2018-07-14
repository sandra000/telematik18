import tkinter as tk


class SymbolList(tk.Frame):

    def __init__(self, parent, symbols):
        tk.Frame.__init__(self, parent)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # prepare data for listbox
        self.symbol_dict = dict()
        self.update_list(symbols)

    def get_selection(self):
        return_list = list()
        for key in self.listbox.selection_get().split():
            return_list.append(self.symbol_dict[key])
        return return_list

    def update_list(self, symbols):
        self.symbol_dict = dict()
        for item in symbols:
            self.symbol_dict[item.symbol_global_id] = item

        for key in self.symbol_dict:
            self.listbox.insert(tk.END, key)
