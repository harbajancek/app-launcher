# Dokumentace aplikace app-launcher

Jan Harbáček\
únor 2023

## Zadání

Zadání je aplikace, přes které lze spustit jiné aplikace. V aplikaci by mělo přidat spustitelný soubor, který po kliknutí na dané tlačítko daný soubor spustí.

Aplikace má dále umět:

- třízení vložených souborů podle různých vlastností
- kategorizovat vložené soubory do různých škatůlků
- spustit více souborů najednou
- různé módy rozložení ikon spustitelných souborů
- možnost spustit jako administrátor
- argumenty pro spuštění, např. spuštění daného videa pomocí aplikace na přehrávání videí

Aplikace je napsaná v Tkinteru, což je knihovna pro grafické rozhraní nejen pro Python.

## Popis chování programu

Ihned po prvním spuštění se objeví okno rozdělené na dvě části. V levé části se nachází spustitelné ikony v jednotlivých kategoriích. Kategorie, podle názvu, kategorizují jednotlivé spustitelné ikony do jmenovaných škatulek. Lze pomocí nich také spustit všechny soubory v dané kategorii.

### Kategorie

Tlačítko `Add Category` spustí popup okno, pomocí jěhož lze přidat novou kategorii do programu. V okně lze vyplnit jméno a při kliknutí tlačítka `Create` kategorii s daným jménem vytvoří a přidá do programu. Tlačítko `Cancel` slouží pro zrušení přidávání kategorie a zničení okna.

Při prvním spuštění je automaticky vytvořená kategorie s názvem **Main**. Pod touto kategorií lze vidět tři tlačítka: `Add`, `Open All` a `Delete`.

### Spustitelný soubor / ikona

Tlačítko `Add` spustí další popup okno, pomocí jehož lze přidat nový spustitelný soubor. Program ukáže formulář se třemi vstupy.

Do prvního lze napsat jméno spustitelného souboru, který se objeví na ikoně pro spuštění souboru.

Další vstup je pro cestu k souboru. Lze jej přidat ručně nebo je nad vstupem tlačítko, které spustí klasické vyhledání souboru. Je nastavený tak, aby ukazoval pouze soubory s příponou **.exe** a složky. Po vybrání souboru se zkopíruje jeho adresa do vstupu.

Třetí vstup je pro argumenty při spuštení souboru. To lze použít pro více specializované spuštění programu. Například pokud vyberete program VLC, program pro pouštení videí, a do argumentů zkopírujete cestu k videu, tak se program spustí a automaticky spustí i dané video.

Podobně jako pro okno pro přidání kategorie se pak dole nachází tlačítka pro přidání ikony do kategorie a případné zrušení přidávání.

Po přidání spustitelného souboru se u dané kategorie objeví tlačítko/ikona s názvem, který se mu zadal ve formuláři. Pokud se na něj klikne levým tlačítkem, tak soubor spustí. Pokud se na něj klikne pravým tlačítkem, objeví se popup menu s jednou možností: `Delete`. Pokud se na něj klikne levým tlačítkem, tak daný spustitelný soubor odstraní z kategorie. Pokud se klikne jinam, tak menu zmizí.

### Ukládání stavu

Při každé změně, přidání a odstranění kategorie nebo ikony se uloží stav/data do souboru `app_launcher_savefile.json` ve stejné složce, jako je spuštěný program. Pomocí jeho si program pamatuje stav kategorií a ikon tak, aby se při dalším spuštění načetli tak, jak byly před zavřením programu.

Program si data ukládá v JSON formátu. Ukládá si seznam kategorií, jejich jména a všechny jejich ikony, také jména a ještě cesty k souborům a argumenty pro spuštění.

### Nastavení programu

Při přidání více spustitelných souborů se může hodit změna rozvržení a seřazení ikon. Na to slouží pravá část hlavního okna. Nachází se zde tři hlavní nastavení. První je typ seřazení, druhý uspořádání seřazení a třetí mód rozvržení. Když se spustí jakékoliv z tlačítek, tak se změní dané nastavení, pokud se nespustila možnost, která je aktuální.

Typ seřazení určuje, podle čeho se ikony budou seřazovat; buď podle jména nebo podle nejnověji přidané. Uspořádání seřazení určuje, pokud budou ikony seřazeny vzestupně nebo sestupně. Mód rozvržení určuje, pokud se ikony zobrazí vedle sebe vertikálně nebo horizontálně.

