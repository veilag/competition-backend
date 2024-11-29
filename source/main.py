from uvicorn import run
from . import app

# 🚀 API для проведения олимпиады
# Для информации перейдите в ../README.md
#
# 👮‍ Разработчик: Галиев Рамиль
#
# Frontend (Для ПК): https://github.com/...
# Frontend (Telegram мини-приложение): https://github.com/...
#
#

if __name__ == "__main__":
    run(app, host="localhost", port=8000)
