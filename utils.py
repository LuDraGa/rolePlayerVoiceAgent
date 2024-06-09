import re
import os

def extract_result(tagstring, raw_input_string):
    # Define the regex pattern to match the content within the <persona_prompt> tags
    pattern = f'<{tagstring}>(.*?)</{tagstring}>'
    
    # Search for the pattern in the input string
    match = re.search(pattern, raw_input_string, re.DOTALL)
    
    # Extract and return the matched content
    if match:
        return match.group(1).strip()
    else:
        return None

def append_to_file(message, filename):
    """
    Appends a list of messages to a markdown file. Creates the file if it does not exist.

    Parameters:
    messages (list of str): List of messages to be appended.
    filename (str): The name of the file to append the messages to.
    """
    with open(filename, 'a') as file:
        file.write(message)