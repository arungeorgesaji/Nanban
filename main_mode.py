import os
import time
from ultralytics import YOLO
import subprocess
import openai
import cv2

openai.api_key = "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"

image_filename = os.path.join(os.path.expanduser("~/Documents/BLIND_PROJECT/"), "captured_image.jpg")
model = YOLO('yolov8x-seg.pt')

microphone_device_index = 2  

def initialize_camera_and_microphone():
    global cap, microphone
    cap = cv2.VideoCapture(0)
    microphone = cv2.VideoCapture(microphone_device_index)
    
def speak(audio):
    subprocess.call(['espeak', audio])

def scan_mode():
    initialize_camera_and_microphone()
    if not cap.isOpened():
        print("Error: Camera not found or could not be opened.")
        return

    try:
        ret, frame = cap.read()

        if ret:
            cv2.imwrite(image_filename, frame)
            print("Image captured and saved as", image_filename)
        else:
            print("Error: Could not capture an image.")
            return

        # Use the microphone to capture audio
        ret, audio_frame = microphone.read()

        results = model(frame)
        names = model.names
        input_words = []
        for r in results:
            for c in r.boxes.cls:
                input_words.append(names[int(c)])

        question = (
            "Explain the word with the top priority in the list "
            "(the one a blind would likely want to know about first ["
            + ', '.join(input_words)
            + "]) in a way a blind person would understand "
            "(highly descriptive and doesn't require much education to understand) "
            "but make sure to cut short it in a way it consists only one sentence or "
            "two at most (try to still keep the sentence highly understandable to a blind "
            "person and they don't need much education to understand it)."
        )

        output = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides descriptions to blind people."},
                {"role": "user", "content": question}
            ])

        response = output['choices'][0]['message']['content'].strip()
        speak(response)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        cap.release()
        microphone.release()
        cv2.destroyAllWindows()
