#!/usr/bin/env python
# -*- coding: utf-8 -*-

from environs import Env
import logging
from telegram import ReplyKeyboardMarkup, ParseMode, ChatAction
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

#read environments variables
env = Env()
env.read_env()

telegramToken = env("TELEGRAM_TOKEN_API")

#config logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
log = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY = range(2)
botName = "Talho"

reply_keyboard = [['AVES', 'BOVINOS', 'SUINOS'],
                  ['INFO', 'SUGESTÕES'],
                  ['ENCERRAR']]

markup = InlineKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(update, context):
    update.message.reply_text(
        "Meu nome é {a}. Serei o seu assistente virtual hoje. Ainda estou aprendendo, "
        "mas vou me esforçar para te ajudar.\n\nO que vai ser para hoje?".format(a=botName),
        reply_markup=markup)

    return CHOOSING

def info_choice(update, context):
    #update.message.reply_text("Informações de funcionamento?\n\nNosso estabelecimento funciona de segunda à sexta, das 08:00 às 19:00.", reply_markup=markup)
    info = "Informações de funcionamento?\n\nNosso estabelecimento funciona de segunda à sexta, das 08:00 às 19:00."
    update.message.reply_text(info)

    return CHOOSING

def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Carnes de {}? Quer dar uma olhada nas nossas promoções?'.format(text.lower())
    )

    return TYPING_REPLY

def received_information(update, context):
    user_data = context.user_data
    log.info(user_data)
    text = update.message.text
    log.info(text)

def info_sugest(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Você quer fazer sugestões? Olha lá hein o que vai escrever!!'
    )

    return TYPING_REPLY

def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("Volte sempre")

    user_data.clear()
    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    log.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    log.info("Initialization Talho bot with token {0}...".format(telegramToken))

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(telegramToken, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(AVES|BOVINOS|SUINOS)$'),
                                      regular_choice),
                       MessageHandler(Filters.regex('^INFO$'),
                                      info_choice),
                       MessageHandler(Filters.regex('^SUGESTÕES$'),
                                      info_sugest)
                       ],
            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information)
                           ]
        },
        fallbacks=[MessageHandler(Filters.regex('^ENCERRAR$'), done)]
    )

    # on different commands - answer in Telegram
    # dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)

    # log errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

    return


if __name__ == '__main__':
    main()