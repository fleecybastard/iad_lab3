import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error


CSV_FILE_NAME = 'ARBUSDT_KLINES.csv'


def main(ema_size=100, alpha=0.1):
    df = pd.read_csv(CSV_FILE_NAME)
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    ema_column_name = "ema_" + str(ema_size)

    initial_mean = df['close_price'].head(ema_size).mean()
    for i in range(len(df)):
        if i == ema_size:
            df.loc[i, ema_column_name] = initial_mean
        elif i > ema_size:
            ema_value = df.loc[i, 'close_price'] * alpha + df.loc[i - 1, ema_column_name] * (1 - alpha)
            df.loc[i, ema_column_name] = ema_value
        else:
            df.loc[i, ema_column_name] = 0
    previous_close_price = df['close_price'][ema_size - 1]
    df.drop(index=df.index[:ema_size], axis=0, inplace=True)
    rmse = mean_squared_error(df['close_price'], df[ema_column_name])
    mape = mean_absolute_percentage_error(df['close_price'], df[ema_column_name])
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for index, row in df.iterrows():
        current_close_price = row['close_price']
        ema_close_price = row[ema_column_name]
        trend = 'UP' if current_close_price - previous_close_price > 0 else 'DOWN'
        ema_trend = 'UP' if ema_close_price - previous_close_price > 0 else 'DOWN'
        if trend == 'UP' and ema_trend == 'UP':
            tp += 1
        elif trend == 'DOWN' and ema_trend == 'DOWN':
            tn += 1
        elif trend == 'DOWN' and ema_trend == 'UP':
            fp += 1
        elif trend == 'UP' and ema_trend == 'DOWN':
            fn += 1
        previous_close_price = current_close_price
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    misc = 1 - accuracy
    print(f'RMSE: {rmse:.10f}')
    print(f'MAPE: {mape:.10f}')
    print(f'TP: {tp}')
    print(f'TN: {tn}')
    print(f'FP: {fp}')
    print(f'FN: {fn}')
    print(f'MISC: {misc}')
    plt.plot(df['close_time'], df['close_price'])
    plt.gcf().autofmt_xdate()
    plt.plot(df['close_time'], df[ema_column_name], color='red')
    plt.show()


if __name__ == '__main__':
    main(41, 0.94)
