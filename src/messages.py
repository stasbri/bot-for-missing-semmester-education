import urllib.error

from telebot import types
import json
import functions
import time
from settings import dict_bd_the_worst_db as db
from functions import get_all, get_costs, get_incomes, add_costs, add_incomes, create_new_user, joke, read_users, save_users


def Make_Row_Keyboard():
    board = types.ReplyKeyboardMarkup(True, False)
    board.row('доходы', 'расходы')
    board.row('добавить доход', 'добавить расход')
    board.add('итог')
    return board


class Waiter:
    def __init__(self):
        self.incomes = False
        self.costs = False


class Message_Handler:
    def __init__(self, bot, master_users: list, cost_acc: dict = read_users(db)):
        self.bot = bot
        self.master_users = master_users
        self.board = Make_Row_Keyboard()
        self.cost_acc = cost_acc
        self.waiting_users = {}
        for key in self.cost_acc.keys():
            self.waiting_users[key] = Waiter()
        self.Send(user_id=list(self.cost_acc.keys()), message='только что произошел рестарт бота, из-за чего все операции по вводу дохода и расхода были прерваны, приносим извинения')

    def Process_Message(self, message):
        text = message.text
        user_id = message.from_user.id
        if user_id not in self.cost_acc.keys():
            self.Send(user_id=user_id,message=create_new_user(db=self.cost_acc, user_id=user_id))
            self.waiting_users[user_id] = Waiter()
            save_users(db, self.cost_acc)
        if self.waiting_users[user_id].incomes:
            try:
                s = float(text)
            except ValueError:
                print('caught error')
                self.Send(user_id=user_id, message='Вы ввели не число, процесс добавления дохода отменен')
                self.waiting_users[user_id].incomes = False
                return
            print(f'{user_id} in incomes')
            self.Send(user_id=user_id, message=add_incomes(db=self.cost_acc, user_id=user_id, amount=float(text)))
            self.waiting_users[user_id].incomes = False
            print(f'destryoedd {user_id} income')
            save_users(db, self.cost_acc)
        elif self.waiting_users[user_id].costs:
            try:
                s = float(text)
            except ValueError:
                self.Send(user_id=user_id, message='Вы ввели не число, процесс добавления расхода отменен')
                self.waiting_users[user_id].costs = False
                return
            print(f'{user_id} in costs')
            self.Send(user_id=user_id, message=add_costs(db=self.cost_acc, user_id=user_id, amount=float(text)))
            self.waiting_users[user_id].costs = False
            print(f'destryoedd {user_id} costs')
            save_users(db, self.cost_acc)
        elif text == 'доходы':
            self.Send(user_id=user_id, message=get_incomes(db=self.cost_acc, user_id=user_id))
        elif text == 'расходы':
            self.Send(user_id=user_id, message=get_costs(db=self.cost_acc, user_id=user_id))
        elif text == 'итог':
            self.Send(user_id=user_id, message=get_all(db=self.cost_acc, user_id=user_id))
        elif text == 'добавить доход':
            self.Send(user_id=user_id, message='Напишите ваш доход одним числом')
            if user_id in self.waiting_users.keys():
                self.waiting_users[user_id].incomes = True
            else:
                self.waiting_users[user_id] = Waiter()
                self.waiting_users[user_id].incomes = True
        elif text == 'добавить расход':
            self.Send(user_id=user_id, message='Напишите ваш расход одним числом')
            if user_id in self.waiting_users.keys():
                self.waiting_users[user_id].costs = True
            else:
                self.waiting_users[user_id] = Waiter()
                self.waiting_users[user_id].costs = True
        elif text == '/start':
            self.Send(user_id=user_id, message='Приветствую')
        else:
            self.Send(user_id=user_id, message=joke())

    def Send(self, user_id, message=None, markup=None):
        if not markup:
            markup = self.board
        if isinstance(user_id, int):
            self.bot.send_message(user_id, message, reply_markup=markup)
        elif isinstance(user_id, list):
            for user in user_id:
                if isinstance(user, int):
                    self.bot.send_message(user, message, reply_markup=markup)
                else:
                    raise ValueError(f'received multiple ids, {user} is incorrect should be int')

        else:
            print(user_id)
            raise ValueError(f'incorrect id {user_id} only int or list of ints')
