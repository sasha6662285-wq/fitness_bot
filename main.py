import telebot
from telebot import types
from datetime import datetime

bot = telebot.TeleBot('8204737238:AAGFkS94NVweezo8Ju8HO5-gEM33gFJ2mbA')

products_breakfast = ["Яйцо","Овсянка","Хлеб","Сыр","Ветчина","Творог","Йогурт","Молоко","Банан","Яблоко","Клубника","Авокадо","Сливочное масло","Мёд",
"Арахисовая паста","Орехи","Блины","Вафли","Круассан","Гречневая каша"]

calories_breakfast = [157,370,250,350,145,121,60,52,89,52,32,160,
748,304,588,600,230,290,406,110]

products_lunch = ["Куриная грудка","Куриное бедро","Говядина","Свинина","Рыба","Лосось","Рис варёный","Гречка варёная","Макароны варёные","Картофель варёный",
"Картофель жареный","Пюре картофельное","Суп куриный","Борщ","Котлета","Пельмени","Плов","Овощной салат","Огурец","Помидор","Брокколи","Фасоль варёная",
"Чечевица варёная","Хлеб","Сыр"]

calories_lunch = [165,209,187,242,120,208,130,110,157,87,192,110,35,50,250,250,180,50,15,18,35,127,116,250,350]

products_dinner = ["Куриная грудка","Индейка","Говядина","Рыба запечённая","Лосось","Яйцо","Творог","Рис варёный","Гречка варёная","Картофель варёный",
"Картофель запечённый","Макароны варёные","Овощной салат","Огурец","Помидор","Брокколи","Цветная капуста","Кабачок","Фасоль варёная","Чечевица варёная",
"Тушёные овощи","Сыр","Хлеб","Кефир 2,5%","Йогурт натуральный"]

calories_dinner = [165,135,187,130,208,157,121,130,110,87,93,157,50,15,18,35,25,24,127,116,65,350,250,53,60]

spisok = {}
user_food = {}
user_states = {}

def select_age_group(callories, message):
    file = open(f'{str(message.from_user.id)}limit', 'w')
    file.write(str(callories))
    file.close()
    file1 = open(f'{str(message.from_user.id)}all_limit', 'w')
    file1.write(str(callories))
    file1.close()

