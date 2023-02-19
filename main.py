################################
# APP-LAUNCHER
# Jan Harbáček
# zimní semestr 2022/2023
# Programování 1 NPRG030
#################################

####################
### DEPENDENCIES ###
####################

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
import json

###############
### CLASSES ###
###############

# Základní třída pro něco spustitelného
class Launchable:
	def __init__(self, name):
		pass
	def open(self):
		pass


# Kategorie, která obsahuje pole spustitelných souborů a dokáže spustit
# všechny najednou
class Category:
	def __init__(self, name, *launchables):
		self.launchables = list(launchables)
		self.name = name
	
	def add_launchables(self, *launchables):
		self.launchables.extend(launchables)
	
	def open_all(self):
		for launchable in self.launchables:
			launchable.open()


# Speciální případ něčeho spustitelného - exe soubor s argumenty
# pomocí subprocess.Popen
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

# Uloží všechny kategorie dané globální proměnnou `categories` a 
# spustitelné soubory v něm do JSON formátu do souboru danou globální 
# proměnnou `save_file`
def save_categories():
	with open(SAVE_FILE, mode='w', encoding='utf-8') as save_file:
		temp_categories = [encode_category(category) for category in categories]
		json.dump(temp_categories, save_file)


# Zakóduje jednotlivou kategorii do JSON formátu
def encode_category(category : Category):
	return {'name':category.name, 'launchables':[encode_launch(launch) for launch in category.launchables]}


# Zakóduje jednotlivý spustitelný soubor do JSON formátu
# Pokud by existoval jiný typ spustitelného souboru, tak lze
# přidat další podmínku
def encode_launch(launch):
	if isinstance(launch, Executable):
		return {'class':'Executable', 'name':launch.name, 'filepath':launch.filepath, 'args':launch.args}
	else:
		raise TypeError(f"I don't know how to encode class '{type(launch)}' to json")


# Načte kategorie ze souboru daným globální proměnnou `save_file`
# do globální proměnné `categories`
# Pokud nelze načíst kategorie nebo je seznam prázdný, tak vrátí seznam se
# základní kategorií s jménem 'Main'
def load_categories():
	global categories
	try:
		with open(SAVE_FILE, mode='r', encoding='utf-8') as save_file:
			temp_categories = json.load(save_file)
			categories = [decode_category(category) for category in temp_categories]

			if len(categories) == 0:
				categories = [Category('Main')]
			
			return
	except IOError:
		print(f"Can't load save file '{SAVE_FILE}'")
	except json.JSONDecodeError:
		print(f"Save file '{SAVE_FILE}' isn't in json format.")

	categories = [Category('Main')]


# Dekóduje kategorii z JSON formátu do třídy `Category`
def decode_category(category : Category):
	return Category(category['name'], *[decode_launch(launch) for launch in category['launchables']])


# Dekóduje spustitelný soubor z JSON formátu do dané třídy
# Pokud by existoval jiný typ spustitelného souboru, tak lze
# přidat další podmínku
def decode_launch(launch):
	if launch['class'] == 'Executable':
		return Executable(launch['name'], launch['filepath'], launch['args'])
	else:
		raise TypeError(f"I don't know how to decode json value of class '{launch['class']}'")

### UI LOGIC ###

## MAIN WINDOW ##

# Vytvoří základní neměnný UI
def starting_ui():
	root.geometry('600x450')

	options_ui()
	category_ui()


# Vytvoří UI na pravé straně, kde jsou možnosti pro změnu rozhraní
# Vytvoří `options_frame`, přidá do něj tlačítka možností a přidá vše do `root`
def options_ui():
	options_frame = ttk.Frame(root)
	options_frame.pack(side=tk.RIGHT, anchor=tk.NE)

	sort_type_ui(options_frame)

	sort_order_ui(options_frame)

	layout_ui(options_frame)


