import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
import json

###############
### CLASSES ###
###############

class Launchable:
	def __init__(self, name):
		pass
	def open(self):
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


class Executable(Launchable):
	def __init__(self, name, filepath, args=''):
		self.name = name
		self.filepath = filepath
		self.args = args
	
	def open(self):
		subprocess.Popen([self.filepath, self.args])


#################
### FUNCTIONS ###
#################

### SAVING AND LOADING DATA ###

def save():
	with open(SAVE_FILE, mode='w', encoding='utf-8') as save_file:
		temp_categories = [encode_category(category) for category in categories]
		json.dump(temp_categories, save_file)


def encode_category(category):
	return {'name':category.name, 'launchables':[encode_launch(launch) for launch in category.launchables]}


def encode_launch(launch):
	if isinstance(launch, Executable):
		return {'class':'Executable', 'name':launch.name, 'filepath':launch.filepath, 'args':launch.args}
	else:
		raise TypeError(f"I don't know how to encode class '{type(launch)}' to json")


def load_categories():
	try:
		with open(SAVE_FILE, mode='r', encoding='utf-8') as save_file:
			temp_categories = json.load(save_file)
			categories = [decode_category(category) for category in temp_categories]

			if len(categories) == 0:
				return [Category('Main')]
			
			return categories
	except IOError:
		print(f"Can't load save file '{SAVE_FILE}'")
	except json.JSONDecodeError:
		print(f"Save file '{SAVE_FILE}' isn't in json format.")


def decode_category(category):
	return Category(category['name'], *[decode_launch(launch) for launch in category['launchables']])


def decode_launch(launch):
	if launch['class'] == 'Executable':
		return Executable(launch['name'], launch['filepath'], launch['args'])
	else:
		raise TypeError(f"I don't know how to decode json value of class '{launch['class']}'")

### UI LOGIC ###

## MAIN WINDOW ##

def starting_ui():
	root.geometry('600x450')

	options_frame = ttk.Frame(root)
	options_frame.pack(side=tk.RIGHT, anchor=tk.NE)

	# sort buttons
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
	ttk.Button(sort_order_frame, text='Asc', command = lambda: set_descending_sort(False)).pack(side=tk.LEFT)
	ttk.Button(sort_order_frame, text='Desc', command = lambda: set_descending_sort(True)).pack(side=tk.LEFT)
	sort_order_frame.pack(anchor=tk.W)

	# layout buttons
	layout_frame = ttk.Frame(options_frame)
	layout_frame['borderwidth'] = 5
	layout_frame['relief'] = 'sunken'
	ttk.Button(layout_frame, text='vertical', command=lambda: set_layout('vertical')).pack(side=tk.LEFT)
	ttk.Button(layout_frame, text='horizontal', command=lambda: set_layout('horizontal')).pack(side=tk.LEFT)
	layout_frame.pack(anchor=tk.W)

	
	add_category_btn = ttk.Button(category_frame, text='Add category', command=window_add_category)
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

def set_layout(change : str):
	global layout
	layout = change
	recreate_ui_data()


def recreate_ui_data():
	# reset container frame
	for child in categories_box.winfo_children():
		child.destroy()
	
	# add categories
	for index, category in enumerate(categories):
		cat_frame = ttk.LabelFrame(categories_box, text=category.name)
		options_frame = ttk.Frame(cat_frame)
		options_frame.pack(anchor=tk.NW)

		ttk.Button(options_frame, text='+', command=lambda category=category : window_add_launchable(category)).pack(side=tk.LEFT)
		ttk.Button(options_frame, text='Open All', command=lambda category=category : category.open_all()).pack(side=tk.LEFT)

		ui_add_launches(cat_frame, index, category)
		cat_frame.pack(anchor=tk.W)
	
	save()


def ui_add_launches(frame, category_index, category):
	sorted_launches = list(enumerate(category.launchables))
	launches_frame = ttk.Frame(frame)
	launches_frame.pack(anchor=tk.NW, pady=10)

	# sort launches in category
	if current_sort == 'newest' and not descending_sort:
		sorted_launches.reverse()
	elif current_sort == 'name':
		sorted_launches.sort(key=lambda launch: launch[1].name, reverse=descending_sort)
	
	# add every launch in category to frame
	for index, launch in sorted_launches:
		launch_button = ttk.Button(
			launches_frame,
			text=launch.name,
			command = lambda index=index : categories[category_index].launchables[index].open() )
		launch_button.pack(side=side_by_layout(), anchor=tk.NW, ipadx=10, ipady=10)

		menu = tk.Menu(root)
		menu.add_command(label = 'Delete', command = lambda index=index: [categories[category_index].launchables.pop(index), recreate_ui_data()])
		launch_button.bind('<Button-3>', lambda event, menu = menu: do_popup(event, menu))


