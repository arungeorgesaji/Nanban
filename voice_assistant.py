import subprocess
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup
import datetime
import json
import io
from pytube import YouTube
from youtube_search import YoutubeSearch
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import openai
import keyboard
from gtts import gTTS
import os
from huggingface_hub import login
from langchain.llms import HuggingFaceHub
import requests

ipdata_api_key = "593fe98fa91127b3b7a2f3ed538cf0b85ecf684657b128afbedb3744"  
url = f'https://api.ipdata.co?api-key={ipdata_api_key}'

time = 'not_set'
strTime = 'not set'

os.environ['HUGGINGFACEHUB_API_TOKEN'] = "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"
login("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")
gemma7b = HuggingFaceHub(repo_id='google/gemma-1.1-7b-it')

def gemma7b_response(input_text,context,length):
    template = f"""
    ###context:{context},
    ###instruction:Please provide your response based solely on the information provided in the context and provide the complete answer.
    ###length: {length}
    ###question:{input_text},
    ###answer:
"""
    response = gemma7b(template).split("###answer:")[1]
    return response

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        speak("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"User said: {query}\n")                                                                           

    except Exception as e:
        speak('Say that again please...')
        query = 'error'
    return query

def classify_action(input_text):
    context = """
I want you to respond with the corresponding number just the number is needed,nothing else should be in the response
basically i will give a list of like questions give me the most similar question

List of Questions
What  is the time right now:1
What is the temperature right now:2
What is the weather right now:3
What is the news/current happenings:4
Play me a song from spotify:5
Play me a song from youtube:6
End of list of questions

If the questions doesnt like mean anything similar to all these questions then respond with Never answer with like a sentence only use the corresponding numbers
and any weird question not similar to any of thhese just answer 0
"""
    length="short"
    return gemma7b_response(input_text,context,length)

def get_response(input_text):
    context = """
The guy who is asking the question is a blind person who is using you inside the product Nanban
you are being used as a voice assistant to answer his queries please answer fully and carefully
please dont leave out any point even though its needs to be if its needed the answer  can always
be long also make sure to respond every question with words only avoid using symbols and numbers
if needed the numbers and symbols should be expressed in word form.
"""
    length = "as long as possible"
    response = gemma7b_response(input_text,context,length)
    clean_response = remove_unwanted_characters(response)
    speak(clean_response)
    
def remove_unwanted_characters(input_text):
    characters_to_remove = ["*",".","-","_",",",":","?","/",">","<","=","^","(",")","{","}","[","]"]

    for char in characters_to_remove:
        input_text = input_text.replace(char, "")
    return input_text

def speak(text, lang='en', output_file='speech.mp3'):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)
    os.system("mpg321 " + output_file)

client_id = 'b13fb24bbdc042e89f761a407c5fa189'
client_secret = '2a72ff62b0364b1ea881978e62ea7abe'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def spotify():
    query=""
    #Ask the user which song they want to hear
    speak("please confirm the song you want to hear")
    track = takecommand().lower()
        
    # Search for the song
    results = sp.search(q=track, limit=1)

    # Extract track details
    track = results['tracks']['items'][0]
    track_name = track['name']
    track_artist = track['artists'][0]['name']
    track_preview_url = track['preview_url']

    print(f"Now playing: {track_name} by {track_artist}")

    # If song has no preview URL, exit
    if track_preview_url is None:
        print("Sorry, the song cannot be played.")
        return

    song_content = AudioSegment.from_file(io.BytesIO(requests.get(track_preview_url).content))
    play(song_content)

def search_song():
    video=""
    speak("please confirm the video you want to hear")
    video = takecommand().lower()
        
    results = YoutubeSearch(video, max_results=1).to_dict()
    if results:
        video_id = results[0]['id']
        url = f"https://www.youtube.com/watch?v={video_id}"
        speak("Downloading  video...")
        download_audio(url)
        speak("Playing video...")
        play_song()
            
    else:
        speak("video not found")

def download_audio(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=".", filename="temp_song")

def play_song():
    song = AudioSegment.from_file("temp_song")
    play(song)

def latestnews():
    api_dict = {
        "business": "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=68412fb931c1440eab8524ba2128d068",
        "entertainment": "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=68412fb931c1440eab8524ba2128d068",
        "health": "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=68412fb931c1440eab8524ba2128d068",
        "science": "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=68412fb931c1440eab8524ba2128d068",
        "sports": "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=68412fb931c1440eab8524ba2128d068",
        "technology": "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=68412fb931c1440eab8524ba2128d068"
    }

    content = None
    url = None
    speak("Which field news do you want, [business], [health], [technology], [sports], [entertainment], [science]")
    news_read = False
    while news_read == False:
        field = takecommand()
        for key, value in api_dict.items():
            if key.lower() in field.lower():
                url = value
                news_read = True
            else:
                url = True
        if url is True:
            pass
        else:
            news = requests.get(url).text
            news = json.loads(news)
            speak("Here is the first news.")

            arts = news["articles"]

            for articles in arts:
                article = articles["title"]
                speak(article)

def get_time():
    strTime = datetime.datetime.now().strftime("%H:%M")
    speak(f"The current time is {strTime}")

def get_temperature():
    location = get_location()
    city = location['city']
    search = f"temperature in {city}"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp_value = data.find("div", class_="BNeawe").text
    speak(f"current {search} is {temp_value}")

def get_location():
    ipdata = requests.get(url).json()
    return ipdata

def voice_mode():
    query = takecommand().lower()
    
    if query=='error':
        return
        
    action = classify_action(query)
    
    if '0' in action:
        get_response(query)
    elif '1' in action:
        get_time()
    elif '2' in action:
        get_temperature()        
    elif '3' in action:
        pass
    elif '4' in action:
        latest_news()
    elif '5' in action:
        spotify()
    elif '6' in action:
       search_song()