Při každém spuštění programu je výchozí nastavení: seřazení podle nejnověji přidaného, uspořádání sestupně a mód rozvržení horizontálně.

## Popis řešení programu

### Knihovny

Aplikace používá pouze knihovny již nainstalované současně s Pythonem. Používá knihovnu `tkinter` pro vytvoření okenní aplikace, knihovnu `subprocess` pro spouštění **.exe** souborů a knihovnu `json` pro ukládání dat do řetězce.

### Globální nastavení a proměnné

Aplikace pracuje s několika globálními proměnnými. Každá určuje nějaký stav aplikace nebo ukládá data relevantní pro celý projekt.

Zde je výčet všech globálních proměnných a jejich účel:

- `SAVE_FILE:str` určuje cestu k souboru z místa spuštění aplikace, do kterého se uloží a z kterého se načtou data. Výchozí hodnota je *app_launcher_savefile.json*.
- `root:tk.Tk` obsahuje  základní okno aplikace. Slouží to pro přidávání prvků, framů a oken.
- `categories:list` obsahuje data kategorií. Obsahuje všechna uložitelná data.
- `current_sort:str` obsahuje pracovní název pro atribut, podle kterého program třídí na ikony v kategoriích. Toto platí pouze pro rozhraní, aplikace třídí jenom kopii a ne samotné ikony v kategorii.
  - V současné době má dvě rozpoznatelné možnosti: *name* a *newest*. Výchozí hodnota je nastavena na *newest*.
- `descending_sort:bool` obsahuje binární atribut, podle kterého program určuje uspořádání seřazení, buď vzestupně nebo sestupně. Toto platí pouze pro rozhraní, aplikace třídí jenom kopii a ne samotné ikony v kategorii.
  - Pokud je hodnota nastavena na *True*, tak program řadí sestupně. Naopak pro *False* program řadí vzestupně. Výchozí hodnota je *True*
- `layout:str` obsahuje pracovní název pro atribut, podle kterého program určuje mód vykreslení ikon. Podle hodnoty se při každém vykreslení určí, kde a jakým způsobem se umístí ikony v kategorii.
  - V současné době má dvě rozpoznatelné možnosti: *vertical* a *horizontal*. Když je hodnota *vertical*, ikony v kategorii se zobrazí pod sebou - vertikálně. Při hodnotě *horizontal* se zobrazí na stranách vedle sebe - horizontálně.
- `categories_container:tk.Frame` je frame, do kterého se přidávají rozhraní kategorií. Když chceme renderovat poprvé nebo znova kategorie, např. po změně, tak se vyvolá funkce `recreate_ui_data`, která odstraní dosavadní obsah a vytvoří nový.

### Data / Třídy

Datová struktura aplikace je relativně jednoduchá a zároveň rozšiřitelná. Jedná se o tři třídy: `Launchable`, `Category` a `Executable`.

`Launchable` slouží jko základní abstraktní třída pro cokoliv spustitelného. Má pouze parametr `name`, která značí zobrazitelné jméno, a metodu `open`, která něco spustí. Pokud tuto třídu dědí jiná třída, tak se může považovat za něco spustitelného a jiná část kódu je všechny může vidět jednotně. Lze tedy v budoucnosti přidat nové typy spustitelných objektů.

`Category` je třída pro uchování kategorie. Má parametr `name`, která znova značí zobrazitelné jméno, vlastní seznam `launchables`, ve kterém uchovává `Launchable` objekty, a metodu `open_all`, která spustí všechny objekty `Launchable` v seznamu `launchables`. Má ještě navíc metodu `add_launchables`, pomocí které se může přidat jeden či více `Launchable`s do seznamu. `Category` si pamatuje pořadí přidaných ikon pro potřeby třídění pro uživatele. Proto by se u seznam `launchables` nemělo měnit pořadí prvků, pouze čtení, kopírování, odstranění a přidání (pomocí `add_launchables`).

`Executable` je (jediný) typ `Launchable`. Jedná se o jeden spustitelný soubor s příponou **.exe**. ...

### Ukládání a načtení dat

Aplikace ukládá data ve formátu JSON. V globální proměnné `categories` si aplikace pamatuje seznam všech kategorií a ikony uložené v nich. Aplikace při uložení zakóduje a při načtení dekóduje kategorie a ikony pomocí pomocných funkcí `encode_category`, `encode_launch`, `decode_category` a `decode_launch`.

