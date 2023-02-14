import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
import ctypes, sys, os
import json
import logging


### CLASSES ###

class Launchable:
	def __init__(self, name):
		pass
	def open(self):
		pass
	def encode(self):
		pass

class Category:
	def __init__(self, name, *launchables):
		self.launchables = list(launchables)
		self.name = name
	
	def add_launchables(self, *launchables):
		self.launchables.extend(launchables)
	
	def open_all(self):
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


### FUNCTIONS ###

def save():
	with open(SAVE_FILE, mode='w', encoding='utf-8') as save_file:
		temp_categories = [encode_category(category) for category in global_categories]
		json.dump(temp_categories, save_file)

def encode_category(category):
	return {'name':category.name, 'launchables':[encode_launch(launch) for launch in category.launchables]}

def encode_launch(launch):
	if isinstance(launch, Executable):
		return {'class':'Executable', 'name':launch.name, 'filepath':launch.filepath, 'args':launch.args}
	elif isinstance(launch, Command):
		return {'class':'Command', 'name':launch.name, 'executable':launch.executable, 'args':launch.args}
	else:
		raise TypeError(f"I don't know how to encode class '{type(launch)}' to json")

def load():
	global global_categories
	try:
		with open(SAVE_FILE, mode='r', encoding='utf-8') as save_file:
			temp_categories = json.load(save_file)
			global_categories = [decode_category(category) for category in temp_categories]
	except IOError:
		print(f"Can't load save file '{SAVE_FILE}'")
	except json.JSONDecodeError:
		print(f"Save file '{SAVE_FILE}' isn't in json format.")

def decode_category(category):
	return Category(category['name'], *[decode_launch(launch) for launch in category['launchables']])

def decode_launch(launch):
	if launch['class'] == 'Executable':
		return Executable(launch['name'], launch['filepath'], launch['args'])
	elif launch['class'] == 'Command':
		return Command(launch['name'], launch['executable'], launch['args'])
	else:
		raise TypeError(f"I don't know how to decode json value of class '{launch['class']}'")

def starting_ui():
	root.geometry('600x450')

	# sort buttons
	options_frame = ttk.Frame(root)
	options_frame.pack(side=tk.RIGHT, anchor=tk.NE)

	sort_type_frame = ttk.Frame(options_frame)
	sort_type_frame['borderwidth'] = 5
	sort_type_frame['relief'] = 'sunken'
	sort_btn = ttk.Button(sort_type_frame, text='Newest', command = lambda: set_current_sort('newest'))
	sort_btn.pack(side=tk.LEFT)
	sort_btn = ttk.Button(sort_type_frame, text='Name', command = lambda: set_current_sort('name'))
	sort_btn.pack(side=tk.LEFT)
	sort_type_frame.pack(anchor=tk.W)

	sort_order_frame = ttk.Frame(options_frame)
	sort_order_frame['borderwidth'] = 5
	sort_order_frame['relief'] = 'sunken'
	sort_order_btn = ttk.Button(sort_order_frame, text='Asc', command = lambda: set_descending_sort(False))
	sort_order_btn.pack(side=tk.LEFT)
	sort_order_btn = ttk.Button(sort_order_frame, text='Desc', command = lambda: set_descending_sort(True))
	sort_order_btn.pack(side=tk.LEFT)
	sort_order_frame.pack(anchor=tk.W)

	
	add_category_btn = ttk.Button(category_frame, text='Add category', command=add_category)
	add_category_btn.pack(anchor=tk.W)
	
	category_frame.pack(expand=True, fill='both', side=tk.LEFT)
	categories_box.pack(expand=True, fill='both')


def set_current_sort(change : str):
	global current_sort
	current_sort = change
	recreate_ui_data()

def set_descending_sort(change : bool):
	global descending_sort
	descending_sort = change
	recreate_ui_data()

def add_category():
	add_cat_window = tk.Toplevel(root)
	add_cat_window.geometry('200x100')
	
	ttk.Label(add_cat_window, text='Category name:').pack(anchor=tk.W)
	entry_name_text = tk.StringVar()
	ttk.Entry(add_cat_window, textvariable=entry_name_text).pack(anchor=tk.W)

	def create_category():
		new_category = Category(entry_name_text.get())
		global_categories.append(new_category)
		recreate_ui_data()
		cancel()
	

	def cancel():
		add_cat_window.destroy()


	ttk.Button(add_cat_window, text='Cancel', command=cancel).pack(side=tk.LEFT, anchor=tk.NW)
	ttk.Button(add_cat_window, text='Create', command=create_category).pack(side=tk.LEFT, anchor=tk.NW)


