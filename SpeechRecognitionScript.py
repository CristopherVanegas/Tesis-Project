import speech_recognition as sr
from RegistrarRostros import RegistrarRostrosApp

r = sr.Recognizer()
mic = sr.Microphone()

print('Start Talking')

commands = [
    'take assistance'
]

def ReconocerComandos():
    while True:
        with mic as source:
            audio = r.listen(source)

        try:
            words = r.recognize_google(audio)
            print(words)

            if words in commands:
                RegistrarRostrosApp()

        except sr.UnknownValueError:
            print('>>> Trying to undestand what you are talking...')
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
