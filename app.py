# app.py
from flask import Flask, request, jsonify

# Создаем Flask-приложение
app = Flask(__name__)

# Эндпоинт для приема вебхуков (сюда будет слать TradingView)
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)  # получаем JSON из запроса
        print("📩 Получен сигнал:", data)     # выводим в консоль (будет видно в логах Render)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("❌ Ошибка:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 400

# Эндпоинт для проверки здоровья (Render будет сюда стучаться)
@app.route("/healthz", methods=["GET"])
def healthz():
    return "ok", 200

# Запуск приложения
if __name__ == "__main__":
    # host="0.0.0.0" — чтобы сервер был доступен снаружи
    # port=5000 — Render автоматически пробрасывает этот порт
    app.run(host="0.0.0.0", port=5000, debug=True)