Aplikace ukládá data po každé změně dat. To se stane při:

- vytvoření nové kategorie
- odstranění kategorie
- vytvoření nové ikony
- odstranění ikony

Po každé této události se vyvolá funkce `recreate_ui_data`, která nejdříve zobrazí změny do UI a pak také uloží data pomocí `save_categories`.

Aplikace načítá data pouze při spuštění aplikace. Pokud nenajde soubor s daty, nepodaří se jí přečíst data nebo jsou data prázdná, tak do `categories` načte prázdnou základní kategorii s jménem *Main*.

`save_categories` otevře nebo vytvoří soubor podle globální proměnné `SAVE_FILE` pomocí příkazu `with open() as file`. Funkce zakóduje kategorie uložené v proměnné `categories` pomocí `encode_category` a výsledek této funkce propíše do souboru, který celý přepíše.

`load_categories` otevře soubor podle globální proměnné `SAVE_FILE` pomocí příkazu `with open() as file`. Funkce přečte obsah souboru, dekóduje jej pomocí `encode_category` a seznam dekódovaných kategorií uloží do globální proměnné `categories`. Pokud nenajde soubor s daty, nepodaří se jí přečíst data nebo jsou data prázdná, tak do `categories` načte seznam s jedinou prázdnou kategorií `Category` s jménem *Main*.

`encode_category` zakóduje danou kategorii parametrem `category:Category` a vratí `str` v JSON formátu. Uloží jej jako JSON objekt s hodnotami řetězec *name* a pole *launchables*, které odpovídají třídě `Category`. Pro zakódování ikon používá funkci `encode_launch`, kterou použije na všechny její ikony a uloží je již zakódované do `list`.

`decode_category` dekóduje kategorii uloženou v JSON formátu a vrátí objekt `Category` z ní vytvořenou. Hodnotu JSON objektu `name` uloží do stejnojmenného atributu. Pro dekódování ikon použije funkci `decode_launch` a všechny uloží do atributu `launchables`.

`encode_launch` podobně jako `encode_category` zakóduje a vratí ikonu danou parametrem `launch`. Funkce jiné typy ikony zákoduje jinak. V současné době je v aplikaci podporovaný pouze typ `Executable`. Pokud dostane funkce jiný typ, tak vyvolá výjimku `TypeError`, která značí, že funkce neví, jak daný typ zakódovat. Typ `Executable` zakóduje jako objekt se čtyřmi řetězcemi: *class*, podle kterého aplikace bude vědět, jak jí dekódovat, a *name*, *filepath* a *args* jako atributy třídy/objektu.

`decode_launch` podobně jako `decode_category` dekóduje JSON objekt a vrátí daný typ ikony. V současné době je v aplikaci podporovaný pouze typ `Executable`. Pokud dostane funkce JSON objekt s hodnotou *class* jinou, než `Executable`, tak vyvolá výjimku `TypeError`, která značí, že funkce neví, jak daný typ dekódovat. Podle hodnoty *class* daného JSON objektu určí, jaké hodnoty dekóduje. Pro typ `Executable` dékoduje hodnoty *name*, *filepath* a *args* do stejnojmenných atribut do objektu typu `Executable`.

### Uživatelské rozhraní

#### Základní okno

Základní okno se vytváří na začátku aplikace pomocí funkce `starting_ui`. Ta do `root` přidá dva framy typu `Frame`: `categories_frame` a `options_frame` pomocí funkcí `category_ui` a `options_ui`.

`category_ui` přidá do `root` frame na levé straně okna. Frame obsahuje tlačítko a další frame `categories_container`. Tlačítko má text *Add Category* a po stisknutí otevře okno pomocí funkce `window_add_category`. Frame `categories_container` slouží jako viditelný seznam kategorií a ikon v nich. Manipuluje s ním funkce `recreate_ui_data`, která z něj odstraní předchozí elementy přidá do něj všechny kategorie v současném stavu.