def recreate_ui_data():
	for child in categories_box.winfo_children():
		child.destroy()
	
	for index, category in enumerate(global_categories):
		cat_frame = ttk.LabelFrame(categories_box, text=category.name)

		ttk.Button(cat_frame, text='+', command=lambda category=category : add_launchable(category)).pack()
		ttk.Button(cat_frame, text='Open All', command=lambda category=category : category.open_all()).pack()

		ui_add_launches(cat_frame, index, category)
		cat_frame.pack(anchor=tk.W)
	
	save()


def ui_add_launches(frame, category_index, category):
	sorted_launches = list(enumerate(category.launchables))

	if current_sort == 'newest' and not descending_sort:
		sorted_launches.reverse()
	elif current_sort == 'name':
		sorted_launches.sort(key=lambda launch: launch[1].name, reverse=descending_sort)
	
	for index, launch in sorted_launches:
		launch_button = ttk.Button(
			frame,
			text=launch.name,
			command = lambda index=index : global_categories[category_index].launchables[index].open() )
		launch_button.pack()

		menu = tk.Menu(root)
		menu.add_command(label = 'Delete', command = lambda index=index: [global_categories[category_index].launchables.pop(index), recreate_ui_data()])
		launch_button.bind('<Button-3>', lambda event, menu = menu: do_popup(event, menu))


def do_popup(event, menu):
	try:
		menu.tk_popup(event.x_root, event.y_root)
	finally:
		menu.grab_release()


def add_launchable(category):
	add_launch_window = tk.Toplevel(root)
	add_launch_window.geometry('350x450')

	notebook = ttk.Notebook(add_launch_window)
	notebook.pack(anchor=tk.N, expand=True)

	exec_frame = ttk.Frame(notebook, width=350, height=450)
	ui_executable(add_launch_window, exec_frame, category)
	exec_frame.pack(fill='both', expand=True)

	notebook.add(exec_frame, text='Executable')

def ui_executable(window, frame, category):
	options_frame = ttk.Frame(frame)
	buttons_frame = ttk.Frame(frame)

	ttk.Label(options_frame, text='Name').pack(anchor=tk.W, padx=20)
	entry_name_text = tk.StringVar()
	ttk.Entry(options_frame, textvariable=entry_name_text, width=50).pack(anchor=tk.W, padx=20)

	ttk.Label(options_frame, text='Filepath').pack(anchor=tk.W, padx=20)
	entry_filepath_text = tk.StringVar()
	ttk.Button(options_frame, text='Choose file', command=lambda:write_filename_to_entry(entry_filepath_text)).pack(anchor=tk.W, padx=20)
	ttk.Entry(options_frame, textvariable=entry_filepath_text).pack(fill='x', padx=20, anchor=tk.W)

	ttk.Label(options_frame, text='Arguments').pack(anchor=tk.W, padx=20)
	entry_args_text = tk.StringVar()
	ttk.Entry(options_frame, textvariable=entry_args_text, width=50).pack(anchor=tk.W, padx=20)

	def write_filename_to_entry(entry_text:tk.StringVar):
		entry_text.set(select_file(exe=True))


	def create_executable():
		new_exec = Executable(entry_name_text.get(), entry_filepath_text.get(), entry_args_text.get())
		category.add_launchables(new_exec)
		recreate_ui_data()
		cancel()
	

	def cancel():
		window.destroy()


	ttk.Button(buttons_frame, text='Cancel', command=cancel).pack(padx=20, side=tk.LEFT)
	ttk.Button(buttons_frame, text='Create', command=create_executable).pack(side=tk.LEFT)
	
	options_frame.pack(fill='x')
	buttons_frame.pack(fill='x')

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
	
### MAIN ###

SAVE_FILE = 'app_launcher_v2_savefile.json'
global_categories = [Category('Main')]
current_sort = 'newest'
descending_sort = True

load()

root = tk.Tk()
root.title('app-launcher')
category_frame = ttk.Frame(root)
categories_box = ttk.Frame(category_frame)

starting_ui()

recreate_ui_data()

root.mainloop()