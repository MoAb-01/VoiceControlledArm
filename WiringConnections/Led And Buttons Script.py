#Lib: gpiozero, lgpio

from gpiozero import Button, RGBLED
from signal import pause
import time
import json
import os

CONFIG_FILE = 'config.json'

default_config = {
    "language_index": 0,
    "mode": "offline",
    "power": True 
}
############################################
Section 1: Config Loader (Save User changes)
############################################
def load_config():
    # Checks if file exists AND is not 0 bytes
    if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Config file corrupted. Loading defaults.")
            return default_config.copy()
    else:
        return default_config.copy()

def save_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


############################################
Section 2: Colors
############################################
languages = ["arabic", "english", "turkish", "french", "spanish"]

language_colors = {
    "arabic": (0, 1, 0),
    "english": (1, 1, 1),
    "turkish": (1, 0, 0),
    "french": (0, 0, 1),
    "spanish": (1, 1, 0)
}

mode_colors = {
    "offline": (0, 1, 1),
    "online": (0.5, 0, 0.5)
}


############################################
Section 3: Physical Pins Connections
############################################

# BUTTONS
# Connect one leg to the GPIO Pin, the other leg to Ground (GND).
lang_button = Button(17, hold_time=1)  # GPIO 17 = Physical Pin 11
mode_button = Button(27, hold_time=1)  # GPIO 27 = Physical Pin 13

# Connect R, G, B legs to the pins below:
led1 = RGBLED(
    red=5,     # GPIO 5  = Physical Pin 29
    green=6,   # GPIO 6  = Physical Pin 31
    blue=13    # GPIO 13 = Physical Pin 33
)

led2 = RGBLED(
    red=19,    # GPIO 19 = Physical Pin 35
    green=26,  # GPIO 26 = Physical Pin 37
    blue=21    # GPIO 21 = Physical Pin 40
)
############################################
Section 4: Config Loader
############################################

# Load config
config = load_config()
current_language_index = config["language_index"]
mode = config["mode"]
power_on = config["power"]

def update_leds():
    if power_on:
        language = languages[current_language_index]
        print(f"Status: ON | Lang: {language} | Mode: {mode}") 
        led1.color = language_colors[language]
        led2.color = mode_colors[mode]
    else:
        print("Status: Power OFF")
        led1.off()
        led2.off()
############################################
Section 4: Toggles and Events
############################################
def next_language():
    print("Language Button Pressed") # Debug text to verify button works
    global current_language_index
    current_language_index = (current_language_index + 1) % len(languages)
    config["language_index"] = current_language_index
    save_config()
    update_leds()

def toggle_mode():
    print("Mode Button Pressed") # Debug text to verify button works
    global mode
    mode = "online" if mode == "offline" else "offline"
    config["mode"] = mode
    save_config()
    update_leds()

def toggle_power():
    print("Power Toggle Held") 
    global power_on
    power_on = not power_on
    config["power"] = power_on
    save_config()
    update_leds()

# Button events
lang_button.when_pressed = next_language
mode_button.when_pressed = toggle_mode
mode_button.when_held = toggle_power  

# Initial LED state
update_leds()
############################################
Debugging And Errors
############################################

# --- MAIN LOOP ---
print("---------------------------------------")
print("Script initialized successfully!")
print("Press Ctrl+C to exit.")
print("---------------------------------------")

try:
    pause()
except KeyboardInterrupt:
    print("\nScript stopped by user (Success).")
