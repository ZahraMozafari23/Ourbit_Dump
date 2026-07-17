from config import *
import requests
import json


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
                }
            )

            print("Telegram Status:", response.status_code)
            print(response.text)

            if response.status_code != 200:
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

if data:
    coins = data["data"]

    print("Coins:", len(coins))

    peaks = load_peaks()

    count = 0

for coin in coins:

    try:
        if coin["sb"] == "NVDAON_USDT":
            print(json.dumps(coin, indent=2))
          
        symbol = coin["sb"]

        if symbol.startswith("~~"):
            continue

        price = float(coin["c"])

        if symbol not in peaks:
            peaks[symbol] = {
                "peak": price,
                "alerted": False
            }

        # اگر سقف جدید ساخت
        if price > peaks[symbol]["peak"]:
            peaks[symbol]["peak"] = price
            peaks[symbol]["alerted"] = False

        peak = peaks[symbol]["peak"]

        if peak <= 0:
            continue

        drop = ((price - peak) / peak) * 100

        print(f"{symbol} | Peak={peak} | Price={price} | Drop={drop:.2f}%")

        if drop <= DROP_PERCENT and not peaks[symbol]["alerted"]:

            message = (
                "🚨 هشدار دامپ\n\n"
                f"🪙 {symbol}\n"
                f"📉 ریزش: {drop:.2f}%\n\n"
                f"📈 Peak: {peak}\n"
                f"💰 قیمت فعلی: {price}"
            )

            if send_message(message):
                peaks[symbol]["alerted"] = True
                print(f"Alert sent: {symbol}")

    except Exception as e:
        print(f"Coin Error ({coin.get('sb','UNKNOWN')}): {e}")
               

            


save_peaks(peaks)

print("Saved Peaks:", len(peaks))

print("Finished")


            

    
