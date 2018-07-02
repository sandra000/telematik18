import tkinter as tk
import matplotlib.animation as animation
from tkinter import ttk #css for tkinter
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# FigureCanvasTkAgg allows us to draw matplotlib to a canvas with TkAgg
# NavigationToolbar2TkAgg is the small toolbar in every matplotlib graph
from matplotlib import pyplot as plt
from ui import FrameLiveCourse
import models
import api
from ui import CorrelationFrame
from ui import HistoryDataFrame
from ui import CryptocurrencyDataFrame
from ui import ExchangeDataFrame
from ui import ImportHistoryFrame
from ui import SymbolDataFrame
from ui import CorrelationGraphFrame
from ui import AutocorrelationGraphFrame
from ui import OhlcGraphFrame

session = models.Session()

### TODO: move to config
# defining constants
LARGE_FONT =("Verdana", 12)
NORM_FONT=("Verdana", 10)
SMALL_FONT =("Verdana", 8)

# DEFAULT VALUES - the user can change them in the menubar later
exchange = "Bitfinex"
datCounter = 9000 # time to update
programName = "btce"
resampleSize = "15Min"
dataPace = "tick" 
candleWidth = 0.008

paneCount = 1

topIndicator = "none"
bottomIndicator = "none"
middleIndicator = "none"
chartLoad = True

darkColor = "#183A54"
lightColor = "#00A3E0"

EMAs = []
SMAs = []
###TODO: until now


def loadChart(run):
  global chartLoad

  if run == "start":
    chartLoad = True

  elif run == "stop":
      chartLoad = False




