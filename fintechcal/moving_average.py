import pandas as pd
import numpy as np

class MovingAverage:
    def __init__(self, data):
        """
        初始化MovingAverage類
        :param data: 包含日期和數值的資料，格式為pandas DataFrame，應包含 'date' 和 'value' 列
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame")
        if 'date' not in data.columns or 'value' not in data.columns:
            raise ValueError("Data must contain 'date' and 'value' columns")
        self.data = data
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data.set_index('date', inplace=True)

    def calculate_sma(self, average_days):
        """
        計算簡單移動平均值（SMA）
        :param average_days: 平均天數
        :return: 包含SMA值的DataFrame
        """
        ma_column_name = f'MA_{average_days}'
        self.data[ma_column_name] = self.data['value'].rolling(window=average_days).mean()
        return self.data[[ma_column_name]]

    def calculate_ema(self, span):
        """
        計算指數移動平均值（EMA）
        :param span: EMA的時間跨度
        :return: 包含EMA值的DataFrame
        """
        ema_column_name = f'EMA_{span}'
        self.data[ema_column_name] = self.data['value'].ewm(span=span, adjust=False).mean()
        return self.data[[ema_column_name]]

    def calculate_wma(self, average_days):
        """
        計算加權移動平均值（WMA）
        :param average_days: 平均天數
        :return: 包含WMA值的DataFrame
        """
        weights = list(range(1, average_days + 1))
        wma_column_name = f'WMA_{average_days}'
        self.data[wma_column_name] = self.data['value'].rolling(window=average_days).apply(lambda prices: np.dot(prices, weights) / sum(weights), raw=True)
        return self.data[[wma_column_name]]
