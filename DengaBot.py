import telebot
from config import keys, TOKEN
from extensions import ConvertionException, WrongConvert

bot =telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    text = (f'Здравствуй {message.chat.username}. '
            'Этот бот поможет вам в конвертации валют. '
            'Для просмотра инструкции по использованию введите команду /help\n'
            'Для просмотра доступных валют введите команду /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = ('Что бы начать работу, введите команду боту следующим образом:\n<имя изначальной валюты> '
            '<в какую валюту перевести> '
            '<количество изначально переводимой валюты> \n'
            'Пример: Рубль Доллар 100 = сколько долларов в 100 рублях')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) != 3:
        bot.reply_to(message, 'Слишком много или мало параметров. Введите команду /values для правильного ввода.')
        return

    quote, base, amount = values

    try:
        total_base = WrongConvert.convert(quote, base, amount)
        text = f'Цена {amount} {quote} в {base} равно {total_base:.2f}'
    except ConvertionException as e:
        text = f'Ошибка конвертации: {e}'
    except Exception as e:
        text = f'Неизвестная ошибка: {e}'

    bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)