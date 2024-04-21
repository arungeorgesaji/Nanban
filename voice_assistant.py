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

openai.api_key = ""

time = 'not_set'
strTime = 'not set'

def give_info_to_gpt():
    global temp, strTime
    search = "temperature in kerala"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp_value = data.find("div", class_="BNeawe").text
    temp = f"current {search} is {temp_value}"
    strTime = datetime.datetime.now().strftime("%H:%M")
    strTime = f"Sir, the time is {strTime}"

give_info_to_gpt()

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

def speak(text, lang='en', output_file='speech.mp3'):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)
    os.system("mpg321 " + output_file)

client_id = 'b13fb24bbdc042e89f761a407c5fa189'
client_secret = '2a72ff62b0364b1ea881978e62ea7abe'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def spotify(query):
    # Search for the song
    results = sp.search(q=query, limit=1)

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

def search_song(query):
    results = YoutubeSearch(query, max_results=1).to_dict()
    if results:
        video_id = results[0]['id']
        url = f"https://www.youtube.com/watch?v={video_id}"
        return url
    else:
        return None

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

def voice_mode():
    query = takecommand().lower()

    if query == 'spotify':
        speak("please confirm the song you want to hear")
        track = takecommand().lower()
        spotify(track)
    
    elif query == 'youtube':
        speak("please confirm the video you want to hear")
        track = takecommand().lower()
        url = search_song(track)
        
        if url:
            print("Downloading song...")
            download_audio(url)
            print("Playing song...")
            play_song()
            
        else:
            print("No results found for the given query.")

    elif query == 'news':
        latestnews()

    elif query == 'error':
        pass

    else:
        question = query + 'response like you are a normal person and a companion to this person'

        output = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides descriptions to blind people. Here are some information you might be able to assist with " + 
                'current temperature or weather is ' + temp + ' current time is ' + strTime + ' use these information incase user asks the user may hot ask for it but here it is just incase and if the use does not ask dont use it and respond normally like as assistant to a blind person '},
                {"role": "user", "content": question}
            ])

        response = output['choices'][0]['message']['content'].strip()
        speak(response)


