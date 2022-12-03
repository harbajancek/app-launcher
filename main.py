import tkinter as tk
from tkinter import ttk
import subprocess

# subprocess.Popen(r'C:\Program Files\VideoLAN\VLC\vlc.exe')
subprocess.Popen('start timeout 5', shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def return_pressed(event):
    print('Return key pressed.')

def log(event):
    print(event)


root = tk.Tk()

btn = ttk.Button(root, text='Save')
btn.bind('<Return>', return_pressed)
btn.bind('<Return>', log, add='+')


btn.focus()
btn.pack(expand=True)

root.mainloop()