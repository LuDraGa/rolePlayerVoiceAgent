import requests

server_url = 'http://127.0.0.1:5000'
# Function to initialize a new VoiceChanger instance
def initialize_voice_changer(base_voice, target_voice):
    response = requests.post(f"{server_url}/init", json={'base_voice': base_voice, 'target_voice': target_voice})
    if response.status_code == 200:
        return response.json()['instance_id']
    else:
        print("Error initializing VoiceChanger:", response.json())
        return None

# Function to call the speak method of a VoiceChanger instance
def use_voice_changer(instance_id, text, output_path):
    response = requests.post(f"{server_url}/speak", json={'instance_id': instance_id, 'text': text, 'output_path': output_path})
    if response.status_code == 200:
        return response.json()['result']
    else:
        print("Error calling speak:", response.json())
        return None

