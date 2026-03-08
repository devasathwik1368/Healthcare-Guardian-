import speech_recognition as sr

def listen_symptoms():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Speak your symptoms...")

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        print("You said:", text)

        return text.lower()

    except:

        return "Could not understand"