from utils import extract_result, append_to_file
from createAgents import createUserProxyAgent, createAssistantAgent, createSpeakingAgent, createGroupChatAgent
from agent_constants import persona_creator_contants
from VoiceAgents.utils import select_audio_file

def get_persona_prompt(persona_agent, user_proxy_agent, character_description):
    result = user_proxy.initiate_chat(
        persona_agent,
        message=f"Create a persona for the following: {character_description}",
        silent=True
    )
    if result:
        chat_messages = result.chat_history
        response_content = result.chat_history[1]["content"]
        persona_system_prompt = extract_result("persona_prompt", response_content)
        return persona_system_prompt
    else:
        return f"You are a method actor: Follow the following description for your character: {character_description} \n\n Do not break character under any circumstance"

if __name__ == "__main__":
    speak = False
    character_descriptions = {
        "batmanClone": 'Batman',
        "supermanClone": 'Superman',
        "matthewMcConaugheyClone": 'Matthey McConaughey'
    }
    user_proxy = createUserProxyAgent()
    persona_agent = createAssistantAgent(persona_creator_contants['name'], persona_creator_contants['system_message'], 1)
    
    persona_agents = []
    for index, (name, description) in enumerate(character_descriptions.items()):
        print(f"Creating persona for {name}")
        persona_prompt = get_persona_prompt(persona_agent, user_proxy, description)
        
        target_voice = None if not speak else select_audio_file(f"For the target voice for {description}")
        character = createSpeakingAgent(name, persona_prompt, target_voice, speak=speak)
        
        print(f"Done {name}: {character}")
        # character = createAssistantAgent(name, persona_prompt)
        persona_agents.append(character)

    print(persona_agents)
    messages = [
        {"role": "system", "content": "You are the group chat manager. A random group will be formed and we will start a movie script writing session. Help them write a script for a movie they are all in. It should be written in a story format. and presented like a read play. WIth scenes and entries and exits and each speaker emoboding the role they are playing to act out the script"},
        {"role": "assistant", "content": "OK."}
    ]
    groupChatAgent = createGroupChatAgent(agents=persona_agents, messages=[], max_round=5)

    chat_result = groupChatAgent.initiate_chat(
        persona_agents[0],
        messages=messages,
        message="""
        We will start a screenplay script writing game:
        
        This is a game of improv we will write a script for a movie that you are all in. 
        <format>
        It should be written in a story format.  
        Presented like a read play. With scenes and entries and exits and each speaker emboding the role they are playing to act out the script.
        </format>

        <rules>
        1. Each of you will write just one scene at a time(keep it tight, engrossing and succinct)[respond with just your scene to continue the story]
        2. Make it engaging and intriguing, while maintaing a good balance in the story line.
        3. Make sure the story is coherent and sensible.
        4. Every story ends in 6-7 scenes. so make sure it reaches a unforced, logical and creative end.
        5. Try to make the story engaging, cohesive, and creative. With a strong beginning, a great story and an amazing end.
        </Writing rules>

        <tips and tricks>
        the aim of the game is to keep it engaging and fun. So to do this we will
        - make the scene endings such that the continuation is open ended and the story could lead anywhere as the game progresses.
        - make the story fun and random, but make sure to maintain a sense of logical flow.
        </tips and tricks>
        Respond with just the scene you make
        """,
        summary_method="reflection_with_llm",
    )
    
    output_file = "results/readplay.md"
    with open(output_file, 'w') as file:
        pass  # This will create or truncate the file
    
    for message in chat_result.chat_history:
        append_to_file(message["content"], output_file)
    
    gca = {**groupChatAgent.__dict__}
    for key in gca.keys():
        print(key)

# x = """
#         <Review session>
#         Each of you will discuss and then give a critical review for the script that you wrote. 
#         We will only discuss the script and not make any changes now. After one round of reviews we are good to move on to the final phase.
#         </Review session>

#         <Final session>
#         In this phase we will finalize the script and make the final edits.
#         </Final session>

#         """,