from config import *
import requests
import json

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

        symbol = coin["sb"]

        if symbol.startswith("~~"):
            continue

        price = float(coin["c"])

        if symbol not in peaks:
            peaks[symbol] = {
                "peak": price,
                "alerted": False
            }

        elif price > peaks[symbol]["peak"]:
            peaks[symbol]["peak"] = price
            peaks[symbol]["alerted"] = False
        drop = ((price - peaks[symbol]["peak"]) / peaks[symbol]["peak"]) * 100

        if drop <= -10:
            print("drop fund:", symbol, f"{drop:.2f}%")

        

        

    save_peaks(peaks)
    print("example:", list(peaks.items())[:3])
    print("seved peaks:", len(peaks))

print("Finished")
