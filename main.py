from utils import extract_result
from createAgents import createUserProxyAgent, createAssistantAgent, createSpeakingAgent, createGroupChatAgent
from agent_constants import persona_creator_contants
from VoiceAgents.utils import select_audio_file

def get_persona_prompt(persona_agent, user_proxy_agent, character_description):
    result = user_proxy.initiate_chat(
        persona_agent,
        message=f"Create a persona for the following: {character_description}",
        silent=False
    )
    if result:
        chat_messages = result.chat_history
        response_content = result.chat_history[1]["content"]
        persona_system_prompt = extract_result("persona_prompt", response_content)
        return persona_system_prompt
    else:
        return f"You are a method actor: Follow the following description for your character: {character_description} \n\n Do not break character under any circumstance"

if __name__ == "__main__":
    character_descriptions = {
        "batmanClone": 'Batman',
        "supermanClone": 'Superman',
        "matthewMcConaugheyClone": 'Matthey McConaughey'
    }
    user_proxy = createUserProxyAgent()
    persona_agent = createAssistantAgent(persona_creator_contants['name'], persona_creator_contants['system_message'], 1)
    
    persona_agents = []
    for index, (name, description) in enumerate(character_descriptions.items()):
        persona_prompt = get_persona_prompt(persona_agent, user_proxy, description)
        target_voice = select_audio_file(f"For the target voice for {description}")
        character = createSpeakingAgent(name, persona_prompt, target_voice)
        # character = createAssistantAgent(name, persona_prompt)
        persona_agents.append(character)

    print(persona_agents)
    messages = [
        {"role": "system", "content": "Let's start with introductions."},
        {"role": "assistant", "content": "OK."}
    ]
    groupChatAgent = createGroupChatAgent(agents=persona_agents, messages=[], max_round=10)

    chat_result = groupChatAgent.initiate_chat(
        persona_agents[0],
        messages=messages,
        message="Communicate to know each other better to become best friends",
        summary_method="reflection_with_llm",
    )
    
    

