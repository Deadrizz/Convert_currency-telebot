import telebot
import requests
from telebot import types
import time
import os
from dotenv import load_dotenv
import json
history_currency = "data_users_currency.json"
data_users_currency = []
if os.path.exists(history_currency):
    with open(history_currency,"r") as f:
        try:
            data_users_currency = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            data_users_currency = []
load_dotenv(".env")
TBOT_API_TOKEN = os.getenv("TBOT_API_TOKEN")
bot = telebot.TeleBot(TBOT_API_TOKEN)
user_data = {}
currency_codes = {
    "USD": 840,
    "EUR": 978,
    "UAH": 980,
    "GBP": 826
}
class Rate_buy_rate_sell:
    def __init__(self):
        # self.currency_code_a = currency_code_a
        # self.currency_code_b = currency_code_b
        self.url = f"https://api.monobank.ua/bank/currency"
        self.cache_data = []
        self.last_update = 0
        self.update_interval = 120
        self.data = self.get_data()
    def get_data(self):
        if time.time() - self.last_update > self.update_interval or not self.cache_data:
            try:
                response = requests.get("https://api.monobank.ua/bank/currency")
                if response.status_code == 200:
                    self.cache_data = response.json()
                    self.last_update = time.time()
            except Exception as e:
                print(f"Error while requesting data {e}")

        return  self.cache_data

    def get_rate(self,currency_code_a,currency_code_b):
        rates = self.get_data()
        if not rates:
            return None,None
        for rate in rates:
            if rate["currencyCodeA"] == currency_code_a and rate["currencyCodeB"] == currency_code_b:
                rate_buy = rate.get("rateBuy") or rate.get("rateCross")
                rate_sell = rate.get("rateSell") or rate.get("rateCross")
                return rate_buy, rate_sell
        return None,None
rate_cache = Rate_buy_rate_sell()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name} {message.from_user.last_name}."
                                     f"This bot is designed for currency conversion. If you need more detailed information, enter:/help")
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id,
                     f"The user can enter an amount and select the source and target currencies for conversion."
                     f"\nThe source currency is set using context (e.g., 980 UAH). "
                     f"\nThe target currency is selected by pressing buttons.")
@bot.message_handler(commands=["history"])
def history_command(message):
    user_id = message.from_user.id
    user_history = [empty for empty in data_users_currency if empty["user_id"] == user_id]
    if not user_history:
        bot.send_message(message.chat.id,"Conversion history is empty")
        return
    response = "Your last 10 conversions\n"
    for empty in user_history[-10:]:
        response += f"{round(empty['amount'],2)} {empty['currency_from']} → {round(empty['result'],2)} {empty['currency_to']}\n"
    bot.send_message(message.chat.id,response)
@bot.message_handler(content_types=['text'])
def text_message(message):
    global amount
    try:
        amount = int(message.text)
        if amount != 0:
            user_data[message.from_user.id] = {"amount":amount}
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("USD")
            btn2 = types.KeyboardButton("UAH")
            markup.row(btn1, btn2)
            btn3 = types.KeyboardButton("EUR")
            btn4 = types.KeyboardButton("GBP")
            markup.row(btn3, btn4)
            bot.send_message(message.chat.id,"Choose the input currency for conversion",reply_markup=markup)
            bot.register_next_step_handler(message, click_on)
        else:
            bot.send_message(message.chat.id,"Please enter a number greater than 0")
    except:
        bot.send_message(message.chat.id,"Please enter a number, for example: 1000")
def click_on(message):
    user_data[message.from_user.id]["currency_from"] = message.text
    currency = user_data[message.from_user.id]["currency_from"]
    if currency == "USD" or currency == "EUR" or currency == "UAH" or currency == "GBP":
        bot.send_message(message.chat.id,f"Your input amount for conversion:{user_data[message.chat.id]['amount']} {currency}\n"
                                         f"To which currency would you like to convert your input amount")
    else:
        bot.send_message(message.chat.id,"Unknown currency. Please use: usd, eur, uah, gbp")
        return
    bot.register_next_step_handler(message, currency_math)
def data_user(user_id, amount, currency_from, currency_to, result):
    empty = {
        "user_id":user_id,
        "amount":amount,
        "currency_from":currency_from,
        "currency_to":currency_to,
        "result":result,

    }
    data_users_currency.append(empty)
    convert_history_max = data_users_currency[-10:]
    with open("data_users_currency.json","w") as f:
        json.dump(convert_history_max,f,ensure_ascii=False, indent=4)

def currency_math(message):
    currency_from = user_data[message.from_user.id]["currency_from"]
    user_data[message.from_user.id]["currency_to"] = message.text.upper()
    currency_to = user_data[message.from_user.id]["currency_to"]
    amount = float(user_data[message.from_user.id]["amount"])
    if currency_from == currency_to:
        bot.send_message(message.chat.id,"Choose another currency — the currencies are the same")
        return
    code_from = currency_codes.get(currency_from)
    code_to = currency_codes.get(currency_to)
    # rate_fetcher = Rate_buy_rate_sell(currency_from, currency_to)
    result = None
    if currency_from == "UAH":
        rate_buy ,_ = rate_cache.get_rate(code_to,980)
        if rate_buy:
            result = amount / rate_buy
    elif currency_to == "UAH":
        _, rate_sell = rate_cache.get_rate(code_from,980)
        if rate_sell:
            result = rate_sell * amount
    else:
        _,rate_sell_from = rate_cache.get_rate(code_from,980)
        rate_buy_to,_ = rate_cache.get_rate(code_to,980)
        if rate_buy_to and rate_sell_from:
            amount_uah = rate_sell_from * amount
            result = amount_uah / rate_buy_to
    if result:
        data_user(
            user_id = message.from_user.id,
            currency_from = currency_from,
            currency_to = currency_to,
            amount = amount,
            result = result
        )

        bot.send_message(message.chat.id,f"Converted amount: {round(result, 2)} {currency_to}\nEnter a new amount")
    else:
        bot.send_message(message.chat.id, "Exchange rate for this operation not found. Try a different currency pair.")





bot.polling()

