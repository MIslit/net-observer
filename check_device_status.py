import asyncio
import subprocess

class Check_Device_Status:
    def __init__(self, bot, settings, CHAT_ID):
        self.bot = bot
        self.settings = settings
        self.CHAT_ID = CHAT_ID
        self.DEVICE_IP = settings.DEVICE_IP
        self.CHECK_INTERVAL = settings.CHECK_INTERVAL
        self.current_device_statuses = {}
        
    async def device_statuses(self):
        reply = ''
        for k, v in self.current_device_statuses.items():
            reply += (f"{k}: {v};\n")
        
        await self.bot.send_message(self.CHAT_ID, f"Все опрошенные устройства:🧾\n{reply}")

    async def check_device_status(self):
        self.current_device_statuses = {}
        device_statuses = {}
        devices_ip = self.DEVICE_IP
        while True:
            for ip in devices_ip:
                for k, v in ip.items():
                    response = subprocess.run(['ping', '-c', '3', k], capture_output=True)

                    if response.returncode == 0:
                        current_status = 'Устройство доступно🟢'
                        self.current_device_statuses[k] = f"({v}) - {current_status}"
                    else:
                        current_status = 'Устройство не доступно🔴'
                        self.current_device_statuses[k] = f"({v}) - {current_status}"

                    try:
                        if self.current_device_statuses != device_statuses:
                            device_statuses[k] = self.current_device_statuses[k]
                            await self.bot.send_message(self.CHAT_ID, f"Статус устройства {v} изменился:\n{current_status}")

                    except KeyError as e:
                        await self.bot.send_message(self.CHAT_ID, f"Ошибка: {e}\n{self.current_device_statuses}\n{device_statuses}")

            await asyncio.sleep(self.CHECK_INTERVAL)

    