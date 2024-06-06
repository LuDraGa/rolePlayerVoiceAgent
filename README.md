# VoiceCloneSpeakerAgent

## SpeakerAgent
Made a voice agent with autogen AssistantAgent

## VoiceCloner
Made a voice cloner with openvoice

## Flask Server Setup
Made a flask server for the voice cloner (openvoice requires Python 3.9, autogen requires Python 3.11)

## Combined Setup
Used them together to make:
- A speakerAgent which can clone any particular voice given an audio clip. 
    - Input required: Clean voice recording of target speaker. [>30s preferred]

### Installations
- VoiceClone
  - `conda create -n voiceclone python=3.9`
  - `conda activate voiceclone`
  - `git clone git@github.com:myshell-ai/OpenVoice.git`
  - `cd OpenVoice`
  - `pip install -e .`
- VoiceAgent
  - `conda create -n voiceagent python=3.11`
  - `conda activate voiceagent`
  - `pip install pyautogen`

### How to Run
- `/voiceClone` [SERVER: localhost:5000] using Python 3.9
    - `cd voiceClone`
    - `conda activate voiceclone`
    - `python3 main.py`
- `/VoiceAgents` using Python 3.11
    - `cd voiceAgents`
    - `conda activate voiceagent`
    - `python3 main.py`

## Pending
- Currently can take and work with only one base voice
    - The base voice is also used for TTS. [As we are currently using OpenAI API for TTS, which takes only a set of default inputs, the base voice will also use an audio clip of one of the same set of voices available]

## Flask Server methods

### init
- **Request:**
    - `base_voice`: base_speaker_audio <mp3 file of base tts voice>
    - `target_voice`: target_speaker_audio <mp3 file of target voice mapping>
- **Response:**
    - `instance_id`: instance_id

### speak
Given text speaks in the target voice
- **Request:**
    - `instance_id`: instance_id of the bot with our voice
    - `text`: text to speak
    - `output_file_path`: to save the speech audio
- **Response:**
    - `output_file_path`
