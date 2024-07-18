import re
from scapy.all import ARP, Ether, srp

class Mac_add:
    def __init__(self, bot, CHAT_ID, message, ip):
        self.CHAT_ID = CHAT_ID
        self.bot = bot
        self.message = message
        self.ip = ip

    # Функция для получения MAC-адресов устройств в сети
    def get_mac_addresses(self, ip):
        # Формируем ARP-запрос для получения MAC-адресов
        arp = ARP(pdst=ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        # Отправляем ARP-запрос и получаем ответы
        result = srp(packet, timeout=2, verbose=0)[0]

        # Извлекаем MAC-адреса из ответов
        mac_addresses = []
        for sent, received in result:
            mac_addresses.append({'IP': received.psrc, 'MAC': received.hwsrc})

        # Возвращаем список MAC-адресов
        return mac_addresses

    # Обработчик текстовых сообщений
    
    async def cmd_find_mac(self, message):
        # Получаем IP-адрес подсети
        target_ip = message.text.split()[1]

        # Проверяем формат введенного IP-адреса
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        if not re.match(ip_pattern, target_ip):
            await self.bot.send_message(self.CHAT_ID, "⚠️Неверный формат IP-адреса. Введите его в формате xxx.xxx.xxx.xxx.")
            return

        # Получаем MAC-адреса устройств в сети
        mac_addresses = self.get_mac_addresses(target_ip)

        # Проверяем, есть ли устройства в сети
        if not mac_addresses:
            await self.bot.send_message(self.CHAT_ID, "❌В данной сети нет активных устройств.")
            return

        # Выводим полученные MAC-адреса
        response = ""
        for device in mac_addresses:
            response += f"✅IP: {device['IP']}, MAC: {device['MAC']}\n"

        # Отправляем сообщение с результатами
        await self.bot.send_message(self.CHAT_ID, response)
