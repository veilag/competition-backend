from uvicorn import run
from . import app

# 🚀 API для проведения олимпиады
# Для информации перейдите в ../README.md
#
# 👮‍ Разработчик: Галиев Рамиль
#
# Фронтенд (Для ПК): https://github.com/...
# Фронтенд (Telegram мини-приложение): https://github.com/...
#
#

if __name__ == "__main__":
    run(app, host="localhost", port=8000)
