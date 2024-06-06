import os
import tkinter as tk


api_key = os.environ.get("OPEN_AI_KEY")
model = "gpt-4o"

def get_config(model=model, api_key=api_key, new_gpt_config={}):
    config_list = [
        {
            "model": model,
            "api_key": api_key,
        }
    ]

    gpt_config = {
        **new_gpt_config,
        "cache_seed": 42,  # change the cache_seed for different trials
        "temperature": 0,
        "config_list": config_list,
        "timeout": 120,
    }
    return config_list, gpt_config


def select_audio_file():
    # Create a Tkinter root window (it will remain hidden)
    root = tk.Tk()
    root.withdraw()

    # Open a file dialog and allow the user to select an audio file
    file_path = tk.filedialog.askopenfilename(
        title="Select an audio file",
        filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac")]
    )

    # Check if a file was selected
    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected.")