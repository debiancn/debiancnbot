#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler
from telegram import Bot
import logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )


def tg_user_command(func):
    """
    Function decorator for every telegram command issued by user.
    """
    def func_wrapper(*args, **kwargs):
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
    pass

@tg_user_command
def unknown(bot: Bot, update):
    bot.send_message(
            chat_id=update.message.chat_id,
            text="Unknown Command.")


if __name__ == "__main__":
    token = None
    with open('token.txt', 'r') as tokenfile:
        token = tokenfile.read()
    if not token:
        raise Exception('ERR_EMPTY_TOKEN')
    updater = Updater(str(token))
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    
    updater.start_polling()
    updater.idle()
