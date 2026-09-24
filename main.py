import telebot
from telebot import types

bot = telebot.TeleBot('8666423933:AAHOwpR41LGBJrDv9s35bg5PDbmXZDme2aI')

products_breakfast = ["Яйцо","Овсянка","Хлеб","Сыр","Ветчина","Творог","Йогурт","Молоко","Банан","Яблоко","Клубника","Авокадо","Сливочное масло","Мёд",
"Арахисовая паста","Орехи","Блины","Вафли","Круассан","Гречневая каша"]

calories_breakfast = [157,370,250,350,145,121,60,52,89,52,32,160,
748,304,588,600,230,290,406,110]

def select_age_group(age, age_group, message):
    file = open(str(message.from_user.id), 'w')
    file.write(str(age_group))
    file.close()
    file1 = open(f'{str(message.from_user.id)}age', 'w')
    file1.write(str(age))
    file1.close()
def create_keyboard(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Возраст')
    btn2 = types.KeyboardButton('Завтрак')
    btn3 = types.KeyboardButton('Обед')
    btn4 = types.KeyboardButton('Ужин')
    markup.add(btn2, btn3, btn4, btn1)
    bot.send_message(message.chat.id, 'Меню загружено✅', reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    print('В системе был зарегистрирован новый пользователь\n', "id:",
    message.from_user.id, "\nИме:", message.from_user.first_name, "\nФамилия:",
    message.from_user.last_name, "\nИме пользователя:", message.from_user.username)
    bot.send_message(message.chat.id, "Ваш возвраст:")

@bot.message_handler()
def age(message):
    for i in range(len(products_breakfast)):
        if message.text.lower() == products_breakfast[i].lower():
            print('"++')
            bot.send_message(message.chat.id, f'{calories_breakfast[i]}, {products_breakfast[i]}')
            return
    if message.text.lower() == 'возраст':
        file = open(str(message.from_user.id), "r")
        text = file.read()
        file.close()
        file1 = open(f'{str(message.from_user.id)}age', 'r')
        text1 = file1.read()
        file1.close()
        if int(text) == 1:
            group = '18-30'
        if int(text) == 2:
            group = '31-45'
        if int(text) == 3:
            group = '46-60'
        if int(text) == 4:
            group = '60+'
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Изменить возраст')
        btn2 = types.KeyboardButton('В меню')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, f'У вас указан возраст: {text1} лет\nВозврастная группа: {group} лет', reply_markup=markup)
        return
    if message.text.lower() == 'завтрак':
        markup = types.ReplyKeyboardMarkup()
        btn = types.KeyboardButton('В меню')
        markup.add(btn)
        for i in range(len(products_breakfast)):
            btn1 = types.KeyboardButton(products_breakfast[i])
            markup.add(btn1)
        bot.send_message(message.chat.id, 'Что вы ели?', reply_markup=markup)
        return
    if message.text.lower() == 'обед':
        bot.send_message(message.chat.id, 'Скоро будет...')
        return
    if message.text.lower() == 'ужин':
        bot.send_message(message.chat.id, 'Скоро будет...')
        return
    if message.text.lower() == 'изменить возраст':
        bot.send_message(message.chat.id, 'Ваш возраст:')
        return
    if message.text.lower() == 'в меню':
        create_keyboard(message)
        return

    if message.text.isdigit():
        age_int = int(message.text)
        if age_int < 18:
            bot.send_message(message.chat.id, 'Рано еще каллории считать')
        if 18 <= age_int <= 30:
            select_age_group(age=age_int, age_group=1, message=message)
            create_keyboard(message)
        if 31 <= age_int <= 45:
            select_age_group(age=age_int, age_group=2, message=message)
            create_keyboard(message)
        if 46 <= age_int <= 60:
            select_age_group(age=age_int, age_group=3, message=message)
            create_keyboard(message)
        if age_int > 60:
            select_age_group(age=age_int, age_group=4, message=message)
            create_keyboard(message)

    else:
        try:
            file = open(str(message.from_user.id), "r")
            file.close()
        except FileNotFoundError:
            bot.send_message(message.chat.id, 'Укажите возвраст в виде числа')
            return
        bot.send_message(message.chat.id, 'И что это такое?')

bot.polling(none_stop=True)