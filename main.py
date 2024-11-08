
import speech_recognition as sr
import datetime
import pyttsx3
import requests
from Extra_Tasks import send_email


recognizer = sr.Recognizer()
engine = pyttsx3.init()


WAKE_WORD = "wake up"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen_for_command():
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        return command


def handle_send_email():
    print("To whom should I send the email?")
    speak("To whom should I send the email?")
    recipient = listen_for_command()

    print("What is the subject of the email?")
    speak("What is the subject of the email?")
    subject = listen_for_command()

    print("What should I say in the email?")
    speak("What should I say in the email?")
    message = listen_for_command()


    response = send_email(recipient, subject, message)
    print(response)
    speak(response)


def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print("Heard:", command)
            if WAKE_WORD in command:
                return True
        except sr.UnknownValueError:
            pass
        return False


def get_city_name():
    print("Please say the name of the city you want the weather info for.")
    speak("Please say the name of the city you want the weather info for.")
    city_name = listen_for_command()
    if city_name:
        print("City:", city_name)
        return city_name
    else:
        print("Couldn't capture the city name.")
        speak("Couldn't capture the city name.")
        return ""


def weather_api(city_name):
    api_key = "your_openweathermap_api_key"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"

    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        weather_description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']

        weather_info = (
            f"The weather in {city_name} is currently {weather_description}, "
            f"with a temperature of {temperature}°C, feels like {feels_like}°C. "
            f"The humidity is {humidity}%, and the wind speed is {wind_speed} meters per second."
        )

        print(weather_info)
        speak(weather_info)
    else:
        error_message = "City not found or an API error occurred."
        print(error_message)
        speak(error_message)


def handle_command(command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        print(f"The time is {current_time}")
        speak(f"The time is {current_time}")

    elif "name" in command:
        print("Hello, I am your assistant!")
        speak("Hello, I am your assistant!")

    elif "weather" in command:
        city_name = get_city_name()
        if city_name:
            weather_api(city_name)

    elif "send email" in command:
        handle_send_email()

    else:
        print("Sorry, I didn't understand that command.")
        speak("Sorry, I didn't understand that command.")


while True:
    if listen_for_wake_word():
        print("Wake word detected. Ready for command.")
        speak("Yes, how can I assist you?")
        command = listen_for_command()
        if command:
            handle_command(command)
        if "stop" in command or "exit" in command:
            print("Goodbye!")
            speak("Goodbye!")
            break
