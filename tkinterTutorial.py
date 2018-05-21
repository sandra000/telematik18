import tkinter as tk
from tkinter import ttk #css for tkinter
import sqlite3

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#FigureCanvasTkAgg allows us to draw matplotlib to a canvas with TkAgg
#NavigationToolbar2TkAgg is the small toolbar in every matplotlib graph
#from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc

import urllib
import json

import pandas as pd
import numpy as np

import models

session = models.Session()

#style.use("ggplot")

 # defining constants
LARGE_FONT =("Verdana", 12)
NORM_FONT=("Verdana", 10)
SMALL_FONT =("Verdana", 8)


#create a live matplotlib graph. Canvas:
#f = Figure(figsize=(10,6), dpi=100)

f = plt.figure()
a = f.add_subplot(111)

# DEFAULT VALUES - the user can change them in the menubar later
exchange = "Bitfinex"
datCounter = 9000 #time to update 
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

def loadChart(run):
  global chartLoad

  if run == "start":
    chartLoad = True

  elif run == "stop":
      chartLoad = False

def tutorial():

  def page2():  #second page; it first closes page1, creates a new window; def page3 is the code to be run when the user clicks on the Next button - it creates page3
    tut.destroy()
    tut2 = tk.Tk()

    def page3():  #third page
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
  if tf == "7d" and resampleSize=="1Min":
    popupmsg("Too much data chosen, choose a smaller timeframe")
  else:
    dataPace = tf
    datCounter = 9000

def changeSampleSize(size, width):
  global resampleSize
  global datCounter
  global candleWidth
  if dataPace == "7d" and resampleSize=="1Min":
    popupmsg("Too much data chosen, choose a smaller timeframe")
  elif dataPace == "tick":
    popupmsg("You are currently viewing tick data, not OHLC.")
  else:
    resampleSize = sizeDat
    datCounter = 9000
    candleWidth = width

def changeExchange(toWhat, pn): #pn is the program name
  global exchange  #we global the variables so we are able to modify them
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

