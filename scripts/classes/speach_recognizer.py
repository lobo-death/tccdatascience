import speech_recognition as sr


class Recognizer:

    def __init__(self, language):
        super().__init__(self)
        self.__language = language
        self.__recognize = sr.Recognizer()

    def sound_recognizer(self, file):
        with self.__recognize as source:
            audio_file = self.__recognize.record(source)

            try:
                sound_recognized = self.__recognize.recognize_google(audio_file, language=self.__language)
                return sound_recognized
            except self.__recognize.UnknownValueError as ex:
                return Exception("Unknow recognization sppech={0}".format(ex))
            except self.__recognize.RequestError as ex:
                return Exception("Error connection to Google service error={0}".format(ex))
