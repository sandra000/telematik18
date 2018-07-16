import tkinter as tk


class ParameterList(tk.Frame):

    def __init__(self, parent, parameters):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.listbox.bind('<<ListboxSelect>>', self.onselect)
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

    def onselect(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.parent.get_data_for_symbol_list(self.parameter_dict[value])
