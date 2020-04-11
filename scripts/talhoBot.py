#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import json

import telebot
from environs import Env
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types

import boto3
from scripts.classes.options_menu import options_bovino, options_aves, options_suinos

# import environment variables
from scripts.models.ProductRepository import ProductRepository
from scripts.models.PurchaseRepository import PurchaseRepository
from scripts.models.UserRepository import UserRepository


env = Env()
env.read_env()

telegram_token = env("TELEGRAM_TOKEN_API")
download_path = env("DOWNLOAD_PATH")
polly_access_key = env("POLLY_ACCESS_KEY")
polly_secret_key = env("POLLY_SECRET_KEY")
bot_name = "Talho"
message_step_one = "O que vai querer? (Clique na opção)"
cart = []
current_interaction = None

polly_client = boto3.Session(
    aws_access_key_id=polly_access_key,
    aws_secret_access_key=polly_secret_key,
    region_name='us-west-2').client('polly')


# logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
log = logging.getLogger(__name__)

bot = telebot.TeleBot(telegram_token)

user_repository = UserRepository()
purchase_repository = PurchaseRepository()
product_repository = ProductRepository()

current_user = None


def main_option_keyboard_markup(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Aves", callback_data=json.dumps({"step": "main", "option": "AVES", "id": chat_id})),
        InlineKeyboardButton("Bovinos", callback_data=json.dumps({"step": "main", "option": "BOVINOS", "id": chat_id})),
        InlineKeyboardButton("Suínos", callback_data=json.dumps({"step": "main", "option": "SUINOS", "id": chat_id})),
        InlineKeyboardButton("Sugestões",
                             callback_data=json.dumps({"step": "main", "option": "SUGESTOES", "id": chat_id})),
        InlineKeyboardButton("Info", callback_data=json.dumps({"step": "main", "option": "INFO", "id": chat_id})),
        InlineKeyboardButton("Encerrar",
                             callback_data=json.dumps({"step": "main", "option": "ENCERRAR", "id": chat_id}))
    )
    return markup


def finalize_or_continue_keyboard_markup(choice):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Continuar comprando",
                             callback_data=json.dumps({"step": "main", "option": "INITIAL", "id": choice["id"]})),
        InlineKeyboardButton("Finalizar",
                             callback_data=json.dumps({"step": "main", "option": "FINALIZE", "id": choice["id"]}))
    )
    return markup


@bot.message_handler(commands=['start', 'help'])
def message_start(message):
    welcome(message)


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    if current_interaction is None:
        welcome(message)
    else:
        log.warning("repass to handle for current interaction {0} ...".format(current_interaction))
        interaction_handle(message, current_interaction)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    choice = json.loads(call.data)
    global current_interaction
    current_interaction = choice
    interaction_handle(call, choice)


def interaction_handle(call, choice):
    global current_interaction
    if choice["step"] == "main":
        if choice["option"] == "AVES":
            # bot.answer_callback_query(call.id, call.data)
            create_submenu(message_step_one, choice, options_aves, "aves")
        elif choice["option"] == "BOVINOS":
            create_submenu(message_step_one, choice, options_bovino, "bovinos")
        elif choice["option"] == "SUINOS":
            create_submenu(message_step_one, choice, options_suinos, "suinos")
        elif choice["option"] == "SUGESTOES":
            sugestoes_menu(choice)
        elif choice["option"] == "INFO":
            info_menu(choice)
        elif choice["option"] == "INITIAL":
            main_menu(choice)
        elif choice["option"] == "FINALIZE":
            fechar_menu(choice)
        else:  # encerrar
            encerrar_menu(choice)
    elif choice["step"] in ("aves", "bovinos", "suinos"):
        if choice["option"] == "INITIAL":
            message = call.json
            log.warning(message["text"])
        elif choice["option"] == "QTDE":
            log.info(choice)
            log.info("Qtde digitada: {0} - ".format(call.json["text"]))
            # save qtde and selected_product in cart

            # return to main menu or finalize
            bot.send_message(choice["id"], "Produto adicionado!",
                             reply_markup=finalize_or_continue_keyboard_markup(choice))
        elif choice["option"] == "-1":
            current_interaction = {"step": "main", "option": "main", "id": choice["id"],
                                   "selected_product:": choice["option"]}
            main_menu(choice)

        else:  # handle for submenu
            log.error(choice)
            current_interaction = {"step": choice["step"], "option": "QTDE", "id": choice["id"],
                                   "selected_product:": choice["option"]}
            markup = types.ForceReply(selective=False)
            bot.send_message(choice["id"], "Digite a quantidade em kg:", reply_markup=markup)

    else:
        print("no step configured ....")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")


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


