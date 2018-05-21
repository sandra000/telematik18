from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import pandas as pd
import json
import urllib
import numpy as np


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


def animate(i, a):
    global refreshRate
    global datCounter

    if chartLoad:
        if paneCount == 1:
            if dataPace == "tick":
                try:
                    if exchange == "Bitfinex":
                        # Subplot 1
                        a = plt.subplot2grid((6, 4), (0, 0), rowspan=5, colspan=4)
                        # full grid 6x4; starting point is (0,0);

                        # Subplot 2
                        a2 = plt.subplot2grid((6, 4), (5, 0), rowspan=1, colspan=4, sharex=a)
                        # if you zoom in a2, it zooms in a too

                        # plotting live data from a website
                        dataLink = "https://api.bitfinex.com/v1/trades/BTCUSD?limit_trades=2000"
                        data = urllib.request.urlopen(dataLink)
                        data = data.read().decode("utf-8")  # data comes in bytes; we decode it to utf-8
                        data = json.loads(data)  # data = data["btc_usd"] is useless for us

                        data = pd.DataFrame(data)

                        data["datestamp"] = np.array(data['timestamp']).astype("datetime64[s]")
                        allDates = data[
                            "datestamp"].tolist()  # probably, because you cant convert directly from dataframe column to a python list; first you have to convert to a numpy array

                        buys = data[(data["type"] == "buy")]
                        # buys["datestamp"]= np.array(buys["timestamp"]).astype("datetime64[s]")
                        buyDates = (buys["datestamp"]).tolist()

                        sells = data[(data["type"] == "sell")]

                        # sells["datestamp"]= np.array(sells["timestamp"]).astype("datetime64[s]")
                        sellDates = (sells["datestamp"]).tolist()

                        volume = data["amount"].apply(float).tolist()

                        a.clear()
                        a.plot_date(buyDates, buys["price"], lightColor, label="buys")
                        a.plot_date(sellDates, sells["price"], darkColor, label="sells")

                        # does not work, because we dont receive the volume data from the alternative site
                        a2.fill_between(allDates, 0, volume, facecolor=darkColor)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        # 5 is the maximum number of values displayed on the x axis
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y %H:%M:%S"))
                        # format of the date
                        plt.setp(a.get_xticklabels(), visible=False)
                        # it removes the labels in the x axis of the first graph

                        # a.legend() # simple legend, be aware it may cover the graph
                        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)

                        title = "BTC-e BTCUSD" "\nLast Price: "  # + str(data["price"].tail(1)) # the index 1999 does not work
                        a.set_title(title)

                        priceData = df['price'].apply(float).tolist()


                except Exception as e:
                    print("Exception: ", e)

            else:
                if datCounter > 12:
                    try:
                        if exchange == "Huobi":
                            if topIndicator != "none":
                                a = plt.subplot2grid((6, 4), (1, 0), rowspan=5, colspan=4)
                                a2 = plt.subplot2grid((6, 4), (0, 0), sharex=a, rowspan=1, colspan=4)
                            else:
                                a = plt.subplot2grid((6, 4), (0, 0), rowspan=6, colspan=4)

                        else:
                            if topIndicator != "none" and bottomIndicator != "none":
                                # Main Graph
                                a = plt.subplot2grid((6, 4), (1, 0), rowspan=3, colspan=4)

                                # Volume
                                a2 = plt.subplot2grid((6, 4), (4, 0), sharex=a, rowspan=1, colspan=4)

                                # Bottom Indicator
                                a3 = plt.subplot2grid((6, 4), (5, 0), sharex=a, rowspan=1, colspan=4)

                                # Top Indicator
                                a0 = plt.subplot2grid((6, 4), (0, 0), sharex=a, rowspan=1, colspan=4)

                            elif topIndicator != "none":
                                # Main Graph
                                a = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4)

                                # Volume
                                a2 = plt.subplot2grid((6, 4), (5, 0), sharex=a, rowspan=1, colspan=4)

                                # Top Indicator
                                a0 = plt.subplot2grid((6, 4), (0, 0), sharex=a, rowspan=1, colspan=4)

                            elif bottomIndicator != "none":

                                # Main Graph
                                a = plt.subplot2grid((6, 4), (0, 0), rowspan=4, colspan=4)

                                # Volume
                                a2 = plt.subplot2grid((6, 4), (4, 0), sharex=a, rowspan=1, colspan=4)

                                # Bottom Indicator
                                a3 = plt.subplot2grid((6, 4), (5, 0), sharex=a, rowspan=1, colspan=4)

                            else:
                                # Main Graph
                                a = plt.subplot2grid((6, 4), (0, 0), rowspan=5, colspan=4)

                                # Volume
                                a2 = plt.subplot2grid((6, 4), (5, 0), sharex=a, rowspan=1, colspan=4)

                        data = urllib.request.urlopen(
                            "http://seaofbtc.com/api/basic/price?key=1&tf=" + dataPace + "&exchange=" + programName).read()
                        data = data.decode()
                        data = json.loads(data)

                        dateStamp = np.array(data[0]).astype("datetime64[s]")
                        dateStamp = dateStamp.tolist()

                        df = pd.DataFrame({'Datetime': dateStamp})

                        df['Price'] = data[1]
                        df['Volume'] = data[2]
                        df['Symbol'] = 'BTCUSD'
                        df['MPLDate'] = df['Datetime'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
                        df = df.set_index("Datetime")

                        OHLC = df['Price'].resample(resampleSize, how="ohlc")
                        OHLC = OHLC.dropna()

                        volumeData = df['Volume'].resample(resampleSize, how={'volume': 'sum'})

                        OHLC["dateCopy"] = OHLC.index
                        OHLC["MPLDates"] = OHLC["dateCopy"].apply(lambda date: mdates.date2num(date.to_pydatetime()))

                        del OHLC["dateCopy"]

                        volumeData["dateCopy"] = volumeData.index
                        volumeData["MPLDates"] = volumeData["dateCopy"].apply(
                            lambda date: mdates.date2num(date.to_pydatetime()))

                        del volumeData["dateCopy"]

                        priceData = OHLC['close'].apply(float).tolist()

                        a.clear()

                        if middleIndicator != "none":
                            for eachMA in middleIndicator:
                                if eachMA[0] == "sma":
                                    sma = pd.rolling_mean(OHLC["close"], eachMA[1])
                                    label = str(eachMA[1]) + " SMA"
                                    a.plot(OHLC["MPLDates"], sma, label=label)

                                if eachMA[0] == "ema":
                                    ewma = pd.stats.moments.ewma
                                    label = str(eachMA[1]) + " EMA"
                                    a.plot(OHLC["MPLDates"], ewma(OHLC["close"], eachMA[1]), label=label)

                            a.legend(loc=0)

                        if topIndicator[0] == "rsi":
                            rsiIndicator(priceData, "top")

                        elif topIndicator == "macd":
                            try:
                                computeMACD(priceData, location="top")

                            except Exception as e:
                                print(str(e))

                        if bottomIndicator[0] == "rsi":
                            rsiIndicator(priceData, "bottom")

                        elif bottomIndicator == "macd":
                            try:
                                computeMACD(priceData, location="bottom")

                            except Exception as e:
                                print(str(e))

                        csticks = candlestick_ohlc(a, OHLC[["MPLDates", "open", "high", "low", "close"]].values,
                                                   width=candleWidth, colorup=lightColor, colordown=darkColor)
                        a.set_ylabel("Price")
                        if exchange != "Huobi":
                            a2.fill_between(volumeData["MPLDates"], 0, volumeData['volume'], facecolor=darkColor)
                            a2.set_ylabel("Volume")

                        a.xaxis.set_major_locator(mticker.MaxNLocator(3))
                        a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

                        if exchange != "Huobi":
                            plt.setp(a.get_xticklabels(), visible=False)

                        if topIndicator != "none":
                            plt.setp(a0.get_xticklabels(), visible=False)

                        if bottomIndicator != "none":
                            plt.setp(a2.get_xticklabels(), visible=False)  # a2 is the Volume

                        x = (len(OHLC['close'])) - 1  # get the last price

                        if dataPace == "1d":
                            title = exchange + " 1 Day Data with " + resampleSize + " Bars\nLast Price: " + str(
                                OHLC['close'][x])
                        if dataPace == "3d":
                            title = exchange + " 3 Day Data with " + resampleSize + " Bars\nLast Price: " + str(
                                OHLC['close'][x])
                        if dataPace == "7d":
                            title = exchange + " 7 Day Data with " + resampleSize + " Bars\nLast Price: " + str(
                                OHLC['close'][x])

                        if topIndicator != "none":
                            a0.set_title(title)

                        else:
                            a.set_title(title)

                        print("New Graph")
                        datCounter = 0



                    except Exception as e:
                        print('failed in the non-tick animate:', str(e))
                        datCounter = 9000

                else:
                    darCounter -= 1
