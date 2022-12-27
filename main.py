import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
import ctypes, sys, os
import json
import logging

SAVE_FILE = 'app_launcher_savefile.json'
global_launches = []
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# subprocess.Popen([r'C:\Program Files\VideoLAN\VLC\vlc.exe', r'C:\Users\honza\Videos\2021-07-02 22-03-18.mkv'])

class Launchable:
    def __init__(self, name):
        pass
    def open(self):
        pass
    def encode(self):
        pass

class MultiLaunch(Launchable):
    def __init__(self, name, *launchables):
        self.launchables = launchables
        self.name = name
    
    def add_launchables(self, *launchables):
        self.launchables.extend(launchables)
    
    def open(self):
        for launchable in self.launchables:
            launchable.open()

class Command(Launchable):
    def __init__(self, name, executable, args:list):
        self.name = name
        self.executable = executable
        self.args = args
    
    def open(self):
        subprocess.Popen(self.args, shell=True,
            executable=self.executable,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

class Executable(Launchable):
    def __init__(self, name, filepath, args=''):
        self.name = name
        self.filepath = filepath
        self.args = args
    
    def open(self):
        subprocess.Popen([self.filepath, self.args])

def do_popup(event, menu):
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()

def select_file(exe=False):
    if exe:
        filetypes = (
            ('Executable files', '*.exe'),
            ('All files', '*.*') # z nějakého důvodu toto musí být
        )

        return filedialog.askopenfilename(
            title='Open an exe file',
            initialdir='/',
            filetypes=filetypes)
    else:
        return filedialog.askopenfilename()

def save_launches():
    with open(SAVE_FILE, mode='w', encoding='utf-8') as save_file:
        temp_launches = [encode_launch(launch) for launch in global_launches]
        json.dump(temp_launches, save_file)

def load_launches():
    global global_launches
    try:
        with open(SAVE_FILE, mode='r', encoding='utf-8') as save_file:
            temp_launches = json.load(save_file)
            global_launches = [decode_launch(x) for x in temp_launches]
    except IOError:
        logging.debug(f"Can't load save file '{SAVE_FILE}'")
    except json.JSONDecodeError:
        logging.debug(f"Save file '{SAVE_FILE}' isn't in json format.")
    finally:
        logging.debug(f"Successfully loaded save file '{SAVE_FILE}'")

def decode_launch(launch):
    if launch['class'] == 'Launchable':
        return MultiLaunch(launch['name'], [decode_launch(x) for x in launch['launchables']])
    elif launch['class'] == 'Executable':
        return Executable(launch['name'], launch['filepath'], launch['args'])
    elif launch['class'] == 'Command':
        return Command(launch['name'], launch['executable'], launch['args'])
    else:
        raise TypeError(f"I don't know how to decode json value of class '{launch['class']}'")

def encode_launch(launch):
    if isinstance(launch, MultiLaunch):
        return {'class':'Launch', 'launchables':[encode_launch(launchable) for launchable in launch['launchables']]}
    elif isinstance(launch, Executable):
        return {'class':'Executable', 'name':launch.name, 'filepath':launch.filepath, 'args':launch.args}
    elif isinstance(launch, Command):
        return {'class':'Command', 'name':launch.name, 'executable':launch.executable, 'args':launch.args}
    else:
        raise TypeError(f"I don't know how to encode class '{type(launch)}' to json")

def recreate_launches_ui():
    for child in launches_frame.winfo_children():
        child.destroy()
    
    for index, launch in enumerate(global_launches):
        launch_button = ttk.Button(
            launches_frame,
            text=launch.name,
            command = lambda index=index : global_launches[index].open() )
        launch_button.pack()
        menu = tk.Menu(root)
        menu.add_command(label = 'Delete', command = lambda index=index: [global_launches.pop(index), recreate_launches_ui()])
        launch_button.bind('<Button-3>', lambda event, menu = menu: do_popup(event, menu))
    
    if len(global_launches) > 0:
        save_launches()

def write_filename_to_entry(entry_text:tk.StringVar):
    entry_text.set(select_file(exe=True))

def open_add_exec_window():
    add_exec_window = tk.Toplevel(root)
    add_exec_window.geometry('350x450')

    options_frame = ttk.Frame(add_exec_window)
    buttons_frame = ttk.Frame(add_exec_window)

    ttk.Label(options_frame, text='Name').pack(anchor=tk.W, padx=20)
    entry_name_text = tk.StringVar()
    ttk.Entry(options_frame, textvariable=entry_name_text, width=50).pack(anchor=tk.W, padx=20)

    ttk.Label(options_frame, text='Filepath').pack(anchor=tk.W, padx=20)
    entry_filepath_text = tk.StringVar()
    ttk.Button(options_frame, text='Choose file', command=lambda:write_filename_to_entry(entry_filepath_text)).pack(anchor=tk.W, padx=20)
    ttk.Entry(options_frame, textvariable=entry_filepath_text).pack(fill='x', padx=20, anchor=tk.W)

    def create_executable():
        new_exec = Executable(entry_name_text.get(), entry_filepath_text.get())
        global_launches.append(new_exec)
        recreate_launches_ui()
        add_exec_window.destroy()
    
    def cancel():
        add_exec_window.destroy()

    ttk.Button(buttons_frame, text='Create', command=create_executable).pack(pady=50)
    ttk.Button(buttons_frame, text='Cancel', command=cancel).pack(pady=50)

    options_frame.pack(fill='x')
    buttons_frame.pack(fill='x')

def open_add_command_window():
    add_command_window = tk.Toplevel(root)
    add_command_window.geometry('350x450')

    options_frame = ttk.Frame(add_command_window)
    buttons_frame = ttk.Frame(add_command_window)

    ttk.Label(options_frame, text='Name').pack(anchor=tk.W, padx=20)
    entry_name_text = tk.StringVar()
    ttk.Entry(options_frame, textvariable=entry_name_text, width=50).pack(anchor=tk.W, padx=20)

    ttk.Label(options_frame, text='Executable path').pack(anchor=tk.W, padx=20)
    selected_executable = tk.StringVar()
    executables = (('PowerShell', 'powershell.exe'),
                   ('Windows Command Line', 'cmd.exe'),
                   ('Custom', 'custom'))

    entry_executable_path_text = tk.StringVar()
    entry_custom_text = ttk.Entry(options_frame, textvariable=entry_executable_path_text, state='disabled', width=50)

    def disable_custom(selected_executable, disable_widgets):
        if selected_executable.get() == 'custom':
            disable_widgets['state'] = 'normal' 
        else:
            disable_widgets['state'] = 'disabled'

    for executable in executables:
        ttk.Radiobutton(
            options_frame,
            text=executable[0],
            value=executable[1],
            variable=selected_executable,
            command=lambda: disable_custom(selected_executable, entry_custom_text)
        ).pack(anchor=tk.W, padx=20)
    
    entry_custom_text.pack(anchor=tk.W, padx=20)

    ttk.Label(options_frame, text='Command').pack(anchor=tk.W, padx=20)
    entry_command_text = tk.StringVar()
    ttk.Entry(options_frame, textvariable=entry_command_text).pack(fill='x', padx=20, anchor=tk.W)

    def create_command():
        executable = selected_executable.get()
        if selected_executable == None:
            executable = entry_executable_path_text.get()
        new_exec = Command(entry_name_text.get(),
                           executable=executable,
                           args=entry_command_text.get())
        global_launches.append(new_exec)
        recreate_launches_ui()
        add_command_window.destroy()
    
    def cancel():
        add_command_window.destroy()


    ttk.Button(buttons_frame, text='Create', command=create_command).pack(pady=50)
    ttk.Button(buttons_frame, text='Cancel', command=cancel).pack(pady=50)

    options_frame.pack(fill='x')
    buttons_frame.pack(fill='x')

# funguje
# subprocess.run('start cmd -Argument"/c timeout 5"', shell=True)
# TODO: pro powershell a bash


load_launches()


root = tk.Tk()
root.geometry('600x450')

add_button = ttk.Button(root, text='Add Executable', command=open_add_exec_window)
add_button.pack()
add_button = ttk.Button(root, text='Add Command', command=open_add_command_window)
add_button.pack()

launches_frame = ttk.Frame(root)
launches_frame.pack(expand=True, fill='both')

recreate_launches_ui()

root.mainloop()