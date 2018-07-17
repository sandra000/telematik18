import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rc
from pandastable import Table, TableModel
from controllers import HistoryController
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import datetime
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, cross_validation, svm

#Technical analysts can use autocorrelation to see how much of an impact past prices for a security have on
# its future price
#Assume an investor is looking to discern if a stock's returns in her portfolio exhibit autocorrelation; the
# stock's returns are related to its returns in previous trading sessions. If the returns do exhibit autocorrelation,
# the stock could be characterized as a momentum stock; its past returns seem to influence its future returns.
# The investor runs a regression with two prior trading sessions' returns as the independent variables and the current
# return as the dependent variable. She finds that returns one day prior have a positive autocorrelation of 0.7, while
# the returns two days prior have a positive autocorrelation of 0.3. Past returns seem to influence future returns, and
# she can adjust her portfolio to take advantage of the autocorrelation and resulting momentum.



class LinearRegressionGraphFrame(tk.Frame):
    figureLinearRegressionChart = plt.figure(figsize=(20, 10))
    valor = tk.StringVar()
    plt.rc('font', size=6)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Linear Regression Price Prediction Charts", font=controller.LARGE_FONT)
        label.pack(pady=5,padx=5)
        self.a1 = self.figureLinearRegressionChart.add_subplot(331)
        self.a2 = self.figureLinearRegressionChart.add_subplot(332)
        self.a3 = self.figureLinearRegressionChart.add_subplot(333)
        self.a4 = self.figureLinearRegressionChart.add_subplot(334)
        self.a5 = self.figureLinearRegressionChart.add_subplot(335)
        self.a6 = self.figureLinearRegressionChart.add_subplot(336)
        self.a7 = self.figureLinearRegressionChart.add_subplot(337)
        self.a8 = self.figureLinearRegressionChart.add_subplot(338)
        self.a9 = self.figureLinearRegressionChart.add_subplot(339)
        plt.subplots_adjust(left=1, bottom=1, right=1.1, top=1.1,
                        wspace=0.5, hspace=0.5)

    def on_show(self):
        self.update()

    def update(self):
        # TODO: fix this
        bitcoin_name = 1

        history = HistoryController.History()  # object for the databank endpoint
        historydata = history.get_all()  # dataframe
        if historydata.values.size == 0:
            return
        historydata_grouped = historydata.groupby('base_currency_id') #symbol_id

        df = historydata_grouped.get_group(bitcoin_name)
        df['date'] = df['start_time_exchange'].map(mdates.date2num)
        df = df.loc[df['symbol_id'] == 16]
        df = df[['ask_price']]


        accuracies = []
        predictions = []

        for x in range(1,10):
            forecast_out = int(x)  # predict x days into future
            df['Prediction'] = df[['ask_price']].shift(-forecast_out)
            X = np.array(df.drop(['Prediction'], 1)) #labels for linear regression
            X = preprocessing.scale(X)
            X_forecast = X[-forecast_out:]
            X = X[:-forecast_out]

            y = np.array(df['Prediction'])
            y = y[:-forecast_out]

            X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

            # train
            clf = LinearRegression()
            clf.fit(X_train, y_train)
            # test
            accuracy = clf.score(X_test, y_test)
            print("accuracy: ", accuracy)

            forecast_prediction = clf.predict(X_forecast)
            print(forecast_prediction)

            accuracies.append(accuracy)
            predictions.append(forecast_prediction)

        self.a1.scatter([1], predictions[0], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[0]))
        self.a1.set_xticks([1])
        self.a1.set_yticks(predictions[0])
        self.a1.set_title("1 day forecast")

        self.a2.plot([1,2], predictions[1], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[1]))
        self.a2.set_xticks([1,2])
        self.a2.set_yticks(predictions[1])
        self.a2.set_title("2 days forecast")

        self.a3.plot(list(range(1,4)), predictions[2], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[2]))
        self.a3.set_xticks(list(range(1,4)))
        self.a3.set_yticks(predictions[2])
        self.a3.set_title("3 days forecast")

        self.a4.plot(list(range(1,5)), predictions[3], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[3]))
        self.a4.set_xticks(list(range(1,5)))
        self.a4.set_yticks(predictions[3])
        self.a4.set_title("4 days forecast")

        self.a5.plot(list(range(1,6)), predictions[4], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[4]))
        self.a5.set_xticks(list(range(1,6)))
        self.a5.set_yticks(predictions[4])
        self.a5.set_title("5 days forecast")

        self.a6.plot(list(range(1,7)), predictions[5], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[5]))
        self.a6.set_xticks(list(range(1,7)))
        self.a6.set_yticks(predictions[5])
        self.a6.set_title("6 days forecast")

        self.a7.plot(list(range(1,8)), predictions[6], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[6]))
        self.a7.set_xticks(list(range(1,8)))
        self.a7.set_yticks(predictions[6])
        self.a7.set_title("7 days forecast")

        self.a8.plot(list(range(1,9)), predictions[7], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[7]))
        self.a8.set_xticks(list(range(1,9)))
        self.a8.set_yticks(predictions[7])
        self.a8.set_title("8 days forecast")

        self.a9.plot(list(range(1,10)), predictions[8], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[8]))
        self.a9.set_xticks(list(range(1,10)))
        self.a9.set_yticks(predictions[8])
        self.a9.set_title("9 days forecast")

        self.a1.grid(True)
        self.a1.legend()

        self.a2.grid(True)
        self.a2.legend()

        self.a3.grid(True)
        self.a3.legend()

        self.a4.grid(True)
        self.a4.legend()

        self.a5.grid(True)
        self.a5.legend()

        self.a6.grid(True)
        self.a6.legend()

        self.a7.grid(True)
        self.a7.legend()

        self.a8.grid(True)
        self.a8.legend()

        self.a9.grid(True)
        self.a9.legend()

        canvas = FigureCanvasTkAgg(self.figureLinearRegressionChart, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        return True

    def get_correlation(self):
        #TODO: sort the history list
        history = HistoryController.History()
        historydata = history.get_all()
        all_base_cuurencies = history.get_all_base_currency_from_history()
        historydata_grouped = historydata.groupby('base_currency_id')
        currency_list = []
        for item in all_base_cuurencies:
            currency_list.append(all_base_cuurencies[item].base_currency.name)
        output_pd = pd.DataFrame(index=currency_list, columns=currency_list)
        for name, group in historydata_grouped:
            currency_name = all_base_cuurencies[name].base_currency.name
            main_currency_arr = group.ask_price.values
            output_arr = []
            for name2, group2 in historydata_grouped:
                tmp_main_currency_arr = main_currency_arr
                current_currency_arr = group2.ask_price.values
                if current_currency_arr.size > main_currency_arr.size:
                    current_currency_arr = np.resize(current_currency_arr, main_currency_arr.shape)
                if current_currency_arr.size < main_currency_arr.size:
                    tmp_main_currency_arr = np.resize(main_currency_arr, current_currency_arr.shape)
                coef = np.corrcoef(tmp_main_currency_arr, current_currency_arr)
                output_arr.append(coef[0,1])
            output_pd.loc[currency_name] = output_arr
        return output_pd


class MyDialog(tk.Frame):
    def __init__(self, parent, valor, title, labeltext='', list_of_symbol_var=[]):
        self.valor = valor

        self.top = tk.Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()
        if len(title) > 0: self.top.title(title)
        if len(labeltext) == 0: labeltext = 'Valor'
        tk.Label(self.top, text=labeltext).pack()
        self.top.bind("<Return>", self.ok)
        self.e = tk.Entry(self.top, text=valor.get())
        self.e.bind("<Return>", self.ok)
        self.e.bind("<Escape>", self.cancel)
        self.e.pack(padx=15)
        self.e.focus_set()
        b = tk.Button(self.top, text="OK", command=self.ok)
        b.pack(pady=5)



        # for var in list_of_symbol_vars:
        #     tk.Checkbutton(self, text="male", variable=var).grid(row=0, sticky=W)

    def ok(self, event=None):
        print("Has escrito ...", self.e.get())
        self.valor.set(self.e.get())
        self.top.destroy()


    def cancel(self, event=None):
        self.top.destroy()


class Checkbar(tk.Frame):

    def __init__(self, parent=None, picks=[], side='left', anchor='w'):
        tk.Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand='yes')
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)