#Function to read the live data from a file
def animate(i):
  #plotting live data from a file
  # pullData = open("sampleData.txt", "r").read()
  # dataList = pullData.split("\n")
  # xs = []
  # ys = []
  # for i in dataList:
  #   if len(i)>1:
  #     x, y = i.split(",")
  #     xs.append(int(x))
  #     ys.append(int(y))
  # a.clear() #clear the graph
  # a.plot(xs,ys)

  global refreshRate
  global datCounter

  if chartLoad:
    if paneCount == 1:
      if dataPace == "tick":
        try:
          if exchange == "Bitfinex":
            #Subplot 1
            a = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
            #full grid 6x4; starting point is (0,0); 

            #Subplot 2
            a2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex = a)
            #if you zoom in a2, it zooms in a too

            #plotting live data from a website
            dataLink = "https://api.bitfinex.com/v1/trades/BTCUSD?limit_trades=2000"
            data = urllib.request.urlopen(dataLink)
            data = data.read().decode("utf-8") #data comes in bytes; we decode it to utf-8
            data = json.loads(data)        # data = data["btc_usd"] is useless for us
            
            data = pd.DataFrame(data)

            data["datestamp"] = np.array(data['timestamp']).astype("datetime64[s]")
            allDates = data["datestamp"].tolist() # probably, because you cant convert directly from dataframe column to a python list; first you have to convert to a numpy array


            buys = data[(data["type"]=="buy")]  
            #buys["datestamp"]= np.array(buys["timestamp"]).astype("datetime64[s]")
            buyDates = (buys["datestamp"]).tolist()
            
            
            sells = data[(data["type"]=="sell")] 

            #sells["datestamp"]= np.array(sells["timestamp"]).astype("datetime64[s]")
            sellDates = (sells["datestamp"]).tolist()

            volume = data["amount"].apply(float).tolist()

            a.clear()
            a.plot_date(buyDates, buys["price"], lightColor, label="buys")
            a.plot_date(sellDates,sells["price"], darkColor, label="sells")
            
            #does not work, because we dont receive the volume data from the alternative site
            a2.fill_between(allDates, 0, volume, facecolor=darkColor)

            a.xaxis.set_major_locator(mticker.MaxNLocator(5))
            #5 is the maximum number of values displayed on the x axis
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y %H:%M:%S"))
            #format of the date
            plt.setp(a.get_xticklabels(), visible=False)
            #it removes the labels in the x axis of the first graph

            #a.legend() # simple legend, be aware it may cover the graph
            a.legend(bbox_to_anchor=(0,1.02,1,.102), loc=3, ncol=2, borderaxespad=0)
            
            title = "BTC-e BTCUSD" "\nLast Price: " #+ str(data["price"].tail(1)) # the index 1999 does not work
            a.set_title(title)

            priceData = df['price'].apply(float).tolist()


        except Exception as e:
          print("Exception: ", e)

      else:
        if datCounter > 12:
            try:
                if exchange == "Huobi":
                    if topIndicator != "none":
                        a = plt.subplot2grid((6,4),(1,0), rowspan=5, colspan = 4)
                        a2 = plt.subplot2grid((6,4),(0,0),sharex=a, rowspan=1, colspan = 4)
                    else:
                        a = plt.subplot2grid((6,4),(0,0), rowspan=6, colspan = 4)

                else:
                    if topIndicator != "none" and bottomIndicator != "none":
                        # Main Graph
                        a = plt.subplot2grid((6,4), (1,0), rowspan = 3, colspan = 4)

                        # Volume
                        a2 = plt.subplot2grid((6,4), (4,0), sharex = a, rowspan = 1, colspan = 4)

                        # Bottom Indicator
                        a3 = plt.subplot2grid((6,4), (5,0), sharex = a, rowspan = 1, colspan = 4)

                        # Top Indicator
                        a0 = plt.subplot2grid((6,4), (0,0), sharex = a, rowspan = 1, colspan = 4)

                    elif topIndicator != "none":
                        # Main Graph
                        a = plt.subplot2grid((6,4), (1,0), rowspan = 4, colspan = 4)

                        # Volume
                        a2 = plt.subplot2grid((6,4), (5,0), sharex = a, rowspan = 1, colspan = 4)

                        # Top Indicator
                        a0 = plt.subplot2grid((6,4), (0,0), sharex = a, rowspan = 1, colspan = 4)

                    elif bottomIndicator != "none":

                        # Main Graph
                        a = plt.subplot2grid((6,4), (0,0), rowspan = 4, colspan = 4)

                        # Volume
                        a2 = plt.subplot2grid((6,4), (4,0), sharex = a, rowspan = 1, colspan = 4)

                        # Bottom Indicator
                        a3 = plt.subplot2grid((6,4), (5,0), sharex = a, rowspan = 1, colspan = 4)

                    else:
                        # Main Graph
                        a = plt.subplot2grid((6,4), (0,0), rowspan = 5, colspan = 4)

                        # Volume
                        a2 = plt.subplot2grid((6,4), (5,0), sharex = a, rowspan = 1, colspan = 4)

                data = urllib.request.urlopen("http://seaofbtc.com/api/basic/price?key=1&tf="+dataPace+"&exchange="+programName).read()
                data = data.decode()
                data = json.loads(data)

                dateStamp = np.array(data[0]).astype("datetime64[s]")
                dateStamp = dateStamp.tolist()

                df = pd.DataFrame({'Datetime':dateStamp})

                df['Price'] = data[1]
                df['Volume'] = data[2]
                df['Symbol'] = 'BTCUSD'
                df['MPLDate'] = df['Datetime'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
                df = df.set_index("Datetime")


                OHLC = df['Price'].resample(resampleSize, how="ohlc")
                OHLC = OHLC.dropna()

                volumeData = df['Volume'].resample(resampleSize, how={'volume':'sum'})

                OHLC["dateCopy"] = OHLC.index
                OHLC["MPLDates"] = OHLC["dateCopy"].apply(lambda date: mdates.date2num(date.to_pydatetime()))

                del OHLC["dateCopy"]


                volumeData["dateCopy"] = volumeData.index
                volumeData["MPLDates"] = volumeData["dateCopy"].apply(lambda date: mdates.date2num(date.to_pydatetime()))

                del volumeData["dateCopy"]

                priceData = OHLC['close'].apply(float).tolist()

                a.clear()

                if middleIndicator != "none":
                  for eachMA in middleIndicator:
                    if eachMA[0] == "sma":
                      sma = pd.rolling_mean(OHLC["close"], eachMA[1])
                      label = str(eachMA[1])+" SMA"
                      a.plot(OHLC["MPLDates"], sma, label=label)

                    if eachMA[0] == "ema":
                      ewma = pd.stats.moments.ewma
                      label = str(eachMA[1])+" EMA"
                      a.plot(OHLC["MPLDates"], ewma(OHLC["close"], eachMA[1]), label=label)

                  a.legend(loc=0)


                if topIndicator[0] == "rsi":
                  rsiIndicator(priceData,"top")

                elif topIndicator == "macd":
                  try:
                    computeMACD(priceData, location = "top")

                  except Exception as e:
                    print(str(e))



                if bottomIndicator[0] == "rsi":
                  rsiIndicator(priceData,"bottom")

                elif bottomIndicator == "macd":
                  try:
                    computeMACD(priceData, location = "bottom")

                  except Exception as e:
                    print(str(e))


                csticks = candlestick_ohlc(a, OHLC[["MPLDates","open","high","low","close"]].values, width = candleWidth, colorup=lightColor, colordown=darkColor)
                a.set_ylabel("Price")
                if exchange != "Huobi":
                  a2.fill_between(volumeData["MPLDates"],0, volumeData['volume'], facecolor = darkColor)
                  a2.set_ylabel("Volume")

                a.xaxis.set_major_locator(mticker.MaxNLocator(3))
                a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

                if exchange != "Huobi":
                  plt.setp(a.get_xticklabels(), visible=False)


                if topIndicator != "none":
                  plt.setp(a0.get_xticklabels(), visible=False)

                if bottomIndicator != "none":
                  plt.setp(a2.get_xticklabels(), visible=False) #a2 is the Volume

                x = (len(OHLC['close']))-1 #get the last price

                if dataPace == "1d":
                  title = exchange+" 1 Day Data with "+resampleSize+" Bars\nLast Price: "+str(OHLC['close'][x])
                if dataPace == "3d":
                  title = exchange+" 3 Day Data with "+resampleSize+" Bars\nLast Price: "+str(OHLC['close'][x])
                if dataPace == "7d":
                  title = exchange+" 7 Day Data with "+resampleSize+" Bars\nLast Price: "+str(OHLC['close'][x])

                if topIndicator != "none":
                  a0.set_title(title)

                else:
                  a.set_title(title)

                print("New Graph")
                datCounter = 0



            except Exception as e:
                print('failed in the non-tick animate:',str(e))
                datCounter = 9000

        else:
          darCounter -= 1        






class SeaofBTCapp(tk.Tk): # SeaofBTCapp is the main class. It inherits from tk.Tk
  
  def __init__(self, *args, **kwargs): 
    #when we call upon the class, this initalize method WILL ALWAYS RUN
    #self is always implied as the first argument
    # *args is any number of variables
    # **kwargs keyword arguments; we are passing through dictionaries
    tk.Tk.__init__(self, *args, **kwargs)
    #initalizing tkinter
    
    
    tk.Tk.wm_title(self, "Sea of BTC client")
    
    
    container = tk.Frame(self)
    #container is the basis of every Tkinter GUI. 
    #Frame is the edges of the basic window
    container.pack(side="top", fill="both", expand=True)
    #pack shoves elements in the window, side="top" means we are placing the element on the top of the window; fill="both" means it fills the limits we set; expand=True means if there is space left, the element should expand and occupy it
    #grid does the same, but we are able to better organize the elemts inside the window
    container.grid_rowconfigure(0, weight=1)
    # 0 is the minimum size, weight=1 means priority equals 1
    container.grid_columnconfigure(0, weight=1)
    
    
    # 1. We define what a menubar is (backend)
    menubar = tk.Menu(container) # puts the menubar inside the container
    filemenu = tk.Menu(menubar, tearoff=0) # puts the File submenu inside the menubar; tearoff means you can detach the menu 
    filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported just yet!"))
    filemenu.add_separator() #adds a line between the menu options
    filemenu.add_command(label="Exit", command=quit)
    # 2. We show the menubar (frontend)
    menubar.add_cascade(label="File", menu=filemenu)
    
    #submenu Exchange
    exchangeChoice = tk.Menu(menubar, tearoff=1)
    #BETC-e does not exist anymore
    #exchangeChoice.add_command(label="BTC-e", command=lambda: changeExchange("BTC-e", "btce"))
    exchangeChoice.add_command(label="Bitfinex", command=lambda: changeExchange("Bitfinex", "bitfinex"))
    exchangeChoice.add_command(label="Bitstamp", command=lambda: changeExchange("Bitstamp", "bitstamp"))
    exchangeChoice.add_command(label="Huobi", command=lambda: changeExchange("Huobi", "huobi"))
    menubar.add_cascade(label="Exchange", menu=exchangeChoice)

    #submenu Data Time Frame Selection
    dataTF = tk.Menu(menubar, tearoff=1)
    dataTF.add_cascade(label="Tick", command=lambda: changeTimeFrame('tick'))
    dataTF.add_cascade(label="1 Day", command=lambda: changeTimeFrame('1d'))
    dataTF.add_cascade(label="3 Day", command=lambda: changeTimeFrame('3d'))
    dataTF.add_cascade(label="1 Week", command=lambda: changeTimeFrame('7d'))
    menubar.add_cascade(label="Data Time Frame", menu=dataTF)

    OHLCI = tk.Menu(menubar, tearoff=1)
    OHLCI.add_command(label="Tick", command= lambda: changeTimeFrame('tick'))
    OHLCI.add_command(label="1 Minute", command= lambda: changeSampleSize('1Min', 0.0005))
    OHLCI.add_command(label="5 Minute", command= lambda: changeSampleSize('5Min', 0.003))
    OHLCI.add_command(label="15 Minute", command= lambda: changeSampleSize('15Min', 0.008))
    OHLCI.add_command(label="30 Minute", command= lambda: changeSampleSize('30Min', 0.016))
    OHLCI.add_command(label="1 Hour", command= lambda: changeSampleSize('1H', 0.032))
    OHLCI.add_command(label="3 Hour", command= lambda: changeSampleSize('3H', 0.096))
    menubar.add_cascade(label="OHLC Interval", menu=OHLCI)

    topIndi = tk.Menu(menubar, tearoff=1)
    topIndi.add_command(label="None", command= lambda: addTopIndicator("none"))
    topIndi.add_command(label="RSI", command= lambda: addTopIndicator("rsi"))
    topIndi.add_command(label="MACD", command= lambda: addTopIndicator("macd"))
    menubar.add_cascade(label="Top Indicator", menu=topIndi)

    mainIndi = tk.Menu(menubar, tearoff=1)
    mainIndi.add_command(label="None", command= lambda: addMiddleIndicator("none"))
    mainIndi.add_command(label="SMA", command= lambda: addMiddleIndicator("sma"))
    mainIndi.add_command(label="EMA", command= lambda: addMiddleIndicator("ema"))
    menubar.add_cascade(label="Main Indicator", menu=mainIndi)

    
    bottomIndi = tk.Menu(menubar, tearoff=1)
    bottomIndi.add_command(label="None", command= lambda: addBottomIndicator("none"))
    bottomIndi.add_command(label="RSI", command= lambda: addBottomIndicator("rsi"))
    bottomIndi.add_command(label="MACD", command= lambda: addBottomIndicator("macd"))
    menubar.add_cascade(label="Bottom Indicator", menu=bottomIndi)
    
    tradeButton = tk.Menu(menubar, tearoff=1)
    tradeButton.add_command(label="Manual Trading", command=lambda: popupmsg("Not live yet"))
    tradeButton.add_command(label="Automated Trading", command=lambda: popupmsg("Not live yet"))
    tradeButton.add_separator()

    tradeButton.add_command(label="Quick Buy", command=lambda: popupmsg("Not live yet"))
    tradeButton.add_command(label="Quick Sell", command=lambda: popupmsg("Not live yet"))
    tradeButton.add_separator()
    
    tradeButton.add_command(label="Setup Quick Buy/Sell", command=lambda: popupmsg("Not live yet"))
    
    menubar.add_cascade(label="Trading", menu=tradeButton)

    startStop = tk.Menu(menubar, tearoff = 1)
    startStop.add_command( label="Resume", command = lambda: loadChart('start'))
    startStop.add_command( label="Pause", command = lambda: loadChart('stop'))
    menubar.add_cascade(label = "Resume/Pause client", menu = startStop)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Tutorial", command=tutorial)
    menubar.add_cascade(label="Help", menu=helpmenu)
    
    
    
    
    
    #fixed, it belongs to the menubar
    tk.Tk.config(self, menu=menubar)
    
    
    self.frames = {} 
    #each frame in frames (dictionary) is a different window in our application. If a certain page is not in self.frames, we cant display it
    # when we want to show a specific window, we run code to change the frame in frames
    
    #packing each page into frames:
    for F in (StartPage, BTCe_Page):
      frame = F(container, self) # main page
      self.frames[F] = frame
      frame.grid(row=0, column=0, sticky="nsew")
      #with grid, we place the frame in the specified row and column
      #sticky=W would align the element to the left edge of the cell, sticky='ew' would stretch the element to west and east (centering and stretching it); sticky="nsew" stretches the element to the size of the window
      #if you dont use a row, default is the first unused row in the grid
      #http://effbot.org/tkinterbook/grid.htm for more grid() options 
    
    self.show_frame(StartPage)
    
  def show_frame(self, cont):
    
    frame = self.frames[cont]
    frame.tkraise()
    #tkraise() raises frame to the front
    

class StartPage(tk.Frame):
  
  def __init__(self, parent, controller):
    
    tk.Frame.__init__(self, parent) #StartPages's parent is the SeaofBTCapp class
    label = tk.Label(self, text="Bitcoin Application\nTrading", font=LARGE_FONT) #like the JavaFX label
    label.pack(pady=10, padx=10) #if you have 1,2 or 3 elements, use pack. Otherwise, use grid()
    button1 = tk.Button(self, text="Agree", command=lambda: controller.show_frame(BTCe_Page))
    #dont pass the function directly to command as command=qf("text"). The function will be executed once and not again. To be able to run the function every time the button is pressed, use lambda:
    button1.pack()
    button2 = tk.Button(self, text="Disagree", command=quit)
    button2.pack()

#reference to how to create a new page
class PageOne(tk.Frame):
  #sometimes you program the whole page under the __init__ function 
  def __init__(self, parent, controller):
    tk.Frame.__init__(self,parent)
    label = tk.Label(self, text="Page One", font=LARGE_FONT) 
    label.pack(pady=10, padx=10) 
    
    button1 = tk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
    button1.pack()
    
    button2 = tk.Button(self, text="Page Two", command=lambda: controller.show_frame(PageTwo))
    button2.pack()
    
    
class BTCe_Page(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self,parent)
    label = tk.Label(self, text="Graph Page", font=LARGE_FONT) 
    label.pack(pady=10, padx=10) 
    
    button1 = tk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
    button1.pack()

#######add a matplotlib graph to the page    
    canvas = FigureCanvasTkAgg(f, self)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # add matplotlib toolbar (zoom, home, etc)
    toolbar = NavigationToolbar2TkAgg(canvas, self)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

  
app = SeaofBTCapp()
app.geometry("1280x720") # size of the window
ani = animation.FuncAnimation(f, animate, interval=1000) #run animate every 2 seconds; beware: while the app is updating, the app becomes frozen
app.mainloop()
#mainloop() is a tkinter method to "run" the app