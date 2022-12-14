import sqlite3
import telebot
import time
from telebot import types

bot = telebot.TeleBot("5803013532:AAEhzm5XmNtKHxK9JgDAJnd_X30js9EcmHM")
one_stings = []

connect = sqlite3.connect('DailyArt.db', check_same_thread=False)
cursor = connect.cursor()

def main ():
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id (
           id INTEGER
       )""")
    connect.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Pictures (
           url TEXT,
           name TEXT,
           author TEXT,
           disk TEXT,
           like TEXT
       )""")
    connect.commit()

if __name__ == "__main__":
    main()


@bot.message_handler(commands=['start'])
def start_message(message):
    #cursor.execute("INSERT INTO pictures(_id, url, name) VALUES(?, ?, ?);", (picture, url, name))
    connect = sqlite3.connect('DailyArt.db', check_same_thread=False)
    cursor = connect.cursor()
    #регистрация
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()

    if data is None:
        user_id = [message.chat.id]
        cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
        connect.commit()
        bot.send_message(message.chat.id, 'Вы зарегестрированы! \nЧтобы остановить бота напишите /stop')
    else:
        bot.send_message(message.chat.id, 'Отлично, Вы уже зарегестрированы! \nЧтобы остановить бота, напишите /stop')

    while(1):
        cursor.execute("SELECT * FROM Pictures")
        one_url = cursor.fetchall()
        for one_string in one_url:
            if Chech_reg(message, cursor):
                global one_stings
                one_stings = one_string
                markup = types.InlineKeyboardMarkup()
                switch_button = types.InlineKeyboardButton(text='Читать описание:', callback_data="readfull")
                markup.add(switch_button)
                bot.send_photo(message.chat.id, one_string[0],
                               "Картина дня: " + one_string[1] + "\n" + "Автор: " + one_string[2],
                               reply_markup=markup)
                time.sleep(15)
            else:
                print("break")
                break
        break
    cursor.close()
    connect.close()



def Chech_reg (message, cursor):
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is not None: return 1
    else: return 0

@bot.callback_query_handler(func=lambda call: True)
def inline(c):
    if c.data == "readfull":
        global one_stings
        bot.send_message( c.message.chat.id, "Описание:" + one_stings[3])



@bot.message_handler(commands=['stop'])
def stop_command(message):
    global connect, cursor
    bot.send_message(message.chat.id, 'Ваш пользователь удалён, но вы всегда можете к нам вернуться!'
                                      ' Просто напишите /start')
    delete_user(message.chat.id, cursor, connect)

def delete_user(user_id, cursor, connect):  # FIX IT
    cursor.execute('''DELETE FROM login_id WHERE id = ?''', (user_id,))
    connect.commit()
bot.polling()