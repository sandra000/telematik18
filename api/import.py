#import from coinapi
import models
from api.coinapi_v1 import CoinAPIv1


def getSymbol(SymbolID, mark_id=-1,base_cryptocurrency_id=-1, quote_cryptocurrency_id=-1):
    #result=session.query(models.Cryptocurrency).filter(models.Cryptocurrency.id.in_([id])).all()
    if (0>1):#(session.query(models.Cryptocurrency).filter(models.Cryptocurrency.id.in_([id])).count()>0):#todo: das hier muss überarbeitet werden; wie geht AND?
        #return(result[0])
        print('Fehler')
    else:
        #if (int(mark_id)>-1):
        sym=models.Symbol(id)
        sym.mark_id=mark_id
        sym.base_cryptocurrency_id=getCryptocurrencyID("",base_cryptocurrency_id)
        sym.quote_cryptocurrenc_id=getCryptocurrencyID('',quote_cryptocurrency_id)
        session.add(sym)
        session.commit()
        return (session.query(models.Cryptocurrency).filter(models.Cryptocurrency.id.in_([id])).all()[0])

def getCryptocurrencyID(name, name_id):
    result=session.query(models.Cryptocurrency).filter(models.Cryptocurrency.name_id.in_([name_id])).all()
    if(session.query(models.Cryptocurrency).filter(models.Cryptocurrency.name_id.like(name_id)).count()>0):
        return(result[0].id)
    else:
        cur=models.Cryptocurrency(name)
        cur.name_id=name_id
        #if(int(id)>-1):
        #cur.id=id
        session.add(cur)
        session.commit()
        return(session.query(models.Cryptocurrency).filter(models.Cryptocurrency.name_id.in_([name_id])).all()[0].id)
    
def getMarketID(name, api_url, website,id=-1):
    result=session.query(models.Mark).filter(models.Mark.name.in_([name])).all()
    if(session.query(models.Mark).filter(models.Mark.name.in_([name])).count()>0):
        return(result[0].id)
    else:
        mark=models.Mark
        #if (float(id)>-1):
        mark.id=id
        mark=models.Mark(name)
        mark.api_url=api_url
        mark.website=website
        session.add(mark)
        session.commit()
        return(session.query(models.Mark).filter(models.Mark.name.in_([name])).all()[0].id)

def insertExchange(mark_id, base_cur_id, quote_cur_id, time_exchange, rate):
    ex=models.Exchange(name)
    ex.mark_id=mark_id
    ex.base_cur_id=base_cur_id
    ex.quote_cur_id=quote_cur_id
    ex.time_exchange=time_exchange
    ex.rate=rate
    session.add(ex)
#    session.commit()
#    return(session.query(models.Exchange).filter(models.Exchange.name_id.in_([name_id])).all()[0].id)

def insertTrade(time, price, size, type, base_cur_id, quote_cur_id, market_id):
    tr=models.Trade(name)
    tr.time=time
    tr.price=price
    tr.size=size
    tr.type=type# das ist immer true, da eigentlich unnötig
    tr.base_cur_id=base_cur_id
    tr.quote_cur_id=quote_cur_id
    tr.market_id=market_id
    session.add(tr)
#    session.commit()

def insertTrade(time, price, size, type, base_cur_id, quote_cur_id, market_id):
    tr=models.Orderbook(name)
    tr.time=time
    tr.price=price
    tr.size=size
    tr.type=type
    tr.base_cur_id=base_cur_id
    tr.quote_cur_id=quote_cur_id
    tr.market_id=market_id
    session.add(tr)
#    session.commit()

session=models.Session()
#basecurID=getCryptocurrencyID('Bitcoin', 'BTC')
#quotecurID=getCryptocurrencyID('Euro', 'EUR')

api_key = 'E696601D-F684-4237-A4DC-E3BF94A959D2'

api = CoinAPIv1(api_key)
exchanges = api.metadata_list_exchanges()

importBaseData=1
    
if (importBaseData>0):
    print('Import Exchanges (Markets)')
    for exchange in exchanges:
        getMarketID(exchange['name'], 'coinapi', exchange['website'], exchange['exchange_id'])
        
