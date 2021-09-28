from pyrogram import Client, filters
from pyrogram.methods import messages
from pyrogram.methods.auth.terminate import Terminate
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import os
import sys
base_dir = os.path.abspath(os.path.join(os.path.dirname('bot_grabber.py'), '..'))
sys.path.append(base_dir)
from sqll.sql import SQL

bot_tokenn = 'bot_tokenn' # ваш бот токен
y = 'текст который \n будет \nдобавлен' # текст который будет добавлен
api_hash = 'api_hash' #приложение
api_id ='api_id'                     #приложение

app = Client('bot_python', api_id =api_id,api_hash = api_hash,bot_token=bot_tokenn)
bd = SQL('../bd.db')
urlr = ''   # не трогать , должен быть пустым
copy_text = '' # не трогать , должен быть пустым
cap_text = ''   # не трогать , должен быть пустым
@app.on_message(filters.chat(bd.get_donor()))
def get_post(client, message):
    username = message.chat.username
    message_id = message.message_id
    print(message)
    print("/////////")
    print(message.entities[0].url)
    if not bd.message_id_exists(username, message_id):
        bd.add_message_id(username, message_id)
        # получение последнего ROWID
        for a in bd.get_last_rowid():
            last_id = a[0]
        # перессылка поста на модерку
        global copy_text
        global cap_text
        global urlr
        urlr = message.entities[0].url
        cap_text = message.caption
        copy_text = message.text
        app.copy_message(bd.get_moder(),from_chat_id = username,message_id = message_id )
        app.send_message(bd.get_moder(), last_id )
        x = client.copy_message(bd.get_channel(),from_chat_id = username, message_id = message_id )
        if message.text == None:
            if message.caption == None:
                x.edit_caption(f'{y}')
            else:
                x.edit_caption(f'{message.caption}\n \n \n {y}')
        else:
        if urlr == None:
            x.edit_text(f'{copy_text}\n \n \n {y}')
        else:
            x.edit_text(f'{copy_text}\n \n \n {y}\n \n{urlr}'))

@app.on_message(filters.chat(bd.get_moder()))
def send_post(client, message):
    message_id = message.message_id
    # получаем запись в таблице
    for item in bd.get_data_in_table(message):
        username = item[0]
        msg_id = item[1]
    x = client.copy_message(bd.get_channel(),from_chat_id = username,message_id = msg_id )
    if copy_text == None:
        if cap_text == None:
            x.edit_caption(f'{y}')
        else:    
            x.edit_caption(f'{cap_text}\n \n \n {y}')
        
    else:
        if urlr == None:
            x.edit_text(f'{copy_text}\n \n \n {y}')
        else:
            x.edit_text(f'{copy_text}\n \n \n {y}\n \n{urlr}')



if __name__ == '__main__':
    print(datetime.today().strftime(f'%H:%M:%S | Bot Telegram-Grabber launched.'))
    app.run()
