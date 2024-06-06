import os
import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class VoiceChanger:
    def __init__(self, base_speaker_audio_examples, target_speaker_audio_examples):
        self.base_speaker_audio_file_path = base_speaker_audio_examples
        self.target_speaker_audio_file_path = target_speaker_audio_examples
        self._openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.base_speaker = "alloy"


        # INITIALIZATIONS
        self.ckpt_base = 'OpenVoice/checkpoints/base_speakers/EN'
        self.ckpt_converter = 'OpenVoice/checkpoints/converter'
        self.device="cuda:0" if torch.cuda.is_available() else "cpu"
        self.output_dir = 'outputs'
        self.base_se = None
        self.target_se = None
        self.base_speaker_output_path = f"{self.output_dir}/base_speaker_output.wav"
        self.target_speaker_output_path = f"{self.output_dir}/target_speaker_output.wav"

        self.tone_color_converter = ToneColorConverter(f'{self.ckpt_converter}/config.json', device=self.device)
        self.tone_color_converter.load_ckpt(f'{self.ckpt_converter}/checkpoint.pth')

        os.makedirs(self.output_dir, exist_ok=True)

    def get_tone_color_embedding(self, audio_file_path):
        speaker_embedding, audio_name = se_extractor.get_se(audio_file_path, self.tone_color_converter, target_dir='processed', vad=True)
        return speaker_embedding

    def base_speaker_tts(self, text, output_file_path):
        response = self._openai_client.audio.speech.create(
            model="tts-1",
            voice=self.base_speaker,
            input=text,
        )
        response.stream_to_file(output_file_path)
        return output_file_path
    
    def convert_tone(self, audio_file_path, output_file_path):
        self.tone_color_converter.convert(
            audio_src_path=audio_file_path, 
            src_se=self.base_se, 
            tgt_se=self.target_se, 
            output_path=output_file_path,
            message="@MyShell"
        )

    def speak(self, text, output_file_path):
        if not output_file_path:
            output_file_path = self.target_speaker_output_path

        if self.base_se is None:
            self.base_se = self.get_tone_color_embedding(self.base_speaker_audio_file_path)
        if self.target_se is None:
            self.target_se = self.get_tone_color_embedding(self.target_speaker_audio_file_path)

        self.base_speaker_tts(text, self.base_speaker_output_path)
        self.convert_tone(self.base_speaker_output_path, output_file_path)
        return output_file_path

