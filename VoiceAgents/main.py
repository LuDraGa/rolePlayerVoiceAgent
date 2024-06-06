from utils import get_config, select_audio_file
from SpeakerAgent import SpeakingAgent
from autogen import UserProxyAgent



if __name__ == "__main__":
    config_list, gpt4_config = get_config()
    base_voice = "/Users/abhiroopprasad/code/voiceClone/VoiceSnippets/alloy.mp3"
    target_voice = select_audio_file()

    superman = SpeakingAgent(
        name="Superman",
        system_message="""
        Pretend to be Superman. Do not break character under any circumstances.
        Be consise(keep words to 20-30)
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
        Be consise(keep words to 20-30)
        """,
        voice="alloy",
        llm_config=gpt4_config,
        max_consecutive_auto_reply=2,
        base_voice=base_voice,
        target_voice=target_voice
    )

    user_proxy = UserProxyAgent(
        name="Admin",
        system_message="A human admin.",
        code_execution_config=False,
        llm_config=gpt4_config,
        human_input_mode="ALWAYS"
    )

    # Ask the question with an image
    result = batman.initiate_chat(
        superman,
        message="""Discuss the new superman movie.""",
    )