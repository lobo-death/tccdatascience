#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import json

import telebot
from environs import Env
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# import environment variables
from scripts.classes.Choice import Choice
from scripts.classes.text_to_speak import TextToSpeak

env = Env()
env.read_env()

telegram_token = env("TELEGRAM_TOKEN_API")
download_path = env("DOWNLOAD_PATH")
bot_name = "Talho"
message_step_one = "O que vai querer?"
cart = []

# logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
log = logging.getLogger(__name__)

bot = telebot.TeleBot(telegram_token)


def main_option_keyboard_markup(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Aves", callback_data=json.dumps({"step": "main", "option": "AVES", "id": chat_id})),
        InlineKeyboardButton("Bovinos", callback_data=json.dumps({"step": "main", "option": "BOVINOS", "id": chat_id})),
        InlineKeyboardButton("Suínos", callback_data=json.dumps({"step": "main", "option": "SUINOS", "id": chat_id})),
        InlineKeyboardButton("Info", callback_data=json.dumps({"step": "main", "option": "INFO", "id": chat_id})),
        InlineKeyboardButton("Encerrar", callback_data=json.dumps({"step": "main", "option": "ENCERRAR", "id": chat_id}))
    )
    return markup


@bot.message_handler(commands=['start', 'help'])
def message_start(message):
    welcome(message)

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    welcome(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    choice = json.loads(call.data)
    if choice["step"] == "main":
        if choice["option"] == "AVES":
            bot.answer_callback_query(call.id, call.data)
            aves_menu(choice)
        elif choice["option"] == "BOVINOS":
            bovinos_menu(choice)
        elif choice["option"] == "SUINOS":
            suinos_menu(choice)
        elif choice["option"] == "SUGESTOES":
            sugestoes_menu(choice)
        elif choice["option"] == "INFO":
            info_menu(choice)
        else: #encerrar
            bot.answer_callback_query(call.id, call.data)
    elif choice["step"] == "aves":
        pass
    elif choice["step"] == "bovinos":
        pass
    elif choice["step"] == "suinos":
        pass
    else:
        print("no step configured ....")


@bot.message_handler(content_types=['document', 'audio', 'voice'])
def handle_docs_audio(message):
    try:
        log.warning(message)

        if (message.content_type == 'voice') or (message.content_type == 'audio'):
            log.warning(message.voice)
            file_id = message.voice.file_id
            file_info = bot.get_file(file_id)
            bot.send_message(message.chat.id, file_info)
            downloaded_file = bot.download_file(file_info.file_path)

            if not os.path.exists(download_path):
                os.mkdir(download_path)

            filename = "./" + download_path + "/audio_" + str(message.chat.id) + str(message.from_user.id) + ".ogg"
            with open(filename, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, "Você enviou um áudio ou voz")
    except Exception as inst:
        log.error("Error in handle_docs_audio {0}".format(inst.args))


def aves_menu(choice):
    log.info("MESSAGE: " + str(choice))
    bot.send_message(choice["id"], message_step_one, reply_markup=aves_option_menu_markup(choice["id"]))


def bovinos_menu(choice):
    log.info(choice)
    bot.send_message(choice["id"], message_step_one, reply_markup=bovinos_option_menu_markup(choice["id"]))


def suinos_menu(choice):
    log.info(choice)
    bot.send_message(choice["id"], message_step_one, reply_markup=suinos_option_menu_markup(choice["id"]))


def info_menu(choice):
    bot.send_message(choice["id"], "Horário de funcionamente: ")


def sugestoes_menu(choice):
    bot.send_message(choice["id"], "Escreva aqui suas sugestões!")


def fechar_menu(choice):
    bot.send_message(choice["id"], "Pedido enviado!")


def encerrar_menu(choice):
    bot.send_message(choice["id"], "Volte sempre!")

def quantidade(choice):
    bot.send_message(choice["id"], "Digite a quantidade que deseja:")

def aves_option_menu_markup(chat_id):
    print("markup aves")
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("1 - Peito .......... por R$ 16,99",
                             callback_data=json.dumps({"step": "aves", "option": "peito", "id": chat_id})),
        InlineKeyboardButton("2 - Tulipinha .... por R$ 22,99",
                             callback_data=json.dumps({"step": "aves", "option": "tulipinha", "id": chat_id})),
        InlineKeyboardButton("3 - Coxa .......... por R$ 19,99",
                             callback_data=json.dumps({"step": "aves", "option": "coxa", "id": chat_id})),
        InlineKeyboardButton("4 - Coração ..... por R$12,99",
                             callback_data=json.dumps({"step": "aves", "option": "coracao", "id": chat_id})),
        InlineKeyboardButton("5 - Voltar",
                             callback_data=json.dumps({"step": "aves", "option": "voltar", "id": chat_id}))
    )
    return markup


