from config import *
from datetime import datetime
import requests
import json


def load_alive_date():
    try:
        with open("alive.json", "r") as f:
            return json.load(f).get("date", "")
    except:
        return ""


def save_alive_date(date):
    with open("alive.json", "w") as f:
        json.dump({"date": date}, f)


def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    success = True

    for chat_id in [CHAT_ID, CHAT_ID_2]:
        if chat_id:
            response = requests.post(
                url,
                data={
                    "chat_id": chat_id,
                    "text": text
                },
                timeout=20
            )

            print("Telegram Status:", response.status_code)

            if response.status_code != 200:
                print(response.text)
                success = False

    return success


def get_market():

    try:
        response = requests.get(API_URL, timeout=20)

        print("API Status:", response.status_code)

        if response.status_code != 200:
            print(response.text)
            return None

        return response.json()

    except Exception as e:
        print("API Error:", e)
        return None


def load_peaks():

    try:
        with open("prices.json", "r") as f:
            return json.load(f)
    except:
        return {}


def save_peaks(data):

    with open("prices.json", "w") as f:
        json.dump(data, f, indent=2)


print("Bot Started")

data = get_market()

if not data:
    print("No market data")
    exit()

coins = data["data"]
found = False

for coin in coins:
    if "LRC" in coin["sb"]:
        print("FOUND:", coin)
        found = True

if not found:
    print("LRC NOT FOUND IN API")
print("Coins:", len(coins))

peaks = load_peaks()

# -------- پیام سلامت روزانه --------

today = datetime.utcnow().strftime("%Y-%m-%d")
last_alive = load_alive_date()

if today != last_alive:

    alive_message = (
        "✅ Bot Alive\n\n"
        f"📅 {today}\n"
        f"📊 Coins: {len(coins)}\n"
        f"💾 Peaks: {len(peaks)}\n\n"
        "🤖 ربات سالم و در حال اجراست."
    )

    if send_message(alive_message):
        save_alive_date(today)

# -------- بررسی ارزها --------

for coin in coins:

    try:

        symbol = coin["sb"]

        if symbol.startswith("~~"):
            continue

        price = float(coin["c"])

        if symbol not in peaks:
            peaks[symbol] = {
                "peak": price,
                "alerted": False
            }


        # درصد تغییر 24 ساعته (همان درصد قرمز اوربیت)
        drop = float(coin["r8"]) * 100

        print(f"{symbol} | Price={price} | 24H={drop:.2f}%")

        if drop > DROP_PERCENT:
            peaks[symbol]["alerted"] = False

        if drop <= DROP_PERCENT and not peaks[symbol]["alerted"]:

            message = (
                "🚨 هشدار دامپ\n\n"
                f"🪙 {symbol}\n"
                f"📉 ریزش 24 ساعته: {drop:.2f}%\n\n"
                f"💰 قیمت فعلی: {price}"
            )

            if send_message(message):
                peaks[symbol]["alerted"] = True
                print(f"Alert sent: {symbol}")

    except Exception as e:
        print(f"Coin Error ({coin.get('sb', 'UNKNOWN')}): {e}")

save_peaks(peaks)

print("Saved Peaks:", len(peaks))
print("Finished")
