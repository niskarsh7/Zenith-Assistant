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

def speak(text):
    engine=pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def gemini_response(prompt):
    try:
        client= genai.Client()
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Gemini API Error:{e}"
    
def wikiResult(query):
    wikipedia.set_lang("en")
    query = query.lower().replace('search','').strip()[1:]
    if len(query.split())==0: 
        query = "wikipedia"
    try:
        return wikipedia.summary(query,sentences=5)
    except Exception as e:
        return "Desired Result Not Found"



def process_command(command):
    command = command.lower()
    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        webbrowser.open("https://www.google.com")

    elif "open my linkedin" in command:
        webbrowser.open("https://www.linkedin.com/in/vansh-kumar-nigam")

    elif command.startswith("search"):
        result = wikiResult(command)
        print("According to Wikipedia:", result)

    elif "today date" in command:
        today = datetime.date.today()
        speak(f"Today's date is {today.strftime('%B %d, %Y')}")

    elif command.startswith("play"):
        song = command.split(" ")[1]
        link = musiclibrary.music[song]
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I don't have the song {song} in the library.")

    elif "tell me news" in command:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey=2770add8f3224cf69928ab33edd9cefc",timeout=15)
            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])
                if articles:
                    speak("Here are the top 5 news headlines:")
                    for article in articles[:5]:
                        title=article.get["title", "No title available"]
                        print("News:",title)
                        speak(title)
            else:
                speak("Failed to retrieve news")
        except Exception as e:
            speak("An error occurred while processing your request.")

    

    elif "ask gemini" in command:
        prompt = command.replace("ask gemini", "").strip()
        if prompt:
            response = gemini_response(prompt)
            print("Gemini says:", response)
            speak(response)
        else:
            speak("Please provide a question after saying 'ask Gemini'")

    elif "stop" in command:
         speak("Shutting down. Goodbye!......")
         exit()
    else:
        speak("Sorry, I didn't understand that command.")
        
         
if __name__ == "__main__":
    speak("Initializing Zenith......")
    while True:
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening for wake word....")
                audio =r.listen(source,timeout=30,phrase_time_limit=30)
                word=r.recognize_google(audio)
                if(word.lower() == "zenith"):
                    print("Hello I am Zenith")
                    speak("how can i help you")
               
            
                    with sr.Microphone() as source:
                        print("Zenith Active.....")
                        audio=r.listen(source)
                        command=r.recognize_google(audio)
                        print(f"You said: {command}")
                        process_command(command)

        except sr.UnknownValueError:
           print("Could not understand audio")
        except sr.RequestError as r:
           print(f" Speech Recognition Error {r})")
        except Exception as e:
            print(f"An error occurred: {e}")
            print ("Restarting Zenith in 5 seconds...")