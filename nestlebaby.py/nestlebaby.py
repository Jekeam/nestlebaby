import telebot, requests, re


bot = telebot.TeleBot("447543291:AAH7U11Ijy-CJgKIRU_0uqFHFmEi4nYLKig")
href = "https://t.me/iv?url=https%3A%2F%2Fwww.nestlebaby.ru%2Farticles%2F{}-nedela-beremennosti&rhash=98467355fd32ee"


week_str = (
'первая',
'вторая',
'третья',
'четвертая',
'пятая',
'шестая',
'седьмая',
'восьмая',
'девятая',
'десятая',
'одиннадцатая',
'двенадцатая',
'тринадцатая',
'четырнадцатая',
'пятнадцатая',
'шестнадцатая',
'семнадцатая',
'восемнадцатая',
'девятнадцатая',
'двадцатая',
'двадцать первая',
'двадцать вторая',
'двадцать третья',
'двадцать четвертая',
'двадцать пятая',
'двадцать шестая',
'двадцать седьмая',
'двадцать восьмая',
'двадцать девятая',
'тридцатая',
'тридцать первая',
'тридцать вторая',
'тридцать третья',
'тридцать четвертая',
'тридцать пятая',
'тридцать шестая',
'тридцать седьмая',
'тридцать восьмая',
'тридцать девятая',
'сороковая')


def log(err):
    print(str(err))

#START
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет {}🖐\r\n".format(message.from_user.first_name)+
                          "Ответь мне пожалуйста, какая у тебя неделя беременности и " \
                          "я расскажу тебе о том, что сейчас происходит с твои младенцем 😉 \r\n\r\n" \
                          "Можешь написать например «35» или «тридцать пятая»")


#HELP
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Тут будет help")


#Любое текстовое сообщение
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    #Проверим это срок в цифрах или тексте
    msg = message.text

    #Ввели число?
    if msg == str(re.sub('\D','', msg )):
        if int(msg) < 41:
            url = href.format(msg)
            url = check_url(url)
            if url:
                bot.reply_to(message, url)
        else:
            not_week(message)
    else:
        #Ввели строкой и понимаем ли мы его?
        if week_str.count(msg) > 0:
            url = href.format(week_str.index(msg)+1)
            url = check_url(url)
            if url:
                bot.reply_to(message, url)
        else:
            bot.reply_to(message, 'Напишите какая у вас неделя, например: «40» или «Сороковая»\r\n'\
                                  'Или воспользуйте справкой /help')


def not_week(message):
    bot.reply_to(message, 'Возможно вы ошиблись, ведь всего 40 недель!')


def check_url(url):
    try:
        rs = requests.get(url)
        if rs.status_code == 200:
            return url
        else:
            log("Ошибка "+str(rs.status_code)+" в ответе "+url)
    except requests.exceptions.ConnectTimeout:
        log("Таймаут при подключении " + url)
    except requests.exceptions.ReadTimeout:
        log("Таймаут при чтении" + url)
    except requests.exceptions.ConnectionError:
        log("Ошибка подключения, похоже ДНС не найден" + url)
    except requests.exceptions.HTTPError as err:
        log('Ошибка '+url)
        log('Ответ : {content}'.format(content=err.response.content))


#LOOP
if __name__ == '__main__':
    bot.polling()