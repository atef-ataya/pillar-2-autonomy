import pyautogui
import time

print("Current mouse position:", pyautogui.position())
print("Screen size detected:", pyautogui.size())
print("\nMoving mouse to center of screen in 3 seconds...")
time.sleep(3)

screen_size = pyautogui.size()
center_x = screen_size[0] // 2
center_y = screen_size[1] // 2

print(f"Moving to: ({center_x}, {center_y})")
pyautogui.moveTo(center_x, center_y, duration=1)
print("Mouse should be at center now!")