# Vytvoří tlačítka pro změnu seřazení podle nějaké vlastnosti a
# přidá je do daného framu `options_frame`
def sort_type_ui(options_frame):
	sort_type_frame = ttk.Frame(options_frame)
	sort_type_frame['borderwidth'] = 5
	sort_type_frame['relief'] = 'sunken'
	sort_btn = ttk.Button(sort_type_frame, text='Newest', command = lambda: set_current_sort('newest'))
	sort_btn.pack(side=tk.LEFT)
	sort_btn = ttk.Button(sort_type_frame, text='Name', command = lambda: set_current_sort('name'))
	sort_btn.pack(side=tk.LEFT)
	sort_type_frame.pack(anchor=tk.W)


# Vytvoří tlačítka pro změnu seřazení vzestupně nebo sestupně a
# přidá je do daného framu `options_frame`
def sort_order_ui(options_frame):
	sort_order_frame = ttk.Frame(options_frame)
	sort_order_frame['borderwidth'] = 5
	sort_order_frame['relief'] = 'sunken'
	ttk.Button(sort_order_frame, text='Asc', command = lambda: set_descending_sort(False)).pack(side=tk.LEFT)
	ttk.Button(sort_order_frame, text='Desc', command = lambda: set_descending_sort(True)).pack(side=tk.LEFT)
	sort_order_frame.pack(anchor=tk.W)


# Vytvoří tlačítka pro změnu rozvržení spustitelných souborů v kategoriích a
# přidá je do daného framu `options_frame`
def layout_ui(options_frame):
	layout_frame = ttk.Frame(options_frame)
	layout_frame['borderwidth'] = 5
	layout_frame['relief'] = 'sunken'
	ttk.Button(layout_frame, text='Vertical', command=lambda: set_layout('vertical')).pack(side=tk.LEFT)
	ttk.Button(layout_frame, text='Horizontal', command=lambda: set_layout('horizontal')).pack(side=tk.LEFT)
	layout_frame.pack(anchor=tk.W)


# Změní nastavení pro seřazení podle vlastnosti: 
# změní globální proměnnou `current_sort` a provede změny rozvržení
def set_current_sort(change : str):
	global current_sort
	current_sort = change
	recreate_ui_data()


# Změní nastavení pro seřazení vzestupně nebo sestupně: 
# změní globální proměnnou `descending_sort` a provede změny rozvržení
def set_descending_sort(change : bool):
	global descending_sort
	descending_sort = change
	recreate_ui_data()


# Změní nastavení pro rozvržení spustitelných souborů v kategoriích: 
# změní globální proměnnou `descending_sort` a provede změny rozvržení
def set_layout(change : str):
	global layout
	layout = change
	recreate_ui_data()


# Vytvoří UI na levé straně, kde jsou rozložené kategorie a jejich spustitelné
# soubory s tlačítkem pro přidání kategorie
def category_ui():
	categories_frame = ttk.Frame(root)
	global categories_container
	categories_container = ttk.Frame(categories_frame)

	add_category_btn = ttk.Button(categories_frame, text='Add Category', command=window_add_category)
	add_category_btn.pack(anchor=tk.W)
	
	categories_frame.pack(expand=True, fill='both', side=tk.LEFT)
	categories_container.pack(expand=True, fill='both')


# Resetuje část, kde jsou umístěné kategorie a znova je přidá
# Toto slouží pro znovupřidání dat po změně
def recreate_ui_data():
	reset_frame(categories_container)

	ui_add_categories_to_frame(categories_container)
	
	save_categories()


# Zničí všechny elementy ve framu
def reset_frame(frame):
	for child in frame.winfo_children():
		child.destroy()


# Přidá UI kategorie do framu
def ui_add_categories_to_frame(frame):
	for index, category in enumerate(categories):
		ui_add_category_to_frame(frame, index, category)


