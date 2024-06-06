#speaking Agent
from openai import OpenAI
import os
from pydub import AudioSegment  
from pydub.playback import play 
from pydub.effects import speedup
from autogen import AssistantAgent, Agent
from typing import Union, Dict, Optional, List
from .VoiceChangerClient import initialize_voice_changer, use_voice_changer
from dotenv import load_dotenv

load_dotenv()

class SpeakingAgent(AssistantAgent):
    def __init__(self, name, llm_config: dict, **kwargs):
        self._voice = kwargs.pop('voice', None) or "alloy"
        self.base_voice_audioFile = kwargs.pop('base_voice', None)
        self.target_voice_audioFile = kwargs.pop('target_voice', None)
        self.instance_id = None
        if self.base_voice_audioFile and self.target_voice_audioFile and self._voice=="alloy":
            response = initialize_voice_changer(self.base_voice_audioFile, self.target_voice_audioFile)  # Initialize once
            self.instance_id = response
        super().__init__(name, llm_config=llm_config, **kwargs)

        try:
            config_list = llm_config["config_list"]
            api_key = config_list[0]["api_key"]
        except Exception as e:
            print("Unable to fetch API Key, because", e)
            api_key = os.getenv("OPENAI_API_KEY")
        self._openai_client = OpenAI(api_key=api_key)
        self._openai_model = "gpt-4o"
         
        # self.agent = 
        # self.register_reply([Agent, None], SpeakingAgent_autogen.speak)

    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        # override and always "silent" the send out message;
        # otherwise, the print log would be super long!
        super().send(message, recipient, request_reply, silent=False)

    def generate_reply(self, **kwargs):
        response = super().generate_reply(**kwargs)

        if response:
            relative_output_path = "./output.mp3"
            absolute_output_path = os.path.abspath(relative_output_path)
            audio_output_file_path = self.text2speech(response, absolute_output_path)
            self.play_audio_file(audio_output_file_path)
        return response

    def play_audio_file(self, file_path):
        # Play the audio file using pydub  
        audio = AudioSegment.from_file(file_path)
        final = speedup(audio, playback_speed=1.25)   
        play(audio)

    def text2speech(self, text, output_file_path):
        if self.instance_id:
            response = use_voice_changer(self.instance_id, text, output_file_path)
        else: 
            response = self._openai_client.audio.speech.create(
                model="tts-1",
                voice=self._voice,
                input=text,
            )

            response.stream_to_file(output_file_path)
        return output_file_path

    def speech2text(self, file_path):
        audio_file= open(file_path, "rb")
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return transcription

