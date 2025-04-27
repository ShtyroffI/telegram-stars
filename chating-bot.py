
import requests
import dotenv
import os
import time

dotenv.load_dotenv()
bot_token = os.getenv("TOKEN_TEST")

# URL для получения обновлений
url = f"https://api.telegram.org/bot{bot_token}/"
last_update_id = 0  # Для отслеживания последнего обработанного сообщения

def send_message(chat_id, text):
    params = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url + "sendMessage", data=params)
    return response.json()

while True:
    try:
        # Получаем обновления с long polling
        updates = requests.get(
            url + "getUpdates",
            params={"offset": last_update_id + 1, "timeout": 30}
        ).json()

        if "result" in updates:
            for update in updates["result"]:
                last_update_id = update["update_id"]
                message = update.get("message")
                if message:
                    chat_id = message["chat"]["id"]
                    text = message.get("text", "")
                    print(f"Новое сообщение: {text}")

                    # Ответ на команду /start
                    if text == "/start":
                        send_message(chat_id, "Привет, я Фараон. Напиши че-нибудь")
                    else:
                        text = input('Введите текст: ')
                        send_message(chat_id, text)

        time.sleep(1)

    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)