from neuralintents import GenericAssistant
import speech_recognition as sr
import pyttsx3 as tts
import sys
import multiprocessing
import time
import os

recognizer = sr.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)
speaker.setProperty('voice', 2)


def create_note():
    global recognizer
    speaker.say("¿Que desea anotar?")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.1)
                audio = recognizer.listen(mic)
                note = recognizer.recognize_google(audio)
                note = note.lower()
                speaker.say("Elige un nombre de archivo")
                speaker.runAndWait()
                recognizer.adjust_for_ambient_noise(mic, duration=0.1)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            with open(f"{filename}.txt", 'w') as f:
                f.write(note)
                done = True
                speaker.say("Nota creada")
                speaker.runAndWait()
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("No entendí eso, dilo denuevo")
            speaker.runAndWait()


todo_list = []


def add_todo():
    global recognizer
    speaker.say("¿Qué actividad desea agregar?")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with sr.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.1)
                audio = recognizer.listen(mic)
                item = recognizer.recognize_google(audio)
                item = item.lower()
                todo_list.append(item)
                done = True
                speaker.say(f"{item} se añadio a la lista")
                speaker.runAndWait()

        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("No entendí eso, dilo denuevo")
            speaker.runAndWait()


def show_todo():
    if len(todo_list) == 0:
        speaker.say("No hay actividades para hacer")
    else:
        speaker.say("Tus actividades son")
        for item in todo_list:
            speaker.say(item)
        speaker.runAndWait()


def hello():
    speaker.say("Hola")
    speaker.runAndWait()


def socialMed():
    socmd = ["youtube","instagram", "facebook", "google", "whatsapp", "reddit", "4chan"]
    for sm in socmd:
        if sm in message:
            print(message)
            speaker.say(f"Abriendo {sm}")
            speaker.runAndWait()
            if sm == "4chan":
                os.system(f'cmd /c start https://{sm}.org"')
            elif sm == "whatsapp":
                os.system(f'cmd /c start https://web.{sm}.com"')
            else:
                os.system(f'cmd /c start https://{sm}.com"')


def _quit():
    speaker.say("te huelo luego socio")
    speaker.runAndWait()
    sys.exit(0)


mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todos": show_todo,
    "exit": _quit,
    "social_media": socialMed

}

assistant = GenericAssistant('intents.json', intent_methods=mappings)
# assistant.train_model()
# assistant.save_model()
assistant.load_model('assistant_model')

while True:
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.1)
            audio = recognizer.listen(mic)
            recognizer.recognize_google(audio, language="es-MX")
            message = recognizer.recognize_google(audio)
            message = message.lower()
            assistant.request(message)
            print(message)

    except sr.UnknownValueError:
        message = ""
