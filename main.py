import speech_recognition as sr
import pyttsx3
import webbrowser
import google.generativeai as genai
import pywhatkit
import requests
import psutil
import wikipedia
import datetime
import subprocess
import os
import pyautogui
import json
import threading
import time
import pyperclip
import screen_brightness_control as sbc
import wmi

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "4ea1f9eab2e24a69872da746421124bf"
weather_api = "f67d6f88b4902446a4dd653f4f2c36db" 


def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiprocess(command):
    genai.configure(api_key="AIzaSyA_MlUCMXTHFV83jf_aTHyXsVMeK1VnjKg")
    model = genai.GenerativeModel("gemini-2.0-flash")
    # FIX: Pass command as a list
    response = model.generate_content([command])
    return response.text

def get_pc_health():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    battery = psutil.sensors_battery()

    health_report = f"CPU usage is at {cpu} percent. "
    health_report += f"RAM usage is at {ram.percent} percent. "
    health_report += f"Disk usage is at {disk.percent} percent. "

    if battery:
        health_report += f"Battery is at {battery.percent} percent and is "
        health_report += "charging." if battery.power_plugged else "not charging."
    else:
        health_report += "Battery status not available."

    return health_report

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            main = data["main"]
            weather = data["weather"][0]
            temp = main["temp"]
            desc = weather["description"]
            return f"The temperature in {city} is {temp} degrees Celsius with {desc}."
        else:
            return "I couldn't find the weather for that city."
    except Exception as e:
        return "There was an error getting the weather."

def load_memory():
    try:
        with open("memory.json", "r") as file:
            return json.load(file)
    except:
        return {}

def save_memory(data):
    with open("memory.json", "w") as file:
        json.dump(data, file)

memory = load_memory()

todo_file = "todo.json"

def load_todo():
    try:
        with open(todo_file, "r") as f:
            return json.load(f)
    except:
        return []

def save_todo(tasks):
    with open(todo_file, "w") as f:
        json.dump(tasks, f)

def set_timer(seconds):
    def countdown():
        time.sleep(seconds)
        speak("Time's up!")
    threading.Thread(target=countdown).start()

def get_clipboard_text():
    try:
        return pyperclip.paste()
    except:
        return ""

def get_cpu_temperature():
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType == u'Temperature' and 'CPU' in sensor.Name:
                return f"CPU temperature is {sensor.Value} degrees Celsius."
        return "Couldn't read CPU temperature."
    except:
        return "Temperature reading failed. Please ensure Open Hardware Monitor is running."

def write_code_from_prompt(prompt, filename="generated_code.py"):
    instruction = f"Write full working code for the following task:\n{prompt}\nMake it clean and readable."
    result = aiprocess(instruction)
    try:
        with open(filename, "a") as f:
            f.write("\n# === New Code ===\n")
            f.write(result + "\n")
        return result
    except Exception as e:
        return f"Error saving code: {e}"

