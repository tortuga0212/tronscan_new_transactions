import telebot
import requests
import datetime as dt

token = '6530355325:AAHOAPiY7cWjJqBH7F4X5c5EVFKXqLIrDKQ'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    mesg = bot.send_message(message.chat.id, 'Привет! Введите кошелек, который хотите отследить')
    bot.register_next_step_handler(mesg, save_text)

def save_text(message):
    message_to_save = message.text
    account_id = message_to_save
    url = f"https://api.trongrid.io/v1/accounts/{account_id}/transactions/trc20"
    params = {
        'limit': 10,
    }
    pages = 1
    num = 0
    itog = ""
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

            itog += (f"{num} | {time_} | {f:>9.02f} {symbol} | {fr} > {to} | {id}\n")

            with open(f"{account_id}.text", 'w') as file:
                file.write(itog)

            bot.send_message(message.chat.id, f"Time transaction: {time_}\n"
                                              f"Amount and token: {f:>9.02f} {symbol}\n"
                                              f"From: {fr}\n"
                                              f"To: {to}\n"
                                              f"Hash: {id}")

if __name__ == '__main__':
    bot.infinity_polling()