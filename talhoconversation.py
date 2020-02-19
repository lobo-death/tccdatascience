#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using nested ConversationHandlers.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import logging

from telegram import ReplyKeyboardMarkup, ParseMode, ChatAction
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

token = '1066937626:AAG9CP9q9Poj9K0xF5oN5HzTwwEIsYqWQVs'
speech = ''

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY = range(2)

reply_keyboard = [['AVES', 'BOVINOS', 'SUINOS'],
                  ['INFO', 'SUGESTÕES'],
                  ['ENCERRAR']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def ordering_to_str(user_data):
    ordering = list()

    for key, value in user_data.items():
        ordering.append('{} - {}'.format(key.lower(), value))

    return "\n".join(ordering).join(['\n', '\n'])


nome = 'Chatoscana'

suinos = {
    '1': 'Lombinho',
    '2': 'Panceta',
    '3': 'Linguiça Toscana'
}

suinos_precos = {
    '1': '13,90',
    '2': '22,90',
    '3': '19,99'
}

info = "Informações de funcionamento?\n\nNosso estabelecimento funciona de segunda à sexta, das 08:00 às 19:00."

conversacao = [
    {
        'opcao': 'Consulta de preços',
        'resposta': [
            {
                'opcao': 'Suínos',
                'resposta':[
                    {
                        'opcao': 'Lombinho',
                        'resposta': 'R$13,99'},
                    {
                        'opcao': 'Panceta',
                        'resposta': 'R$22,99'},
                    {
                        'opcao': 'Linguiça Toscana',
                        'resposta': 'R$19,99'}
                ],
            },
            {
                'opcao':'Aves',
                'resposta':[
                    {
                        'opcao': 'Peito',
                        'resposta': 'R$16,99'},
                    {
                        'opcao': 'Tulipinha',
                        'resposta': 'R$22,99'},
                    {
                        'opcao': 'Coxa',
                        'resposta': 'R$19,99'},
                    {
                        'opcao': 'Coração',
                        'resposta': 'R$12,99'}
                ],
            },
            {
                'opcao': 'Bovinos',
                'resposta':[
                    {
                        'opcao': 'Maminha Angus',
                        'resposta': 'R$45,99'},
                    {
                        'opcao': 'Picanha Argentina Angus',
                        'resposta': 'R$79,99'},
                    {
                        'opcao': 'Chorizo Angus',
                        'resposta': 'R$52,99'},
                    {
                        'opcao': 'Entrecôt Angus',
                        'resposta': 'R$59,99'}
                ]
            }
        ]
    },
    {
        'opcao': 'Encomenda',
        'resposta': 'Serviço temporariamente indisponível.'
    },
    {
        'opcao': 'Calculadora de Churrasco',
        'resposta': 'Serviço temporariamente indisponível.'
    },
    {
        'opcao': 'Dica do chefe',
        'resposta': 'Serviço temporariamente indisponível.'
    },
    {
        'opcao': 'Informações Sobre o Açougue',
        'resposta': 'Nosso estabelecimento funciona de segunda à sexta, das 08:00 às 19:00.'
    },
    {
        'opcao': 'Sugestões',
        'resposta': 'Nos ajude a melhorar! Digite sua sugestão para nosso estabelecimento.'
    },
    {
        'opcao': 'Outros',
        'resposta':'Digite um telefone para que nosso CEO César entre em contato para te ajudar.'
    }
]


def lista_de_opcoes(nome, conversation_level):
    print('{}: Digite o número do item de seu interesse ;)'.format(nome))
    menu = []
    for idx, opcao in enumerate(conversation_level):
        menu.append('\t{} - {}'.format(idx+1, opcao['opcao']))
    return menu


#def introducao_chatbot(nome):
#    return ''.format(a=nome)
def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Carnes de {}? Quer dar uma olhada nas nossas promoções?'.format(text.lower())
    )

    return TYPING_REPLY

def info_sugest(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Você quer fazer sugestões? Olha lá hein o que vai escrever!!'
    )

    return TYPING_REPLY


def info_choice(update, context):
    #update.message.reply_text("Informações de funcionamento?\n\nNosso estabelecimento funciona de segunda à sexta, das 08:00 às 19:00.", reply_markup=markup)
    update.message.reply_text(info)

    return CHOOSING

def resposta_chatbot(user_input, opcao):
    print(opcao)
    if user_input in opcao:
        return respostas[user_input] + '\n{}: Podemos te ajudar com mais alguma opção? Se sim, digite o número desejado.'.format(nome)
    else:
        return 'Desculpe, não entendi. Você poderia digitar a opção novamente?'.format(nome)

def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    if category.lower() == 'aves' and text.lower() in ['y', 'yes', 's', 'si', 'sim', 'quero']:
        update.message.reply_text(
            "1 - Peito .......... por R$ 16,99 ;\n"
            "2 - Tulipinha .... por R$ 22,99 ;\n"
            "3 - Coxa .......... por R$ 19,99 ;\n"
            "4 - Coração ..... por R$12,99 ."
        )
        update.message.reply_text("E vai levar o que? E vai querer quanto?")
    elif category.lower() == 'bovinos' and text.lower() in ['y', 'yes', 's', 'si', 'sim', 'quero']:
        update.message.reply_text("Para hoje vamos ter:\n\n"
            "1 - Maminha Angus ................por R$ 45,99 ;\n"
            "2 - Picanha Argentina Angus ..por R$ 79,99 ;\n"
            "3 - Chorizo Angus ...................por R$ 52,99 ;\n"
            "4 - Entrecôt Angus ..................por R$ 59,99 ."
        )
        update.message.reply_text("E vai levar o que? E vai querer quanto?")
    elif category.lower() == 'suinos' and text.lower() in ['y', 'yes', 's', 'si', 'sim', 'quero']:

        update.message.reply_text(
            "1 - Lombinho ................. por R$ 13,99 ;\n"
            "2 - Panceta .................... por R$ 22,99 ;\n"
            "3 - Linguiça Toscana ..... por R$19,99 ."
        )
        user_input = input().lower()
        resposta_chatbot(user_input, suinos_precos)
        update.message.reply_text("E vai levar o que? E vai querer quanto?")
    else:
        update.message.reply_text("Ok, quer escolher outro tipo de carne?")

    #update.message.reply_text("Pronto! Só vai querer carne de {} para hoje? Você deseja mais alguma coisa?.".format(ordering_to_str(user_data)), reply_markup=markup)

    return CHOOSING

def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("Aqui está o resumo do seu pedido:"
                              "{}"
                              "Muito obrigado e volte sempre!".format(ordering_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text("Meu nome é {a}. Serei o seu assistente virtual hoje. Ainda estou aprendendo, mas vou me esforçar para te ajudar.\n\nO que vai ser para hoje?".format(a=nome), reply_markup=markup)

    return CHOOSING


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('Ops! Eu acho que eu me perdi...')


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

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

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()