import pyttsx3
from pydub import AudioSegment

DEFAULT_RATE = 170
DEFAULT_VOLUME = 1
DEFAULT_LANGUAGE = "pt_BR"


class TextToSpeak:

    def __init__(self, search_language=DEFAULT_LANGUAGE):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", DEFAULT_RATE)
        self.engine.setProperty("volume", DEFAULT_VOLUME)
        self.voices = self.engine.getProperty('voices')
        self.language = search_language

    def __filter_available_language(self, voices):
        if self.language in voices.languages:
            return True
        else:
            return False

    def get_available_voice(self):
        list_of_filtered_voices = list(filter(self.__filter_available_language, self.voices))
        if len(list_of_filtered_voices) > 0:
            return list_of_filtered_voices[0].id
        else:
            return Exception("No voice found for this language")

    def set_voice(self, selected_voice):
        self.engine.setProperty("voice", selected_voice)

    def say(self, text):
        self.engine.say(text)
        self.__destroy()

    def save_voice_to_file(self, text, file_path, file_destination, audio_format="ogg"):
        self.engine.save_to_file(text=text, filename=file_path)
        self.__destroy()
        AudioSegment.from_file(file_path).export(file_destination, format=audio_format)
        return file_destination

    def __destroy(self):
        self.engine.runAndWait()
        self.engine.stop()


if __name__ == '__main__':
    speak = TextToSpeak()
    speak.set_voice(speak.get_available_voice())
    speak.say("Oi")

    speak.save_voice_to_file("oi oi oi", "../download_files/audio.out", "audioconvertido.ogg")