def process_command(c):
    c_lower = c.lower()
    if "open google" in c_lower:
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c_lower:
        webbrowser.open("https://www.youtube.com")
    elif "open instagram" in c_lower:
        webbrowser.open("https://www.instagram.com")
    elif "open prime" in c_lower:
        webbrowser.open("https://primevideo.com")
    elif "open facebook" in c_lower: 
        webbrowser.open("https://www.facebook.com")
    elif "open twitter" in c_lower:
        webbrowser.open("https://www.twitter.com")
    elif "open whatsapp" in c_lower:
        webbrowser.open("https://web.whatsapp.com")
    elif "open linkedin" in c_lower:
        webbrowser.open("https://www.linkedin.com")
    elif "time" in c_lower:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
    elif "date" in c_lower:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")
    elif c_lower.startswith("play "):
        song = c_lower.split("play ", 1)[1].strip()
        if song:
            speak(f"Playing {song} on YouTube.")
            try:
                pywhatkit.playonyt(song)
            except:
                speak("Sorry, I couldn't play that song.")
        else:
            speak("Please specify the song name.")
    elif "news" in c_lower:
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            for article in articles[:5]:
                speak(article["title"])
        else:
            speak("Sorry, I couldn't fetch the news.")
    elif "pc health" in c_lower or "system status" in c_lower:
        health = get_pc_health()
        print(health)
        speak(health)
    elif "tell me about" in c_lower:
        try:
            if "who is" in c_lower:
                topic = c_lower.split("who is", 1)[1].strip()
            else:
                topic = c_lower.split("tell me about", 1)[1].strip()

            if topic:
                summary = wikipedia.summary(topic, sentences=2)
                print(summary)
                speak(summary)
            else:
                speak("Please tell me the topic you want to search on Wikipedia.")
        except wikipedia.exceptions.DisambiguationError as e:
            speak("That topic is too broad. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find anything on Wikipedia.")
        except Exception as e:
            speak("An error occurred while fetching information from Wikipedia.")
            print(f"Wikipedia Error: {e}")
    elif "weather" in c_lower:
        speak("Which city should I check the weather for?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        try:
            city = recognizer.recognize_google(audio)
            weather_report = get_weather(city)
            print(weather_report)
            speak(weather_report)
        except:
            speak("Sorry, I could not understand the city name.")
    elif "mute volume" in c_lower:
        pyautogui.press("volumemute")
        speak("Volume muted.")
    elif "increase volume" in c_lower:
        for _ in range(5):
            pyautogui.press("volumeup")
        speak("Volume increased.")
    elif "decrease volume" in c_lower:
        for _ in range(5):
            pyautogui.press("volumedown")
        speak("Volume decreased.")
    elif "open" in c_lower and "app" in c_lower:
        if "chrome" in c_lower:
            subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
            speak("Opening Chrome.")
        elif "notepad" in c_lower:
            subprocess.Popen("notepad.exe")
            speak("Opening Notepad.")
        elif "vs code" in c_lower or "visual studio" in c_lower:
            subprocess.Popen("code")  # Assuming code is added to PATH
            speak("Opening Visual Studio Code.")
        else:
            speak("I couldn't find that app.")
    elif "shutdown" in c_lower:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif "restart" in c_lower:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")
    elif "lock" in c_lower:
        speak("Locking the computer.")
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif "take note" in c_lower or "note" in c_lower:
        speak("What should I write down?")
        with sr.Microphone() as source:
            note_audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            try:
                note_text = recognizer.recognize_google(note_audio)
                with open("notes.txt", "a") as f:
                    f.write(f"{datetime.datetime.now()}: {note_text}\n")
                speak("Note saved.")
            except:
                speak("Sorry, I couldn't catch that.")
    elif "remind me" in c_lower:
        speak("What should I remind you?")
        with sr.Microphone() as source:
            reminder_audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            try:
                reminder_text = recognizer.recognize_google(reminder_audio)
                with open("reminders.txt", "a") as f:
                    f.write(f"{datetime.datetime.now()}: {reminder_text}\n")
                speak("Reminder noted.")
            except:
                speak("I couldn't understand your reminder.")
    elif "screenshot" in c_lower or "take screenshot" in c_lower:
        file_path = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(file_path)
        speak("Screenshot taken and saved.")
    
    elif "add task" in c_lower or "remember task" in c_lower:
        speak("What task should I add?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        try:
            task = recognizer.recognize_google(audio)
            tasks = load_todo()
            tasks.append(task)
            save_todo(tasks)
            speak("Task added.")
        except:
            speak("Sorry, I couldn't understand.")
    elif "list tasks" in c_lower:
        tasks = load_todo()
        if tasks:
            speak("Here are your tasks:")
            for task in tasks:
                speak(task)
        else:
            speak("You have no tasks.")
    elif "clear tasks" in c_lower:
        save_todo([])
        speak("All tasks cleared.")
    elif "set timer" in c_lower:
        speak("For how many seconds?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
        try:
            seconds = int(recognizer.recognize_google(audio).split()[0])
            set_timer(seconds)
            speak(f"Timer set for {seconds} seconds.")
        except:
            speak("I couldn't set the timer.")
    elif "focus mode" in c_lower or "study mode" in c_lower:
        speak("Starting focus mode.")
        # Open necessary apps/websites
        subprocess.Popen("notepad.exe")
        subprocess.Popen("WhatsApp.exe")
        webbrowser.open("https://chat.openai.com")
        webbrowser.open("https://youtube.com")
        # Optional: Block distracting sites by modifying hosts file or use external tool
        speak("Focus mode activated. Let's get productive!")
    elif "summarize clipboard" in c_lower:
        text = get_clipboard_text()
        if text:
            result = aiprocess("Summarize this:\n" + text[:3000])
            speak(result[:500])
            print(result)
        else:
            speak("Clipboard is empty.")
    elif "explain code" in c_lower:
        code = get_clipboard_text()
        if code:
            result = aiprocess("Explain this code:\n" + code[:3000])
            speak(result[:500])
            print(result)
        else:
            speak("Clipboard is empty.")
    elif "fix grammar" in c_lower:
        text = get_clipboard_text()
        if text:
            prompt = "Correct the grammar of the following:\n" + text
            result = aiprocess(prompt)
            speak("Here's the corrected version.")
            print(result)
            speak(result[:500])
        else:
            speak("Clipboard is empty.")
    elif "increase brightness" in c_lower:
        try:
            current = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(min(100, current + 20))
            speak("Brightness increased.")
        except:
            speak("Failed to adjust brightness.")

    elif "low brightness" in c_lower:
        try:
            current = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(max(0, current - 20))
            speak("Brightness decreased.")
        except:
            speak("Failed to adjust brightness.")
    elif "free up ram" in c_lower or "clean memory" in c_lower:
        speak("Freeing up memory.")
        os.system("echo Y | PowerShell.exe Clear-RecycleBin")
        speak("Recycle bin cleared. I recommend closing unused programs too.")
    elif "type" in c_lower:
        speak("What should I type?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio)
            pyautogui.write(text)
            speak("Typed successfully.")
        except:
            speak("Couldn't catch that.")
    elif "write code" in c_lower or "generate code" in c_lower:
        speak("What code should I write for you?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        try:
            prompt = recognizer.recognize_google(audio)
            speak("Generating code. Please wait.")
            code = write_code_from_prompt(prompt)
            print(code)
            speak("Code has been generated and saved.")
        except:
            speak("Sorry, I couldn't understand the coding task.")
    elif "cpu temperature" in c_lower or "pc temperature" in c_lower or "system heat" in c_lower or "check temperature" in c_lower or "temperature" in c_lower:
        speak("Checking temperature...")
        temp = get_cpu_temperature()
        print(temp)
        speak(temp)
    elif "thank you" in c_lower or "thanks" in c_lower:
        speak("no problem, sir. Its my job to make your life easier.")
    else:
        output = aiprocess(c)
        speak(output)

# waiting_for_command = False 

if __name__ == "__main__":
    hour = datetime.datetime.now().hour
    if hour < 12:
        greet = "Good morning"
    elif hour < 18:
        greet = "Good afternoon"
    else:
        greet = "Good evening"

    memory = {'name': 'sir'}
    speak(f"{greet}, {memory['name']}. Initializing hira, your assistant.")


while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            command = recognizer.recognize_google(audio)
            if command.lower() == "hira":
                speak("yes sir,")
                print("Listening....")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    try:
                        command = recognizer.recognize_google(audio)
                        print(command)
                        process_command(command)
                    except sr.UnknownValueError:
                        print("Could not understand the audio")
                        speak("Sorry, I could not understand the audio.")
                    except sr.RequestError as e:
                        print(f"Recognition error; {e}")
                        speak("Sorry, there was a recognition error.")
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
        except Exception as e:
            print(f"An error occurred: {e}")