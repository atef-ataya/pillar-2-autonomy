from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

class VisionAI:
    """AI brain that sees and decides actions"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.conversation_history = []
    
    def analyze_screen_and_decide(self, screenshot_data, task_description):
        """Send screenshot to AI and get next action"""
        
        screenshot_base64 = screenshot_data['image']
        logical_size = screenshot_data['logical_size']
        
        system_prompt = f"""You are a desktop automation agent with vision capabilities.

SCREEN: {logical_size[0]}x{logical_size[1]} pixels

Your actions:
1. click(x, y) - Click at coordinates
2. press(key) - Press a key
3. type(text) - Type text
4. complete(result) - Task is TRULY finished

CRITICAL RULES:
- NEVER say complete until you SEE the final result on screen
- To open apps: Use Command+Space (Spotlight), type app name, press return
- After pressing return to open an app, WAIT to see if it actually opened
- If you just pressed return but don't see the app window yet, the task is NOT complete
- Only use "complete" when you can VISUALLY CONFIRM the task is done

For opening apps, use this workflow:
1. Press "command+space" to open Spotlight
2. Type the app name
3. Press "return"
4. WAIT and check next iteration - did the app window appear?
5. If no app window visible yet, try opening it again
6. Only after app is VISIBLY OPEN, proceed with the task

Return JSON:
{{
    "reasoning": "detailed observation - what do you SEE on screen right now?",
    "action": "click|press|type|complete",
    "x": <number>,
    "y": <number>,
    "key": "<string>",
    "text": "<string>",
    "result": "<string>"
}}
"""
        
        user_message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Task: {task_description}\n\nWhat do you SEE on screen RIGHT NOW? Describe the visible windows and UI elements. What should you do next?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{screenshot_base64}"
                    }
                }
            ]
        }
        
        self.conversation_history.append(user_message)
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + self.conversation_history,
            max_tokens=500,
            temperature=0.1
        )
        
        assistant_message = response.choices[0].message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        json_match = re.search(r'\{.*\}', assistant_message, re.DOTALL)
        if json_match:
            decision = json.loads(json_match.group())
            return decision
        else:
            raise ValueError(f"AI didn't return valid JSON: {assistant_message}")
