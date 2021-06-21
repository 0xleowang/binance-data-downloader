import csv
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from binance.client import Client
from binance.enums import HistoricalKlinesType
from tqdm import tqdm
from utils import read_symbols, create_path

INTERVALS = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w']
START_TIME = 1569852000000  # 2019-10-01-00:00:00


def get_parser():
    parser = ArgumentParser(description="This is a script to download historical klines data", formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', dest='interval', default='5m', help='KLINE interval')
    return parser


def download_kline(symbol, klines_type, interval):
    """Download spot/futures klines for selected symbol, and save the data into csv files.

    Args:
        symbol (str): e.g., 'BTCUSDT'
        klines_type (str): 'spot' or 'futures'
        interval ([type]): e.g., '5m' for 5 minutes interval
    """
    if klines_type == 'spot':
        klines_enum = HistoricalKlinesType.SPOT
    elif klines_type == 'futures':
        klines_enum = HistoricalKlinesType.FUTURES
    try:
        klines = client.get_historical_klines(
            symbol=symbol,
            klines_type=klines_enum,
            interval=interval,
            start_str=START_TIME,
            limit=1000
        )
    except Exception:
        print(f'No {klines_type} data for {symbol}')
        return
    # write into csv
    with open(f'./data/{klines_type}/{interval}/{symbol}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['Open time',
             'Open',
             'High',
             'Low',
             'Close',
             'Volume',
             'Close time',
             'Quote asset volume',
             'Number of trades',
             'Taker buy base asset volume',
             'Taker buy quote asset volume',
             'Ignore']
        )
        writer.writerows(klines)


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])

    if args.interval not in INTERVALS:
        raise NameError('Invalid interval')

    client = Client()
    symbols = read_symbols()

    for symbol in tqdm(symbols):
        create_path('spot', args.interval)
        klines = download_kline(symbol, 'spot', args.interval)
        create_path('futures', args.interval)
        klines = download_kline(symbol, 'futures', args.interval)
