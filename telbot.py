import re
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
from telebot.mastermind import get_response
import logging

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='viktorsbot.log')
app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()


    if text == "/start":
        # print the welcoming
        logging.info('Пользователь {} нажал кнопку /start'.format(update.message.chat.usrname))
        bot_welcome = """
       Привет {}. Я бот. Меня сделал виктор. Пока я ничего не умею.
       """.format(update.message.chat.first_name)
        # send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

        #Сделал коммент на основном компе
    else:
        try:
            # clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)
            # create the api link for the avatar based on

            # reply with a photo to the name the user sent,

            # bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
        except Exception:
            # if things went wrong
            bot.sendMessage(chat_id=chat_id, text="Возникли проблемы со связью, обратитесь в рабочие часы",
                            reply_to_message_id=msg_id)

    return 'ok'


# Запускаем этот метод один раз
@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():  # Отображает текст при переходе на домен.
    logging.info('Заходил на главную')
    return 'Это щчень главная страница'
@app.route('/page')
def page():
    return 'Ты на этой странице'

if __name__ == '__main__':
    logging.info('Запустилм скрипт')
    app.run(threaded=True)