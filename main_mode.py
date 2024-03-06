import os
from ultralytics import YOLO
from gtts import gTTS
import math
import yaml
import cv2

focal_length = 790
sensor_width = 3.63
image_filename = os.path.join(os.path.expanduser("~/Documents/Blind_Linux/"), "captured_image.jpg")
model = YOLO('models/yolov8m-seg.pt')

def calculate_distance(sensor_width, focal_length, object_pixel_width, screen_pixel_width, true_width):
    # Calculate FOV
    fov = 2 * math.atan(0.5 * sensor_width / focal_length)

    # Calculate angle of arc
    angle_of_arc = fov * (object_pixel_width / screen_pixel_width)

    # Calculate true distance
    true_distance = (true_width / 2) / math.tan(angle_of_arc / 2)

    return true_distance / 240

def speak(text, lang='en', output_file='speech.mp3'):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)
    os.system("mpg321 " + output_file)

def load_object_widths(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return data

object_widths = load_object_widths("/home/arun/Documents/Blind_Linux/width.yaml")
    
def check_location(x_min, y_min, x_max, y_max, frame_width, frame_height):
    # Calculate the center of the object
    object_center_x = (x_min + x_max) // 2
    object_center_y = (y_min + y_max) // 2
    
    # Calculate the center of the frame
    frame_center_x = frame_width // 2
    frame_center_y = frame_height // 2
    
    # Calculate the margin of error
    margin_of_error = 10
    
    # Check the position of the object
    if object_center_x < frame_center_x - margin_of_error:
        return "left"
    elif object_center_x > frame_center_x + margin_of_error:
        return "right"
    else:
        return "front"

def scan_mode():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite(image_filename, frame)
        frame = cv2.imread(image_filename)

        if frame is None:
            print("Error: Unable to load image.")
            return

        results = model(frame)
        names = model.names
        frame_height, frame_width, _ = frame.shape
        
        for result in results:
            for box in result.boxes:
                coordinates = box.xyxy
                name = names[int(box.cls)]
                x_min, y_min, x_max, y_max = coordinates[0][0].item(),coordinates[0][1].item(),coordinates[0][2].item(),coordinates[0][3].item()
                position = check_location(int(x_min), int(y_min), int(x_max), int(y_max), frame_width, frame_height)
                if name in object_widths:
                    true_width = object_widths[name]  # Get the width from the YAML file
                    distance = calculate_distance(sensor_width, focal_length, int(x_max)-int(x_min), frame_width, true_width)
                    message = f"There is a {name}, around {distance:.2f} centimeters away and it is in your {position}."
                    speak(message)
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

