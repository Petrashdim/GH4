from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

TINKOFF_TOKEN = os.environ.get("TINKOFF_TOKEN")  # токен храним в Render Secrets
TINKOFF_API_URL = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.OrdersService/PostOrder"

@app.route("/healthz", methods=["GET"])
def healthz():
    return "ok", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Получен webhook:", data)

    try:
        action = data.get("action", "buy")  # buy / sell
        ticker = data.get("ticker", "SBER")  # тикер, можно менять
        lots = int(data.get("contracts", 1))  # количество

        # Маппинг: action → direction
        side = "ORDER_DIRECTION_BUY" if action == "buy" else "ORDER_DIRECTION_SELL"

        # JSON-заявка в Тинькофф
        payload = {
            "figi": "BBG004730N88",  # FIGI инструмента (пример: Сбербанк)
            "quantity": lots,
            "price": {
                "units": 0,
                "nano": 0  # рыночная заявка, если цену не указывать
            },
            "direction": side,
            "accountId": "",   # сюда можно вставить Account ID
            "orderType": "ORDER_TYPE_MARKET",
            "orderId": "tv-" + str(os.urandom(4).hex())
        }

        headers = {
            "Authorization": f"Bearer {TINKOFF_TOKEN}",
            "Content-Type": "application/json"
        }

        resp = requests.post(TINKOFF_API_URL, headers=headers, json=payload)
        print("Ответ Тинькофф:", resp.text)

        return jsonify({"status": "order_sent", "tinkoff_response": resp.json()}), 200

    except Exception as e:
        print("Ошибка:", e)
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
