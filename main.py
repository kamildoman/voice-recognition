# The program gonna tell you current time, weather in Warsaw, definition of something from wikipedia, give a compliment
# to your wife, can also tell you that it doesn't speak Polish, Russian and Chinese. Say "stop" to stop the program


import speech_recognition as sr
import wikipedia
import datetime
import requests
import config
import pyttsx3

recognizer = sr.Recognizer()
run_progam = True
speaker = pyttsx3.init()
speaker.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")


def get_weather():
    CITY = "warsaw"
    API_KEY = config.API_KEY

    link = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API_KEY}"

    r = requests.get(link)
    data = r.json()

    weather = data["weather"][0]["main"]
    temperature = data["main"]["temp"]
    return weather, temperature


def talk(text):
    speaker.say(text)
    speaker.runAndWait()


def listener():
    try:
        with sr.Microphone() as source:
            voice = recognizer.listen(source)
            command = ""
            command = recognizer.recognize_google(voice)
            
    except:
        pass
    return command



def run_program():
    command = listener()
    print(command)

    #listener might hear some sound but not recognize any word, then it returns None
    if command is None:
        talk("I can't hear you")

    else:
        if "definition of" in command and len(command) > 14:
            word = command.split(" ")[2:]
            try:
                definition = wikipedia.summary(word, sentences=1)
            except:
                definition = f"Sorry, I don't know what is {word}"
            
            talk(definition)

        elif "stop" in command:
            global run_progam
            talk("Ok, stopping now. Bye bye")
            speaker.stop()
            run_progam = False

        elif "time" in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"it's {time} now")

        elif "beautiful" in command:
            talk("Yes, your wife is very beautiful")

        elif "weather" in command:
            weather, temperature = get_weather()
            talk(f"It's {weather} today in Warsaw. The temperature is {temperature}") 

        elif "chinese" in command.lower():
            speaker.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0")
            talk("我不会说中文")
            speaker.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0") 
        
        elif "russian" in command.lower():
            speaker.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0")
            talk("я не могу говорить по русски")
            speaker.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")  
        
        elif "polish" in command.lower():
            speaker.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PL-PL_PAULINA_11.0")
            talk("Ja nie mówię po polsku. Tylko angielski")
            speaker.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")     
        
        else:
            talk("I don't understand")




while run_progam:
    run_program()


    









