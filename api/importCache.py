# import from coinapi
import models
from api.coinapi_v1 import CoinAPIv1
from datetime import datetime, date, time
import dateutil.parser

#TODO: transform it to class?
def main_import():

    def get_symbol(symbol_id):
        #TODO: chagne it to findOne
        result = session.query(models.Symbol).filter(models.Symbol.symbol_global_id == symbol_id).all()
        if len(result) > 0:
            return result[0]
        return -1

    def get_symbol_id(symbol_id):
        #TODO: chagne it to findOne
        result = session.query(models.Symbol).filter(models.Symbol.symbol_global_id == symbol_id).all()
        if len(result) > 0:
            return result[0].id
        return -1


    def insert_symbol(symbol_id, mark_id=-1, base_cryptocurrency_id=-1, quote_cryptocurrency_id=-1):
        if session.query(models.Symbol).filter(models.Symbol.symbol_global_id == symbol_id).count() == 0:
            sym = models.Symbol(id)
            sym.mark_id = get_market_id_by_name(mark_id)
            sym.symbol_global_id = symbol_id
            sym.base_cryptocurrency_id = get_cryptocurrency_id(base_cryptocurrency_id)
            sym.quote_cryptocurrency_id = get_cryptocurrency_id(quote_cryptocurrency_id)
            session.add(sym)
            session.commit()
            return True


    def get_cryptocurrency_id(name_id):
        # TODO: chagne it to findOne
        result = session.query(models.Cryptocurrency).filter(models.Cryptocurrency.name_id.in_([name_id])).all()
        if len(result) > 0:
            return result[0].id
        return -1


    def insert_cryptocurrency(name, name_id):
        if session.query(models.Cryptocurrency).filter(models.Cryptocurrency.name_id == name_id).count() == 0:
            cur = models.Cryptocurrency(name)
            cur.name_id = name_id
            session.add(cur)
            session.commit()
            return True


    def get_market_id_by_name(name):
        result = session.query(models.Mark).filter(models.Mark.exchange_global_id == name).all()
        if len(result) > 0:
            return result[0].id
        return 0


    def insert_market(name, api_url, website, id=-1):
        if session.query(models.Mark).filter(models.Mark.name.in_([name])).count() == 0:
            mark = models.Mark(name)
            mark.api_url = api_url
            mark.website = website
            mark.exchange_global_id = id
            session.add(mark)
            session.commit()
            return True

    def insert_history(ohlcv, symbol, base_currency_id, quote_currency_id):
        #TODO: do this get_cryptocurrency_id only one time id use symbols
        # TODO: flush data for the first
        # now only for BITSTAMP_SPOT_BTC_USD

        ohlcv_new = models.History()
        ohlcv_new.start_time_exchange = dateutil.parser.parse(ohlcv['time_period_start'])
        ohlcv_new.last_time_exchange = dateutil.parser.parse(ohlcv['time_period_end'])
        ohlcv_new.ask_price = ohlcv['price_open']
        ohlcv_new.ask_price_last = ohlcv['price_close']
        ohlcv_new.ask_size = ohlcv['volume_traded']
        ohlcv_new.ask_price_high = ohlcv['price_high']
        ohlcv_new.ask_price_low = ohlcv['price_low']
        ohlcv_new.base_currency_id = base_currency_id
        ohlcv_new.quote_currency_id = quote_currency_id
        ohlcv_new.symbol_id = symbol
        #mark_id =
        session.add(ohlcv_new)
        session.commit()
        return True


    def insertExchange(mark_id, base_cur_id, quote_cur_id, time_exchange, rate):
        ex = models.Exchange(name)
        ex.mark_id = mark_id
        ex.base_cur_id = base_cur_id
        ex.quote_cur_id = quote_cur_id
        ex.time_exchange = time_exchange
        ex.rate = rate
        session.add(ex)
    #    session.commit()
    #    return(session.query(models.Exchange).filter(models.Exchange.name_id.in_([name_id])).all()[0].id)

    def insertTrade(time, price, size, type, base_cur_id, quote_cur_id, market_id):
        tr = models.Trade(name)
        tr.time = time
        tr.price = price
        tr.size = size
        tr.type = type  # das ist immer true, da eigentlich unnötig
        tr.base_cur_id = base_cur_id
        tr.quote_cur_id = quote_cur_id
        tr.market_id = market_id
        session.add(tr)
    #   session.commit()

    def insert_orderbook(time, price, size, type, base_cur_id, quote_cur_id, market_id):
        tr = models.Orderbook(name)
        tr.time = time
        tr.price = price
        tr.size = size
        tr.type = type
        tr.base_cur_id = base_cur_id
        tr.quote_cur_id = quote_cur_id
        tr.market_id = market_id
        session.add(tr)
    #session.commit()

    def update_exchanges(api):
        exchanges = api.metadata_list_exchanges()

        # Start of import
        print('Import Exchanges (Markets)')
        for exchange in exchanges:
            insert_market(exchange['name'], 'coinapi', exchange['website'], exchange['exchange_id'])

    def update_currencies(api):
        assets = api.metadata_list_assets()
        print('import Assets (Currencies)')
        for asset in assets:
            insert_cryptocurrency(asset['name'], asset['asset_id'])

    def update_symbols(api):
        symbols = api.metadata_list_symbols()
        print('import Symbols (Currency-Pairs/Market)')
        # TODO Batch insert
        for symbol in symbols:
            if (symbol['symbol_type'] == 'SPOT'):
                insert_symbol(symbol['symbol_id'], symbol['exchange_id'], symbol['asset_id_base'],
                              symbol['asset_id_quote'])

            if (symbol['symbol_type'] == 'FUTURES'):
                print('Future delivery time: %s' % symbol['future_delivery_time'])

            if (symbol['symbol_type'] == 'OPTION'):
                print('Option type is call: %s' % symbol['option_type_is_call'])
                print('Option strike price: %s' % symbol['option_strike_price'])
                print('Option contract unit: %s' % symbol['option_contract_unit'])
                print('Option exercise style: %s' % symbol['option_exercise_style'])
                print('Option expiration time: %s' % symbol['option_expiration_time'])

    def update_OHCL_histories(api, symbol):
        start_of_2018 = date(2018, 1, 1).isoformat()
        date_now = date.today().isoformat()
        #marketID = get_market_id_by_name('BITSTAMP')

        symbol_from_db = get_symbol(symbol)
        symbol_id = symbol_from_db.id
        base_currency_id = symbol_from_db.base_cryptocurrency_id
        quote_currency_id = symbol_from_db.quote_cryptocurrency_id
        ohlcv_historical = api.ohlcv_historical_data(symbol, {
            'period_id': '1DAY',
            'time_start': start_of_2018,
            'time_end': date_now,
            'limit': 10000
        })
        for ohlcv in ohlcv_historical:
            insert_history(ohlcv, symbol_id, base_currency_id, quote_currency_id)

    #Entrypoint
    session = models.Session()
    api_key = 'E696601D-F684-4237-A4DC-E3BF94A959D2'

    coin_api = CoinAPIv1(api_key)

    #update_exchanges(coin_api)
    #update_currencies(coin_api)
    #update_symbols(coin_api)
    update_OHCL_histories(coin_api, 'BITSTAMP_SPOT_BTC_USD')
    update_OHCL_histories(coin_api, 'BITSTAMP_SPOT_ETH_USD')
    update_OHCL_histories(coin_api, 'BITSTAMP_SPOT_LTC_USD')
    update_OHCL_histories(coin_api, 'BITSTAMP_SPOT_XRP_USD')
    update_OHCL_histories(coin_api, 'KRAKEN_SPOT_ZEC_USD')
    update_OHCL_histories(coin_api, 'KRAKEN_SPOT_BTC_USD')
    update_OHCL_histories(coin_api, 'KRAKEN_SPOT_DASH_USD')
    return True
        # latest_trades = api.trades_latest_data_all()
        #
        # for data in latest_trades:
        #     sym = GetSymbol(data['symbol_id'])
        #     insertTrade(data['time_exchange'], data['price'], data['size'], true, sym.base_cryptocurrency_id,
        #                 sym.quote_cryptocurrency_id, sym.mark_id)
        # session.commit()

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
