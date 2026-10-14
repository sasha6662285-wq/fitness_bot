import telebot
from telebot import types

bot = telebot.TeleBot('8204737238:AAGFkS94NVweezo8Ju8HO5-gEM33gFJ2mbA')

products_breakfast = ["Яйцо","Овсянка","Хлеб","Сыр","Ветчина","Творог","Йогурт","Молоко","Банан","Яблоко","Клубника","Авокадо","Сливочное масло","Мёд",
"Арахисовая паста","Орехи","Блины","Вафли","Круассан","Гречневая каша"]

calories_breakfast = [157,370,250,350,145,121,60,52,89,52,32,160,
748,304,588,600,230,290,406,110]

spisok = {}
user_food = {}
user_states = {}


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
    user_id = message.from_user.id
    user_states[user_id] = "waiting_age"
    print('В системе был зарегистрирован новый пользователь\n', "id:",
    message.from_user.id, "\nИме:", message.from_user.first_name, "\nФамилия:",
    message.from_user.last_name, "\nИме пользователя:", message.from_user.username)
    bot.send_message(message.chat.id, "Ваш возвраст:")

@bot.message_handler()
def age(message):
    try:
        file1 = open(f'{str(message.from_user.id)}age', 'r')
        text1 = file1.read()
        file1.close()
    except FileNotFoundError:
        age_select = True

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
        btn2 = types.KeyboardButton('Готово')
        markup.add(btn, btn2)
        for i in range(len(products_breakfast)):
            btn1 = types.KeyboardButton(products_breakfast[i])
            markup.add(btn1)
        user_id = message.from_user.id
        user_states[user_id] = "spisok"
        bot.send_message(message.chat.id, 'Что вы ели?', reply_markup=markup)
        return

    if message.text.lower() == 'обед':
        bot.send_message(message.chat.id, 'Скоро будет...')
        return

    if message.text.lower() == 'ужин':
        bot.send_message(message.chat.id, 'Скоро будет...')
        return

    if message.text.lower() == 'изменить возраст':
        user_id = message.from_user.id
        user_states[user_id] = "waiting_age"
        bot.send_message(message.chat.id, 'Ваш возраст:')
        return

    if message.text.lower() == 'в меню':
        user_id = message.from_user.id
        user_states[user_id] = "menu"

    if message.text.lower() == 'готово':
        if spisok == {}:
            bot.send_message(message.chat.id, 'В списке ничего нет')
            return
        user_id = message.from_user.id
        foods = spisok.get(user_id, [])

        total = sum(item['calories'] for item in foods)

        file = open(f"{str(message.from_user.id)}gramms", "w")
        all_calories = 0
        for item in spisok[user_id]:
            calories = item['calories']
            all_calories += calories
            print(calories)
        text = file.write(str(all_calories))
        file.close()
        bot.send_message(message.chat.id,f'Сохранено ✅')
        bot.send_message(message.chat.id,f'Всего: {total:.1f} ккал')

        spisok.pop(user_id, None)
        user_food.pop(user_id, None)
        return


    for i in range(len(products_breakfast)):
        if message.text.lower() == products_breakfast[i].lower():
            user_id = message.from_user.id
            user_food[user_id] = i

            bot.send_message(message.chat.id, 'Сколько вы съели (в граммах)?')
            return

    if message.text.isdigit():
        user_id = message.from_user.id
        if user_states.get(user_id) == "waiting_age":
            age_int = int(message.text)
            if age_int < 18:
                bot.send_message(message.chat.id, 'Рано еще каллории считать')
            if 18 <= age_int <= 30:
                select_age_group(age=age_int, age_group=1, message=message)
                user_id = message.from_user.id
                user_states[user_id] = "menu"
            if 31 <= age_int <= 45:
                select_age_group(age=age_int, age_group=2, message=message)
                user_id = message.from_user.id
                user_states[user_id] = "menu"
            if 46 <= age_int <= 60:
                select_age_group(age=age_int, age_group=3, message=message)
                user_id = message.from_user.id
                user_states[user_id] = "menu"
            if age_int > 60:
                select_age_group(age=age_int, age_group=4, message=message)
                user_id = message.from_user.id
                user_states[user_id] = "menu"
        else:
            user_id = message.from_user.id

            if user_id not in user_food:
                bot.send_message(
                    message.chat.id,
                    'Сначала выберите продукт.'
                )
                return

            grams = int(message.text)
            i = user_food[user_id]

            calories = calories_breakfast[i] * grams / 100

            if user_id not in spisok:
                spisok[user_id] = []

            spisok[user_id].append({
                'product': products_breakfast[i],
                'grams': grams,
                'calories': calories
            })

            user_food.pop(user_id)

            total = sum(
                item['calories'] for item in spisok[user_id]
            )
            all_product = ''
            for item in spisok[user_id]:
                product = item['product']
                if all_product == '':
                    all_product = all_product + product
                else:
                    all_product = f'{all_product}, ' + product
            bot.send_message(message.chat.id, 'Добавлено ✅')
            bot.send_message(message.chat.id,f'Продукты: {all_product}\n')
            return

    user_id = message.from_user.id
    if user_states.get(user_id) == "menu":
        create_keyboard(message)
        return

    else:
        try:
            file = open(str(message.from_user.id), "r")
            file.close()
        except FileNotFoundError:
            bot.send_message(message.chat.id, 'Укажите возвраст в виде числа')
            return
        bot.send_message(message.chat.id, 'И что это такое?')

    user_id = message.from_user.id
    if user_states.get(user_id) == "menu":
        create_keyboard(message)
        return

bot.polling(none_stop=True)
