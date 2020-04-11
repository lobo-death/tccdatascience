import speech_recognition as sr
from pydub import AudioSegment as audioSegment
import os

TEMP_WAV_PATH = "./download_files/wav/"


class Recognizer:

    def __init__(self, language):
        self.__language = language
        self.__recognize = sr.Recognizer()

    def sound_recognizer(self, filename, file):
        wav_file = self.__convert_files_to_format(
            filename=filename,
            file=file,
            format_name="wav",
            export_path=TEMP_WAV_PATH)
        with sr.AudioFile(wav_file) as source:
            audio_file = self.__recognize.record(source)

            try:
                sound_recognized = self.__recognize.recognize_google(audio_file, language=self.__language)
                return sound_recognized
            except sr.UnknownValueError as ex:
                return Exception("Unknow recognization sppech={0}".format(ex))
            except sr.RequestError as ex:
                return Exception("Error connection to Google service error={0}".format(ex))

    def __convert_files_to_format(self, filename, file, format_name, export_path):
        if not os.path.exists(export_path):
            os.mkdir(export_path)
        ogg = audioSegment.from_file(file=file, format="ogg")
        destination_filename = filename[:-4] + "." + format_name
        ogg.export(export_path + destination_filename, format=format_name)
        return export_path + destination_filename
