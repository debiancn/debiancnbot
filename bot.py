#!/usr/bin/env python3

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
import logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )

import requests
import bs4

def tg_user_command(func):
    """
    Function decorator for every telegram command issued by user.
    """
    def func_wrapper(*args, **kwargs):
        logging.info('message is '+str(args[1].message))
        result = func(*args, **kwargs)
        return result
    return func_wrapper

@tg_user_command
def start(bot: Bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello World!')

@tg_user_command
def hello(bot: Bot, update):
    bot.sendMessage(update.message.chat_id,
                    text='Hello {0}'.format(update.message.from_user.first_name))

@tg_user_command
def bug(bot, update):
    """
    Retrieve Debian BTS information according to bug number.

    Currently, we only send the bug title.
    """
    # make sure it is dedicated for self
    #TODO FIXME

    # make sure we have correct bug number
    try:
        bug_number = int(update.message.text.split(' ')[1])
        if bug_number < 1 or bug_number > 1500000:
            raise ValueError('ERR_BUG_NUMBER_INVALID')
    except ValueError:
        bot.send_message(
                update.message.chat_id,
                text='<b>ERR</b> invalid input.',
                parse_mode=telegram.ParseMode.HTML
                )
    r = requests.get('https://bugs.debian.org/{}'.format(str(bug_number)))
    html_title_text = bs4.BeautifulSoup(r.text).title.text
    bot.send_message(
            update.message.chat_id,
            text='<a href="https://bugs.debian.org/{0}">{1}</a>'.format(
                    str(bug_number),
                    html_title_text,
                    ),
            parse_mode=telegram.ParseMode.HTML,
            )

@tg_user_command
def unknown(bot: Bot, update):
    bot.send_message(
            chat_id=update.message.chat_id,
            text="Unknown Command.")


if __name__ == "__main__":
    token = None
    with open('token.txt', 'r') as tokenfile:
        token = tokenfile.readline().split('\n')[0]
        logging.info('token is {}.'.format(token))
    if not token:
        raise Exception('ERR_EMPTY_TOKEN')
    updater = Updater(token)
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('bug', bug))
    updater.dispatcher.add_handler(MessageHandler([Filters.command], unknown))
    
    updater.start_polling()
    updater.idle()
