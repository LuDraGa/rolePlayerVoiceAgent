from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
import os
import sys
from VoiceAgents.SpeakerAgent import SpeakingAgent
from VoiceAgents.utils import get_config

config_list, gpt4_config = get_config()

def createSpeakingAgent(name, system_message, target_voice, base_voice="/Users/abhiroopprasad/code/voiceCloneAgent/voiceClone/VoiceSnippets/alloy.mp3", speak=True):
    agent = SpeakingAgent(
        name=name,
        system_message=system_message,
        voice="alloy",
        llm_config=gpt4_config,
        max_consecutive_auto_reply=2,
        base_voice=base_voice if speak else None,
        target_voice=target_voice
    )
    if not speak:
        agent.mute()
    return agent

def createAssistantAgent(name, system_message, max_consecutive_auto_reply=2):
    agent = AssistantAgent(
        name=name,
        system_message=system_message,
        llm_config=gpt4_config,
        max_consecutive_auto_reply=max_consecutive_auto_reply
    )
    return agent


def createUserProxyAgent(system_message="A human admin"):
    return UserProxyAgent(
        name="Admin",
        system_message=system_message,
        code_execution_config=False,
        human_input_mode="NEVER"
    )

def createGroupChatAgent(agents, max_round=5, messages=[]):
    group_chat = GroupChat(agents=agents, messages=messages, max_round=max_round, send_introductions=True)
    group_chat_manager = GroupChatManager(groupchat=group_chat, llm_config=gpt4_config)
    return group_chat_manager

