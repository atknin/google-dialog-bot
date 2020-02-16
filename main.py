#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import apiai, json
def extract_chat_id(update):
    query = update.callback_query
    if query:
        chat_id = query.message.chat.id
    else:
        chat_id = update.message.chat_id
    return chat_id

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    chat_id = extract_chat_id(update)
    bot.send_message(chat_id=chat_id, text='Привет, я готов с тобой поболтать', parse_mode="HTML")


def nanolek_dialog(bot, update):
    if 'знаешь' in update.message.text or 'слышал' in update.message.text: bot.send_message(chat_id=update.message.chat_id, text='О да, я знаю эту компанию, нанолек защищает жизнь и здоровье людей')
    else: bot.send_message(chat_id=update.message.chat_id, text='Ух ты, ты тоже знаешь про нанолек, мне запретили говорить сегодня на эту тему, чтобы я ничего не сказал лишнего')


def echo(bot, update):
    if 'нанолек' in update.message.text or 'nanolek' in update.message.text: return nanolek_dialog(bot, update)
    request = apiai.ApiAI('0de460cffca14d36bf5b342de2b317a7').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response: bot.send_message(chat_id=update.message.chat_id, text=response)
    else: bot.send_message(chat_id=update.message.chat_id, text='Я Вас не очень сейчас понял!')

def help(bot, update):
    chat_id = extract_chat_id(update)
    bot.send_message(chat_id=chat_id, text='Тебе нужна помошь? – просто общайся со мной', parse_mode="HTML")


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token = "1047952823:AAGrA7imBWzpHWSI0o5LOml7Sp5HijkwVfs")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()