def create_submenu(message, choice, options, step_name):
    log.info("creating submenu: " + str(choice))
    bot.send_message(choice["id"],
                     message,
                     reply_markup=create_option_menu_markup(choice["id"], options, step_name))


def info_menu(choice):
    global current_interaction
    bot.send_message(choice["id"], "Horário de funcionamento: Seg a Sex. 8:00 às 18:00 ")

    ssml = """
            <speak>
                <p>Horário de funcionamento: Segunda a Sexta das 8:00 às 18:00 </p>                         
             </speak> """

    response = polly_client.synthesize_speech(VoiceId='Vitoria',
                                              OutputFormat='ogg_vorbis',
                                              LanguageCode='pt-BR',
                                              TextType='ssml',
                                              Text=ssml)

    audio = response['AudioStream'].read()
    bot.send_chat_action(choice["id"], "record_audio")
    bot.send_voice(choice["id"], audio)
    current_interaction = None


def sugestoes_menu(choice):
    global current_interaction
    bot.send_message(choice["id"], "Escreva aqui suas sugestões!")


    ssml = """
                <speak>
                    <p>Escreva aqui suas sugestões</p>                         
                 </speak> """

    response = polly_client.synthesize_speech(VoiceId='Vitoria',
                                              OutputFormat='ogg_vorbis',
                                              LanguageCode='pt-BR',
                                              TextType='ssml',
                                              Text=ssml)

    audio = response['AudioStream'].read()
    bot.send_chat_action(choice["id"], "record_audio")
    bot.send_voice(choice["id"], audio)
    current_interaction = None


def fechar_menu(choice):
    global current_interaction
    bot.send_message(choice["id"], "Pedido confirmado, ele será enviado assim que for processado.\n Volte sempre!")


    ssml = """
                <speak>
                    <p>Pedido confirmado, ele será enviado assim que for processado.</p>      
                    <p>Obrigado pela preferência. Volte sempre!</p>                       
                 </speak> """

    response = polly_client.synthesize_speech(VoiceId='Vitoria',
                                              OutputFormat='ogg_vorbis',
                                              LanguageCode='pt-BR',
                                              TextType='ssml',
                                              Text=ssml)

    audio = response['AudioStream'].read()
    bot.send_chat_action(choice["id"], "record_audio")
    bot.send_voice(choice["id"], audio)
    current_interaction = None
    cart = []
    choice = None


def encerrar_menu(choice):
    global current_interaction
    bot.send_message(choice["id"], "Volte sempre!")


    ssml = """
                <speak>
                    <p>Volte sempre!</p>                         
                 </speak> """

    response = polly_client.synthesize_speech(VoiceId='Vitoria',
                                              OutputFormat='ogg_vorbis',
                                              LanguageCode='pt-BR',
                                              TextType='ssml',
                                              Text=ssml)

    audio = response['AudioStream'].read()
    bot.send_chat_action(choice["id"], "record_audio")
    bot.send_voice(choice["id"], audio)
    current_interaction = None
    cart = []


def create_option_menu_markup(chat_id, options, step_name):
    log.info("creating {0} menu markup ...".format(step_name))
    global current_interaction

    markup = InlineKeyboardMarkup(row_width=1)
    for option in options:
        if option["type"] == "instructions":
            bot.send_message(chat_id, option["text"])

            response = polly_client.synthesize_speech(VoiceId='Vitoria',
                                                      OutputFormat='ogg_vorbis',
                                                      LanguageCode='pt-BR',
                                                      TextType='ssml',
                                                      Text=option['ssml'])

            audio = response['AudioStream'].read()
            bot.send_chat_action(chat_id, "record_audio")
            bot.send_voice(chat_id, audio)
        elif option["type"] in ("item", "action"):
            step = {"step": step_name, "option": option['code'], "id": chat_id}
            if option["code"] == "-1":
                markup.add(
                    InlineKeyboardButton(
                        option["description"],
                        callback_data=json.dumps(step))
                )
            else:
                markup.add(
                    InlineKeyboardButton(
                        "{0} - {1} - R$ {2}".format(option["code"], option["description"], option["price"]),
                        callback_data=json.dumps(step))
                )
    current_interaction = {"step": step_name, "option": "INITIAL", "id": chat_id}
    return markup


