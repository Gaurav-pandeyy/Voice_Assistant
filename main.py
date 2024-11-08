from http.client import responses

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


def get_city_name():
    print("Please Say the name of the city you want the weather info for.")
    speak("Please Say the name of the city you want the weather info for.")
    city_name = listen()
    if city_name:
        print("City: ", city_name)
        return city_name
    else:
        print("Couldn't Capture the city name.")
        speak("Couldn't Capture the city name.")
        return ""


def weather_api(city_name):
    api_key = ""
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
            f"The weather is {city_name} is currently {weather_description}"
            f"With a temperature of {temperature}°C, feels like {feels_like}°C."
            f"The Humidity is {humidity}%, and the wind speed is {wind_speed} meters per second."
        )

        print(weather_info)
        speak(weather_info)
    else:
        error_message = "City not found or an API error occured."
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
        weather_api()

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
