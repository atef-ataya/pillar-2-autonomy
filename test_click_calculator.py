import pyautogui
import time

print("In 3 seconds, will click at (640, 360) - center of screen")
print("This should click the Calculator icon if it's centered")
time.sleep(3)

print("Clicking now...")
pyautogui.click(640, 360)
print("Click completed!")

time.sleep(1)
print("\nTrying double-click...")
pyautogui.doubleClick(640, 360)
print("Double-click completed!")
