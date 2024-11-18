import json
import speech_recognition as sr
import datetime
import pyttsx3
import requests
from Extra_Tasks import send_email
import time
import spacy


# Load configuration
def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config


config = load_config()
WAKE_WORDS = config["wake_words"]  # List of wake words

recognizer = sr.Recognizer()
engine = pyttsx3.init()
nlp = spacy.load("en_core_web_sm")  # Load spaCy language model


# Speak text using pyttsx3
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Listen for voice commands
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


# Analyze command using spaCy
def analyze(command):
    doc = nlp(command)

    # Print tokens for debugging
    print("Tokens:")
    for token in doc:
        print(f"{token.text} - {token.pos_}")

    # Print named entities for debugging
    print("\nNamed Entities:")
    for ent in doc.ents:
        print(f"{ent.text} ({ent.label_}) - {spacy.explain(ent.label_)}")

    # Determine intent based on command content
    if "email" in command or any(token.text.lower() == "email" for token in doc):
        print("\nIntent: Send Email")
        recipient = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        return {"intent": "email", "recipient": recipient}

    if "weather" in command or any(token.text.lower() == "weather" for token in doc):
        print("\nIntent: Get Weather")
        city = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
        return {"intent": "weather", "city": city}

    if "time" in command or any(token.text.lower() == "time" for token in doc):
        print("\nIntent: Get Time")
        return {"intent": "time"}

    return {"intent": "unknown"}


# Handle email sending
def handle_send_email():
    print("What is the subject of the email?")
    speak("What is the subject of the email?")
    subject = listen_for_command()

    print("What should I say in the email?")
    speak("What should I say in the email?")
    message = listen_for_command()

    response = send_email(subject, message)
    print(response)
    speak(response)


# Ask for city name if not provided
def get_city_name():
    print("Which city's weather would you like to know?")
    speak("Which city's weather would you like to know?")
    city_name = listen_for_command()
    if city_name:
        city_name = city_name.strip()
        print("City:", city_name)
        return city_name
    else:
        print("Couldn't capture the city name.")
        speak("Couldn't capture the city name.")
        return ""


# Fetch weather using OpenWeatherMap API
def weather_api(city_name):
    api_key = "1632e63a399027cee77feffe63353bc2"
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
            f"The weather in {city_name} is currently {weather_description}, \n"
            f"with a temperature of {temperature}°C, feels like {feels_like}°C. \n"
            f"The humidity is {humidity}%, and the wind speed is {wind_speed} meters per second.\n"
        )

        print(weather_info)
        speak(weather_info)
    else:
        error_message = "City not found or an API error occurred."
        print(error_message)
        speak(error_message)


# Handle commands based on intent
def handle_command(command):
    analysis = analyze(command)  # Use spaCy to determine intent and extract info
    intent = analysis.get("intent")

    if intent == "time":
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        print(f"The time is {current_time}")
        speak(f"The time is {current_time}")

    elif intent == "weather":
        city_name = analysis.get("city")
        if city_name:
            weather_api(city_name[0])  # Use the first detected city
        else:
            # Ask user for city name if not detected
            city_name = get_city_name()
            if city_name:
                weather_api(city_name)

    elif intent == "email":
        recipient = analysis.get("recipient")
        handle_send_email()
        # Optional: Use recipient for further customization

    else:
        print("Sorry, I didn't understand that command.")
        speak("Sorry, I didn't understand that command.")


# Listen for wake word
def listen_for_wake_word():
    with sr.Microphone() as source:
        print(f"Listening for wake words: {', '.join(WAKE_WORDS)}...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print("Heard:", command)
            for wake_word in WAKE_WORDS:
                if wake_word in command:
                    return True
        except sr.UnknownValueError:
            pass
        return False


# Main loop with KeyboardInterrupt exception handling
try:
    while True:
        if listen_for_wake_word():
            print("Wake word detected. Ready for command.")
            speak("Yes, how can I assist you?")

            while True:
                command = listen_for_command()

                if command:
                    handle_command(command)

                    if "stop" in command or "exit" in command:
                        print("Goodbye!")
                        speak("Goodbye!")
                        time.sleep(1)
                        break

                time.sleep(0.5)

except KeyboardInterrupt:
    print("\nProgram interrupted. Exiting...")
    speak("Program interrupted. Exiting...")
    recognizer = None
    engine.stop()
    time.sleep(1)
