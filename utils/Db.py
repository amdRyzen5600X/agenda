import json
from aiogram import types


CustomUser = dict[str, str | int]
Chat = dict[str, CustomUser]
DB = dict[str, Chat]

def add_new_chat(db: DB, msg: types.Message) -> None:
    add_chat = {
            str(msg.chat.shifted_id): {
                str(msg.from_user.id): {
                    "username": str(msg.from_user.username),
                    "count": 1,
                    }
                }
            }
    db.update(add_chat)

def add_new_user(db: DB, msg: types.Message) -> None:
    users = db.get(str(msg.chat.shifted_id))
    add_user = {
            str(msg.from_user.id): {
                "username": str(msg.from_user.username),
                "count": 1
                }
            }
    if users is None:
        add_new_chat(db, msg)
        return
    users.update(add_user)
    db.update({ str(msg.chat.shifted_id): users})

def increase_count(db: DB, msg: types.Message) -> None:
    users = db.get(str(msg.chat.shifted_id))
    if users is None:
        add_new_chat(db, msg)
        return

    user = users.get(str(msg.from_user.id))
    if user is None:
        add_new_user(db, msg)
        return

    count = user.get("count")
    if count is None:
        add_new_user(db, msg)
        return

    user.update({"count": int(count)+1})
    users.update({ str(msg.from_user.id): user})
    db.update({ str(msg.chat.shifted_id): users})

def load_db(filepath: str) -> DB:
    with open(filepath, "r") as file:
        db = json.loads(file.read())

    return db

def save_changes(db: DB, filepath: str) -> None:
    with open(filepath, 'w') as file:
        file.write(json.dumps(db))

def format_dict_to_leadreboard(chat: Chat, counter: int) -> str:
    users = [x for x in chat.values()]
    users.sort(key=lambda x: x.get("count"), reverse=True)
    res = '<strong>Таблица лидеров:</strong>\n'
    for user in users[:10]:
        res = f'{res}{user["username"]}: {user["count"]}\n'

    res = f'{res}\n--------\n<strong>До сообщения с агитацией: <i>{15 - counter}</i></strong>'

    return res


if __name__ == "__main__":
    db = load_db("db.json")
    print(format_dict_to_leadreboard(db.get("1720756304")))
