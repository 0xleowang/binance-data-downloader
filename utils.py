def save_symbols(symbols):
    with open('symbols.txt', 'w') as f:
        f.write('\n'.join(symbols))


def read_symbols():
    with open('symbols.txt', 'r') as f:
        raw_text = f.read()
    return raw_text.split('\n')