# Přidá UI kategorii do framu
# Přidá tlačítka pro přidání spustitelného souboru, tlačítko pro spuštění
# všech spustitelných souborů v kategorii a odstranění kategorie
def ui_add_category_to_frame(frame, category_index, category):
	cat_frame = ttk.LabelFrame(frame, text=category.name)
	cat_frame.pack(anchor=tk.W)

	options_frame = ttk.Frame(cat_frame)
	options_frame.pack(anchor=tk.NW)

	ttk.Button(options_frame, text='Add', command=lambda category=category : window_add_launchable(category)).pack(side=tk.LEFT)
	ttk.Button(options_frame, text='Open All', command=lambda category=category : category.open_all()).pack(side=tk.LEFT)
	ttk.Button(options_frame, text='Delete', command=lambda category_index=category_index : delete_category(category_index)).pack(side=tk.LEFT)

	ui_add_launches_to_frame(cat_frame, category_index, category)


# Odstraní kategorii z globálního seznamu a resetuje ui
def delete_category(category_index):
	categories.pop(category_index)
	recreate_ui_data()


# Přidá do framu UI spustitelné soubory v kategorii
def ui_add_launches_to_frame(frame, category_index, category):
	launches_frame = ttk.Frame(frame)
	launches_frame.pack(anchor=tk.NW, pady=10)

	sorted_launches = sorted_indexed_launches_by_options(category.launchables)
	
	for index, launch in sorted_launches:
		ui_add_launch_to_frame(launches_frame, category_index, index, launch)


# Vrátí seřazené spustitelné soubory podle globálních nastavení s indexy podle
# původního seznamu
def sorted_indexed_launches_by_options(launches):
	sorted_launches = list(enumerate(launches))
	if current_sort == 'newest' and not descending_sort:
		sorted_launches.reverse()
	elif current_sort == 'name':
		sorted_launches.sort(key=lambda launch: launch[1].name, reverse=descending_sort)
	return sorted_launches


# Přidá do framu UI tlačítko pro spuštění spustitelného souboru
def ui_add_launch_to_frame(frame, category_index, launch_index, launch):
	launch_button = ttk.Button(
		frame,
		text=launch.name,
		command = lambda launch_index=launch_index : categories[category_index].launchables[launch_index].open() )
	launch_button.pack(side=side_by_layout(), anchor=tk.NW, ipadx=10, ipady=10)

	ui_add_menu_to_launch(launch_button, category_index, launch_index)

	
# Přidá k tlačítku spustitelného souboru menu, které se objeví po stisknutí
# pravého tlačítka, pomocí kterého lze spustitelný soubor odstranit z kategorie
def ui_add_menu_to_launch(launch_button, category_index, launch_index):
	menu = tk.Menu(root)
	menu.add_command(label = 'Delete', command = lambda launch_index=launch_index: [categories[category_index].launchables.pop(launch_index), recreate_ui_data()])
	launch_button.bind('<Button-3>', lambda event, menu = menu: do_popup(event, menu))


# Vrátí tkinter konstantu pro umístění elementu podle zvoleného nastavení layoutu
def side_by_layout():
	if layout == 'horizontal':
		return tk.LEFT
	else:
		return tk.TOP


## POPUPS / OTHER WINDOWS ##

# Vytvoří popup okno z menu elementu
def do_popup(event, menu):
	try:
		menu.tk_popup(event.x_root, event.y_root)
	finally:
		menu.grab_release()


# Vytvoří okno pro vytvoření nové kategorie
def window_add_category():
	# Vytvoření okna
	add_cat_window = tk.Toplevel(root)
	add_cat_window.geometry('200x100')
	
	# Vstup pro zadání jména kategorie
	ttk.Label(add_cat_window, text='Category name:').pack(anchor=tk.W)
	entry_name_text = tk.StringVar()
	ttk.Entry(add_cat_window, textvariable=entry_name_text).pack(anchor=tk.W)
	
	
	# Vytvoří kategorii, přetvoří UI a zničí okno
	def create_category():
		new_category = Category(entry_name_text.get())
		categories.append(new_category)
		recreate_ui_data()
		cancel_window(add_cat_window)


	# Tlačítka pro zrušení přidávání kategorie a vytvoření kategorie
	ttk.Button(add_cat_window, text='Cancel', command=lambda: cancel_window(add_cat_window)).pack(side=tk.LEFT, anchor=tk.NW)
	ttk.Button(add_cat_window, text='Create', command=create_category).pack(side=tk.LEFT, anchor=tk.NW)


