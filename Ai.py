import requests
import pyttsx3
import speech_recognition as sr
import googlesearch
import yt_dlp

# Function to speak the text
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech using the microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        speak("Sorry, I couldn't understand the audio.")
        return ""
    except sr.RequestError:
        print("Could not request results, please check your internet connection.")
        speak("Could not request results, please check your internet connection.")
        return ""

# Function to search Google and speak the results
def google_search(query):
    speak(f"Searching Google for {query}")
    search_results = list(googlesearch.search(query, num=5))
    print("Top results:")
    for result in search_results:
        print(result)
    return search_results

# Function to download a file from a URL
def download_file(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        message = f"Downloaded successfully: {save_path}"
        print(message)
        speak(message)
    else:
        message = "Failed to download the file."
        print(message)
        speak(message)

# Function to download a YouTube video
def download_youtube_video(url, save_path):
    ydl_opts = {
        'outtmpl': save_path,
        'format': 'best'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    message = f"YouTube video downloaded successfully: {save_path}"
    print(message)
    speak(message)

# Function to get weather data from OpenWeatherMap (requires API key)
def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        weather = data['weather'][0]['description']
        message = f"Weather in {city}: {temp}°C, {weather}"
        print(message)
        speak(message)
    else:
        message = "Failed to fetch weather data."
        print(message)
        speak(message)

# Main function to control the flow based on user speech input
if __name__ == "__main__":
    speak("What do you want to do?")
    choice = recognize_speech()

    if choice == "download":
        speak("Enter the file URL")
        file_url = input("Enter the file URL: ")
        file_name = file_url.split("/")[-1]  # Extract filename from URL
        download_file(file_url, file_name)

    elif choice == "youtube":
        speak("Enter the YouTube video URL")
        video_url = input("Enter the YouTube video URL: ")
        save_path = "%(title)s.%(ext)s"  # Save with video title as filename
        download_youtube_video(video_url, save_path)

    elif choice == "weather":
        speak("Enter the city name")
        city_name = input("Enter city name: ")
        api_key = "YOUR_OPENWEATHER_API_KEY"  # Replace with your actual OpenWeather API key
        get_weather(city_name, api_key)

    elif "search" in choice:
        query = choice.replace("search", "").strip()
        google_search(query)

    else:
        message = "Invalid choice."
        print(message)
        speak(message)