#        print('Exchange ID: %s' % exchange['exchange_id'])
#        print('Exchange website: %s' % exchange['website'])
#        print('Exchange name: %s' % exchange['name'])

    assets = api.metadata_list_assets()
    print('import Assets (Currencys)')
    for asset in assets:
        getCryptocurrencyID(asset['name'],asset['asset_id'])
    #    print('Asset ID: %s' % asset['asset_id'])
    #    print('Asset name: %s' % asset['name'])
    #    print('Asset type (crypto?): %s' % asset['type_is_crypto'])

    symbols = api.metadata_list_symbols()
    print('import Symbols (Currency-Pairs/Market)')
    for symbol in symbols:
        getSymbol(symbol['symbol_id'],symbol['exchange_id'],symbol['asset_id_base'],symbol['asset_id_quote'])
    
#    print('Symbol ID: %s' % symbol['symbol_id'])
#    print('Exchange ID: %s' % symbol['exchange_id'])
#    print('Symbol type: %s' % symbol['symbol_type'])
#    print('Asset ID base: %s' % symbol['asset_id_base'])
#    print('Asset ID quote: %s' % symbol['asset_id_quote'])
#
#    if (symbol['symbol_type'] == 'FUTURES'):
#        print('Future delivery time: %s' % symbol['future_delivery_time'])
#
#    if (symbol['symbol_type'] == 'OPTION'):
#        print('Option type is call: %s' % symbol['option_type_is_call'])
#        print('Option strike price: %s' % symbol['option_strike_price'])
#        print('Option contract unit: %s' % symbol['option_contract_unit'])
#        print('Option exercise style: %s' % symbol['option_exercise_style'])
#        print('Option expiration time: %s' % symbol['option_expiration_time'])
#
#Problem: nicht vom Marktplatz abhängig, damit unbrauchbar
#exchange_rate = api.exchange_rates_get_specific_rate('BTC', 'USD')
#print('Time: %s' % exchange_rate['time'])
#print('Base: %s' % exchange_rate['asset_id_base'])
#print('Quote: %s' % exchange_rate['asset_id_quote'])
#print('Rate: %s' % exchange_rate['rate'])
#last_week = datetime.date(2018, 5, 20).isoformat()
#
#Problem: s.o.
#exchange_rate_last_week = api.exchange_rates_get_specific_rate('BTC', 'USD', {'time': last_week})
#print('Time: %s' % exchange_rate_last_week['time'])
#print('Base: %s' % exchange_rate_last_week['asset_id_base'])
#print('Quote: %s' % exchange_rate_last_week['asset_id_quote'])
#print('Rate: %s' % exchange_rate_last_week['rate'])
#
#problem: s.o.
#current_rates = api.exchange_rates_get_all_current_rates('BTC')
#
#print("Asset ID Base: %s" % current_rates['asset_id_base'])
#for rate in current_rates['rates']:
#    print('Time: %s' % rate['time'])
#    print('Quote: %s' % rate['asset_id_quote'])
#    print('Rate: %s' % rate['rate'])
#
#periods = api.ohlcv_list_all_periods()
#
#for period in periods:
#    print('ID: %s' % period['period_id'])
#    print('Seconds: %s' % period['length_seconds'])
#    print('Months: %s' % period['length_months'])
#    print('Unit count: %s' % period['unit_count'])
#    print('Unit name: %s' % period['unit_name'])
#    print('Display name: %s' % period['display_name'])
#
#ohlcv_latest = api.ohlcv_latest_data('BITSTAMP_SPOT_BTC_USD', {'period_id': '1MIN'})
#
#for period in ohlcv_latest:
#    print('Period start: %s' % period['time_period_start'])
#    print('Period end: %s' % period['time_period_end'])
#    print('Time open: %s' % period['time_open'])
#    print('Time close: %s' % period['time_close'])
#    print('Price open: %s' % period['price_open'])
#    print('Price close: %s' % period['price_close'])
#    print('Price low: %s' % period['price_low'])
#    print('Price high: %s' % period['price_high'])
#    print('Volume traded: %s' % period['volume_traded'])
#    print('Trades count: %s' % period['trades_count'])
#
#start_of_2016 = datetime.date(2016, 1, 1).isoformat()
    marketID=getMarketID('BITSTAMP')
    print('TODO: einfügen')
    #ohlcv_historical = api.ohlcv_historical_data('BITSTAMP_SPOT_BTC_USD', {'period_id': '1MIN', 'time_start': start_of_2016})
