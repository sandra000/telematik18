import tkinter as tk


class ParameterList(tk.Frame):

    def __init__(self, parent, parameters):
        tk.Frame.__init__(self, parent)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # prepare data for listbox
        self.parameter_dict = dict()
        for item in parameters:
            self.parameter_dict[repr(item)] = item

        for key in self.parameter_dict:
            self.listbox.insert(tk.END, key)

    def get_selection(self):
        return_list = list()
        for key in self.listbox.selection_get().split():
            return_list.append(self.parameter_dict[key])
        return return_list
