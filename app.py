from flask import Flask, request
import requests

app = Flask(__name__)

# твой токен Тинькофф API (получаешь в ЛК)
TINKOFF_TOKEN = "ТОКЕН_ОТСЮДА"

# адрес API
BASE_URL = "https://api-invest.tinkoff.ru/openapi"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # получаем JSON от TradingView
    print("Пришёл сигнал:", data)

    # пример: создаём лимитный ордер на покупку 10 акций Сбера
    order = {
        "figi": "BBG004730N88",  # FIGI Сбербанк
        "quantity": 10,
        "price": 270.00,
        "direction": "BUY",
        "accountId": "ТВОЙ_ACCOUNT_ID",
        "orderType": "LIMIT"
    }

    headers = {"Authorization": f"Bearer {TINKOFF_TOKEN}"}
    r = requests.post(BASE_URL + "/orders/limit-order", json=order, headers=headers)

    return {"status": "ok", "tinkoff_response": r.json()}

if __name__ == "__main__":
    app.run(port=5000)