`options_frame` přidá do `root` frame na pravé straně okna. Frame obsahuje tři další framy: `sort_type_frame`, `sort_order_frame` a `layout_frame`, které do sebe přidá pomocí funkcí `sort_type_ui`, `sort_order_ui` a `layout_ui` v tomto pořadí. Každý tento frame obsahuje dvě tlačítka, která mění stav globálních proměnných `current_sort`, `descending_sort` a `layout`. Když se nějaké tlačítko spustí, tak vyvolá příslušnou funkci, buď `set_current_sort`, `set_descending_sort` nebo `set_layout`. Do parametru funkce přidá definovanou hodnotu podle daného tlačítka. Například tlačítko s textem *Vertical* změní globální proměnnou `layout` na hodnotu `vertical`.

`recreate_ui_data` renderuje aktuální stav kategorií v globální proměnné `category` do `categories_container`. Nejdříve pomocí funkce `reset_frame` odstraní všechny elementy v `categories_container`. Poté pomocí `ui_add_categories_to_frame` přidá do `categories_container` jednotlivé kategorie.

`ui_add_categories_to_frame` přidá pomocí `ui_add_category_to_frame` každou kategorii zvlášť. Musí do `ui_add_category_to_frame` přidat, na jakém indexu v `category` se daná kategorie nachází, aby na ně mohla odkazovat při volání `lambda` funkcí, např. pro mazání kategorie.

`ui_add_category_to_frame` vytvoří frame `cat_frame`, ve kterém jsou tři tlačítka a další frame `launches_frame` obsahující ikony kategorie. Tlačítko `Add` otevře okno pomocí funkce `window_add_launchable`, v kterém lze přidat ikonu do kategorie. Tlačítko `Open All` vyvolá metodu `open_all` dané kategorie, která spustí všechny ikony najednou. Tlačítko `Delete` ihned odstraní celou kategorii. `launches_frame` přidá pomocí `ui_add_launches_to_frame`.

`ui_add_launches_to_frame` vytvoří `launches_frame`, umístí jej do `cat_frame` a přidá do něj všechny ikony v kategorii. Nejdříve pomocí funkce `sorted_indexed_launches_by_options` získá seřazený zkopírovaný seznam ikon `launchables` v kategorii a v daném pořadí přidá všechny pomocí funkce `ui_add_launch_to_frame` do `launches_frame`.

`sorted_indexed_launches_by_options` pomocí globálních parametrů seřadí zkopírovaný seznam ikon a vrátí jej. Když je `current_sort` nastavený nastavený na *newest*, tak na jej nemusí seřadit, protože kategorie si pořadí přidaných ikon pamatuje implicitně. Jenom vrátí opačně seřazený seznam podle `descending_sort`. Když je `current_sort` nastavený nastavený na *name*, tak ikony seřadí podle abecedy jejich jména. Znova je převrátí podle `descending_sort`. Poté seznam vrátí.

`ui_add_launch_to_frame` vytvoří tlačítko s názvem ikony v textu a při spuštění tlačítka vyvolá funkci `open` dané ikony. Pomocí funkce `side_by_layout` získá tkinter směr pro rozložení ikon horizontálně či vertikálně. Také pomocí funkce `ui_add_menu_to_launch` vytvoří neviditelné menu, které se objeví, když se na tlačítko klikne pravým tlačítkem myši.

`ui_add_menu_to_launch` pomocí `tk.Menu` vytvoří neviditelný element, který se objeví při stisknutí tlačítka ikony pravým tlačítkem myši. V menu se nachází volba *Delete*, která odstraní danou ikonu z kategorie. Menu využívá pro objevení funkci `do_popup`.

#### Přidávácí okna

`window_add_category` vytvoří nové malé okno `add_cat_window`, pomocí kterého lze vytvořit novou kategorii. Nachází se v něm vstup typu `ttk.Entry` s nadtextem *Category name* a dvě tlačítka *Cancel* a *Create*. Do vstupu *Category name* lze napsat jméno kategorie a pak tlačítkem *Create* lze kategorii vytvořit. Kategorie se pomocí pomocné funkce `create_category` přidá do `categories` a renderuje se změna pomocí `recreate_ui_data`. Pak se okno uzavře pomocí funkce `cancel_window`, do které se dodá parametr okna `add_cat_window`. Tlačítko *Cancel* stejným způsobem uzavře okno, jen bez uložení.

`window_add_launchable` vytvoří nové malé okno `add_launch_window`, pomocí kterého lze vytvořit novou ikonu v kategorii. Pro potenciální budoucí způsoby spustitelných věcí vytvoří `tk.Notebook` se zatím pouze jedním formulářem pro `Executable`. Formulář se do něj přidá pomocí funkce `ui_executable`.

