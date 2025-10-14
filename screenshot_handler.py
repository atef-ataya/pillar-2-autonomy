import pyautogui
from PIL import Image
import base64
from io import BytesIO
import platform

class ScreenshotHandler:
    """Captures and processes screenshots for AI vision"""
    
    def __init__(self):
        self.scale_factor = self._detect_scale_factor()
        print(f"[INFO] Display scale factor detected: {self.scale_factor}")
    
    def _detect_scale_factor(self):
        """Detect display scaling on macOS"""
        if platform.system() == 'Darwin':  # macOS
            try:
                # Try to detect retina/scaling
                from AppKit import NSScreen
                screen = NSScreen.mainScreen()
                backing_scale = screen.backingScaleFactor()
                return backing_scale
            except:
                # Fallback: compare logical vs physical pixels
                screenshot = pyautogui.screenshot()
                logical_size = pyautogui.size()
                actual_size = screenshot.size
                
                scale_x = actual_size[0] / logical_size[0]
                scale_y = actual_size[1] / logical_size[1]
                
                # Use average scale
                return (scale_x + scale_y) / 2
        return 1.0
    
    def capture_screen(self):
        """Take a screenshot and return as base64-encoded image with metadata"""
        # Capture the entire screen
        screenshot = pyautogui.screenshot()
        
        # Get actual dimensions
        actual_width, actual_height = screenshot.size
        logical_width, logical_height = pyautogui.size()
        
        # Resize for API efficiency
        max_dimension = 1920
        screenshot.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
        
        # Convert to base64 for OpenAI API
        buffered = BytesIO()
        screenshot.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            'image': img_base64,
            'actual_size': (actual_width, actual_height),
            'logical_size': (logical_width, logical_height),
            'scale_factor': self.scale_factor
        }
    
    def get_screen_dimensions(self):
        """Get current screen resolution"""
        return pyautogui.size()
