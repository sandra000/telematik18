import tkinter as tk
from matplotlib import pyplot as plt
import numpy as np
from controllers import HistoryController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ui.components import SymbolList
from sklearn import svm
from sklearn import neural_network


class NeuronalesNetzFrame(tk.Frame):
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

        label = tk.Label(self, text="Neural Forecast", font=controller.LARGE_FONT)
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

        btn_train_selected = tk.Button(self, text="Train", command=self.train)
        btn_train_selected.grid(row=4, column=12)

        btn_forecast_selected = tk.Button(self, text="Forecast", command=self.forecast)
        btn_forecast_selected.grid(row=4, column=13)

    def on_show(self):
        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history()
        self.symbol_list = SymbolList(self, self.symbol_data)
        self.symbol_list.grid(row=1, column=10, rowspan=3, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.symbol_list.config(relief=tk.GROOVE, bd=2)
        self.update()


    def train_neuralNet(self, data, trainlength):# returns trained neural network
        maxID=len(data)-trainlength-1-1
        inValues=[]
        outValues=[]
        for i in range(maxID):
            Values=[]
            for j in range(trainlength):
                #Values.append(float(data[i+j+1]/data[i+j]))
                Values.append(float(data[i+j+1]))
            inValues.append(Values)
            #outValues.append(int(data[i+trainlength+2]/data[trainlength+1]*1000000+0.5))
            outValues.append(int(data[i+trainlength+2]*1000+0.5))
        neuralNet=svm.SVC()
        #neuralNet=svm.SVR()

        neuralNet.fit(inValues,outValues)
        return neuralNet
    
    def predictNeural(self,neuralNet,data,trainlength):
        maxID=len(data)-trainlength-1
        inValues=[]
        for i in range(maxID):
            Values=[]
            for j in range(trainlength):
                #Values.append(float(data[i+j+1]/data[i+j]))
                Values.append(float(data[i+j+1]))
            inValues.append(Values)
        outValues=neuralNet.predict(inValues)
        result=[]
        for i in range(trainlength+1):
            #result.append(data[i]/1000.)
            result.append(0)
        for i in range(len(outValues)):
            #result.append(outValues[i]/1000000.*data[trainlength+1+i])
            result.append(outValues[i]/1000.)
        return result

    def update(self):
        self.a.cla()  # which clears data but not axes
        symbol_selected = self.symbol_selected
        history = HistoryController.History()
        if len(symbol_selected):
            for item in symbol_selected:
                current_history_data = history.get_by_symbol_id(item.id)
                current_prices = current_history_data.ask_price.values#.pct_change(12).dropna()
                self.a.plot(current_prices, label=item.symbol_global_id)
        else:
            bitcoin_name = "BITSTAMP_SPOT_BTC_USD"
            bitcoin_symbol = list(filter(lambda x: x.symbol_global_id == bitcoin_name, self.symbol_data))[0]
            history_data = history.get_by_symbol_id(bitcoin_symbol.id)
            current_prices = history_data.ask_price.values#pct_change(12).dropna()
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

    def train(self):
        self.symbol_selected = self.symbol_list.get_selection()
        self.update()
        self.neuralNet = self.train_neuralNet(self.getData(maxfaktor=0.8),30)

    def forecast(self):
        self.symbol_selected = self.symbol_list.get_selection()
        self.update()
        ergebnis=self.predictNeural(self.neuralNet,self.getData(),30)     
        self.a.plot(ergebnis, label="Neural Forecast")
        self.canvas.draw()

    def getData(self, maxLen=-1, maxfaktor=1.):
        symbol_selected = self.symbol_selected
        history = HistoryController.History()
        allData=[]
        if len(symbol_selected):
            for item in symbol_selected:
                current_history_data = history.get_by_symbol_id(item.id)
                current_prices = current_history_data.ask_price.values#pct_change(12).dropna()
                allData.append(current_prices.tolist())
        else:
            bitcoin_name = "BITSTAMP_SPOT_BTC_USD"
            bitcoin_symbol = list(filter(lambda x: x.symbol_global_id == bitcoin_name, self.symbol_data))[0]
            history_data = history.get_by_symbol_id(bitcoin_symbol.id)
            current_prices = history_data.ask_price.values#pct_change(12).dropna()
            if current_prices.size == 0:
                return
            allData.append(current_prices.tolist())
        data=[]
        minlen=100000#Abfragen sind immer mit limit 10000, somit wird 100000 nie erreicht
        for i in range(len(allData)):# Eigentlich sollte man nat�rlich gleichlange reihen nehmen, sonst ist es irgendwie sinnlos...
            if minlen>len(allData[i]):
                minlen=len(allData[i])
        if maxfaktor<1:
            maxLen=minlen*maxfaktor*len(allData)
        for i in range(minlen):
            for j in range(len(allData)):
                #data.append(int(allData[i][len(allData[i])-1-minlen+j]*1000))
                data.append(allData[j][len(allData[j])-1-minlen+i])
                if maxLen>-1:
                    if len(data)>maxLen:
                            return data
                
        return data