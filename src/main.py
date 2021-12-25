import telebot

from settings import token, master_user_id
import time
from messages import Message_Handler

if token is None:
    print('no token received')
    raise ValueError('no token on cost_acc_bot')

bot = telebot.TeleBot(token)

handler = Message_Handler(bot=bot, master_users=master_user_id)


@bot.message_handler(commands=['start'])
def message_listener(message):
    handler.Process_Message(message)


@bot.message_handler(content_types='text')
def message_listener(message):
    handler.Process_Message(message)
    print(message.text, message.from_user.id)


bot.infinity_polling()
