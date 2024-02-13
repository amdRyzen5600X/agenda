from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters 
from utils import Db
from config import TOKEN


API_TOKEN = TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db = Db.load_db("db.json")
global counter
counter = 0

@dp.message_handler(
        filters.IDFilter(chat_id=["-1001720756304", "-1001854457142"]), 
        filters.RegexpCommandsFilter(regexp_commands=['naz(h)?mi_esli_(ty_)?za.*'])
        )
@dp.message_handler(
        filters.IDFilter(user_id=["1072746639", "6434668397"]), 
        filters.RegexpCommandsFilter(regexp_commands=['naz(h)?mi_esli_(ty_)?za.*'])
    )
async def send_an_agenda(msg: types.Message) -> None:
    global counter
    counter += 1
    Db.increase_count(db, msg)
    Db.save_changes(db, "db.json")
    text = """
    <strong>Мерей Абдикарим</strong>, студентка группы SE-2201, баллотируется на пост <strong>президента Студенческого правительства.</strong> В своей студенческой жизни Мерей занимает различные роли – от старосты и ментора первокурсников до админа Телеграм-каналов AITU Science и члена AITUSA.

<strong>Подпишитесь на канал Мерей and stay tuned! https://t.me/Mereysstuff</strong>
    """
    if counter == 50:
        await msg.reply(text, parse_mode='html')
        counter = 0

@dp.message_handler(commands=["leaderboard"])
async def send_leaderboard(msg: types.Message) -> None:
    chatstat = db.get(str(msg.chat.shifted_id))
    if chatstat is None:
        text = "в данном чате ещё никто не использовал агитацию"
        await msg.reply(text)

    text = Db.format_dict_to_leadreboard(db.get(str(msg.chat.shifted_id)), counter)

    await msg.reply(text, parse_mode='html')
# @dp.message_handler(commands=["start"])
# async def test(msg: types.Message):
#     await msg.reply("aaa")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

