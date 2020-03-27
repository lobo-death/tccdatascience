import pyttsx3
from pydub import AudioSegment


engine = pyttsx3.init() # object creation

# get/set velocity (rate) to speak
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)


# get/set volume
volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)   #volume between 0 (min) and 1 (max)

# get/set instaled voices in system
voices = engine.getProperty('voices')
for voice in voices:
    print(voice)


def filterLanguageByString(voice):
    if 'pt_BR' in voice.languages:
        return True
    else:
        return False


filteredBrazilianVoices = filter(filterLanguageByString, voices)

print(type(filteredBrazilianVoices))
voices = list(filteredBrazilianVoices)
print(type(voices))
for name in filteredBrazilianVoices:
    print(name)


print("id :" + voices[0].id)

engine.setProperty('voice', voices[0].id)  #set selected voice

engine.say("O que gostaria de pedir? ")
engine.say("O que vai levar? ")
engine.say("Você escolheu sugestões")
engine.save_to_file(
    text="Vocë escolheu bovinos! Essas são as promoções que temos para hoje.",
    filename="./textToSpeak3.out")
engine.runAndWait()
engine.stop()

# convert raw audio format to mp3
AudioSegment.from_file("./textToSpeak3.out").export('./converted2.mp3', format="mp3")

