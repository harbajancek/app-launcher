# Dokumentace aplikace app-launcher

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



## Zhodnocení práce