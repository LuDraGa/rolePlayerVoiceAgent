import re

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