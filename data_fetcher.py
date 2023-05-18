from binance import Client
from config import API_KEY, API_SECRET, KLINES_DATA
import pandas as pd


class DataFetcher:
    def __init__(self) -> None:
        self.__client = Client(API_KEY, API_SECRET)

    def fetch(self, symbol: str, start_time: str, file_name: str, interval: str, limit: int) -> None:
        limit = self.__correct_limit(limit)
        print(limit)
        klines = self.__client.get_klines(symbol=symbol,
                                          interval=interval,
                                          limit=limit,
                                          startTime=start_time,
                                          )

        self.__dump_to_csv(file_name, klines)

    def __dump_to_csv(self, file_name: str, data: list) -> None:
        df = pd.DataFrame(data, columns=KLINES_DATA)
        df.drop(df.columns[[-1, -2, -3]], axis=1, inplace=True)
        df.to_csv(file_name, index=False)

    def __correct_limit(self, limit: int) -> int:
        if limit < 0 or limit > 1500:
            return 1000
        return limit


if __name__ == '__main__':
    banan = DataFetcher()
    banan.fetch('ARBUSDT', '1681332600000', 'ARBUSDT_KLINES.csv', '1m', 1000)