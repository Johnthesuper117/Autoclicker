import tkinter as tk
import threading
import time
from pynput import mouse, keyboard

class AutoClicker:
    def __init__(self):
        self.running = False
        self.delay = 1.0
        self.button = mouse.Button.left
        self.key = None
        self.stop_key = "f8"
        self.listener = None
        self.key_combination = None

    def start_clicking(self):
        while self.running:
            if self.key is not None:
                keyboard.Controller().press(self.key)
                keyboard.Controller().release(self.key)
            else:
                mouse.Controller().click(self.button)
            time.sleep(self.delay)

    def toggle(self, key):
        if self.key_combination is None:
            return

        if all(k in self.pressed_keys for k in self.key_combination):
            if self.running:
                self.running = False
                if self.listener:
                    self.listener.stop()
            else:
                self.running = True
                threading.Thread(target=self.start_clicking).start()

    def on_press(self, key):
        self.pressed_keys.add(key)
        self.toggle(key)

    def on_release(self, key):
        self.pressed_keys.discard(key)

    def start(self):
        self.pressed_keys = set()
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            self.listener.join()

class AutoClickerGUI:
    def __init__(self, root, autoclicker):
        self.autoclicker = autoclicker
        self.root = root
        self.root.title("AutoClicker")

        self.delay_label = tk.Label(root, text="Delay (seconds):")
        self.delay_label.pack()
        self.delay_entry = tk.Entry(root)
        self.delay_entry.pack()
        self.delay_entry.insert(0, "1.0")

        self.type_label = tk.Label(root, text="Type (mouse/key):")
        self.type_label.pack()
        self.type_var = tk.StringVar(value="mouse")
        self.type_mouse = tk.Radiobutton(root, text="Mouse", variable=self.type_var, value="mouse")
        self.type_mouse.pack()
        self.type_key = tk.Radiobutton(root, text="Key", variable=self.type_var, value="key")
        self.type_key.pack()

        self.button_label = tk.Label(root, text="Mouse Button (left/right):")
        self.button_label.pack()
        self.button_entry = tk.Entry(root)
        self.button_entry.pack()
        self.button_entry.insert(0, "left")

        self.key_label = tk.Label(root, text="Key (e.g., 'a', 'ctrl+z'):")
        self.key_label.pack()
        self.key_entry = tk.Entry(root)
        self.key_entry.pack()
        self.key_entry.insert(0, "")

        self.toggle_label = tk.Label(root, text="Toggle Key Combination (e.g., ctrl+z, alt+tab):")
        self.toggle_label.pack()
        self.toggle_entry = tk.Entry(root)
        self.toggle_entry.pack()
        self.toggle_entry.insert(0, "f8")

        self.start_button = tk.Button(root, text="Apply Settings", command=self.apply_settings)
        self.start_button.pack()

        self.info_label = tk.Label(root, text="Press the specified key combination to start/stop clicking")
        self.info_label.pack()

    def apply_settings(self):
        try:
            delay = float(self.delay_entry.get())
            input_type = self.type_var.get()
            button = self.button_entry.get().lower()
            key = self.key_entry.get().lower()
            toggle_key = self.toggle_entry.get().lower()

            self.autoclicker.delay = delay
            
            if input_type == "mouse":
                if button not in ["left", "right"]:
                    raise ValueError("Invalid mouse button")
                self.autoclicker.button = mouse.Button.left if button == "left" else mouse.Button.right
                self.autoclicker.key = None
            elif input_type == "key":
                self.autoclicker.button = None
                self.autoclicker.key = self.parse_key(key)
            else:
                raise ValueError("Invalid input type")

            self.autoclicker.key_combination = self.parse_key_combination(toggle_key)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
        except AttributeError as e:
            tk.messagebox.showerror("Error", f"Invalid key or toggle key: {key}")

    def parse_key(self, key):
        key_parts = key.split("+")
        if len(key_parts) == 1:
            return key_parts[0]
        else:
            return "+".join(key_parts)

    def parse_key_combination(self, key_combination):
        keys = key_combination.split("+")
        key_set = set()

        for key in keys:
            if key == "ctrl":
                key_set.add(keyboard.Key.ctrl)
            elif key == "shift":
                key_set.add(keyboard.Key.shift)
            elif key == "alt":
                key_set.add(keyboard.Key.alt)
            else:
                key_set.add(getattr(keyboard.Key, key, key))

        return key_set

if __name__ == "__main__":
    autoclicker = AutoClicker()
    root = tk.Tk()
    app = AutoClickerGUI(root, autoclicker)
    threading.Thread(target=autoclicker.start).start()
    root.mainloop()
