import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musiclibrary
import requests
from google import genai
import os
import datetime
import wikipedia 


os.environ["GEMINI_API_KEY"]= "AIzaSyClkgH2yCu5C_BBFu6Ow-AekSIyV08F-TY"

import threading

class ZenithAssistant:
    def __init__(self, on_speak_callback=None, on_listen_callback=None):
        self.on_speak_callback = on_speak_callback
        self.on_listen_callback = on_listen_callback
        self.engine = pyttsx3.init()
        self.lock = threading.Lock()

    def speak(self, text):
        if self.on_speak_callback:
            self.on_speak_callback(text)
        
        with self.lock:
            self.engine.say(text)
            self.engine.runAndWait()

    def gemini_response(self, prompt):
        try:
            client = genai.Client()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text
        except Exception as e:
            return f"Gemini API Error:{e}"

    def wikiResult(self, query):
        wikipedia.set_lang("en")
        query = query.lower().replace('search','').strip()[1:]
        if len(query.split())==0: 
            query = "wikipedia"
        try:
            return wikipedia.summary(query, sentences=5)
        except Exception as e:
            return "Desired Result Not Found"

    def process_command(self, command):
        command = command.lower()
        if "open youtube" in command:
            webbrowser.open("https://www.youtube.com")

        elif "open google" in command:
            webbrowser.open("https://www.google.com")

        elif "open my linkedin" in command:
            webbrowser.open("https://www.linkedin.com/in/vansh-kumar-nigam")

        elif command.startswith("search"):
            result = self.wikiResult(command)
            print("According to Wikipedia:", result)
            self.speak(f"According to Wikipedia: {result}")

        elif "today date" in command:
            today = datetime.date.today()
            self.speak(f"Today's date is {today.strftime('%B %d, %Y')}")

        elif command.startswith("play"):
            parts = command.split(" ", 1)
            if len(parts) > 1:
                song = parts[1]
                if song in musiclibrary.music:
                    link = musiclibrary.music[song]
                    webbrowser.open(link)
                else:
                    self.speak(f"Sorry, I don't have the song {song} in the library.")
            else:
                self.speak("Please specify a song name.")

        elif "tell me news" in command:
            try:
                r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey=2770add8f3224cf69928ab33edd9cefc", timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    articles = data.get("articles", [])
                    if articles:
                        self.speak("Here are the top 5 news headlines:")
                        for article in articles[:5]:
                            title = article.get("title", "No title available")
                            print("News:", title)
                            self.speak(title)
                else:
                    self.speak("Failed to retrieve news")
            except Exception as e:
                self.speak("An error occurred while processing your request.")

        elif "ask gemini" in command:
            prompt = command.replace("ask gemini", "").strip()
            if prompt:
                response = self.gemini_response(prompt)
                print("Gemini says:", response)
                self.speak(response)
            else:
                self.speak("Please provide a question after saying 'ask Gemini'")

        elif "stop" in command:
            self.speak("Shutting down. Goodbye!")
            exit()
        
        else:
            self.speak("Sorry, I didn't understand that command.")

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            if self.on_listen_callback:
                self.on_listen_callback("Listening for wake word...")
            print("Listening for wake word....")
            try:
                audio = r.listen(source, timeout=30, phrase_time_limit=30)
                word = r.recognize_google(audio)
                if word.lower() == "zenith":
                    if self.on_listen_callback:
                        self.on_listen_callback("Zenith Active...")
                    print("Hello I am Zenith")
                    self.speak("How can I help you")
                    
                    with sr.Microphone() as source:
                        print("Zenith Active.....")
                        audio = r.listen(source)
                        command = r.recognize_google(audio)
                        if self.on_listen_callback:
                            self.on_listen_callback(f"You said: {command}")
                        print(f"You said: {command}")
                        self.process_command(command)
            except sr.UnknownValueError:
                pass 
            except sr.RequestError as e:
                print(f"Speech Recognition Error {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    def simple_speak_callback(text):
        print(f"Zenith: {text}")

    bot = ZenithAssistant(on_speak_callback=simple_speak_callback)
    bot.speak("Initializing Zenith......")
    while True:
        bot.listen()
