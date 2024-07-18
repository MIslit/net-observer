import asyncio
from aiogram.types import ParseMode

class Ping():
    def __init__(self, message, ip):
        self.message = message
        self.message = ip
        
    async def ping_ip(self, ip):
        process = await asyncio.create_subprocess_exec(
            'ping', '-c', '4', ip,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return f"{stdout.decode()}\n\nОшибки (если есть):\n{stderr.decode()}"

    async def ping(self, message):
        try:
            ip_address = message.text.split(' ')[1]
            ping_result = await self.ping_ip(ip_address)
            response = f"✅Результат ping для IP-адреса {ip_address}:\n```{ping_result}```"
        except IndexError:
            response = "⚠Пожалуйста, укажите IP-адрес после команды /ping."

        await message.reply(response, parse_mode=ParseMode.MARKDOWN)
