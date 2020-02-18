from tkinter import *
from imageProcessor import ImageProcessor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import urllib

class TkWindow:
    def __init__(self):
        self.isActive = False
        self.location = ""
        self.window = Tk()
        self.window.geometry(f'600x{self.window.winfo_screenheight() - 60}+{self.window.winfo_screenwidth()-600}+0')
        self.window.attributes('-topmost', True)

        # Used to remove the title tabs
        self.window.overrideredirect(1)
        self.create_widgets()
        self.window.withdraw()
        self.imageProcessor = ImageProcessor(self.get_dimensions())
    
    def create_widgets(self):
        self.text = Label(self.window, text = self.location)
        self.text.pack()
        
        self.fig = plt.Figure(figsize=(6, 6))
        self.a = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack()

    def get_dimensions(self):
        return {
            'height': self.window.winfo_screenheight(),
            'width': self.window.winfo_screenwidth()
        }

    def update_location(self):
        self.location = self.imageProcessor.process_screenshot('location')
        if len(self.location) != 0:
            self.text["text"] = self.location['UniqueName']
            self.window.after(400, self.update_location)
            ablionMap = self.getResponse(f"https://www.albiononline2d.com/en/map/api/nodes/{self.location['Index']}")['resourceNodes']
            self.a.scatter(ablionMap["origX"], ablionMap["origY"], color='red')
            self.canvas.draw()

    def getResponse(self, url):
        request = urllib.request.urlopen(url)
        if (request.getcode() == 200):
            data = request.read()
        return data
        
    def start_loop(self):
        self.update_location()
        self.window.mainloop()
        
    def toggle_visibility(self):
        self.isActive = not self.isActive
        self.window.deiconify() if self.isActive else self.window.withdraw()

    def destroy(self):
        self.window.destroy()