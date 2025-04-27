import os
import dotenv
import aiohttp
import asyncio
import ssl
import certifi


dotenv.load_dotenv()
bot_token = os.getenv("TOKEN")
url = f"https://api.telegram.org/bot{bot_token}/"
last_update_id = 0
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(cafile=certifi.where())

async def send_message(session: aiohttp.ClientSession, chat_id: int, text: str) -> dict:
    params = {"chat_id": chat_id, "text": text}
    async with session.post(url + "sendMessage", data=params) as response:
        return await response.json()

async def process_updates(session: aiohttp.ClientSession):
    global last_update_id
    async with session.get(
        url + "getUpdates",
        params={"offset": last_update_id + 1, "timeout": 30}
    ) as response:
        updates = await response.json()
        
        if "result" in updates:
            for update in updates["result"]:
                last_update_id = update["update_id"]
                message = update.get("message")
                if message:
                    chat_id = message["chat"]["id"]
                    text = message.get("text", "")
                    print(f"Новое сообщение: {text}")

                    if text == "/start":
                        await send_message(session, chat_id, "Привет! Я теперь асинхронный! ⚡")
                    else:
                        await send_message(session, chat_id, f"Эхо: {text}")


async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        while True:
            try:
                await process_updates(session)
                await asyncio.sleep(0.1)
            except aiohttp.ClientError as e:
                print(f"Ошибка подключения: {e}")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Неизвестная ошибка: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())