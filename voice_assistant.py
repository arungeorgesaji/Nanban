import subprocess
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup
import datetime
import json
import io
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import openai

openai.api_key = "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"

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"User said: {query}\n")

    except Exception as e:
        speak('Say that again please...')
        query = 'error'
    return query
 
def speak(audio):
    subprocess.call(['espeak', audio])
   
client_id = 'b13fb24bbdc042e89f761a407c5fa189'
client_secret = '2a72ff62b0364b1ea881978e62ea7abe'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_track_audio_features(track_id):
    return sp.audio_features(track_id)[0]

def get_similar_tracks(track_audio_features):
    results = sp.recommendations(seed_tracks=[track_audio_features['id']], limit=10)
    return results['tracks']

def play_track(track):
    preview_url = track['preview_url']

    if preview_url:
        response = requests.get(preview_url)
        audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
        play(audio)
    else:
        print("No preview available for this track.")

def music(track_name):
    results = sp.search(q=track_name, limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        print(f"Track found: {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")

        audio_features = get_track_audio_features(track['id'])

        similar_tracks = get_similar_tracks(audio_features)

        print("\nTop track:")

        if similar_tracks:
            top_track = similar_tracks[0]
            top_track_info = f"{top_track['name']} by {', '.join([artist['name'] for artist in top_track['artists']])}"
            print(top_track_info)
            play_track(top_track)
    else:
        print("No track found.")

def temp():
    search = "temperature in kerala"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    speak(f"current{search} is {temp}")

def time():
    strTime = datetime.datetime.now().strftime("%H:%M")
    speak(f"Sir, the time is {strTime}")

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
    news_read=False
    while news_read==False:
        field = takecommand()
        for key, value in api_dict.items():
            if key.lower() in field.lower():
                url = value
                news_read=True
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

    if query=='spotify':
        speak("please confirm the song you want to hear")
        track = takecommand().lower()
        music(track)

    elif query=='temperature':
        temp()

    elif query=='time':
        time()

    elif query=='news':
        latestnews()

    elif query == 'error':
        pass

    else:
        question = query + 'response like you are a normal person and a companion to this person'

        output = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides descriptions to blind people."},
                {"role": "user", "content": question}
            ])

        response = output['choices'][0]['message']['content'].strip()
        speak(response)