def create_keyboard(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Лимит')
    btn2 = types.KeyboardButton('Завтрак')
    btn3 = types.KeyboardButton('Обед')
    btn4 = types.KeyboardButton('Ужин')
    markup.add(btn2, btn3, btn4, btn1)
    bot.send_message(message.chat.id, 'Меню загружено✅', reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_states[user_id] = "waiting_limit"
    bot.send_message(message.chat.id, "Укажите лимит калорий в день:")

@bot.message_handler()
def call(message):
    time = datetime.now()
    print(time.time().hour)
    if time.time().hour <= 0:
        file1 = open(f'{str(message.from_user.id)}all_limit', 'r')
        text1 = file1.read()
        file1.close()
        file = open(f'{str(message.from_user.id)}limit', "w")
        file.write(text1)
        file.close()

    try:
        file1 = open(f'{str(message.from_user.id)}limit', 'r')
        text1 = file1.read()
        file1.close()
    except FileNotFoundError:
        user_id = message.from_user.id
        user_states[user_id] = "waiting_limit"

    if message.text.lower() == ('лимит'):
        file = open(f'{str(message.from_user.id)}limit', "r")
        text = file.read()
        file.close()
        file1 = open(f'{str(message.from_user.id)}all_limit', "r")
        text1 = file1.read()
        file1.close()
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Изменить лимит')
        btn2 = types.KeyboardButton('В меню')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, f'Лимит в день: {text1}\nСегодня осталось: {float(text):.1f} калорий', reply_markup=markup)
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
        user_states[user_id] = "breakfast"
        bot.send_message(message.chat.id, 'Что вы кушали?', reply_markup=markup)
        return

    if message.text.lower() == 'обед':
        markup = types.ReplyKeyboardMarkup()
        btn = types.KeyboardButton('В меню')
        btn2 = types.KeyboardButton('Готово')
        markup.add(btn, btn2)
        for i in range(len(products_lunch)):
            btn1 = types.KeyboardButton(products_lunch[i])
            markup.add(btn1)
        user_id = message.from_user.id
        user_states[user_id] = "lunch"
        bot.send_message(message.chat.id, 'Что вы кушали?', reply_markup=markup)
        return

    if message.text.lower() == 'ужин':
        markup = types.ReplyKeyboardMarkup()
        btn = types.KeyboardButton('В меню')
        btn2 = types.KeyboardButton('Готово')
        markup.add(btn, btn2)
        for i in range(len(products_dinner)):
            btn1 = types.KeyboardButton(products_dinner[i])
            markup.add(btn1)
        user_id = message.from_user.id
        user_states[user_id] = "dinner"
        bot.send_message(message.chat.id, 'Что вы кушали?', reply_markup=markup)
        return

    if message.text.lower() == 'изменить лимит':
        user_id = message.from_user.id
        user_states[user_id] = "waiting_limit"
        bot.send_message(message.chat.id, 'Укажите лимит калорий в день:')
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

        file = open(f"{str(message.from_user.id)}limit", "r")
        limit = float(file.read())
        print(limit)
        file.close()

        file = open(f"{str(message.from_user.id)}limit", "w")
        for item in spisok[user_id]:
            calories = item['calories']
            limit -= float(calories)
            print(calories)
        text = file.write(str(limit))
        file.close()
        bot.send_message(message.chat.id,f'Сохранено ✅')
        bot.send_message(message.chat.id,f'Всего: {total:.1f} ккал')

        file = open(f"{str(message.from_user.id)}limit", "r")
        limit = float(file.read())
        file.close()
        if float(limit) == 0:
            bot.send_message(message.chat.id, 'На сегодня лимит закончился')
        if float(limit) < 0:
            bot.send_message(message.chat.id, f'Вы превысили лимит на {-(limit)}')

        spisok.pop(user_id, None)
        user_food.pop(user_id, None)
        user_states[user_id] = 'menu'

    user_id = message.from_user.id
    if user_states.get(user_id) == "breakfast":
        for i in range(len(products_breakfast)):
            if message.text.lower() == products_breakfast[i].lower():
                user_id = message.from_user.id
                user_food[user_id] = i

                bot.send_message(message.chat.id, 'Сколько вы съели (в граммах)?')
                return

    if user_states.get(user_id) == "lunch":
        for i in range(len(products_lunch)):
            if message.text.lower() == products_lunch[i].lower():
                user_id = message.from_user.id
                user_food[user_id] = i

                bot.send_message(message.chat.id, 'Сколько вы съели (в граммах)?')
                return

    if user_states.get(user_id) == "dinner":
        for i in range(len(products_dinner)):
            if message.text.lower() == products_dinner[i].lower():
                user_id = message.from_user.id
                user_food[user_id] = i

                bot.send_message(message.chat.id, 'Сколько вы съели (в граммах)?')
                return

    if message.text.isdigit():
        user_id = message.from_user.id
        if user_states.get(user_id) == "waiting_limit":
            call_int = int(message.text)
            select_age_group(callories=call_int, message=message)
            user_id = message.from_user.id
            user_states[user_id] = "menu"
        else:
            user_id = message.from_user.id

            if user_id not in user_food:
                bot.send_message(message.chat.id, 'Сначала выберите продукт.')
                return

            if user_states.get(user_id) == "breakfast":
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

            if user_states.get(user_id) == "lunch":
                grams = int(message.text)
                i = user_food[user_id]

                calories = calories_lunch[i] * grams / 100

                if user_id not in spisok:
                    spisok[user_id] = []

                spisok[user_id].append({
                    'product': products_lunch[i],
                    'grams': grams,
                    'calories': calories
                })

            if user_states.get(user_id) == "dinner":
                grams = int(message.text)
                i = user_food[user_id]

                calories = calories_dinner[i] * grams / 100

                if user_id not in spisok:
                    spisok[user_id] = []

                spisok[user_id].append({
                    'product': products_dinner[i],
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
            bot.send_message(message.chat.id, 'Укажите лимит калорий в виде числа')
            return
        bot.send_message(message.chat.id, 'И что это такое?')

    user_id = message.from_user.id
    if user_states.get(user_id) == "menu":
        create_keyboard(message)
        return

bot.polling(none_stop=True)
