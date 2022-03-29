""" Данная программа - бот для telegram который может добавлять задачу набранную с консоли на дату "сегодня", "завтра"
и "остальное". Так же есть возможность добавить случайную задачу на дату "сегодня". Так же есть возможность вывода
задач по любой из данных дат.
-----------------------------------------------------------

(C) 2022 Sergey Matofonov, Russia, Sevastopol
Released under GNU Public License (GPL)
email: phaeton.kz@gmail.com
-----------------------------------------------------------
"""
import telebot
from telebot import types
import random

token = ''  # Здесь нужно указать свой токен

bot = telebot.TeleBot(token)

HELP = """
HELP - вывести список доступных команд.
ADD - добавить задачу в список (название задачи запрашиваем у пользователя).
RANDOM - добавить случайную задачу на дату "Сегодня".
SHOW - напечатать все добавленные задачи.
"""
# глобальная переменная для выбора режима показа меню Добавление или показ задач
mode = ''
# Список случайных задач
RANDOM_TASK = ['Записаться на курс в Нетологию.', 'Написать письмо Гвидо.', 'Покормить кошку.', 'Помыть машину.']

# Пустой слоаврь куда будут добавляться даты в виде ключей и задачи в виде значений
tasks = {}


def add_todo(date, task):
    """Функция добавляет задачу к определенной дате"""
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = [task]


@bot.message_handler(commands=['start'])
def start(message, greeting=True):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_help = types.KeyboardButton('❓ HELP')
    btn_add = types.KeyboardButton('✔ ADD')
    btn_random = types.KeyboardButton('➕ RANDOM')
    btn_show = types.KeyboardButton('👀 SHOW')
    markup.add(btn_add, btn_random, btn_show, btn_help)
    if greeting:  # greeting - флаг проверки, если пользователь впервые, -  поздороваться
        bot.send_message(message.chat.id, text='Привет, {0.first_name}! Я бот планирования задач. Выбери команду '
                                               'или нажми на кнопку ПОМОЩЬ, для получения списка команд'
                         .format(message.from_user), reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                         text='{0.first_name}! Выбери команду или нажми на кнопку ПОМОЩЬ, для получения'
                              ' списка команд'
                         .format(message.from_user), reply_markup=markup)


# @bot.message_handler(content_types=['text'])
def second_menu(message):
    # Выводится внутреннее меню с возможностью выбора доступной даты для задачи
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Сегодня')
    btn2 = types.KeyboardButton('Завтра')
    btn3 = types.KeyboardButton('Остальное')
    back = types.KeyboardButton('НАЗАД')
    markup.add(btn1, btn2, btn3)
    markup.add(back)
    bot.send_message(message.chat.id, text='На какой день?', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    # Выполнение различных действий в зависимости от выбранного пункта меню
    global mode
    if message.text == '❓ HELP':
        bot.send_message(message.chat.id, HELP)
    elif message.text == '➕ RANDOM':
        random_add(message)
    elif message.text == '👀 SHOW':
        mode = 'show'
        second_menu(message)
    elif message.text == '✔ ADD':
        mode = 'add'
        second_menu(message)
    elif (message.text == 'Сегодня') and (mode == 'add'):
        command_add(message)
    elif (message.text == 'Сегодня') and (mode == 'show'):
        day_of_list = 'сегодня'
        show(message, day_of_list)
    elif (message.text == 'Завтра') and (mode == 'add'):
        command_add(message)
    elif (message.text == 'Завтра') and (mode == 'show'):
        day_of_list = 'завтра'
        show(message, day_of_list)
    elif (message.text == 'Остальное') and (mode == 'add'):
        command_add(message)
    elif (message.text == 'Остальное') and (mode == 'show'):
        day_of_list = 'остальное'
        show(message, day_of_list)
    elif message.text == 'НАЗАД':
        bot.send_message(message.chat.id, text='Вы вернулись в главное меню.')
        greeting = False  # Ставим флаг приветствие в False, чтобы не здороваться еще раз в главном меню.
        start(message, greeting)


def command_add(message):
    # Выбираем дату
    day = message.text.lower()
    msg = bot.send_message(message.chat.id, f'Введите задачу на день {day}: ')
    bot.register_next_step_handler(msg, command_add_task, day)


def command_add_task(message, date):
    #  Добавляем задачу и сразу же проверяем, если задача менее 3х символов, то задачу не добавляем
    if len(message.text) >= 3:
        add_todo( date, message.text)
        text = 'Задача ' + message.text + ' добавлена на дату ' + date
    else:
        bot.send_message(message.chat.id, text='Задача менее 3-х символов. Выберите дату и повторите ввод')
        return
    bot.send_message(message.chat.id, text)


def random_add(message):
    # Добавление случайной задачи из списка на дату "Сегодня"
    date = 'сегодня'
    task = random.choice(RANDOM_TASK)
    add_todo(date, task)
    text = 'Задача ' + task + ' добавлена на дату ' + date
    bot.send_message(message.chat.id, text)


def show(message, date):
    # Вывод всех задач на выбранную дату
    if date in tasks:
        text = date.upper() + '\n'
        for task in tasks[date]:
            text = text + '[] ' + task + '\n'
    else:
        text = 'Задач на эту дату нет'
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':  # бесконечный цикл
    bot.polling(none_stop=True)
