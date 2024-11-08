import speech_recognition as sr
import datetime
import pyttsx3
import requests

# Initialize recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        return command


def handle_command(command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        print(f"The time is {current_time}")
        speak(f"The time is {current_time}")

    elif "name" in command:
        print("Hello, I am your assistant!")
        speak("Hello, I am your assistant!")
    else:
        print("Sorry, I didn't understand that command.")
        speak("Sorry, I didn't understand that command.")


while True:
    command = listen()
    if command:
        handle_command(command)
    if "stop" in command or "exit" in command:
        print("Goodbye!")
        speak("Goodbye!")
        break
