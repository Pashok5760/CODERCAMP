import telebot
from telebot import types

API_TOKEN = '1648129406:AAGwM1NZsKi-E1L2QzJiw0mJgYF-1sNeXRI'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}
user_chats = 0


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.languages = None
        self.sex = None

        keys = ['age', 'languages', 'git_acc', 'will_learn', 'project_um', 'want_admin']
        for key in keys:
            self.key = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, """\
Привет, я бот сообщества CODERCAMP, если хочешь зарегистрироваться ввели /reg

""")


@bot.message_handler(commands=['reg'])
def send_welcome1(message):
    try:
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, "Введите ваше имя или никнейм:  ")
        bot.register_next_step_handler(msg, process_name_step)


    except Exception as e:

        bot.reply_to(message, 'oooops')


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.send_message(chat_id, 'Введи свой возраст: ')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.send_message(chat_id, 'Возраст должен быть числом, введи его повторно: ')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Python', 'C++', 'C#', 'JAVA', 'jS', 'Ruby', 'GOLANG')
        msg = bot.send_message(chat_id, 'Пожалуйста выберите какой язык знаете или введите его (их): ',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, process_language_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_language_step(message):
    try:
        chat_id = message.chat.id
        language = message.text
        user = user_dict[chat_id]
        user.languages = language

        msg = bot.send_message(chat_id, 'Вставьте ссылку на ваш аккаунт гитхаб, если нет - напишите нет: ')
        bot.register_next_step_handler(msg, process_git_acc_step)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_git_acc_step(message):
    try:
        chat_id = message.chat.id
        git_acc1 = message.text
        user = user_dict[chat_id]
        user.git_acc = git_acc1
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Python', 'C++', 'C#', 'JAVA', 'jS', 'Ruby', 'GOLANG')
        msg = bot.send_message(chat_id, 'Какой язык программирования вы бы хотели выучить? ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_want_lang_step)

    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_want_lang_step(message):
    try:
        chat_id = message.chat.id
        will_learn = message.text
        user = user_dict[chat_id]
        user.will_learn = will_learn
        msg = bot.send_message(chat_id,
                               'Наш проект, похож на open source, в него могут делать вклад все участники, какой вы вклад можете сделать в наше сообщество')
        bot.register_next_step_handler(msg, process_project_um_step)
    except Exception as e:
        bot.reply_to(message, '12!')


def process_project_um_step(message):
    try:
        chat_id = message.chat.id
        project_um = message.text
        user = user_dict[chat_id]
        user.project_um = project_um
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add('Да', 'Нет')
        msg = bot.send_message(chat_id, 'Хотели бы вы стать администратором на проекте: ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_want_admin_step)
    except Exception as e:
        bot.reply_to(message, 'oops!')


def process_want_admin_step(message):
    try:
        global user_chats
        chat_id = message.chat.id
        want_adm = message.text
        name = message.from_user.username
        name1 = message.from_user.first_name
        user = user_dict[chat_id]
        user.want_admin = want_adm
        bot.send_message(chat_id, f'Ваше имя/(или никнейм) - {user.name} \n'
                         + f'Ваш возраст  -  {user.age} \n'
                         + f'Вы знаете язык(ки)  -  {user.languages} \n'
                         + f'Ваш аккаунт github  -  {user.git_acc} \n'
                         + f'Вы собираетесь выучить  -  {user.will_learn} \n'
                         + f'Вы можете сделать для нашего проекта  -  {user.project_um} \n'
                         + f'Ваш выбор стать администратором  -  {user.want_admin}')
        markup = types.InlineKeyboardMarkup()
        site_btn = types.InlineKeyboardButton(text='Принять', callback_data='yes')
        site_btn1 = types.InlineKeyboardButton(text='Отклонить', callback_data='no')
        markup.add(site_btn, site_btn1)
        user_chats = message.from_user.id

        bot.send_message(-1001423822051, 'Заявка от ' + name + ' (' + name1 + ') ' + '\n'
                         + f'Имя/(или никнейм) - {user.name} \n'
                         + f'Возраст  -  {user.age} \n'
                         + f'Знает язык(ки)  -  {user.languages} \n'
                         + f'Аккаунт github  -  {user.git_acc} \n'
                         + f'Собирается выучить  -  {user.will_learn} \n'
                         + f'Может сделать для нашего проекта  -  {user.project_um} \n'
                         + f'Выбор стать администратором  -  {user.want_admin}'
                         + f'ID человека = {user_chats}', reply_markup=markup)


    except Exception as e:
        bot.reply_to('oops!')


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, '(' + call.from_user.username +  ')' +  ' Принял')
        bot.send_message(call.message.chat.id, call.message.from_user.first_name + '(' + call.from_user.username + ')' + ' в нашу команду')
        print(user_chats)
        bot.send_message(user_chats, """
       Ты принят в наше сообщество👩🏾‍💻

        Ты сюда пришел, чтобы научиться чему-то новому или просто провести время с людьми с похожими интересами👨🏻‍💻

        У нас сейчас есть 3 ресурса:

        -💽Склад (канал с курсами и книгами) - https://t.me/joinchat/AzHrJONbFec1NGMy
        - 👨🏼‍💻Чат(общение программистов) - https://t.me/joinchat/XA_gQwveeAdhNDIy
        - 🎥Медиа-Канал(фильмы, сериалы, тиктоки по IT-тематике, в одном месте) - https://t.me/joinchat/-iEekHA18MdlZjky
        """)
    else:
        bot.send_message(call.message.chat.id,
                         call.from_user.first_name + '(' + call.from_user.username + ')' + ' Отклонил заявку' + '(' + call.from_user.username + ')')
        bot.send_message(user_chats, 'Извини, но тебя не приняли((')


# def process_sex_step(message):
#   try:
#        chat_id = message.chat.id
#        sex = message.text
#        user = user_dict[chat_id]
#
#        user.sex = sex
#
#        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
#    except Exception as e:
#        bot.reply_to(message, 'oooops')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.


# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!

bot.polling()
