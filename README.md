# 💱 Currency Converter Telegram Bot

A Telegram bot built with Python that allows users to convert between currencies using real-time exchange rates from [Monobank API](https://api.monobank.ua/).

## 📦 Features

- Convert between UAH, USD, EUR, and GBP.
- Interactive currency selection using Telegram buttons.
- Real-time exchange rates with caching (updates every 2 minutes).
- Maintains individual user conversion history (stored in `data_users_currency.json`).
- Commands:
  - `/start` – Greet the user.
  - `/help` – Show usage instructions.
  - `/history` – Show the last 10 conversions of the user.

## ⚙️ Technologies Used

- Python 3
- [pyTelegramBotAPI (telebot)](https://github.com/eternnoir/pyTelegramBotAPI)
- [Monobank Currency API](https://api.monobank.ua/bank/currency)
- `requests`, `json`, `dotenv`

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Set up virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

Inside the root folder, create a `.env` file and add your bot token:

```env
TBOT_API_TOKEN=your_telegram_bot_token
```

### 5. Run the bot

```bash
python main.py
```

The bot will start polling and become active in Telegram.

## 🗂 Project Structure

```
project/
│
├── main.py                   # Main bot logic
├── data_users_currency.json  # User conversion history (auto-generated)
├── .env                      # Environment file for API token
├── requirements.txt          # Python dependencies
└── README.md                 # Project description
```

## 📝 Example Use

1. Send `/start` to the bot.
2. Enter an amount, e.g. `1000`.
3. Choose a currency to convert from (e.g. `USD`).
4. Choose a currency to convert to (e.g. `UAH`).
5. Get the result, e.g. `Converted amount: 38000.0 UAH`.

## 📂 History Feature

Each user's last 10 conversions are saved in a local JSON file:
```json
[
  {
    "user_id": 123456,
    "amount": 100,
    "currency_from": "USD",
    "currency_to": "UAH",
    "result": 3900.0
  }
]
```

## 📄 License

This project is for educational purposes and is licensed under the MIT License.

---

✅ Feel free to contribute or fork this project!
