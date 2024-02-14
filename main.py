import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup 
from utils import Db
from config import TOKEN


API_TOKEN = TOKEN
db = Db.load_db("db.json")

async def start_bot():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)
    global counter
    counter = 0
    dp.register_message_handler(
            send_an_agenda, 
            filters.RegexpCommandsFilter(regexp_commands=['naz(h)?mi_esli_(t[yi]_)?za.*'])
    )
    dp.register_message_handler(
            send_leaderboard, 
            commands=["leaderboard"]
    )
    await set_commands(bot)
    await dp.start_polling()


async def send_an_agenda(msg: types.Message) -> None:
    global counter
    counter += 1
    try:
        Db.increase_count(db, msg)
        Db.save_changes(db, "db.json")
        text = """
<strong>Мерей Абдикарим</strong>, студентка группы SE-2201, баллотируется на пост <strong>президента Студенческого правительства.</strong> В своей студенческой жизни Мерей занимает различные роли – от старосты и ментора первокурсников до админа Телеграм-каналов AITU Science и члена AITUSA.

<strong>Подпишитесь на канал Мерей and stay tuned! https://t.me/Mereysstuff</strong>
        """
        if counter == 15:
            irm = InlineKeyboardMarkup()
            irm.insert(InlineKeyboardButton(text='🫰Узнать подробнее🫰', url="https://t.me/Mereysstuff"))
            await msg.reply(text, parse_mode='html', reply_markup=irm)
            counter = 0
    except TypeError:
        return

async def send_leaderboard(msg: types.Message) -> None:
    try:
        chatstat = db.get(str(msg.chat.shifted_id))
        if chatstat is None:
            text = "в данном чате ещё никто не использовал агитацию"
            await msg.reply(text)

        text = Db.format_dict_to_leadreboard(db.get(str(msg.chat.shifted_id)), counter)

        await msg.reply(text, parse_mode='html')
    except TypeError:
        return

async def set_commands(bot: Bot):
    commands = [
            types.BotCommand(command='/leaderboard', description='топ 10 лучших агитаторов'),
    ]
    await bot.set_my_commands(commands)

if __name__ == "__main__":
    asyncio.run(start_bot())
