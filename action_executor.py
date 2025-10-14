import pyautogui
import time
import platform
import subprocess

class ActionExecutor:
    """Executes physical actions on the computer"""
    
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.2  # Shorter pause for faster double-click
    
    def execute(self, decision):
        """Execute the AI's decision"""
        action = decision.get("action")
        reasoning = decision.get("reasoning", "")
        
        print(f"[AGENT] {reasoning}")
        print(f"[ACTION] {action}")
        
        if action == "click":
            x = decision["x"]
            y = decision["y"]
            print(f"[ACTION] Single-clicking at ({x}, {y})")
            pyautogui.click(x, y)
            time.sleep(0.5)
            print("[ACTION] Now pressing return to open")
            pyautogui.press('return')
            time.sleep(1.5)
            
        elif action == "double_click":
            x = decision["x"]
            y = decision["y"]
            print(f"[ACTION] Double-clicking at ({x}, {y})")
            # Do two rapid clicks manually for better reliability
            pyautogui.click(x, y)
            time.sleep(0.05)  # Very short delay
            pyautogui.click(x, y)
            time.sleep(1.5)
            
        elif action == "type":
            text = decision["text"]
            print(f"[ACTION] Typing: {text}")
            pyautogui.write(text, interval=0.1)
            
        elif action == "press":
            key = decision["key"]
            print(f"[ACTION] Pressing: {key}")
            
            if key in ['return', 'enter']:
                pyautogui.press('return')
            elif platform.system() == 'Darwin' and '+' in key:
                if key == "command+space":
                    subprocess.run(['osascript', '-e', 'tell application "System Events" to keystroke space using command down'])
                else:
                    keys = key.split('+')
                    pyautogui.hotkey(*keys)
            else:
                pyautogui.press(key)
            
            time.sleep(0.8)
            
        elif action == "complete":
            result = decision.get("result", "Task completed")
            print(f"[COMPLETE] {result}")
            return {"status": "complete", "result": result}
        
        return {"status": "continue"}
