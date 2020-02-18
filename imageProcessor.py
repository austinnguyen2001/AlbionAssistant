from PIL import Image, ImageGrab
import pytesseract
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

class ImageProcessor:
    def __init__(self, args):
        self.args = args
        with open('world.json') as f:
            self.data = json.load(f)
    
    def process_screenshot(self, args):
        if args == 'location':
            screenshot = ImageGrab.grab(bbox=(self.args['width'] - 260, self.args['height'] - 45, self.args['width'] - 70, self.args['height'] - 15))
            text = pytesseract.image_to_string(screenshot)
            
            matches = [loc for loc in self.data if loc['UniqueName'] in text]
            if matches: bestMatch = max(matches, key=lambda loc: len(loc['UniqueName']))
            else: bestMatch = ""
            return bestMatch
            
        return ""

