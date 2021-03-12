# Fire Emblem Heroes Wiki Bot
This repository hosts various Python3 scripts use to create and update pages on the [Fire Emblem Heroes Wiki](https://feheroes.gamepedia.com/).

<details>
<summary>Table of Contents</summary>

1. [Utilisation](#utilisation)
    1. [Dependencies](#dependencies)
    2. [Personal Data](#personal-data)
2. [Scripts](#scripts)
    1. [Util](#util)
    2. [Map Util](#map-util)
    3. [Wiki Util](#wiki-util)
    4. [PList Splitter](#plist-splitter)
    5. [Map](#map)
    6. [Redirect](#redirect)
    7. [Reward](#reward)
    8. [Scenario](#scenario)
    9. [Mission](#mission)
    10. [Mjölnir's Strike Result](#msresult)
    11. [Page generators](#page-generators)
    12. [Event Map](#event-map)

</details>

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
    - Create `data.json` and `otherLanguages.json` files. `data.json` holds every message present in Data and Menu folder of `USEN/Messages`. This correspond to every string use by the game, except unit's lines and scenarios. `otherLanguages.json` holds the same message, but in all languages.
    - Warning: `data.json` make several Mb of size, and `otherLanguages.json` is almost 10 times bigger.
- Constants:
    - `URL`: The URL of the FeH Wiki API.
    - `TODO`: A string equal to "TODO: ". When print, shall be written on a yellow background.
    - `ERROR`: A string equal to "ERROR: ". When print, shall be written on a red background.
    - `ROMAN`: A list of roman number, up to 10.
    - `DIFFICULTIES`: The list of the difficulties, sort by increasing difficulties.
    - `TIME_FORMAT`: The format string use by the wiki.
    - `MIN_TIME`: The minimal time, as a string following `TIME_FORMAT`.
    - `MAX_TIME`: The maximal time, as a string following `TIME_FORMAT`.
- Global variables:
    - `DATA`: The object that is written in data.json when use as a main.
    - `BGM`: An object using BGM name as key, and file name as value. Manually updated.
    - \+ the 7 globals defined in `PersonalData.py`.
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
<div align="right"><a href="#fire-emblem-heroes-wiki-bot">Top</a></div>

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
<div align="right"><a href="#fire-emblem-heroes-wiki-bot">Top</a></div>

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
<div align="right"><a href="#fire-emblem-heroes-wiki-bot">Top</a></div>

### [PList Splitter](/plistSplitter.py)
- As a main:
    - Split all plist given as parameters according to their informations.
- Constants:
- Globals variables:
- Functions:
<div align="right"><a href="#fire-emblem-heroes-wiki-bot">Top</a></div>

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
        - \* Hero Battle
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
<div align="right"><a href="#fire-emblem-heroes-wiki-bot">Top</a></div>

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
<div align="right"><a href="#fire-emblem-heroes-wiki-bot">Top</a></div>

### [Reward](/reward.py)
- As a main:
- Constants:
    - `ITEM_KIND`: The different kinds of item. Some kind are still unknow, and are therefore left as "".
    - `COLOR`: The colors use by Shard and Badge. Note that when there is no `Universal`, `Scarlet` is indexed as 0, and so on.
    - `AA_ITEM`: The different [Arena Assault](https://feheroes.gamepedia.com/Arena_Assault) items.
    - `ELEMENT`: Blessing elements. The first one is no blessing.
    - `FB_RANK`
    - `THRONE`
    - `MOVE`: The move type use by the game, sort as in.
    - `WEAPON`: The weapon type use by the game, sort as in.
    - `AETHER_STONE`: Some [Aether Stone](https://feheroes.gamepedia.com/Aether_Stone) type. Somehow outdated.
    - `DIVINE_CODES`: Some [Divine Codes](https://feheroes.gamepedia.com/Divine_Code) type. Currently empty as it as been automatized.
- Global variables:
- Functions:
    - `parseReward`: Convert a JSON reward into an object acceptable by [Module:RewardText](https://feheroes.gamepedia.com/Module:RewardText). Its format is use almost eveywhere on the wiki.
<div align="right"><a href="#fire-emblem-heroes-wiki-bot">Top</a></div>

### [Scenario](/scenario.py)
- As a main:
    - Print the story associated to the tag pass as parameter.
- Constants:
- Global variables:
    - `UNIT_IMAGE`: An object with the `face_name` of unit as key, and the unit as value. The key use are the same as [here](https://feheroes.gamepedia.com/Module:ScenarioArchiveToWiki/data).
- Functions:
    - `Conversation`: Return the whole [StoryTextTable](https://feheroes.gamepedia.com/Template:StoryTextTable) block relativ to the map given as parameter, from section asked only.
    - `StoryNavBar`: Return a [Story Navbar](https://feheroes.gamepedia.com/Template:Story_Navbar). Ask for the user for previous and next story, but may make suggestion.
    - `Story`: Return the Story section of a page, including every conversation and the navbar.
<div align="right"><a href="#fire-emblem-heroes-wiki-bot">Top</a></div>

### [Mission](/Mission.py)
- As a main:
    - Consider the first two arguments as time, or use `MIN_TIME` and `MAX_TIME` instead, and call `Mission` with these.
- Constants:
    - `SORTING_PATTERN`: The patterns use to identifiate missions as part of a group.
- Global variables:
- Functions:
    - `Mission`: Return every missions which begin between the given start and end time.
    - `MissionsOf`: Return every missions define on the file associated to the given update.
<div align="right"><a href="#fire-emblem-heroes-wiki-bot">Top</a></div>

### [MSResult](/MSResult.py)
- As a main:
    - Update [Mjölnir's Strike](https://feheroes.gamepedia.com/Mjölnir%27s_Strike) page with values described on the official website. Mjölnir's Strike numbers must be passed as parameters.
- Constants:
- Global variables:
- Functions:
<div align="right"><a href="#fire-emblem-heroes-wiki-bot">Top</a></div>

### Page generators
The below files all work the same way. Their main will pass each argument to the corresponding function depending on the format of that one, and will print its result.

Their is mainly two kind of function.
+ Functions that generate a single page: Take an id as parameter, and return the content of the page
+ Functions that may generate several page: Take an id as parameter, and return an object with the page's name as key, and its content as value.
-----------------------
* Page generators:
    - [`StoryParalogue.py`](/StoryParalogue.py): Generate [Story](https://feheroes.gamepedia.com/Story_Maps) and [Paralogue](https://feheroes.gamepedia.com/Paralogue_Maps) maps.
    - [`TD.py`](/TD.py): Generate [Tactics Drills](https://feheroes.gamepedia.com/Tactics_Drills) maps.
    - [`HO.py`](/HO.py): Generate [Heroic Ordeals](https://feheroes.gamepedia.com/Heroic_Ordeals) maps.
    - [`DerivedMap.py`](/DerivedMap.py): Generate [Chain Challenge](https://feheroes.gamepedia.com/Chain_Challenge) and [Squad Assault](https://feheroes.gamepedia.com/Squad_Assault) maps.
    - [`HB.py`](/HB.py): Generate [Grand](https://feheroes.gamepedia.com/Grand_Hero_Battle_maps), [Bound](https://feheroes.gamepedia.com/Bound_Hero_Battle_maps), [Legendary](https://feheroes.gamepedia.com/Legendary_Hero_Battle_maps) and [Mythic](https://feheroes.gamepedia.com/Mythic_Hero_Battle_maps) Hero Battle maps.
    - [`RD.py`](/RD.py): Generate [Rival Domains](https://feheroes.gamepedia.com/Rival_Domains) maps.
    - [`TT.py`](/TT.py): Generate [Tempest Trials](https://feheroes.gamepedia.com/Tempest_Trials) pages.
    - [`FB.py`](/FB.py): Generate [Forging Bonds](https://feheroes.gamepedia.com/Forging_Bonds) pages.
    - [`LL.py`](/LL.py): Generate [Lost Lore](https://feheroes.gamepedia.com/Lost_Lore) pages.
    - [`HoF.py`](/HoF.py): Generate [Hall of Forms](https://feheroes.gamepedia.com/Hall_of_Forms) pages.
    - [`MS.py`](/MS.py): Generate [Mjölnir's Strike](https://feheroes.gamepedia.com/Mjölnir%27s_Strike) pages.
    - [`FP.py`](/FP.py): Generate [Frontline Phalanx](https://feheroes.gamepedia.com/Frontline_Phalanx) pages.
    - [`PoL.py`](/PoL.py): Generate [Pawns of Loki](https://feheroes.gamepedia.com/Pawns_of_Loki) pages.
- Constants:
    - TD.`TD_KIND`: Tactics Drills types.
    - HO.`SERIES_BGM`: The BGMs used on Heroic Ordeals, depending on the game of the hero.
    - TT.`TT_DIFFICULTIES `: Strings use on Tempest Trials pages. It represent the difficulty, the level of the initial enemies and the number of battles.
    - FB.`COLORS`: The colors used on Forging Bonds.
    - LL.`extraTeams`: The amount of lines require to acquire a new team. Will eventually disappear.
    - PoL.`WEAPON_CATEGORY`: An object with a mask as key, and the category of weapon associated as value. Wrote as binary to make it more understandable.
- Global variables:
- Functions:
    - StoryParalogue.`StoryMap`: Generate a single Story Map page. Its id must be `S\d{4}`.
    - StoryParalogue.`StoryGroup`: Generate several Story Map pages. Its id must be `C\d{4}`.
    - StoryParalogue.`ParalogueMap`: Generate a single Paralogue Map page. Its id must be `X\d{4}`.
    - StoryParalogue.`ParalogueGroup`: Generate several Paralogue Map pages. Its id must be `CX\d{3}`.
    - TD.`TacticsDrills`: Generate a single Tactics Drills page. Its id must be `P[ABC]\d{3}`.
    - HO.`HeroicOrdeals`: Generate a single Heroic Ordeals page. Its id must be `H\d{4}`.
    - DerivedMap.`ChainChallengeMap`: Generate a single Chain Challenge page (Single and Double). Its id must be `ST_[SX]\d{4}`.
    - DerivedMap.`ChainChallengeGroup`: Generate several Chain Challenge pages. Its id must be `ST_(C\d{4}|CX\d{3})`.
    - DerivedMap.`SquadAssault`: Generate a single Squad Assault page. Its id must be `SB_\d{4}`.
    - HB.`GrandHeroBattle`: Generate a single Grand Hero Battle page. Its id must be `T\d{4}`.
    - HB.`BoundHeroBattle`: Generate a single Bound Hero Battle page. Its id must be `T\d{4}`.
    - HB.`LegendaryHeroBattle`: Generate a single Legendary/Mythic Hero Battle page. Its id must be `L\d{4}`.
    - RD.`RivalDomains`: Generate a single Rival Domains page. Its id must be `Q\d{4}`.
    - TT.`TempestTrials`: Generate several Tempest Trials pages (usually only one). Its id must be `W\d{4}` or `\d+_\w+`.
    - FB.`ForgingBonds`: Generate several Forging Bonds pages (usually only one). Its id must be `\d+_\w+`.
    - LL.`LostLore`: Generate several Lost Lore pages (usually only one). Its id must be `\d+_\w+`.
    - HoF.`HallOfForms`: Generate several Hall of Forms pages (usually only one). Its id must be `\d+_\w+`.
    - MS.`MjolnirsStrike`: Generate several Mjölnir's Strike pages (usually only one). Its id must be `\d+_\w+`.
    - FP.`FrontlinePhalanx`: Generate several Frontline Phalanx pages (usually only one). Its id must be `\d+_\w+`.
    - PoL.`PawnsOfLoki`: Generate several Pawns of Loki (usually only one). Its id must be `\d+_\w+`.
<div align="right"><a href="#fire-emblem-heroes-wiki-bot">Top</a></div>

### [Event Map](/EventMap.py)
- As a main:
    - When passing two arguments of format `V\d{4}`, call `EventGroup` with these two.
    - When passing a single arguments of format `V\d{4}`, call `EventMap` with it.
    - Otherwise, call `readPersonalJson` with the argument.
- Constants:
    - `WEAPON_TYPE`: A list of tag corresponding to the japanese name of a weapon.
    - `MAGIC_TYPE`: A list of list of tome `tag_id`.
    - `BEAST_TYPE`: A list of beast suffix, corresponding to the different move type.
- Global variables:
    - `UNITS`: An object with a unit fullname as key, and the unit object as value.
- Functions:
    - `readPersonalJson`: Read the json passed as parameter, following the order needed to create an event map. This is here to let you do
    ```bash
    python3 EventMap.py event.json | python3 EventMap.py idTag [idTag2]
    ```
    - `EventMap`: Generate a single event map, and return it. Its id must be `V\d{4}`. Every informations are ask to the player.
    - `EventGroup`: Generate several event maps, and return them as an object. Its ids must be `V\d{4}`. Every informations are ask to the player.
    - `exportEventMap`: Call `EventMap` or `EventGroup` and save pages to the FeH Wiki.
<div align="right"><a href="#fire-emblem-heroes-wiki-bot">Top</a></div>
