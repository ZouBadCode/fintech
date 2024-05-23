# finmain.py
import pandas as pd
from moving_average import MovingAverage
import yfinance as yf
def get_user_inputs():
    inputs = []
    while True:
        indicator_type = input("輸入指標類型 (SMA, EMA, WMA) 或 'DONE' 完成輸入: ").upper()
        if indicator_type == 'DONE':
            break
        average_days = int(input(f"輸入 {indicator_type} 的天數: "))
        inputs.append((indicator_type, average_days))
    return inputs

def main():
    # 讀取數據
    ticker = 'AAPL'
    stock_data = yf.download(ticker, start='2021-01-01', end='2021-12-31')
    stock_data = stock_data[['Close']].reset_index()
    stock_data.rename(columns={'Date': 'date', 'Close': 'value'}, inplace=True)
    # 初始化MovingAverage類
    ma = MovingAverage(stock_data)

    # 獲取用戶輸入的指標類型和天數
    user_inputs = get_user_inputs()

    # 存儲計算結果的DataFrame
    results = ma.data[['value']].copy()

    # 根據用戶輸入計算不同的移動平均值
    for indicator_type, average_days in user_inputs:
        if indicator_type == 'SMA':
            result = ma.calculate_sma(average_days)
        elif indicator_type == 'EMA':
            result = ma.calculate_ema(average_days)
        elif indicator_type == 'WMA':
            result = ma.calculate_wma(average_days)
        else:
            print(f"未知的指標類型: {indicator_type}")
            continue
        results = pd.concat([results, result], axis=1)

    # 輸出結果
    print(results)

    # 將結果保存到CSV文件
    results.to_csv('result.csv')
    
if __name__ == "__main__":
    main()