def welcome(message):
    log.debug(message)
    chat_id = message.chat.id
    log.info(message.from_user)
    bot.send_chat_action(chat_id, "typing")
    user_id = message.from_user.id

    try:
        current_user = UserRepository.find_by_id(user_id)


        response = polly_client.synthesize_speech(VoiceId='Vitoria',
                                                  OutputFormat='ogg_vorbis',
                                                  LanguageCode='pt-BR',
                                                  TextType='ssml',
                                                  Text="<speak>Bem vindo novamente!</speak>")
        audio = response['AudioStream'].read()
        bot.send_chat_action(chat_id, "record_audio")
        bot.send_voice(chat_id, audio)

    except Exception:
        log.warning("Not exists user for id {id}, creating ...".format(id=user_id))
        users = [{'id': message.from_user.id, 'name': message.from_user.first_name, 'street': 'rua i'}]
        try:
            current_user = UserRepository.create(users)
            print("usuario criado: {0}".format(current_user.name))
        except:
            current_user = UserRepository.find_by_id(user_id)

        message = "Selecione ou fale uma das opções abaixo:"
        bot.send_message(chat_id, message, reply_markup=main_option_keyboard_markup(chat_id))

    user_message = "Olá {user_name}".format(user_name=current_user.name)
    bot.send_message(chat_id, user_message)
    welcome_message = "Meu nome é {bot}, serei seu assistente virtual." \
                      "O quê deseja pedir?".format(bot=bot_name)

    welcome_message_ssml = """
                                <speak>
                                    <p>Olá {user_name}! Meu nome é {bot}, serei sua assistente virtual!</p>
                                    <p>Fale um dos itens abaixo ou clique no botão referente a sua escolha.</p>
                                    <p>Aves</p>
                                    <p>Bovinos</p>
                                    <p>Suínos</p>
                                    <p>Sugestões</p>
                                    <p>Info</p>
                                    <p>Encerrar</p>
                                               
                                 </speak>
                           """.format(user_name=message.from_user.first_name, bot=bot_name)



    response = polly_client.synthesize_speech(VoiceId='Vitoria',
                                              OutputFormat='ogg_vorbis',
                                              LanguageCode='pt-BR',
                                              TextType='ssml',
                                              Text=welcome_message_ssml)

    audio = response['AudioStream'].read()
    bot.send_chat_action(chat_id, "record_audio")
    bot.send_voice(chat_id, audio)
    bot.send_message(chat_id, welcome_message, reply_markup=main_option_keyboard_markup(chat_id))


def main_menu(choice):
    chat_id = choice["id"]
    welcome_message_ssml = """
                                    <speak>
                                        <p>Fale um dos itens abaixo ou clique no botão referente a sua escolha.</p>
                                        <p>Aves</p>
                                        <p>Bovinos</p>
                                        <p>Suínos</p>
                                        <p>Sugestões</p>
                                        <p>Info</p>
                                        <p>Encerrar</p>

                                     </speak>
                               """


    response = polly_client.synthesize_speech(VoiceId='Vitoria',
                                              OutputFormat='ogg_vorbis',
                                              LanguageCode='pt-BR',
                                              TextType='ssml',
                                              Text=welcome_message_ssml)

    audio = response['AudioStream'].read()
    bot.send_chat_action(chat_id, "record_audio")
    bot.send_voice(chat_id, audio)
    message = "Selecione ou fale uma das opções abaixo:"
    bot.send_message(chat_id, message, reply_markup=main_option_keyboard_markup(chat_id))


bot.polling(none_stop=True, interval=0, timeout=60)
