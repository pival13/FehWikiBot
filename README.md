# Fire Emblem Heroes Wiki Bot
This repository hosts various Python3 scripts use to create and update pages on the [Fire Emblem Heroes Wiki](https://feheroes.gamepedia.com/).

## Utilisation
### Dependencies
The following dependencies are needed in order to the scripts to work properly:
- [feh-assets-json](https://github.com/HertzDevil/feh-assets-json): HertzDevil repository containing converted version of the Fire Emblem Heroes binaries into JSON objects. This repository will be use whenever possible, and is assumed to always be up-to-date.
- [requests](https://requests.readthedocs.io/en/master/user/install/#install): A module use to perform HTTP requests. Needed in order to create or alter pages, or use the Fire Emblem Heroes Wiki API.
- [num2words](https://pypi.org/project/num2words/): A module use to convert a number into a string. Mainly use on page creation.
- PIL or Pillow: A module use to manipulate image. Needed for everything image related.

The next dependencies are only use by the Reverse part:
- [feh-bin](https://rubygems.org/gems/feh-bin/versions/0.1.0): A [Ruby](https://www.ruby-lang.org/en/) module use to compress and decompress FeH binaries (format `.bin.lz`).
- [pycrypto](https://pypi.org/project/pycrypto/): A module use to decrypt reward informations, as those are encrypted using an AES in Counter mode.
Depending what is your intent using this repository, all dependencies may not be necessaries.

### Personal Data
A `PersonalData.py` module must also be created. This module is use to get some of the needed informations, such as the location of the Fire Emblem Heroes files, or the user who will be use to perform posts.

For sensitiv information, such as password, it is recommand to store them on your environnement, and get them with `os.environ`.

This module must define the following global variable:
- `USER`: The Gamepedia/Fandom user name
- `BOT`: The name of the bot. One can be created [here](https://feheroes.gamepedia.com/Special:BotPasswords)
- `PASSWD`: The password of the bot.
- `JSON_ASSETS_DIR_PATH`: The absolute path to the [feh-assets-json](https://github.com/HertzDevil/feh-assets-json)/files/assets folder on your device.
- `BINLZ_ASSETS_DIR_PATH`: The absolute path to the assets folder containing the unaltered binaries of the Fire Emblem Heroes assets on your device. You can follow the instructions on [this page](https://feheroes.gamepedia.com/Fire_Emblem_Heroes_Wiki:Extracting_game_assets) in order to get these.

You can also define the following variables, despite these being currently unused:
- `WEBP_ASSETS_DIR_PATH`: The absolute path to the assets folder containing the unaltered files of the Fire Emblem Heroes assets on your device. If you extract data yourselves, it will be the same as `BINLZ_ASSETS_DIR_PATH`.
- `APK_ASSETS_DIR_PATH`: The absolute path to the assets folder of the Fire Emblem Heroes APK on your device. You can follow the same steps as above to get them, while navigating to folder `app` instead of `data`.

## Scripts
Most of the scripts present can either be use as a module or as a main script. Below will be explain the use of each files:

### [Util](/util.py)
- As a main:
    - Create `data.json` and `otherLanguages.json` files, holding every message, except characters lines and scenarios. Warning: data.json make several Mb, and otherLanguages.json is almost 10x bigger.
- Constants:
    - `URL`: The URL of the FeH Wiki API.
    - `TODO`: A string equal to "TODO: ". When print, shall be written on a yellow background.
    - `ERROR`: A string equal to "ERROR: ". When print, shall be written on a red background.
    - `ROMAN`: A list of roman number, up to 10.
    - `DIFFICULTIES`: The list of the difficulties, order by increasing difficulties.
    - `TIME_FORMAT`: The format string use be the wiki.
    - `MIN_TIME`: The minimal time, as a string following `TIME_FORMAT`.
    - `MAX_TIME`: The maximal time, as a string following `TIME_FORMAT`.
- Global variables:
    - `DATA`: The object that is written in data.json when use as a main.
    - `BGM`: An object using BGM name as key, and file name as value. Manually updated.
    - + the 7 globals defined in `PersonalData.py`.
- Functions:
    - `timeDiff`: Return the time `time` with a difference of `diff` on format `TIME_FORMAT`.
    - `cleanStr`: Replace any non-ascii characters with an ascii approximation and remove non alphanumeric, space, dot, dash or underscore characters.
    - `readFehData`: Read the content of a JSON file and return it.
    - `fetchFehData`: Read the content of all JSON files of a directory and return them.
    - `getName`: Return the name associated to a given `id_tag`.
    - `getBgm`: Return a list of BGMs related to map `map_id`.
    - `askFor`: Wait for an user response.
    - `askAgreed`: Wait for an user Yes or No, and return accordingly.
    - `fehBotLogin`: Connect to the FeH Wiki API and return the session object.
    - `cargoQuery`: Return the result of the query.

### [Map Util](/mapUtil.py)
- As a main:
    - Return the [In other language template](https://feheroes.gamepedia.com/Template:OtherLanguages) use by the FeH Wiki corresponding to the `id_tag` passed as parameter.
- Constants:
    - `USE_ALLY_STATS`, `USE_ENEMY_STATS`: Two lists use to create the Unit Data. See [here](https://feheroes.gamepedia.com/Module:UnitData/doc#Unit_definition) for more information.
- Gloabl variables:
    - `WEAPONS`: An object using weapon's id as key and the object associated with it as value.
    - `REFINED`: An object using refined weapon's id as key and the object associated with it as value.
- Functions:
    - `mapTerrain`: Return the content of a cell on a terrain.
    - `containDebris`: Return true if a cell contain a destroyable object.
    - `needBackdrop`: Return true if a map need a backdrop. In fact, it return whether there is alpha or not.
    - `MapImage`: Return the [MapLayout template/module](https://feheroes.gamepedia.com/Module:MapLayout) corresponding to the parameters given.
    - `MapInfobox`: Return the [Map Infobox template](https://feheroes.gamepedia.com/Template:Map_Infobox) corresponding to the parameters given.
    - `Availability`: Return the Availability section corresponding to the parameters given.
    - `MapAvailability`: Return the Map Availability section corresponding to the parameters given. Do not confound it with the previous, as this one will call [the MapDates template](https://feheroes.gamepedia.com/Template:MapDates), therefore will store information on a [Cargo table](https://feheroes.gamepedia.com/Special:CargoTables/MapDates).
    - `UnitData`: Return the content of a single parameter of the [UnitData module](https://feheroes.gamepedia.com/Module:UnitData).
    - `InOtherLanguage`: Return the [OtherLangage template](https://feheroes.gamepedia.com/Template:OtherLanguages) corresponding toe the parameters given.

### [Wiki Util](/wikiUtil.py)
- As a main:
    - Nothing is done. It is where I use to set new bots, but I either delete them once their job is done or move them to a separate function.
- Constants:
- Globals variables:
- Functions:
    - `waitSec`: Wait for a given amount of time.
    - `getPages`: Get all pages with name matching the given regex pattern.
    - `getPagesWith`: Get all pages using the [search property](https://www.mediawiki.org/wiki/API:Search) of the [FeH Wiki API](https://feheroes.gamepedia.com/Special:ApiSandbox).
    - `getPageContent`: Get the content of all pages given as parameters.
    - `exportPage`: Overwrite the content of a page with the one given.
    - `deleteToRedirect`: Delete the given page and recreate it as a redirect to another page.

### [PList Splitter](/plistSplitter.py)
- As a main:
    - Split all plist given as parameters according to their informations.
- Constants:
- Globals variables:
- Functions:

### [Map](/map.py)
- As a main:
    - Call the main function. See below.
- Constants:
- Globals variables:
- Functions:
    - `exportMap`: Binding of wikiUtil's exportPage. Display a message depending of the result.
    - `exportGroup`: Call `exportMap` on each element of the given object.
    - `parseMapId`: Parse a map_id and create the associated page if it doesn't exist. The following pages will be created that way:
        - Story Map
        - Paralogue Map
        - Heroic Ordeal
        - Tactic Drills
        - * Hero Battle
        - Rival Domains
        - Event Map
        - Chain Challenge
        - Squad Assault
    - `findEvents`: Get all events related to a given update and create pages associated to them. The following events are currently handled:
        - Tempest Trials
        - Forging Bonds
        - Lost Lore
        - Hall of Forms
        - Mjölnir's Strike
        - Frontline Phalanx
        - Pawns of Loki
    - `findUpcoming`: Print all upcoming special map.
    - `parseTagUpdate`: Get all maps related to a given update and call `parseMapId` with them. Plus call `findEvents` and `findUpcoming`.
    - `main`: For each argument:
        - Call `parseTagUpdate` if an argument use format `\d+_\w+`.
        - Call `findUpcoming` if the argument is `upcoming`.
        - Call `parseMapId` otherwise.

### [Redirect](/redirect.py)
- As a main:
    - Call the main function. See below.
- Constants:
- Global variables:
    - `SKILL_DATA`: A list of all skills available, weapons included.
    - `ACCESSORY_DATA`: A list of all accessories available.
- Functions:
    - `getWeaponName`: Get the name of a weapon with the name of the file.
    - `getAccessoryName`: Get the name of an accessory the name of the file.
    - `redirect`: Create a new redirect page.
    - `main`: Get all new files from the beginning of the day or the time given as parameter, and create redirect for all those needing one.