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
    search_results = search_google(input_text)
    location = get_location()
    city = location['city']
    country = location['country_name']
    local_time = get_time()
    template = f"""
    ###context:{context},
    ###instruction:Provide the complete answer,also you can use the search results which I have got for the same query but I cannot confirm its related please carefully access if its need and if its needed you can assist in providing the response to the user.Also make sure to use proper grammer and other characters as this is being read by a text to speech program also you are allowed to your own answer its not necessary you use the google results but for information like time and stuff which changes like you might not exactly know of right now please refer the search results and using that please provide trhe approprita answer in a human friendly way.Also you can use all the other informatioh provided if necessary.Please dont use unnecessary information and just respond with the information the user asked for 
    ###Search Results from Google for the Same Query: {search_results}
    ###Users country of origin : {country}
    ###Users city of origin : {city}
    ###Users local time: {local_time}
    ###length: {length}
    ###question:{input_text},
    ###answer:
"""
    response = gemma7b(template).split("###answer:")[1].split("**Answer:**")[0]
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
    print(response)
    clean_response = remove_unwanted_characters(response)
    speak(clean_response)
    
def remove_unwanted_characters(input_text):
    characters_to_remove = ["*","_",":","?","/",">","<","=","^","(",")","{","}","[","]"]

    for char in characters_to_remove:
        input_text = input_text.replace(char, "")
    return input_text

def speak(text, lang='en', output_file='speech.mp3'):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)
    os.system("mpg321 " + output_file)

client_id = 'b13fb24bbdc042e89f761a407c5fa189'
client_secret = '2a72ff62b0364b1ea881978e62ea7abe'

def search_song():
    while True:
        video=""
        speak("please confirm the song you want to hear or use exit to exit")
        video = takecommand().lower()
    
        if video=="error":
            continue
        elif video=="exit":
            speak("Exiting music mode")
            break

        results = YoutubeSearch(video, max_results=1).to_dict()
        if results:
            video_id = results[0]['id']
            url = f"https://www.youtube.com/watch?v={video_id}"
            speak("Downloading  song from youtube...")
            download_audio(url)
            speak("Playing song...")
            play_song()
            
        else:
           speak("song not found")

def download_audio(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=".", filename="temp_song")

def play_song():
    song = AudioSegment.from_file("temp_song")
    play(song)

def get_time():
    strTime = datetime.datetime.now().strftime("%H:%M")
    return strTime

def search_google(query, num_results=10):
    """
    Perform a Google search and return snippets of search results as a string.
    
    Args:
    - query: The search query.
    - num_results: Number of search results to retrieve (default is 10).
    
    Returns:
    - A string containing snippets of search results.
    """
    search_url = f"https://www.google.com/search?q={query}&num={num_results}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    snippets = []
    for result in soup.find_all('div', class_='tF2Cxc'):
        snippet = result.find('span', class_='aCOpRe').text
        snippets.append(snippet)
    
    return '\n'.join(snippets)

def get_location():
    ipdata = requests.get(url).json()
    return ipdata

def voice_mode():
    query = takecommand().lower()
    
    if query=='error':
        return
        
    if query=="music mode" or query=="music mod":
        search_song()                          
    else:
        get_response(query)

