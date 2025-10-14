from screenshot_handler import ScreenshotHandler
from ai_brain import VisionAI
from action_executor import ActionExecutor
import sys
import time

class AutonomyAgent:
    """Main agent orchestrator - See, Think, Act loop"""
    
    def __init__(self):
        self.screen = ScreenshotHandler()
        self.brain = VisionAI()
        self.hands = ActionExecutor()
        self.max_iterations = 25
    
    def run(self, task):
        """Execute a task autonomously"""
        print(f"\n{'='*60}")
        print(f"TASK: {task}")
        print(f"{'='*60}\n")
        
        for iteration in range(self.max_iterations):
            print(f"\n--- Iteration {iteration + 1} ---")
            
            try:
                # 1. SEE: Capture current screen state
                print("[AGENT] Taking screenshot...")
                screenshot_data = self.screen.capture_screen()
                
                # 2. THINK: Ask AI what to do next
                print("[AGENT] Analyzing screen and deciding action...")
                decision = self.brain.analyze_screen_and_decide(
                    screenshot_data, 
                    task
                )
                
                # 3. ACT: Execute the decision
                result = self.hands.execute(decision)
                
                # Check if task is complete
                if result.get("status") == "complete":
                    print(f"\n{'='*60}")
                    print(f"SUCCESS: {result['result']}")
                    print(f"{'='*60}\n")
                    return result['result']
                
                # Brief pause before next iteration
                time.sleep(1.5)
                
            except Exception as e:
                print(f"[ERROR] Iteration {iteration + 1} failed: {e}")
                continue
        
        print(f"\n[WARNING] Max iterations ({self.max_iterations}) reached")
        return "Task incomplete - max iterations exceeded"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python autonomy_agent.py '<task description>'")
        sys.exit(1)
    
    task = sys.argv[1]
    agent = AutonomyAgent()
    
    try:
        agent.run(task)
    except KeyboardInterrupt:
        print("\n\n[INFO] Agent stopped by user")
    except Exception as e:
        print(f"\n\n[FATAL ERROR] {e}")
