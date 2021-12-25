import typing
import time
from typing import Dict, List
import random


class Money:
    def __init__(self, money = 0, time = str(time.ctime())):
        self.money = money
        self.date = time


def my_encoder(d:Dict[int, List[Money]]) -> str:
    text = ''
    for name in d.keys():
        text += str(name) + '; '
        for money in d[name]:
            text += f'{money.money}, {money.date} $'
        text += '#'
    return text

def my_decoder(text) -> Dict[int, List[Money]]:
    d = {}
    t = text.split('#')
    for one_user in t:
        print(one_user)
        if one_user not in  ['', ' ']:
            u = one_user.split(';')
            user_id = int(u[0])
            d[user_id] = []
            for element in u[1].split('$'):
                print(element)
                if element not in ['', ' ']:
                    print(len(element))
                    money =  float(element.split(',')[0])
                    date = element.split(',')[1]
                    d[user_id].append(Money(money, date))
    return d


def read_users(file_name):
    try:
        f = open(file_name, 'r')
        users = f.read()
        f.close()
        users = my_decoder(users)
    except FileNotFoundError:
        f = open(file_name, 'w')
        f.write(my_encoder({}))
        f.close()
        users = dict()
    res = dict()
    for key in users.keys():
        res[int(key)] = users[key]
    return res


def save_users(file_name, users:Dict):
    f = open(file_name, 'w')
    f.write(my_encoder(users))
    f.close()


def get_incomes(db:Dict[int, List[Money]], user_id: int) -> float:
    total = 0
    for i in db.get(user_id, []):
        if i.money >= 0:
            total += i.money
    return total

def get_costs(db:Dict[int, List[Money]], user_id: int) -> float:
    total = 0
    for i in db.get(user_id, []):
        if i.money < 0:
            total += i.money
    return - total

def get_all(db:Dict[int, List[Money]], user_id) -> str:
    resulting_message = ''
    total = 0
    for i in db.get(user_id, []):
        if i.money >= 0:
            resulting_message += f'Доход {str(i.money)} в {str(i.date)}\n'
        else:
            resulting_message += f'Расход { str(- i.money)} в {str(i.date)}\n'
        total += i.money
    resulting_message += f'Всего денег {str(total)}'
    return resulting_message


def add_incomes(db:Dict[int, List[Money]], user_id: int, amount: int) -> str:
    if user_id in db.keys():
        db[user_id].append(Money(amount))
        return f'Добавил доход в размере {str(amount)} во время {str(time.ctime())}'
    db[user_id] = [Money(amount)]
    return f'Создал нового пользователяю \nДобавил доход в размере {str(amount)} во время {str(time.ctime())}'


def add_costs(db: Dict[int, List[Money]], user_id: int, amount: int) -> str:
    if user_id in db.keys():
        db[user_id].append(Money( - amount))
        return f'Добавил расход в размере {str(amount)} во время {str(time.ctime())}'
    db[user_id] = [Money(amount)]
    return f'Создал нового пользователяю \nДобавил расход в размере {str(amount)} во время {str(time.ctime())}'


def create_new_user(db: Dict[int, List[Money]], user_id: int) -> str:
    db[user_id] = []
    return f'Создал нового пользователя'




def joke():
    msg = 'вы ввели что-то не то, поэтому вот вам сомнительная шутка\nвпредь пользуйтесь встроенной клавиатурой\n'
    l = ['К девушке на дискотеке подходит парень и говорит: - Девушка, вашей маме зять не нужен?" Девушка издает звук утки. Давид испуганно отскакивает. Подходит второй парень со словами: - почему такая красивая девушка танцует одна? Девушка издает звук дельфина. паернь пугается, отходит, озираясь настороженно на странную девушку. Попытку предпринимает третий парень: - Девушка, позвольте угостить вас коктейлем? Девушка издает звук индюка (парень в страхе убегает) и звонит отцу: - Алле, пап, забери меня отсюда, вокруг одни животные, лезут и лезут!',
         '- Саша в костюме зайчика, Маша в костюме снежинки. О боже! Что это за зверь такой?!\n - Это Вася. Он в костюме первого января.',
         'Матч был настолько договорным, что его заверил нотариус',
         'В терминалах электронной очереди появилась кнопка "Мне только спросить".']
    msg += l[random.randint(0, len(l) - 1)]
    return msg