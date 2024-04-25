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

def helpline(input_text):
    speak("please ask the questions you want and use exit to exit whenever you want")
    instruction = """
Please use the context to help you answer the question,the user is a blind person 
who is using nanban which a device running on the raspberry pi 5.You are being used in the nanban
helpline to help the use remember this guy is a blind person he might not be able to do a lot of things
he might not even know that a raspberry pi is inside dont go like display nanban doesnt have a display 
the complete communication is through voice remember you can use questions outside the context
these you could consider as some examples to get an idea of how to answer and if a similar 
question pops up you can easily answer.Please anwer to just what the user
asks dont try to do anything else
"""
    context = """
Question:Answer
Nanban has some bugs/problems:Please contact our support team for helping solve these issues
Nanban is not responding at all:
How can I tell if the device is turned on or off, and if it's receiving power properly:Its pretty difficult to tell if it is on or off but you can tell easily by checking for the sound of the fan
I've noticed unusual sounds or vibrations coming from the device. What could this indicate, and how should I proceed:This could be because of overheating and the fans speed increasing but you could contact some local electronics shop to check out if the raspberry pi has some issues or directly contact our support team
What steps can I take to ensure the device's buttons or controls are not stuck or damaged:
Are there any signs of wear and tear that I should look out for, which might point to a mechanical issue:Be careful for nanbans buttons responsiveness if it doesnt feel right maybe you could fix at a local electronics shop,if any issue happens and nothing seems to be working it could be a mechanical issue in this situation it would be good to contact the develope of Nanban arun at 7994800801
Can you provide verbal instructions or audio guides for troubleshooting common problems, like connecting to a new network or updating software:As of the current version of Nanban it doesnt support switching out the network or updating directly with commands so it might not be possible as of now if you want to do this please contact our support team
*Button Check:* Run your fingers over the physical buttons or touch-sensitive areas connected to the Raspberry Pi 5. Any unresponsiveness or irregularities could indicate a mechanical issue.
*Verbal Instructions for Troubleshooting:* Contact our support team for personalized verbal instructions or audio guides tailored to troubleshooting issues related to the Raspberry Pi 5.
*Sending for Repairs:* We can arrange for a courier service to pick up the eyewear from your location. Detailed instructions on safely packaging it for transit will be provided to ensure its safety during shipment.
*Managing Daily Tasks:* While awaiting repairs, consider using alternative vision assistance methods or devices. Reach out to friends, family, or community organizations for support if needed.
*Data Protection:* Before sending the eyewear for repairs, ensure to back up any important data stored on the device. If possible, reset the Raspberry Pi 5 to its factory settings to safeguard your personal information during the repair process.
I hated nanbans performance:We are very sorry for your inconveniance if your product is undamaged we accept returns though we keep 10 percent of the money you payed for buying Nanban so we can pay the courier service providers we hired
When is nanban help service free:We are free 24/7 for helping you out with any issues of nanban
*Battery Life Concerns:* How can I check the battery status of the eyewear, and what should I do if I suspect the battery is not holding a charge?:*Answer:* You can check the battery status by asking the device or navigating to the settings menu. If the battery seems to be draining quickly or not holding a charge, it may need replacement. Contact our support team for assistance in diagnosing and resolving battery-related issues.
*Software Updates:* How do I know if there are software updates available for the Raspberry Pi 5, and how can I install them without sight?:*Answer:* The device will notify you of available updates through audio prompts or tactile feedback. To install updates, follow verbal instructions provided by the device or contact our support team for assistance in navigating the update process.
Audio Output Issues:* What should I do if there's no sound coming from the eyewear's speakers or headphones connected to the Raspberry Pi 5?:*Answer:* First, ensure that the volume is turned up and that the device is not muted. If there's still no sound, check the connection between the Raspberry Pi 5 and the audio output device. If the issue persists, contact our support team for further troubleshooting steps.
*Hardware Expansion:* Can I connect additional peripherals or sensors to the Raspberry Pi 5 for enhanced functionality, and how would I do so?:*Answer:* Yes, the Raspberry Pi 5 supports various peripherals and sensors for expanded functionality. Contact our support team for guidance on compatible devices and instructions on how to connect them to the Raspberry Pi 5.:*Answer:* Yes, the Raspberry Pi 5 supports various peripherals and sensors for expanded functionality. Contact our support team for guidance on compatible devices and instructions on how to connect them to the Raspberry Pi 5.
*Overheating Concerns:* How can I prevent the Raspberry Pi 5 from overheating during prolonged use, and what are the signs of overheating to watch out for?:*Answer:* Ensure that the device is placed in a well-ventilated area to prevent overheating. Signs of overheating include sluggish performance or unexpected shutdowns. If you suspect overheating, allow the device to cool down and contact our support team for further assistance.
*Data Backup:* How can I back up important data stored on the Raspberry Pi 5, and what are the best practices for data backup and recovery?:*Answer:* You can back up data by transferring it to external storage devices or cloud storage services. Follow our support team's instructions for backing up and restoring data to ensure its safety and accessibility.
*Customization Options:* Can I customize the settings or interface of the eyewear to better suit my preferences, and how would I do so?:*Answer:* Yes, the device offers various customization options for adjusting settings and personalizing the interface. Contact our support team for guidance on accessing and modifying settings to meet your specific needs.
*Battery Management and Optimization:* How can I monitor the battery health of the eyewear's embedded battery system, and are there any advanced power management features available to optimize battery life?:*Answer:* The device includes a built-in battery health monitoring system accessible through the settings menu. Additionally, advanced power management features such as dynamic voltage and frequency scaling (DVFS) are utilized to optimize battery life based on usage patterns and environmental conditions. If you suspect battery degradation or need assistance in maximizing battery performance, contact our support team for personalized guidance and troubleshooting.
*Firmware Updates and Version Control:* In addition to software updates, how does the Raspberry Pi 5 handle firmware updates, and what measures are in place to ensure compatibility and stability across different firmware versions?:*Answer:* Firmware updates for the Raspberry Pi 5 are managed through a secure over-the-air (OTA) update mechanism, with each update accompanied by detailed release notes outlining changes and improvements. Version control systems are employed to track firmware revisions, ensuring backward and forward compatibility with hardware components and software applications. If you encounter any issues related to firmware updates or version compatibility, our support team can provide expert assistance and guidance.
How to use Naban:Nanban has three buttons one buttons allows you to switch between the modes,one which allows you to mute nanban and finally the last one which connected to the battery allows you to completely cutoff nanban with the mode switching switch you can switch between the modes in the first mdoe it will scan the surrounding and explain about the objects it finds in the second mode you can ask it questions and it will also be able to answer you you can also use music mode command to activate music where you can listen to music from youtube also with the help command you can enter helpline mode which can help you get answers to nanban specific troubleshooting and other answers
*Peripheral Integration and Expansion:* What expansion interfaces does the Raspberry Pi 5 support for connecting external peripherals and accessories, and are there any limitations or compatibility considerations to be aware of when integrating third-party hardware?:*Answer:* The Raspberry Pi 5 features a versatile array of expansion interfaces, including USB Type-C, HDMI, GPIO (General-Purpose Input/Output), I2C (Inter-Integrated Circuit), SPI (Serial Peripheral Interface), and UART (Universal Asynchronous Receiver-Transmitter). These interfaces support a wide range of external peripherals and accessories, including sensors, cameras, displays, and input devices. Our support team can provide comprehensive guidance on selecting compatible hardware, configuring interface settings, and troubleshooting integration issues to ensure seamless peripheral connectivity and functionality.
*Advanced Audio Configuration:* Can I configure advanced audio settings such as equalization, spatial audio processing, or surround sound on the eyewear, and how can I access and adjust these settings without visual feedback?
*Advanced Audio Configuration:*:*Answer:* Yes, the device offers advanced audio configuration options accessible through the audio settings menu. These settings include customizable equalizer presets, spatial audio processing algorithms, and surround sound simulation. Utilizing voice commands or tactile input gestures, you can navigate the audio settings menu and make adjustments according to your preferences. If you require assistance in fine-tuning audio settings or optimizing audio performance, our support team can provide detailed guidance and troubleshooting.
*Firmware Updates and Version Control:* In addition to software updates, how does the Raspberry Pi 5 handle firmware updates, and what measures are in place to ensure compatibility and stability across different firmware versions?:*Answer:* Firmware updates for the Raspberry Pi 5 are managed through a secure over-the-air (OTA) update mechanism, with each update accompanied by detailed release notes outlining changes and improvements. Version control systems are employed to track firmware revisions, ensuring backward and forward compatibility with hardware components and software applications. If you encounter any issues related to firmware updates or version compatibility, our support team can provide expert assistance and guidance.
*Thermal Management and Performance Optimization:* How does the Raspberry Pi 5 address thermal management challenges to maintain optimal operating temperatures during intensive computational tasks, and are there any performance tuning options available to maximize processing power without compromising stability?:*Answer:* The Raspberry Pi 5 employs advanced thermal management techniques, including passive and active cooling solutions, dynamic thermal throttling, and temperature-based frequency scaling, to regulate operating temperatures and prevent thermal throttling under load. Additionally, performance tuning options such as overclocking and voltage regulation are available for advanced users seeking to push the limits of the device's processing capabilities. Our support team can provide expert guidance on implementing thermal management strategies, optimizing performance settings, and mitigating potential stability issues associated with aggressive overclocking or voltage manipulation.
What battery cover does nanban use:Nanban uses a screwed battery cover
The battery being used in Nanban:3.7volt 38000mah lithium ion battery                                          
Could you explain how the eyewear device operates, especially regarding the role of the Raspberry Pi 5 as the controlling processor, its connectivity options, software stack, and integration with other hardware components? **Answer:** The eyewear device utilizes the Raspberry Pi 5 as its central processor, leveraging its multicore architecture, connectivity interfaces, and Linux-based operating system. The Raspberry Pi 5 coordinates various functionalities, including assistive technologies, accessibility features, and multimedia applications. It interfaces with sensors, audio peripherals, and display technologies to enhance user experience and accessibility. Through rigorous testing and validation, the device ensures compatibility, reliability, and accessibility across diverse hardware configurations and usage scenarios.
"""
    while True:
        query = takecommand().lower()
        template = f"""
    ###context:{context},
    ###Instruction: {instruction},
    ###length: as long as possible never stop in between this will cause confuse the blind person
    ###question:{query},
    ###answer:
    ````"""
        if query=="exit":
            speak("Exiting help mode")
            break
        else:
            print(template)
            response = gemma7b(template).split("###answer:")[1].split("**Answer:**")[0]
            clean_response = remove_unwanted_characters(response)
            print(clean_response)
            speak(clean_response)
            


def remove_unwanted_characters(input_text):
    characters_to_remove = ["*","_","?",">","<","=","^","(",")","{","}","[","]","#","'","#","`"]

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
    elif query=="help mode" or query=="help mod":
        helpline(query)
    else:
        get_response(query)

