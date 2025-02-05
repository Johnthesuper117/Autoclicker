import tkinter as tk
from tkinter import messagebox
from pynput.mouse import Button, Controller
from pynput.mouse import Listener as MouseListener
from threading import Thread
import time

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Autoclicker")
        
        # Variables
        self.clicking = False
        self.interval = tk.DoubleVar(value=0.1)  # Default interval 0.1 seconds
        self.mouse = Controller()
        
        # Create GUI Components
        self.create_widgets()
        
    def create_widgets(self):
        # Interval Label and Entry
        self.interval_label = tk.Label(self.root, text="Click Interval (seconds):")
        self.interval_label.pack()
        
        self.interval_entry = tk.Entry(self.root, textvariable=self.interval)
        self.interval_entry.pack()
        
        # Start Button
        self.start_button = tk.Button(self.root, text="Start", command=self.start_clicking)
        self.start_button.pack()
        
        # Stop Button
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_clicking)
        self.stop_button.pack()
        
        # Exit Button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack()
        
    def start_clicking(self):
        if not self.clicking:
            self.clicking = True
            self.thread = Thread(target=self.autoclick)
            self.thread.start()
            messagebox.showinfo("Autoclicker", "Autoclicker Started!")
        
    def stop_clicking(self):
        if self.clicking:
            self.clicking = False
            self.thread.join()
            messagebox.showinfo("Autoclicker", "Autoclicker Stopped!")
            
    def autoclick(self):
        while self.clicking:
            self.mouse.click(Button.left)
            time.sleep(self.interval.get())
        
    def exit_program(self):
        self.stop_clicking()
        self.root.destroy()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
