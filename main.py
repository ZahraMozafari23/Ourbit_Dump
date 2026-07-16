from config import *
import requests


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


print("Bot Started")

data = get_market()

if data:
    coins = data["data"]

    print("Coins:", len(coins))

    count = 0

for coin in coins:

    symbol = coin["sb"]

    if symbol.startswith("~~"):
        continue

    price = float(coin["c"])

    print(symbol, price)

    count += 1

    if count == 5:
        break

print("Finished")