def meeat_option_menu_markup(chat_id, options, step):
    markup = InlineKeyboardMarkup(row_width=1)
    for option in options:
        step = {"step": step, "option": option['opcao'], "id": chat_id}
        if option["codigo"] == "-1":
            markup.add(
                InlineKeyboardButton(
                    "Voltar",
                    callback_data=json.dumps(step))
            )
        else:
            markup.add(
                InlineKeyboardButton(
                    "{0} - {1} .......... por R$ {2}".format(option["codigo"], option["descricao"], option["preco"]),
                    callback_data=json.dumps(step))
            )
    return markup

def bovinos_option_menu_markup(chat_id):
    print("bovinos menu ...")
    options = [
        {
            'codigo': "1",
            'descricao': 'Maminha Angus',
            'preco': 'R$45,99',
            'opcao': 'maminha'
        },
        {
            'codigo': "2",
            'descricao': 'Picanha Argentina Angus',
            'preco': 'R$79,99',
            'opcao': 'picánha'
        },
        {
            'codigo': "3",
            'descricao': 'Chorizo Angus',
            'preco': 'R$52,99',
            'opcao': 'chorizo'
        },
        {
            'codigo': "4",
            'descricao': 'Entrecôt Angus',
            'preco': 'R$59,99',
            'opcao': 'entrecot'
        },
        {
            'codigo': "-1",
            'descricao': 'Voltar',
            'preco': 'R$59,99',
            'opcao': 'entrecot'
        }
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    for option in options:
        step = {"step": "bovinos", "option": option['opcao'], "id": chat_id}
        if option["codigo"] == "-1":
            markup.add(
                InlineKeyboardButton(
                    "Voltar",
                    callback_data=json.dumps(step))
            )
        else:
            markup.add(
                InlineKeyboardButton("{0} - {1} .......... por R$ {2}".format(option["codigo"], option["descricao"], option["preco"]), callback_data=json.dumps(step))
            )
    return markup


def suinos_option_menu_markup(chat_id):
    markup = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("1 - Peito .......... por R$ 16,99",
                             callback_data=json.dumps({"step": "aves", "option": "peito", "id": chat_id})),
        InlineKeyboardButton("2 - Tulipinha .... por R$ 22,99",
                             callback_data=json.dumps({"step": "aves", "option": "tulipinha", "id": chat_id})),
        InlineKeyboardButton("3 - Coxa .......... por R$ 19,99",
                             callback_data=json.dumps({"step": "aves", "option": "coxa", "id": chat_id})),
        InlineKeyboardButton("4 - Coração ..... por R$12,99",
                             callback_data=json.dumps({"step": "aves", "option": "coracao", "id": chat_id})),
        InlineKeyboardButton("5 - Voltar",
                             callback_data=json.dumps({"step": "aves", "option": "voltar", "id": chat_id}))
    )
    return markup


def welcome(message):
    log.debug(message)
    chat_id = message.chat.id
    log.info(message.from_user)
    bot.send_chat_action(chat_id, "typing")
    user_message = "Olá {user_name}".format(user_name=message.from_user.first_name)
    bot.send_message(chat_id, user_message)
    welcome_message = "Meu nome é {bot}, serei seu assistente virtual." \
                      ";;O quê deseja pedir?".format(bot=bot_name)

    speak = TextToSpeak()
    speak.set_voice(speak.get_available_voice())
    converted_audio = speak.save_voice_to_file(welcome_message, "./audio.out", "./audio.ogg", "ogg")

    bot.send_chat_action(chat_id, "record_audio")
    bot.send_voice(chat_id, open(converted_audio, "rb"))
    bot.send_message(chat_id, welcome_message, reply_markup=main_option_keyboard_markup(chat_id))


bot.polling(none_stop=True, interval=0, timeout=60)
