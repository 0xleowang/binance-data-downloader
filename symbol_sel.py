from binance.client import Client
from utils import save_symbols

client = Client()
info = client.futures_exchange_info()
symbols_info = info['symbols']
symbols = [
    s['symbol'] for s in symbols_info if
    s['status'] == 'TRADING' and
    s['contractType'] == 'PERPETUAL' and
    s['symbol'].endswith('USDT')
]
save_symbols(symbols)
print(f'{len(symbols)} symbols have ben selected and saved to symbols.txt')