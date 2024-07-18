import asyncio
import requests

class Check_url:
    def __init__(self, bot, settings, CHAT_ID, WEBSITE_URL, CHECK_INTERVAL, website_status):
        self.bot = bot
        self.settings = settings
        self.CHAT_ID = settings.CHAT_ID
        self.WEBSITE_URL = settings.WEBSITE_URL
        self.CHECK_INTERVAL = settings.CHECK_INTERVAL
        self.website_status = website_status
        
    async def cmd_check_website(self):        
        await self.bot.send_message(self.CHAT_ID, f"🌎Статус сайта {self.WEBSITE_URL}: {self.website_status}")

    # Функция для проверки состояния сайта
    async def check_website(self):
        while True:
            try:
                response = requests.get(self.WEBSITE_URL)
                if response.status_code == 200:
                  new_status = 'Сайт доступен🟢'
                else:
                   new_status = f"Сайт недоступен🔴\n(код состояния: {response.status_code})"
            except requests.RequestException as e:
                new_status = f"⚠️Ошибка при попытке доступа к сайту: {str(e)}"
            
            if new_status != self.website_status:
                self.website_status = new_status
                await self.bot.send_message(self.CHAT_ID, f"❗Статус сайта {self.WEBSITE_URL} изменился:\n{self.website_status}")
            
            await asyncio.sleep(self.CHECK_INTERVAL)

    