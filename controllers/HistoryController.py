import models
import numpy as np
import pandas as pd


class History(object):

    session = models.Session()

    def get_history_by_base_currency(self, currency_id):
        return self.session.query(models.History).join(models.History.base_currency).filter(models.History.base_currency_id == currency_id).all()

    def get_all(self):
        query = self.session.query(models.History).join(models.History.base_currency)
        return pd.read_sql(query.statement, self.session.bind)

    def get_by_symbol_id(self, symbol_id):
        query = self.session.query(models.History).filter(models.History.symbol_id == symbol_id)
        return pd.read_sql(query.statement, self.session.bind)

    def get_all_base_currency_from_history(self):
        base_currencies = self.session.query(models.History).group_by(models.History.base_currency_id).all()
        currency_dict = dict()
        for item in base_currencies:
            currency_dict[item.base_currency_id] = item
        return currency_dict

    def get_all_symbol_from_history(self):
        symbol_in_history = self.session.query(models.History).join(models.History.symbol).group_by(
            models.History.symbol_id).all()
        symbol_list = list()
        for item in symbol_in_history:
            symbol_list.append(item.symbol)
        return sorted(symbol_list, key=lambda symbol: symbol.symbol_global_id)

    def get_all_parameter_from_history(self):
        parameter_in_history = self.session.query(models.History).join(models.History.parameter).group_by(
            models.History.parameter_id).all()
        parameter_list = list()
        for item in parameter_in_history:
            parameter_list.append(item.parameter)
        return parameter_list

    def get_all_symbol_from_history_by_parameter(self, parameter_id):
        symbol_in_history = self.session.query(models.History).join(models.History.symbol).group_by(
            models.History.symbol_id).filter(models.History.parameter_id == parameter_id).all()
        symbol_list = list()
        for item in symbol_in_history:
            symbol_list.append(item.symbol)
        return sorted(symbol_list, key=lambda symbol: symbol.symbol_global_id)
