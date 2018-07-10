# import from coinapi
import models
from api.coinapi_v1 import CoinAPIv1
from datetime import datetime, date, time
import dateutil.parser
from sqlalchemy import func


class MainImport(object):

    session = models.Session()

    api_key = 'E696601D-F684-4237-A4DC-E3BF94A959D2'

    api = CoinAPIv1(api_key)

    def get_symbol(self, symbol_id):
        result = self.session.query(models.Symbol).filter(models.Symbol.symbol_global_id == symbol_id).first()
        if result:
            return result
        return -1

    def get_symbol_id(self, symbol_id): 
        result = self.session.query(models.Symbol).filter(models.Symbol.symbol_global_id == symbol_id).first()
        if result:
            return result.id
        return -1

    def insert_symbol(self, symbol_id, mark_id=-1, base_cryptocurrency_id=-1, quote_cryptocurrency_id=-1):
        if self.session.query(models.Symbol).filter(models.Symbol.symbol_global_id == symbol_id).count() == 0:
            sym = models.Symbol(id)
            sym.mark_id = self.get_market_id_by_name(mark_id)
            sym.symbol_global_id = symbol_id
            sym.base_cryptocurrency_id = self.get_cryptocurrency_id(base_cryptocurrency_id)
            sym.quote_cryptocurrency_id = self.get_cryptocurrency_id(quote_cryptocurrency_id)
            self.session.add(sym)
            #self.session.commit() # wird erst am Ende committed
            return True

    def get_cryptocurrency_id(self, name_id):
        # TODO: chagne it to findOne
        result = self.session.query(models.Cryptocurrency).filter(models.Cryptocurrency.name_id.in_([name_id])).first()
        if result:
            return result.id
        return -1

    def insert_cryptocurrency(self, name, name_id):
        if self.session.query(models.Cryptocurrency).filter(models.Cryptocurrency.name_id == name_id).count() == 0:
            cur = models.Cryptocurrency(name)
            cur.name_id = name_id
            self.session.add(cur)
            self.session.commit()
            return True
    def get_parameter(self, period_id,time_start,time_end,limit):
        result = self.session.query(models.Parameter).filter(models.Parameter.period_id == period_id).filter(models.Parameter.time_start==time_start).filter(models.Parameter.time_end==time_end).filter(models.Parameter.limit==limit).first()
        if result:
            return result
        return -1

    def insert_paramter(self, period_id,time_start,time_end,limit):
        cur = models.Parameter()
        cur.period_id = period_id
        cur.time_start=time_start
        cur.time_end=time_end
        cur.limit=limit
        self.session.add(cur)
        self.session.commit()
        #return self.session.query(func.max(models.Parameter.id)).scalar()
        result = self.session.query(models.Parameter).filter(models.Parameter.period_id == period_id).filter(models.Parameter.time_start==time_start).filter(models.Parameter.time_end==time_end).filter(models.Parameter.limit==limit).first()
        if result:
            return result
        return -1

    def get_market_id_by_name(self, name):
        result = self.session.query(models.Mark).filter(models.Mark.exchange_global_id == name).first()
        if result:
            return result.id
        return 0

    def insert_market(self, name, api_url, website, id=-1):
        if self.session.query(models.Mark).filter(models.Mark.name.in_([name])).count() == 0:
            mark = models.Mark(name)
            mark.api_url = api_url
            mark.website = website
            mark.exchange_global_id = id
            self.session.add(mark)
            self.session.commit()
            return True

    def insert_history(self, ohlcv, symbol, base_currency_id, quote_currency_id,parameter):
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
        ohlcv_new.parameter_id=parameter.id
        #print('P:')
        #print(parameter)
        #mark_id =
        self.session.add(ohlcv_new)
        self.session.commit()
        return True

    
    def update_exchanges(self):
        exchanges = self.api.metadata_list_exchanges()

        # Start of import
        print('Import Exchanges (Markets)')
        for exchange in exchanges:
            self.insert_market(exchange['name'], 'coinapi', exchange['website'], exchange['exchange_id'])

    def update_currencies(self):
        assets = self.api.metadata_list_assets()
        print('import Assets (Currencies)')
        for asset in assets:
            self.insert_cryptocurrency(asset['name'], asset['asset_id'])

    def update_symbols(self):
        symbols = self.api.metadata_list_symbols()
        print('import Symbols (Currency-Pairs/Market)')
        # TODO Batch insert
        for symbol in symbols:
            if (symbol['symbol_type'] == 'SPOT'):
                self.insert_symbol(symbol['symbol_id'], symbol['exchange_id'], symbol['asset_id_base'],
                              symbol['asset_id_quote'])

#            if (symbol['symbol_type'] == 'FUTURES'):
#                print('Future delivery time: %s' % symbol['future_delivery_time'])
#
#            if (symbol['symbol_type'] == 'OPTION'):
#                print('Option type is call: %s' % symbol['option_type_is_call'])
#                print('Option strike price: %s' % symbol['option_strike_price'])
#                print('Option contract unit: %s' % symbol['option_contract_unit'])
#                print('Option exercise style: %s' % symbol['option_exercise_style'])
#                print('Option expiration time: %s' % symbol['option_expiration_time'])
        self.session.commit() #schreibt die Aenderungen in die Datenbank

    def update_ohcl_histories(self, symbol, period='1DAY',start_time=date(2018, 1, 1).isoformat(),end_time=date.today().isoformat(),limit=10000):
        #start_of_2018 = date(2018, 1, 1).isoformat()
        #date_now = date.today().isoformat()
        #marketID = get_market_id_by_name('BITSTAMP')
        
        symbol_from_db = self.get_symbol(symbol)
        symbol_id = symbol_from_db.id
        parameter=self.get_parameter(period,start_time,end_time,limit)
        if (parameter==-1):
            parameter=self.insert_paramter(period,start_time,end_time,limit)
        else:
            self.session.execute('DELETE FROM histories WHERE symbol_id='+str(symbol_id)+' AND parameter_id='+str(parameter.id))
            self.session.commit()
            
        base_currency_id = symbol_from_db.base_cryptocurrency_id
        quote_currency_id = symbol_from_db.quote_cryptocurrency_id
        ohlcv_historical = self.api.ohlcv_historical_data(symbol, {
            'period_id': period,
            'time_start': start_time, #start_of_2018,
            'time_end': end_time,
            'limit': limit
        })
        for ohlcv in ohlcv_historical:
            self.insert_history(ohlcv, symbol_id, base_currency_id, quote_currency_id,parameter)

    def update_all_ohcl_histories(self):
        self.update_ohcl_histories('BITSTAMP_SPOT_BTC_USD')
        self.update_ohcl_histories('BITSTAMP_SPOT_ETH_USD')
        self.update_ohcl_histories('BITSTAMP_SPOT_LTC_USD')
        self.update_ohcl_histories('BITSTAMP_SPOT_XRP_USD')
        self.update_ohcl_histories('KRAKEN_SPOT_ZEC_USD')
        self.update_ohcl_histories('KRAKEN_SPOT_BTC_USD')
        self.update_ohcl_histories('KRAKEN_SPOT_DASH_USD') 