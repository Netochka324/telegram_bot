import sys
import requests
from telebot import types, TeleBot

token = '5875525598:AAFfWTn7YzahCIxWfcHuhl6DqoHFQJED_YA'
bot = TeleBot(token)


def create_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    drnk_btn = types.InlineKeyboardButton(text='Хочу пить!', callback_data='1')
    eat_btn = types.InlineKeyboardButton(text='Хочу есть!', callback_data='2')
    walk_btn = types.InlineKeyboardButton(text='Хочу гулять!', callback_data='3')
    sleep_btn = types.InlineKeyboardButton(text='Хочу спать!', callback_data='4')
    joke_btn = types.InlineKeyboardButton(text='Хочу анекдот!', callback_data='5')
    weather_btn = types.InlineKeyboardButton(text='Прогноз погоды!', callback_data='6')
    ex_btn = types.InlineKeyboardButton(text='Выход', callback_data='0')
    keyboard.add(drnk_btn, eat_btn, walk_btn, sleep_btn, joke_btn, weather_btn, ex_btn)
    return keyboard


# функция срабатывает на запуск бота
@bot.message_handler(commands=['start', 'старт', 'поехали'])
# чтобы бот стартовал по команде старт, нужен декоратор, кот перехватывает это сообщение
def start_bot(message):
    klava = create_keyboard()
    bot.send_message(
        message.chat.id,
        'Добрый день! Выберите, что хотите.',
        reply_markup=klava
    )


btn_spis = {
    '1': ["https://vash-ng.ru/wp-content/uploads/2018/07/Voda-dlya-bragi-scaled-1170x650.jpg", 'Вода'],
    '2': ["https://st3.depositphotos.com/1558912/34385/i/1600/depositphotos_343858742-stock-photo-"
          "grilled-salmon-fish-steak-with.jpg", 'Еда'],
    '3': ["https://www.rukita.co/stories/wp-content/uploads/2022/04/frank-busch-9UUdERAEghM-unsplash-"
          "1360x905.jpg", 'Прогулка'],
    '4': ["https://kartinkin.net/uploads/posts/2022-02/1646023023_31-kartinkin-net-p-kartinki-dlya-sna-32.jpg",
          'Сон']
}


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data in '1234':
            data = btn_spis[call.data]
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=data[0],
                caption=data[1],
                reply_markup=create_keyboard()
            )
        elif call.data == '5':
            URL = 'https://geek-jokes.sameerkumar.website/api?format=txt'
            sp = list(map(str, requests.get(URL)))
            bot.send_message(
                chat_id=call.message.chat.id,
                text=sp[0].lstrip("b'").replace("\\n", "").replace("\\", "")
            )

        elif call.data == '6':
            api_weather_key = '268493ae80d7db908fa00f4858ea2ba1'
            city = 'minsk'

            url_weather = f"https://api.openweathermap.org/data/2.5/find?q={city},BY&type=like&callback=test&appid={api_weather_key}&units=metric"

            b = requests.get(url_weather)
            data = b.text
            bot.send_message(
                chat_id=call.message.chat.id,
                text=data
            )

        elif call.data == '0':
            bot.send_message(
                chat_id=call.message.chat.id,
                text="Уже уходите?! До новых встреч."
            )
            bot.stop_bot()


bot.polling(non_stop=True)