`ui_executable` vytvoří formulář pro vytvoření nové ikony typu `Executable`. Ve formuláři má tři vstupy `tk.Entry` s názvy *Name*, *Filepath* a *Arguments*. Do *Name* lze napsat jméno ikony, do *Filepath* cestu k **.exe** souboru a do *Arguments* argumenty spuštění. Do *Filepath* se nemusí psát cesta ručně. Nachází se nad ním tlačítko *Choose file*, které vyvolá funkcí `write_filename_to_entry` klasické vybírací popup okno. Funkce pak do proměnné `entry_filepath_text` typu `StringVar` napíše vybraný soubor a automaticky se díky tomu přepíše do vstupu. Pak se dole nachází dvě tlačítka *Cancel* a *Create*. *Create* podobně jako u `window_add_category` vyvolá pomocnou funkci `create_executable`, která vytvoří novou ikonu typu `Executable`, přidá jej do kategorie pomocí `category.add_launchables`, renderuje změnu pomocí `recreate_ui_data` a uzavře okno pomocí `cancel_window`, do které se dodá parametr okna `add_launch_window` (ve `ui_executable` funkci uložené jako `window`). Stejným způsobem tlačítko *Cancel* uzavře okno, jen bez změny a bez uložení.

#### Pomocné UI funkce

`side_by_layout` podle globální proměnné `layout` vrátí korespondující vlastnost elementu pro ikony. Pro hodnotu *horizontal* vrátí `tk.LEFT`, aby se ikony umisťovaly vedle sebe, a jinou hodnotu (*vertical*) vrátí `tk.TOP`, aby se ikony umisťovaly pod sebou.

`do_popup` vytvoří podle daného parametru `menu` nové popup okno na místě myši. Funguje tak, že když myš někam klikne levým tlačítkem, tak se popup okno zruší. Pokud `menu` vlastní nějaké možnosti, tak po kliknutí vyvolá její `command` atribut.

`popup_select_file` vytvoří klasické popup okno pro zvolení souboru. Pokud je parametr `exe` nastavený na *True*, tak se ve výběru objeví pouze soubory s příponou **.exe** a složky. Zvolenou cestu k souboru vrátí jako `str`.

`cancel_window` jednoduše odstraní dané okno parametrem `window`.

## Zhodnocení práce

Myslím, že jsem aplikaci vytvořil docela dobře. Splnil jsem všechny požadavky, avšak třeba rozložení ikon jsem udělal triviální. Koukal jsem se na možnost udělat mód, kde jsou ikony po stranách a pak při overflow by se další ikona umístila na dalším řádku, ale řešení není triviální a bylo by už moc komplikované. Jediný požadavek, který jsem nesplnil, je možnost spuštění jako administrátor. Nenašel jsem řešení, které by bylo kompatibilní tak, aby aplikace fungovala zároveň se spuštěnou aplikací.

Myslím si, že jsem vytvořil dobře kód tak, aby se dalo přidat další způsob něco spustit. V dřívější verzi jsem chtěl spustit příkaz v příkazovém řádku, ale to nakonec nebylo pro splnění požadavků potřeba a navíc se mi to stejně nepovedlo zprovoznit. Každopádně když se najde způsob, jak takhle spustit příkaz, tak to lze relativně jednoduše přidat do programu. Jen se musí vytvořit nová třída pod `Launchable`, přidat způsob kódování do JSON a vytvoření formuláře pro přidání do kategorie.

Podle mého názoru jsem také dobře postavil kód čitelně a s ne příliš dlouhými funkcemi, které by dělaly hodně najednou. Mohl jsem zkrátit funkce pro vytváření přídávacích oken, ale přišlo mi, že by to bylo zbytečné.

Aplikace by šla vylepšit ještě vzhledem. Můj styl je určitě funkční, ale ne úplně intuitivní nebo spíš neestetický.

Z vytváření aplikace si určitě budu pamatovat, jak jsem zvládl volat lambda funkce na dané elementy v seznamu. Když jsem přidával do funkce v lambdě jen prvek ve for cyklu, tak si každá lambda pamatovala jen poslední prvek. Pak jsem přišel na to, že lze do lambdy přidat parametr, který se uloží právě jen do této volání lambdy a mohl jsem pak třeba volat různé ikony.
