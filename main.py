import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

from settings import Settings
from check_url import Check_url
from mac_add import Mac_add
from ssh import SSH
from check_device_status import Check_Device_Status
from tracert import Tracert
from ping import Ping


settings = Settings()

bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)

CHAT_ID = settings.CHAT_ID
CHECK_INTERVAL = settings.CHECK_INTERVAL  # Интервал проверки в секундах
WEBSITE_URL = settings.WEBSITE_URL
AUTHORIZED_USERS = settings.AUTHORIZED_USERS

message = ''
ip = ''
command = ''
website_status = ''

check_url = Check_url(bot, settings, CHAT_ID, WEBSITE_URL, CHECK_INTERVAL, website_status)
mac_add = Mac_add(bot, CHAT_ID, message, ip)
ssh = SSH(message)
cds = Check_Device_Status(bot, settings, CHAT_ID)
tracert = Tracert(message, ip)
ping_ip = Ping(message, ip)

class AuthMiddleware(BaseMiddleware):
    """ Проверка авторизации """
    async def on_pre_process_update(self, update, data):
        if update.message:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        else:
            return

        if user_id not in AUTHORIZED_USERS:
            if update.message:
                await update.message.reply("🚫Не авторизованный доступ. Вам не разрешено использовать этого бота. Обратитесь к системному администратору.🔒")
            elif update.callback_query:
                await update.callback_query.message.answer("🚫Не авторизованный доступ. Вам не разрешено использовать этого бота. Обратитесь к системному администратору.🔒")
            raise CancelHandler()

dp.middleware.setup(AuthMiddleware())

async def start():
    await dp.bot.send_message(CHAT_ID, "🟢System started!\nНапиши /help, чтобы узнать, что я умею👨🏻‍💻")

# Автоматическая проверка состояния сайта
async def check_websites():
    await check_url.check_website()

async def check_device_status():
    await cds.check_device_status()

@dp.message_handler(commands=["help"])
async def cmd_help(message):
    await message.reply(f'📋Список команд:\n/check - проверка статуса системы✅\n/check_devices - проверка статуса устройств🖥️\n/check_webiste🌎\n/ssh_connect - соединение через ssh🔒\n/get_mac - получение mac-адреса🕵️‍♂️\n/ping - проверки доступности узла сети🌐\n/tracert - для определения маршрута🔎\n/exit - выключение бота❌\n')

@dp.message_handler(commands=["check"])
async def cmd_check(message):
    await message.reply("System status: online🟢")

@dp.message_handler(commands=["check_devices"])
async def check_devices(message):
    await cds.device_statuses()

@dp.message_handler(commands=["check_website"])
async def cmd_check_website(message):
    await check_url.cmd_check_website()

@dp.message_handler(commands=["ssh_connect"])
async def ssh_connect(message):
    await ssh.get_routes(message)

@dp.message_handler(commands=["get_mac"])
async def find_mac_addresses(message):
    await mac_add.cmd_find_mac(message)

@dp.message_handler(commands=['traceroute'])
async def traceroute(message):
    await tracert.traceroute(message)

@dp.message_handler(commands=['ping'])
async def ping(message):
    await ping_ip.ping(message)

@dp.message_handler(commands=["exit"])
async def cmd_exit(message):
    await message.answer("System stoped!🔴")
    raise SystemExit

def main():    
    dp.register_message_handler(help, commands="help")
    dp.register_message_handler(cmd_check, commands="check")
    dp.register_message_handler(traceroute, commands="tracert")
    dp.register_message_handler(ping, commands="ping")
    dp.register_message_handler(check_devices, commands="check_devices")
    dp.register_message_handler(cmd_check_website, commands="check_website")
    dp.register_message_handler(ssh_connect, commands="ssh_connect")
    dp.register_message_handler(find_mac_addresses, commands="get_mac")
    dp.register_message_handler(cmd_exit, commands="exit")
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.create_task(check_websites())
    loop.create_task(check_device_status())
    
    main()  