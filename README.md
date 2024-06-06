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
- Will also have to install 
    pydub
    flask
    openai
    torch

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

## Usage

If the speaking agent's voice is anything other than alloy, then the base OpenAI voice model named will be used (e.g., onyx, echo, etc.). 

- If the voice is alloy and any of `base_voice` or `target_voice` is not defined, then alloy is used.
- If the voice is alloy and both `base_voice` and `target_voice` are defined, then alloy is used as the voice.

For `base_voice`, use an audio clip of alloy.

```python
superman = SpeakingAgent(
    name="Superman",
    system_message="""
    Pretend to be Superman. Do not break character under any circumstances.
    Be concise (keep words to 20-30).
    """,
    voice="echo",
    llm_config=gpt4_config,
    max_consecutive_auto_reply=2,
    base_voice=base_voice,
    target_voice=target_voice
)

batman = SpeakingAgent(
    name="Batman",
    system_message="""
    Pretend to be Batman. Do not break character under any circumstances.
    Be concise (keep words to 20-30).
    """,
    voice="alloy",
    llm_config=gpt4_config,
    max_consecutive_auto_reply=2,
    base_voice=base_voice,
    target_voice=target_voice
)