# Vytvoří okno pro vytvoření nového spustitelného souboru do dané kategorie
def window_add_launchable(category):
	# Vytvoření okna
	add_launch_window = tk.Toplevel(root)
	add_launch_window.geometry('350x450')

	# Vytvoření notebook elementu pro případné další typy spustitelného souboru
	notebook = ttk.Notebook(add_launch_window)
	notebook.pack(anchor=tk.N, expand=True)

	# Vytvoření formuláře pro spustitelný soubor EXE
	exec_frame = ttk.Frame(notebook, width=350, height=450)
	ui_executable(add_launch_window, exec_frame, category)
	exec_frame.pack(fill='both', expand=True)
	notebook.add(exec_frame, text='Executable')


# Vytvoří formulář pro vytvoření spustitelného souboru EXE do dané kategorie
def ui_executable(window, frame, category):
	# Vytvoření podpůrných framů
	options_frame = ttk.Frame(frame)
	buttons_frame = ttk.Frame(frame)
	options_frame.pack(fill='x')
	buttons_frame.pack(fill='x')

	# Vstup pro zadání jména spustitelného souboru
	ttk.Label(options_frame, text='Name').pack(anchor=tk.W, padx=20)
	entry_name_text = tk.StringVar()
	ttk.Entry(options_frame, textvariable=entry_name_text, width=50).pack(anchor=tk.W, padx=20)

	# Vstup pro vyhledání či zadání cesty souboru
	ttk.Label(options_frame, text='Filepath').pack(anchor=tk.W, padx=20)
	entry_filepath_text = tk.StringVar()
	ttk.Button(options_frame, text='Choose file', command=lambda:write_filename_to_entry(entry_filepath_text)).pack(anchor=tk.W, padx=20)
	ttk.Entry(options_frame, textvariable=entry_filepath_text).pack(fill='x', padx=20, anchor=tk.W)

	# Vstup pro argumenty při spuštění souboru
	ttk.Label(options_frame, text='Arguments').pack(anchor=tk.W, padx=20)
	entry_args_text = tk.StringVar()
	ttk.Entry(options_frame, textvariable=entry_args_text, width=50).pack(anchor=tk.W, padx=20)


	# Přidá spustitelný soubor EXE do kategorie
	def create_executable():
		new_exec = Executable(entry_name_text.get(), entry_filepath_text.get(), entry_args_text.get())
		category.add_launchables(new_exec)
		recreate_ui_data()
		cancel_window(window)


	# Tlačítka pro zrušení přidávání kategorie a vytvoření kategorie
	ttk.Button(buttons_frame, text='Cancel', command=lambda: cancel_window(window)).pack(padx=20, side=tk.LEFT)
	ttk.Button(buttons_frame, text='Create', command=create_executable).pack(side=tk.LEFT)


# Otevře popup okno pro vybrání souboru
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


# Zničí okno
def cancel_window(window):
	window.destroy()


# Otevře popup okno pro vybrání souboru a
# zapíše zvolený soubor do daného StringVaru
def write_filename_to_entry(entry_text:tk.StringVar):
	entry_text.set(popup_select_file(exe=True))


############
### MAIN ###
############
def main():
	# globální proměnné
	global SAVE_FILE
	global root
	global categories
	global current_sort
	global descending_sort
	global layout
	global categories_container

	# počáteční proměnné v globálních proměnných
	SAVE_FILE = 'app_launcher_savefile.json'
	current_sort = 'newest'
	descending_sort = True
	layout = 'vertical'
	load_categories()

	# vytvoření základního okna
	root = tk.Tk()
	root.title('app-launcher')
	starting_ui()

	# integrovat data do UI
	recreate_ui_data()

	# zapnutí mainloop
	root.mainloop()

if __name__ == "__main__":
	main()