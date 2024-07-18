import asyncio
from aiogram.types import ParseMode

class Tracert():
    def __init__(self, message, ip):
        self.message = message
        self.message = ip
        
    async def traceroute_ip(self, ip):
        process = await asyncio.create_subprocess_exec(
            'traceroute', ip,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return f"{stdout.decode()}\n\nОшибки (если есть):\n{stderr.decode()}"

    async def traceroute(self, message):
        try:
            ip_address = message.text.split(' ')[1]
            traceroute_result = await self.traceroute_ip(ip_address)
            response = f"✅Результат traceroute для IP-адреса {ip_address}:\n```{traceroute_result}```"
        except IndexError:
            response = "⚠Пожалуйста, укажите IP-адрес после команды /traceroute."

        await message.reply(response, parse_mode=ParseMode.MARKDOWN)