# Return side option based on layout
def side_by_layout():
	if layout == 'horizontal':
		return tk.LEFT
	else:
		return tk.TOP


## POPUPS / OTHER WINDOWS ##

# Make popup from menu
def do_popup(event, menu):
	try:
		menu.tk_popup(event.x_root, event.y_root)
	finally:
		menu.grab_release()


def window_add_category():
	# Create window
	add_cat_window = tk.Toplevel(root)
	add_cat_window.geometry('200x100')
	
	# Name input
	ttk.Label(add_cat_window, text='Category name:').pack(anchor=tk.W)
	entry_name_text = tk.StringVar()
	ttk.Entry(add_cat_window, textvariable=entry_name_text).pack(anchor=tk.W)

	def create_category():
		new_category = Category(entry_name_text.get())
		categories.append(new_category)
		recreate_ui_data()
		cancel()
	

	def cancel():
		add_cat_window.destroy()


	# cancel and create buttons
	ttk.Button(add_cat_window, text='Cancel', command=cancel).pack(side=tk.LEFT, anchor=tk.NW)
	ttk.Button(add_cat_window, text='Create', command=create_category).pack(side=tk.LEFT, anchor=tk.NW)


def window_add_launchable(category):
	# Create window
	add_launch_window = tk.Toplevel(root)
	add_launch_window.geometry('350x450')

	# Create notebook
	notebook = ttk.Notebook(add_launch_window)
	notebook.pack(anchor=tk.N, expand=True)

	# Create executable creation form
	exec_frame = ttk.Frame(notebook, width=350, height=450)
	ui_executable(add_launch_window, exec_frame, category)
	exec_frame.pack(fill='both', expand=True)
	notebook.add(exec_frame, text='Executable')


def ui_executable(window, frame, category):
	options_frame = ttk.Frame(frame)
	buttons_frame = ttk.Frame(frame)
	options_frame.pack(fill='x')
	buttons_frame.pack(fill='x')

	# Name input
	ttk.Label(options_frame, text='Name').pack(anchor=tk.W, padx=20)
	entry_name_text = tk.StringVar()
	ttk.Entry(options_frame, textvariable=entry_name_text, width=50).pack(anchor=tk.W, padx=20)

	# EXE Filepath input
	ttk.Label(options_frame, text='Filepath').pack(anchor=tk.W, padx=20)
	entry_filepath_text = tk.StringVar()
	ttk.Button(options_frame, text='Choose file', command=lambda:write_filename_to_entry(entry_filepath_text)).pack(anchor=tk.W, padx=20)
	ttk.Entry(options_frame, textvariable=entry_filepath_text).pack(fill='x', padx=20, anchor=tk.W)

	# Arguments input
	ttk.Label(options_frame, text='Arguments').pack(anchor=tk.W, padx=20)
	entry_args_text = tk.StringVar()
	ttk.Entry(options_frame, textvariable=entry_args_text, width=50).pack(anchor=tk.W, padx=20)


	# Open file select and print selected file's path to entry
	def write_filename_to_entry(entry_text:tk.StringVar):
		entry_text.set(popup_select_file(exe=True))


	# Add executable to category
	def create_executable():
		new_exec = Executable(entry_name_text.get(), entry_filepath_text.get(), entry_args_text.get())
		category.add_launchables(new_exec)
		recreate_ui_data()
		cancel()
	

	# Cancel window
	def cancel():
		window.destroy()


	# create and cancel buttons
	ttk.Button(buttons_frame, text='Cancel', command=cancel).pack(padx=20, side=tk.LEFT)
	ttk.Button(buttons_frame, text='Create', command=create_executable).pack(side=tk.LEFT)


# Open popup of selecting a file
def popup_select_file(exe=False):
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


############
### MAIN ###
############
def main():
	global SAVE_FILE
	global root
	global categories
	global current_sort
	global descending_sort
	global layout
	global category_frame
	global categories_box

	SAVE_FILE = 'app_launcher_v2_savefile.json'

	current_sort = 'newest'
	descending_sort = True
	layout = 'vertical'

	categories = load_categories()

	root = tk.Tk()
	root.title('app-launcher')
	category_frame = ttk.Frame(root)
	categories_box = ttk.Frame(category_frame)

	starting_ui()

	recreate_ui_data()

	root.mainloop()

if __name__ == "__main__":
	main()