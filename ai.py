import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import webbrowser
import pyjokes
import sys

r = sr.Recognizer()

phone_numbers = {"aman": '9161480879', "miku": '6388630191', "bebo": '9554215841', "chiku": '8400606914'}
bank_account_numbers = {'tt': '444444', 'mm': '4433334'}


def speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # male(0), female(1)
    engine.say(command)
    engine.runAndWait()


# ----------- Command Handlers -----------
def play_song(query):
    song = query.replace("play", "").strip()
    speak(f"Playing {song}")
    pywhatkit.playonyt(song)


def tell_date(_):
    today = datetime.date.today().strftime("%B %d, %Y")
    speak(f"Today's date is {today}")


def tell_time(_):
    timenow = datetime.datetime.now().strftime('%H:%M')
    speak(f"The time is {timenow}")


def search_person(query):
    person = query.replace("who is", "").strip()
    info = wikipedia.summary(person, sentences=1)
    speak(info)


def search_topic(query):
    topic = query.replace("tell me about", "").strip()
    info = wikipedia.summary(topic, sentences=1)
    speak(info)


def get_phone_number(query):
    for name, number in phone_numbers.items():
        if name in query:
            speak(f"{name}'s phone number is {number}")
            return
    speak("Sorry, I don't have that phone number.")


def get_account_number(query):
    for bank, acc in bank_account_numbers.items():
        if bank in query:
            speak(f"{bank} bank account number is {acc}")
            return
    speak("Sorry, I don't have that account number.")


def open_website(query):
    if "google" in query:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif "youtube" in query:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    elif "whatsapp" in query:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp Web")
    else:
        site = query.replace("open", "").strip()
        url = f"https://{site}.com"
        webbrowser.open(url)
        speak(f"Opening {site}")


def tell_joke(_):
    joke = pyjokes.get_joke()
    speak(joke)


def exit_program(_):
    speak("Goodbye! Have a great day!")
    sys.exit()


# ----------- Command Mapping -----------
command_map = {
    "play": play_song,
    "date": tell_date,
    "time": tell_time,
    "who is": search_person,
    "tell me about": search_topic,
    "phone number": get_phone_number,
    "account number": get_account_number,
    "open": open_website,
    "joke": tell_joke,
    "exit": exit_program,
    "shutdown": exit_program
}


# ----------- Main Function -----------
def commands():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            speak("Listening... what can I do for you?")
            audioin = r.listen(source)
            my_text = r.recognize_google(audioin).lower()
            print("You said:", my_text)

            # Match command
            for keyword, action in command_map.items():
                if keyword in my_text:
                    action(my_text)
                    exit_program(my_text)   # exit after performing
                    return
            else:
                speak("Sorry, I couldn't understand that. Exiting now.")
                exit_program(my_text)

    except Exception as e:
        print("Error in capturing:", e)
        speak("Sorry, I could not understand that. Exiting now.")
        sys.exit()


# ----------- Run Once and Exit -----------
speak("Hi there! I am your assistant. Ask me one thing.")
commands()
