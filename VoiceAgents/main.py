from utils import get_config, select_audio_file
from SpeakerAgent import SpeakingAgent
from autogen import UserProxyAgent



if __name__ == "__main__":
    config_list, gpt4_config = get_config()
    base_voice = select_audio_file("For base voice")
    
    
    target_voice_1 = select_audio_file("For superman")
    superman = SpeakingAgent(
        name="Superman",
        system_message="""
        Pretend to be Superman. Do not break character under any circumstances.
        Be consise(keep words to 20-30)
        """,
        voice="alloy",
        llm_config=gpt4_config,
        max_consecutive_auto_reply=2,
        base_voice=base_voice,
        target_voice=target_voice_1
    )

    target_voice_2 = select_audio_file("For batman")
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
        target_voice=target_voice_2
    )

    # Ask the question with an image
    result = batman.initiate_chat(
        superman,
        message="""Discuss the new superman movie.""",
    )