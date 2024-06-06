# VoiceCloneSpeakerAgent

## SpeakerAgent
Made a voice agent with autogen AssistantAgent.

## VoiceCloner
Made a voice cloner with openvoice.

## Flask Server
Made a flask server for the voice cloner (openvoice requires python 3.9, autogen requires python 3.11).

Used them together to make:
- **SpeakerAgent**: Can clone any particular voice given an audio clip.
  - **Input required**: Clean voice recording of target speaker. [>30s preferred]

### How to Run
- `/Users/abhiroopprasad/code/voiceClone` [SERVER: localhost:5000] `python3.9`
  - `conda activate openvoice`
  - `python3 main.py`
- `/Users/abhiroopprasad/code/VoiceAgents` `python3.11`
  - `conda activate autogenstudio`
  - `python3 main.py`

### Pending
- Currently can take and work with only one base voice
  - The base voice is also used for TTS. [As we are currently using OpenAI API for TTS, which takes only a set of default inputs, the base voice will also use an audio clip of one of the same set of voices available]

## Flask Server Endpoints

### init
- **Request**:
  ```json
  {
      "base_voice": "base_speaker_audio",
      "target_voice": "target_speaker_audio"
  }
