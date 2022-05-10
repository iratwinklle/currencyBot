import telebot
from config import keys, TOKEN
from extensions import ConversionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message):
    mess = f'Привет, {message.from_user.first_name} {message.from_user.last_name}. \n ' \
           f'Это бот для получения информации о валютах. \n ' \
           f'Для того, чтобы начать работу с ботом Вам необходимо отправить сообщение в виде: \n' \
           f' <b>&ltимя валюты, цену которой Вы хотите узнать&gt ' \
           f'&ltимя валюты, в которой надо узнать цену первой валюты&gt' \
           f' &ltколичество первой валюты&gt.</b> \n \n' \
           f'<u>Например:</u> доллар евро 1\n \n ' \
           f'<b>Команды, с которыми можно обратиться к боту:</b> \n' \
           f'/start - инструкции по применению бота\n' \
           f'/help - инструкции по применению бота\n' \
           f'/values - увидеть список доступных валют'

    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['values'])
def help(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConversionException('Не верное количество параметров')
        base, quote, amount = values
        total_quote = CryptoConverter.get_price(base, quote, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(massage, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {keys[base]} - {total_quote} {keys[quote]}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)