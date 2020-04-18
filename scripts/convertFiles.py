#!/usr/bin/env python

import os
from pydub import AudioSegment as audioSegment
import speech_recognition as sr
import unidecode
from fuzzywuzzy import process

strOptions = ["bovinos".upper(), "suinos".upper(), "aves".upper(), "info".upper(), "sugestoes".upper(), "encerrar".upper()]

SOURCE_PATH = "../audio/ogg/"
DESTINATION_PATH = "../audio/mp3/"
DESTINATION_WAV_PATH = "../audio/wav/"
TEMP_WAV_PATH = "../audio/temp/"

print("path: {0}".format(os.path.abspath(SOURCE_PATH)))


def trimAudioFiles(audio_file, decibeis =- 50, chunk = 10):
    silent_miliseconds = 0
    while audio_file[silent_miliseconds : silent_miliseconds + chunk].dBFS < decibeis:
        silent_miliseconds += chunk

    return silent_miliseconds


def convertOggFilesToFormat(filename, file, formatName, exportPath):
    if not os.path.exists(exportPath):
        os.mkdir(exportPath)
    ogg = audioSegment.from_file(file=file, format="ogg")
    destinationFilename = filename[:-4] + "." + formatName

    if formatName == "wav":
        ogg.export(exportPath + destinationFilename, format=formatName, codec="pcm_s16le", bitrate="16000")
    else:
        ogg.export(exportPath + destinationFilename, format=formatName)
    return exportPath + destinationFilename


files = os.listdir(SOURCE_PATH)

for file in files:
    filename = file
    sourceOggFile = SOURCE_PATH + file
    try:
        sourceWavFile = convertOggFilesToFormat(filename, sourceOggFile, "wav", TEMP_WAV_PATH)

        recognizer = sr.Recognizer()
        with sr.AudioFile(sourceWavFile) as source:
            audio = recognizer.record(source)  # read the entire audio file

            try:
                soundRecognized = recognizer.recognize_google(audio, language="pt-BR")
                ratios = process.extract(unidecode.unidecode(soundRecognized).upper(), strOptions)
                highest = process.extractOne(unidecode.unidecode(soundRecognized).upper(), strOptions)
                mp3AudioDirectory = DESTINATION_PATH + unidecode.unidecode(highest[0]).upper() + "/"
                wavAudioDirectory = DESTINATION_WAV_PATH + unidecode.unidecode(highest[0]).upper() + "/"
                #convertOggFilesToFormat(unidecode.unidecode(soundRecognized).upper() + "_" + highest[0] + "_" + filename,
                #                        sourceOggFile, "mp3", mp3AudioDirectory)
                convertOggFilesToFormat(
                    unidecode.unidecode(soundRecognized).upper() + "_" + highest[0] + "_" + filename,
                    sourceOggFile, "wav", wavAudioDirectory)

                print(filename + " identificado como " + soundRecognized + " - sondex: " + highest[0])

            except sr.UnknownValueError:
                print(filename + " Google nao identificou o audio")
                mp3AudioDirectory = DESTINATION_PATH + unidecode.unidecode("UNKNOWN").upper() + "/"
                wavAudioDirectory = DESTINATION_WAV_PATH + unidecode.unidecode("UNKNOWN").upper() + "/"
                #convertOggFilesToFormat("UNKNOWN_" + filename,
                #                        sourceOggFile, "mp3", mp3AudioDirectory)
                convertOggFilesToFormat("UNKNOWN_" + filename,
                                        sourceOggFile, "wav", wavAudioDirectory)
            except sr.RequestError as e:
                print(filename + " Problemas na chamada ao serviço {0}".format(e))

    except Exception as e:
        print("Não foi possivel converter o arquivo: ")



print("Todos os arquivos processados!")
