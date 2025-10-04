from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Берём токен из переменных окружения (ты уже сделал setx TINKOFF_TOKEN "...")
TINKOFF_TOKEN = os.environ.get("TINKOFF_TOKEN")

@app.route("/healthz", methods=["GET"])
def health():
    return "OK", 200

# Этот маршрут принимает сигнал от TradingView (webhook)
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📩 Получен сигнал:", data)   # вывод в консоль для проверки

    # Пример запроса к Tinkoff OpenAPI (смотри песочницу!)
    if TINKOFF_TOKEN:
        url = "https://api-invest.tinkoff.ru/openapi/sandbox/portfolio"
        headers = {"Authorization": f"Bearer {TINKOFF_TOKEN}"}
        r = requests.get(url, headers=headers)
        print("📊 Ответ Тинькофф API:", r.json())  # тоже выведем в консоль

    return jsonify({"status": "ok", "received": data})

if __name__ == "__main__":
    # Flask слушает порт 5000
    app.run(host="0.0.0.0", port=5000)
