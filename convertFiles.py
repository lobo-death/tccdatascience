#!/usr/bin/env python

import os
from pydub import AudioSegment as audioSegment
import speech_recognition as sr

SOURCE_PATH = "./audio/ogg/"
DESTINATION_PATH = "./audio/mp3/"
TEMP_WAV_PATH = "./audio/wav/"


def trimAudioFiles(audio_file, decibeis =- 50, chunk = 10):
    silent_miliseconds = 0
    while audio_file[silent_miliseconds : silent_miliseconds + chunk].dBFS < decibeis:
        silent_miliseconds += chunk

    return silent_miliseconds

def convertOggFilesToFormat(filename, file, formatName, exportPath):
    ogg = audioSegment.from_file(file=file, format="ogg")
    destinationFilename = filename[:-4] + "." + formatName
    ogg.export(exportPath + destinationFilename, format=formatName)
    return exportPath + destinationFilename

if not os.path.exists(DESTINATION_PATH):
    os.mkdir(DESTINATION_PATH)

if not os.path.exists(TEMP_WAV_PATH):
    os.mkdir(TEMP_WAV_PATH)


files = os.listdir(SOURCE_PATH)

for file in files:
    filename = file
    sourceOggFile = SOURCE_PATH + file
    sourceWavFile = convertOggFilesToFormat(filename, sourceOggFile, "wav", TEMP_WAV_PATH)

    recognizer = sr.Recognizer()
    with sr.AudioFile(sourceWavFile) as source:
        audio = recognizer.record(source)  # read the entire audio file

        try:
            soundRecognized = recognizer.recognize_google(audio, language="pt-BR")
            convertOggFilesToFormat(soundRecognized + "_" + filename, sourceOggFile, "mp3", DESTINATION_PATH)
            print(filename + " identificado como " + soundRecognized)

        except sr.UnknownValueError:
            print("Google nao identificou o audio")
        except sr.RequestError as e:
            print("Problemas na chamada ao serviço {0}".format(e))



print("Todos os arquivos processados!")
