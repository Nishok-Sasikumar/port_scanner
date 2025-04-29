import socket
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import random

# --- Main window setup ---
root = tk.Tk()
root.title("HACKER PORT SCANNER")
root.attributes('-fullscreen', True)
root.configure(bg="#0f0f0f")

# --- Matrix Rain Background ---
class MatrixRain(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#0f0f0f", highlightthickness=0)
        self.chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()<>?/|\\'
        self.drops = []
        self.speed = 15
        self.font_size = 12
        self.column_width = 8

        self.bind("<Configure>", self.on_resize)
        self.after(33, self.animate)

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.create_drops()

    def create_drops(self):
        self.drops = []
        for _ in range(int(self.width / self.column_width)):
            x = random.randint(0, self.width)
            y = random.randint(-self.height, 0)
            self.drops.append((x, y))

    def animate(self):
        self.delete("char")
        for i, (x, y) in enumerate(self.drops):
            char = random.choice(self.chars)
            self.create_text(x, y, text=char, fill="#00ff00", font=("Courier", self.font_size), tags="char")
            self.drops[i] = (x, y + self.speed)
            if y > self.height:
                self.drops[i] = (random.randint(0, self.width), random.randint(-100, 0))
        self.after(30, self.animate)

matrix = MatrixRain(root)
matrix.pack(fill="both", expand=True)

# --- Frame for content ---
frame = tk.Frame(root, bg="#0f0f0f")
frame.place(relx=0.5, rely=0.1, anchor="n")

label = tk.Label(frame, text="Target IP Address:", font=("Courier", 18), bg="#0f0f0f", fg="#00ff00")
label.grid(row=0, column=0, pady=10, padx=10)

ip_entry = tk.Entry(frame, font=("Courier", 18), width=20)
ip_entry.grid(row=0, column=1, pady=10, padx=10)

start_button = tk.Button(frame, text="Start Scan", font=("Courier", 16, "bold"), bg="#00ff00", fg="#0f0f0f", command=lambda: threading.Thread(target=start_scan).start())
start_button.grid(row=0, column=2, padx=10)

# Progress bar
progress_bar = ttk.Progressbar(root, length=400, mode="determinate")
progress_bar.place(relx=0.5, rely=0.2, anchor="n")

# Result Text Box
result_box = scrolledtext.ScrolledText(root, font=("Courier", 12), width=120, height=25, bg="#0f0f0f", fg="#00ff00")
result_box.place(relx=0.5, rely=0.3, anchor="n")

# --- Flash random hacker messages ---
def flash_hacking_message():
    messages = [
        "ACCESS GRANTED ✅",
        "PORT HACKED 🔥",
        "BREACH DETECTED 🚨",
        "TARGET COMPROMISED 💀",
        "INTRUSION SUCCESSFUL 💻",
        "FIREWALL BYPASSED 🛡️",
        "SERVER BREACHED 📡",
    ]
    msg = random.choice(messages)

    flash_label = tk.Label(matrix, text=msg, font=("Courier New", 24, "bold"),
                           bg="#0f0f0f", fg="#00ff00")
    
    x_pos = random.uniform(0.2, 0.8)
    y_pos = random.uniform(0.1, 0.5)

    flash_label.place(relx=x_pos, rely=y_pos, anchor="center")
    root.after(800, flash_label.destroy)

# --- Port Scanning Functions ---
open_ports = []

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.05)
        result = s.connect_ex((target, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown Service"
            open_ports.append((port, service))
        s.close()
    except Exception as e:
        pass

def start_scan():
    target = ip_entry.get()
    if not target:
        return

    open_ports.clear()
    result_box.delete('1.0', tk.END)
    
    progress_bar["maximum"] = 1024
    progress_bar["value"] = 0

    threading.Thread(target=scan_ports, args=(target, 1, 1024)).start()

def scan_ports(target, start, end):
    count = 0
    for port in range(start, end + 1):
        scan_port(target, port)
        count += 1
        progress_bar["value"] = count
        root.update_idletasks()

        if random.randint(1, 25) == 5:  # Random flashy hacking text
            flash_hacking_message()

    display_open_ports()

def display_open_ports():
    if open_ports:
        result_box.insert(tk.END, "=== Open Ports and Services ===\n\n")
        for port, service in open_ports:
            result_box.insert(tk.END, f"[OPEN] Port {port} - {service}\n")
    else:
        result_box.insert(tk.END, "No open ports found!\n")

# --- Key Bindings ---
def exit_program(event=None):
    root.destroy()

root.bind('<Escape>', exit_program)

# --- Start the GUI ---
root.mainloop()
