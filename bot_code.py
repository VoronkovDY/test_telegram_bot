from decouple import config
import telebot
import wikipedia
import re

bot_password = config('password', default='44')

bot = telebot.TeleBot(bot_password)

# устанавливаем русский язык в вики
wikipedia.set_lang("ru")

# получаем данные с вики и очищаем информацию
def get_wiki_data(s):
    try:
        wiki_all_text = wikipedia.page(s)
        wiki_text1 = wiki_all_text.content[:1000] # берем первую тысячу символов
        wiki_massive = wiki_text1.split('.') # делим по точкам
        wiki_massive = wiki_massive[:-1] # убираем инфу после последней точки
        wiki_text2 = '' # создаем переменную для итогового текста
        for x in wiki_massive: # чотаем строки где нет "равно", т.е кроме заголовков
            if not('==' in x):
                if(len((x.strip())) > 3): # если в строке больше 3 символов, добавляем ее к нашей переменной
                   wiki_text2 = wiki_text2 + x + '.' # возвращаем точки на место
            else:
                break
        # убираем разметку при помощи регулярных выражений
        wiki_text2 = re.sub('\([^()]*\)', '', wiki_text2)
        wiki_text2 = re.sub('\([^()]*\)', '', wiki_text2)
        wiki_text2 = re.sub('\{[^\{\}]*\}', '', wiki_text2)
        return wiki_text2
    # исключение, если вики вернуло ошибку
    except Exception as e:
        return 'В энциклопедии нет информации об этом'
# обрабатываем командлу start
@bot.message_handler(commands = ["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')

# получаем сообщение
@bot.message_handler(content_types = ["text"])
def handle_text(message):
    bot.send_message(message.chat.id, get_wiki_data
    (message.text))

# Запускаем бота
bot.infinity_polling()