#
#for period in ohlcv_historical:
#    print('Period start: %s' % period['time_period_start'])
#    print('Period end: %s' % period['time_period_end'])
#    print('Time open: %s' % period['time_open'])
#    print('Time close: %s' % period['time_close'])
#    print('Price open: %s' % period['price_open'])
#    print('Price close: %s' % period['price_close'])
#    print('Price low: %s' % period['price_low'])
#    print('Price high: %s' % period['price_high'])
#    print('Volume traded: %s' % period['volume_traded'])
#    print('Trades count: %s' % period['trades_count'])
#

    latest_trades = api.trades_latest_data_all()

    for data in latest_trades:
        sym=GetSymbol(data['symbol_id'])
        insertTrade(data['time_exchange'], data['price'], data['size'], true, sym.base_cryptocurrency_id, sym.quote_cryptocurrency_id, sym.mark_id)
    session.commit()
##        print('Symbol ID: %s' % data['symbol_id'])
##        print('Time Exchange: %s' % data['time_exchange'])
##        print('Time CoinAPI: %s' % data['time_coinapi'])
##        print('UUID: %s' % data['uuid'])
##        print('Price: %s' % data['price'])
##        print('Size: %s' % data['size'])
##        print('Taker Side: %s' % data['taker_side'])
##
##latest_trades_doge = api.trades_latest_data_symbol('BITTREX_SPOT_BTC_DOGE')
##
##for data in latest_trades_doge:
##    print('Symbol ID: %s' % data['symbol_id'])
##    print('Time Exchange: %s' % data['time_exchange'])
##    print('Time CoinAPI: %s' % data['time_coinapi'])
##    print('UUID: %s' % data['uuid'])
##    print('Price: %s' % data['price'])
##    print('Size: %s' % data['size'])
##    print('Taker Side: %s' % data['taker_side'])
##
##historical_trades_btc = api.trades_historical_data('BITSTAMP_SPOT_BTC_USD', {'time_start': start_of_2016})
##
##for data in historical_trades_btc:
##    print('Symbol ID: %s' % data['symbol_id'])
##    print('Time Exchange: %s' % data['time_exchange'])
##    print('Time CoinAPI: %s' % data['time_coinapi'])
##    print('UUID: %s' % data['uuid'])
##    print('Price: %s' % data['price'])
##    print('Size: %s' % data['size'])
##    print('Taker Side: %s' % data['taker_side'])
##
##current_quotes = api.quotes_current_data_all()
##print(current_quotes)
##for quote in current_quotes:
##    print('Symbol ID: %s' % quote['symbol_id'])
##    print('Time Exchange: %s' % quote['time_exchange'])
##    print('Time CoinAPI: %s' % quote['time_coinapi'])
##    print('Ask Price: %s' % quote['ask_price'])
##    print('Ask Size: %s' % quote['ask_size'])
##    print('Bid Price: %s' % quote['bid_price'])
##    print('Bid Size: %s' % quote['bid_size'])
##    if 'last_trade' in quote:
##        print('Last Trade: %s' % quote['last_trade'])
##
##current_quote_btc_usd = api.quotes_current_data_symbol('BITSTAMP_SPOT_BTC_USD')
##
##print('Symbol ID: %s' % current_quote_btc_usd['symbol_id'])
##print('Time Exchange: %s' % current_quote_btc_usd['time_exchange'])
##print('Time CoinAPI: %s' % current_quote_btc_usd['time_coinapi'])
##print('Ask Price: %s' % current_quote_btc_usd['ask_price'])
##print('Ask Size: %s' % current_quote_btc_usd['ask_size'])
##print('Bid Price: %s' % current_quote_btc_usd['bid_price'])
##print('Bid Size: %s' % current_quote_btc_usd['bid_size'])
##if 'last_trade' in current_quote_btc_usd:
##    last_trade = current_quote_btc_usd['last_trade']
##    print('Last Trade:')
##    print('- Taker Side: %s' % last_trade['taker_side'])
##    print('- UUID: %s' % last_trade['uuid'])
##    print('- Time Exchange: %s' % last_trade['time_exchange'])
##    print('- Price: %s' % last_trade['price'])
##    print('- Size: %s' % last_trade['size'])
##    print('- Time CoinAPI: %s' % last_trade['time_coinapi'])
##
##quotes_latest_data = api.quotes_latest_data_all()
##
##for quote in quotes_latest_data:
##    print('Symbol ID: %s' % quote['symbol_id'])
##    print('Time Exchange: %s' % quote['time_exchange'])
##    print('Time CoinAPI: %s' % quote['time_coinapi'])
##    print('Ask Price: %s' % quote['ask_price'])
##    print('Ask Size: %s' % quote['ask_size'])
##    print('Bid Price: %s' % quote['bid_price'])
##    print('Bid Size: %s' % quote['bid_size'])
##
##quotes_latest_data_btc_usd = api.quotes_latest_data_symbol('BITSTAMP_SPOT_BTC_USD')
##
##for quote in quotes_latest_data_btc_usd:
##    print('Symbol ID: %s' % quote['symbol_id'])
##    print('Time Exchange: %s' % quote['time_exchange'])
##    print('Time CoinAPI: %s' % quote['time_coinapi'])
##    print('Ask Price: %s' % quote['ask_price'])
##    print('Ask Size: %s' % quote['ask_size'])
##    print('Bid Price: %s' % quote['bid_price'])
##    print('Bid Size: %s' % quote['bid_size'])
##
##quotes_historical_data_btc_usd = api.quotes_historical_data('BITSTAMP_SPOT_BTC_USD', {'time_start': start_of_2016})
##
##for quote in quotes_historical_data_btc_usd:
##    print('Symbol ID: %s' % quote['symbol_id'])
##    print('Time Exchange: %s' % quote['time_exchange'])
##    print('Time CoinAPI: %s' % quote['time_coinapi'])
##    print('Ask Price: %s' % quote['ask_price'])
##    print('Ask Size: %s' % quote['ask_size'])
##    print('Bid Price: %s' % quote['bid_price'])
##    print('Bid Size: %s' % quote['bid_size'])
##
##orderbooks_current_data = api.orderbooks_current_data_all()
##
##for data in orderbooks_current_data:
##    print('Symbol ID: %s' % data['symbol_id'])
##    print('Time Exchange: %s' % data['time_exchange'])
##    print('Time CoinAPI: %s' % data['time_coinapi'])
##    print('Asks:')
##    for ask in data['asks']:
##        print('- Price: %s' % ask['price'])
##        print('- Size: %s' % ask['size'])
##    print('Bids:')
##    for bid in data['bids']:
##        print('- Price: %s' % bid['price'])
##        print('- Size: %s' % bid['size'])
##
##orderbooks_current_data_btc_usd = api.orderbooks_current_data_symbol('BITSTAMP_SPOT_BTC_USD')
##
##print('Symbol ID: %s' % orderbooks_current_data_btc_usd['symbol_id'])
##print('Time Exchange: %s' % orderbooks_current_data_btc_usd['time_exchange'])
##print('Time CoinAPI: %s' % orderbooks_current_data_btc_usd['time_coinapi'])
##print('Asks:')
##for ask in orderbooks_current_data_btc_usd['asks']:
##    print('- Price: %s' % ask['price'])
##    print('- Size: %s' % ask['size'])
##print('Bids:')
##for bid in orderbooks_current_data_btc_usd['bids']:
##    print('- Price: %s' % bid['price'])
##    print('- Size: %s' % bid['size'])
##
##orderbooks_latest_data_btc_usd = api.orderbooks_latest_data('BITSTAMP_SPOT_BTC_USD')
##
##for data in orderbooks_latest_data_btc_usd:
##    print('Symbol ID: %s' % data['symbol_id'])
##    print('Time Exchange: %s' % data['time_exchange'])
##    print('Time CoinAPI: %s' % data['time_coinapi'])
##    print('Asks:')
##    for ask in data['asks']:
##        print('- Price: %s' % ask['price'])
##        print('- Size: %s' % ask['size'])
##    print('Bids:')
##    for bid in data['bids']:
##        print('- Price: %s' % bid['price'])
##        print('- Size: %s' % bid['size'])
##
##orderbooks_historical_data_btc_usd = api.orderbooks_historical_data('BITSTAMP_SPOT_BTC_USD', {'time_start': start_of_2016})
##
##for data in orderbooks_historical_data_btc_usd:
##    print('Symbol ID: %s' % data['symbol_id'])
##    print('Time Exchange: %s' % data['time_exchange'])
##    print('Time CoinAPI: %s' % data['time_coinapi'])
##    print('Asks:')
##    for ask in data['asks']:
##        print('- Price: %s' % ask['price'])
##        print('- Size: %s' % ask['size'])
##    print('Bids:')
##    for bid in data['bids']:
##        print('- Price: %s' % bid['price'])
##        print('- Size: %s' % bid['size'])
##
##twitter_latest_data = api.twitter_latest_data()
##twitter_historical_data = api.twitter_historical_data({'time_start': start_of_2016})