def tutorial():

  def page2():  # second page; it first closes page1, creates a new window; def page3 is the code to be run when the user clicks on the Next button - it creates page3
    tut.destroy()
    tut2 = tk.Tk()

    def page3():  # third page
      tut2.destroy()
      tut3 = tk.Tk()
      tut3.wm_title("Part 3!")

      label = ttk.Label(tut3, text="Part 3", font=NORM_FONT)
      label.pack(side="top", fill="x", pady=10)
      B1 = ttk.Button(tut3, text="Done!", command= tut3.destroy)
      B1.pack()
      tut3.mainloop()

    tut2.wm_title("Part 2!")
    label = ttk.Label(tut2, text="Part 2", font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(tut2, text="Next", command= page3)
    B1.pack()
    tut2.mainloop()

  tut = tk.Tk()
  tut.wm_title("Tutorial") # First page of the tutorial
  label = ttk.Label(tut, text="What do you need help with?", font=NORM_FONT)
  label.pack(side="top", fill="x", pady=10)

  B1 = ttk.Button(tut, text = "Overview of the application", command=page2)
  B1.pack()

  B2 = ttk.Button(tut, text = "How do I trade with this client?", command=lambda:popupmsg("Not yet completed"))
  B2.pack()

  B3 = ttk.Button(tut, text = "Indicator Questions/Help", command=lambda:popupmsg("Not yet completed"))
  B3.pack()

  tut.mainloop()

def addTopIndicator(what):
  global topIndicator
  global datCounter

  if dataPace == "tick":
    popupmsg("Indicators in tick data not available")

  if what == "none":
    topIndicator = what
    datCounter = 9000 # we keep resetting the value of datCounter, because it forces an update  

  elif what == "rsi":
    rsiQ = tk.Tk() # new window
    rsiQ.wm_title("Periods for the RSI") # give the window a title
    label = ttk.Label(rsiQ, text="Choose how many periods you would like to use")
    label.pack(side="top", fill="x", pady=10)

    e = ttk.Entry(rsiQ) #ttk input text field
    e.insert(0,14)
    e.pack() # no need to enter attributes, because it will be place right under the label
    e.focus_set()

    def callback(): #for the button b, run when user clicks on Submit
      global topIndicator
      global datCounter

      periods = (e.get())  # gets user input
      group = []
      group.append("rsi")
      group.append(periods)

      topIndicator = group
      datCounter = 9000 #force an update
      rsiQ.destroy()

    b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
    b.pack()
    tk.mainloop()

  elif what == "macd":
    #global topIndicator #we have to global those variables to be able to alter them
    #global datCounter
    topIndicator = "macd"
    datCounter = 9000

def addBottomIndicator(what):
  global bottomIndicator
  global datCounter

  if dataPace == "tick":
    popupmsg("Indicators in tick data not available")

  if what == "none":
    bottomIndicator = what
    datCounter = 9000 # we keep resetting the value of datCounter, because it forces an update  

  elif what == "rsi":
    rsiQ = tk.Tk() # new window
    rsiQ.wm_title("Periods for the RSI") # give the window a title
    label = ttk.Label(rsiQ, text="Choose how many periods you would like to use")
    label.pack(side="top", fill="x", pady=10)

    e = ttk.Entry(rsiQ) #ttk input text field
    e.insert(0,14)
    e.pack() # no need to enter attributes, because it will be place right under the label
    e.focus_set()

    def callback(): #for the button b, run when user clicks on Submit
      global bottomIndicator
      global datCounter

      periods = (e.get())  # gets user input
      group = []
      group.append("rsi")
      group.append(periods)

      bottomIndicator = group
      datCounter = 9000 #force an update
      rsiQ.destroy()

    b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
    b.pack()
    tk.mainloop()

  elif what == "macd":
    #global topIndicator #we have to global those variables to be able to alter them
    #global datCounter
    bottomIndicator = "macd"
    datCounter = 9000

def addMiddleIndicator(what):
    global middleIndicator
    global datCounter

    if dataPace == "tick":
        popupmsg("Indicators in Tick Data not available.")

    if what != "none":
        if middleIndicator == "none":
            if what == "sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want your SMA to be.")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global datCounter

                    middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    datCounter = 9000
                    print("middle indicator set to:",middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

            if what == "ema":
                midIQ = tk.Tk()
                #midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want your EMA to be.")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global datCounter

                    middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    datCounter = 9000
                    print("middle indicator set to:",middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()
                
        else:
            if what == "sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want your SMA to be.")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global datCounter

                    #middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    datCounter = 9000
                    print("middle indicator set to:",middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()



                
            if what == "ema":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want your EMA to be.")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global datCounter

                    #middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    datCounter = 9000
                    print("middle indicator set to:",middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

    else:
        middleIndicator = "none"


def changeTimeFrame(tf):
    global dataPace
    global datCounter
    if tf == "7d" and resampleSize == "1Min":
        popupmsg("Too much data chosen, choose a smaller timeframe")
    else:
        dataPace = tf
        datCounter = 9000


def changeSampleSize(size, width):
    global resampleSize
    global datCounter
    global candleWidth
    if dataPace == "7d" and resampleSize == "1Min":
        popupmsg("Too much data chosen, choose a smaller timeframe")
    elif dataPace == "tick":
        popupmsg("You are currently viewing tick data, not OHLC.")
    # else:
    # #TODO: we dont use this
    #     resampleSize = sizeDat
    #     datCounter = 9000
    #     candleWidth = width


def changeExchange(toWhat, pn):  # pn is the program name
    global exchange  # we global the variables so we are able to modify them
    global datCounter
    global programName

    exchange = toWhat
    datCounter = 9000
    programName = pn


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
        tk.Frame.__init__(self, parent)  # StartPages's parent is the MainForm class
        #label = tk.Label(self, text="Cryptocurrencies \nTrading Analyse", font=LARGE_FONT)  # like the JavaFX label
        #label.pack(pady=10, padx=10)  # if you have 1,2 or 3 elements, use pack. Otherwise, use grid()
        #button1 = tk.Button(self, text="Agree", command=lambda: controller.show_frame(BTCe_Page))
        # dont pass the function directly to command as command=qf("text").
        # The function will be executed once and not again.
        # To be able to run the function every time the button is pressed, use lambda:
        #button2 = tk.Button(self, text="Disagree", command=quit)
        #button1.pack()
        #button2.pack()
        self.valor = tk.StringVar()
        self.valor.set("Hola Manejando datos") # ?????? why we need this
        tk.Label(self, textvariable=self.valor).pack()

        # #TODO: we dont use this
        # button2 = tk.Button(self, text="Page Two", command=lambda: controller.show_frame(PageTwo))
        # button2.pack()

# reference to how to create a new page
class PageOne(tk.Frame):
    # sometimes you program the whole page under the __init__ function
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()


class BTCe_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        ### add a matplotlib graph to the page
        canvas = FigureCanvasTkAgg(controller.f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # add matplotlib toolbar (zoom, home, etc)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # run animate every 2 seconds; beware: while the app is updating, the app becomes frozen


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
        menubar.add_cascade(label="Windows", menu=correlation_menu)

        data_menu = tk.Menu(menubar, tearoff=1)
        data_menu.add_command(label="Markets", command=lambda: self.show_frame(ExchangeDataFrame))
        data_menu.add_command(label="Currencies", command=lambda: self.show_frame(CryptocurrencyDataFrame))
        data_menu.add_command(label="Symbols", command=lambda: self.show_frame(SymbolDataFrame))
        data_menu.add_command(label="History", command=lambda: self.show_frame(HistoryDataFrame))
        menubar.add_cascade(label="Show data", menu=data_menu)

        # submenu Exchange
        exchangeChoice = tk.Menu(menubar, tearoff=1)
        # BETC-e does not exist anymore
        # exchangeChoice.add_command(label="BTC-e", command=lambda: changeExchange("BTC-e", "btce"))
        exchangeChoice.add_command(label="Bitfinex", command=lambda: changeExchange("Bitfinex", "bitfinex"))
        exchangeChoice.add_command(label="Bitstamp", command=lambda: changeExchange("Bitstamp", "bitstamp"))
        exchangeChoice.add_command(label="Huobi", command=lambda: changeExchange("Huobi", "huobi"))
        menubar.add_cascade(label="Exchange", menu=exchangeChoice)

        # # submenu Data Time Frame Selection
        # dataTF = tk.Menu(menubar, tearoff=1)
        # dataTF.add_cascade(label="Tick", command=lambda: changeTimeFrame('tick'))
        # dataTF.add_cascade(label="1 Day", command=lambda: changeTimeFrame('1d'))
        # dataTF.add_cascade(label="3 Day", command=lambda: changeTimeFrame('3d'))
        # dataTF.add_cascade(label="1 Week", command=lambda: changeTimeFrame('7d'))
        # menubar.add_cascade(label="Data Time Frame", menu=dataTF)
        #
        # OHLCI = tk.Menu(menubar, tearoff=1)
        # OHLCI.add_command(label="Tick", command=lambda: changeTimeFrame('tick'))
        # OHLCI.add_command(label="1 Minute", command=lambda: changeSampleSize('1Min', 0.0005))
        # OHLCI.add_command(label="5 Minute", command=lambda: changeSampleSize('5Min', 0.003))
        # OHLCI.add_command(label="15 Minute", command=lambda: changeSampleSize('15Min', 0.008))
        # OHLCI.add_command(label="30 Minute", command=lambda: changeSampleSize('30Min', 0.016))
        # OHLCI.add_command(label="1 Hour", command=lambda: changeSampleSize('1H', 0.032))
        # OHLCI.add_command(label="3 Hour", command=lambda: changeSampleSize('3H', 0.096))
        # menubar.add_cascade(label="OHLC Interval", menu=OHLCI)
        #
        # topIndi = tk.Menu(menubar, tearoff=1)
        # topIndi.add_command(label="None", command=lambda: addTopIndicator("none"))
        # topIndi.add_command(label="RSI", command=lambda: addTopIndicator("rsi"))
        # topIndi.add_command(label="MACD", command=lambda: addTopIndicator("macd"))
        # menubar.add_cascade(label="Top Indicator", menu=topIndi)
        #
        # mainIndi = tk.Menu(menubar, tearoff=1)
        # mainIndi.add_command(label="None", command=lambda: addMiddleIndicator("none"))
        # mainIndi.add_command(label="SMA", command=lambda: addMiddleIndicator("sma"))
        # mainIndi.add_command(label="EMA", command=lambda: addMiddleIndicator("ema"))
        # menubar.add_cascade(label="Main Indicator", menu=mainIndi)
        #
        # bottomIndi = tk.Menu(menubar, tearoff=1)
        # bottomIndi.add_command(label="None", command=lambda: addBottomIndicator("none"))
        # bottomIndi.add_command(label="RSI", command=lambda: addBottomIndicator("rsi"))
        # bottomIndi.add_command(label="MACD", command=lambda: addBottomIndicator("macd"))
        # menubar.add_cascade(label="Bottom Indicator", menu=bottomIndi)
        #
        # tradeButton = tk.Menu(menubar, tearoff=1)
        # tradeButton.add_command(label="Manual Trading", command=lambda: popupmsg("Not live yet"))
        # tradeButton.add_command(label="Automated Trading", command=lambda: popupmsg("Not live yet"))
        # tradeButton.add_separator()
        #
        # tradeButton.add_command(label="Quick Buy", command=lambda: popupmsg("Not live yet"))
        # tradeButton.add_command(label="Quick Sell", command=lambda: popupmsg("Not live yet"))
        # tradeButton.add_separator()
        #
        # tradeButton.add_command(label="Setup Quick Buy/Sell", command=lambda: popupmsg("Not live yet"))
        #
        # menubar.add_cascade(label="Trading", menu=tradeButton)

        startStop = tk.Menu(menubar, tearoff=1)
        startStop.add_command(label="Resume", command=lambda: loadChart('start'))
        startStop.add_command(label="Pause", command=lambda: loadChart('stop'))
        menubar.add_cascade(label="Resume/Pause client", menu=startStop)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Tutorial", command=tutorial)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # set menubar
        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        # each frame in frames (dictionary) is a different window in our application.
        # If a certain page is not in self.frames, we cant display it
        # when we want to show a specific window, we run code to change the frame in frames

        # packing each page into frames:
        for F in (StartPage, BTCe_Page, CorrelationFrame):
            frame = F(container, self)  # main page
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            # with grid, we place the frame in the specified row and column
            # sticky=W would align the element to the left edge of the cell,
            # sticky='ew' would stretch the element to west and east (centering and stretching it);
            # sticky="nsew" stretches the element to the size of the window
            # if you dont use a row, default is the first unused row in the grid
            # http://effbot.org/tkinterbook/grid.htm for more grid() options

        for F in (HistoryDataFrame, CryptocurrencyDataFrame, ExchangeDataFrame, SymbolDataFrame, CorrelationGraphFrame, ImportHistoryFrame, AutocorrelationGraphFrame, OhlcGraphFrame):
            frame = F(container, self)  # main page
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        a = self.f.add_subplot(111)
        # THIS is life animation
        # ani = animation.FuncAnimation(self.f, FrameLiveCourse, fargs=[a], interval=1000)
        self.f.canvas.draw()
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        if frame.update:
            frame.update()
        frame.tkraise()
        # tkraise() raises frame to the front


app = MainForm()
app.geometry("1280x720")
app.mainloop()

