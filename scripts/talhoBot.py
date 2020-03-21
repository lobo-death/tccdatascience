#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

import telebot
from environs import Env
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# import environment variables
from scripts.classes.text_to_speak import TextToSpeak

env = Env()
env.read_env()

telegram_token = env("TELEGRAM_TOKEN_API")
download_path = env("DOWNLOAD_PATH")
bot_name = "Talho"

# logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
log = logging.getLogger(__name__)

bot = telebot.TeleBot(telegram_token)


def main_option_keyboard_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Aves", callback_data="AVES"),
        InlineKeyboardButton("Bovinos", callback_data="BOVINOS"),
        InlineKeyboardButton("Suínos", callback_data="SUINOS"),
        InlineKeyboardButton("Info", callback_data="INFO"),
        InlineKeyboardButton("Encerrar", callback_data="ENCERRAR")
    )
    return markup


@bot.message_handler(commands=['start', 'help'])
def message_start(message):
    welcome(message)

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    welcome(message)

#https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/inline_keyboard_example.py

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "AVES":
        bot.answer_callback_query(call.id, call.data)
        aves_menu(call)
    elif call.data == "BOVINOS":
        bot.answer_callback_query(call.id, call.data)
    else:
        bot.answer_callback_query(call.id, call.data)


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


def aves_menu(message):
    log.info(message)

def bovinos_menu(message):
    log.info(message)

def info_menu(message):
    log.info(message)



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
    bot.send_message(chat_id, welcome_message, reply_markup=main_option_keyboard_markup())


bot.polling(none_stop=True, interval=0, timeout=60)
