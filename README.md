# Nanban

Nanban is a device designed to aid the visually impaired by scanning its surroundings and providing auditory feedback to the user. It is built using the Raspberry Pi platform and incorporates object detection, distance measurement, and voice assistant capabilities.

## Introduction
Nanban is a versatile device equipped with features to assist the visually impaired in navigating their surroundings and accessing useful information. With its object detection mode and voice assistant mode, users can interact with the device to gain awareness of their environment and receive helpful insights.

## Features
### Object Detection Mode
- Nanban utilizes a camera to detect objects in the user's surroundings.
- Distance measurement functionality provides approximate distances to detected objects using predetermined average widths and the object pixel width which is provided by YOLOv8.
- Mathematical equations, including trigonometric calculations, are employed for distance approximation.

### Voice Assistant Mode
- Users can switch to voice assistant mode to access various functionalities:
  - Get current time, temperature, and news updates.
  - Access YouTube for audio playback.
  - Interact with a friendly and emotionally bonding assistant.

### Hardware
- Raspberry Pi is the primary hardware platform used for Nanban.
- Two switches are integrated into the device for mode switching and volume control.

## Files
- **main.py**: Main file responsible for running the Nanban device.
- **main_mode.py**: Implements the object detection mode functionality.
- **voice_assistant_mode.py**: Implements the voice assistant mode functionality.
- **widths.yaml**: Contains predetermined average widths of objects for distance measurements.
- **pulse.py**: Manages the second switch, controlling volume and program pausing/resuming.
- **Nanban_launcher.desktop**: Allows the launch of Nanban on the startup of Raspberry Pi.

## Usage
To use Nanban, follow these steps:
1. Connect the Raspberry Pi to necessary peripherals (camera, switches, etc.).
2. Run the `main.py` file to start the Nanban device.
3. Switch between object detection mode and voice assistant mode using the designated switches.
4. Interact with Nanban to receive auditory feedback and assistance.

## Future Development
The Nanban project is an ongoing effort, and future developments may include:
- Refinement of object detection algorithms for improved accuracy.
- Integration of additional voice assistant functionalities.
- Enhancement of user interface and accessibility features.

##Installation
1.Clone the repository:

    git clone https://github.com/arungeorgesaji/Nanban.git

2.Install Packages:

    pip install gpiozero pulsectl ultralytics gtts opencv-python pyyaml spotipy requests beautifulsoup4 pytube youtube-search-python pydub SpeechRecognition openai==0.28 keyboard youtube-dl

3.Make nanban run on startup:

- Move the Nanban_launcher.desktop into .config/autostart(create autostart if it does not exist also .config is hidden folder)
- Change the path given inside the Nanban_launcher.desktop to represent the correct path to main.py inside the cloned folded named Nanban
- Now reboot for the changes to take effect

    
