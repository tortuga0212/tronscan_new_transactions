import datetime as dt
import requests

account_id = "TF8JfBNesNnXzvqTZA9HU9wzMjUfnAfFZp"
url = f"https://api.trongrid.io/v1/accounts/{account_id}/transactions/trc20"

pages = 1
num = 0
itog = ""

params = {
    'limit': 10,
}

def get_info():
    global num, itog
    for _ in range(0, pages):
        r = requests.get(url, params=params, headers={"accept": "application/json"})
        params['fingerprint'] = r.json().get('meta', {}).get('fingerprint')

        for tr in r.json().get('data', []):
            num += 1
            id = tr.get('transaction_id')
            symbol = tr.get('token_info', {}).get('symbol')
            fr = tr.get('from')
            to = tr.get('to')
            v = tr.get('value', '')
            dec = -1 * int(tr.get('token_info', {}).get('decimals', '6'))
            f = float(v[:dec] + '.' + v[dec:])
            time_ = dt.datetime.fromtimestamp(float(tr.get('block_timestamp', '')) / 1000)

            print(f"{num} | {time_} | {f:>9.02f} {symbol} | {fr} > {to} | {id}")

            itog += (f"{num} | {time_} | {f:>9.02f} {symbol} | {fr} > {to} | {id}\n")

            with open(f"{account_id}.text", 'w') as file:
                file.write(itog)
def main():
    return get_info()

if __name__ == '__main__':
    main()