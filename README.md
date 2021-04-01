# Fire Emblem Heroes Wiki Bot
This repository hosts various Python3 scripts use to create and update pages on the [Fire Emblem Heroes Wiki](https://feheroes.fandom.com/wiki/).

## Utilisation
### Dependencies
The following dependencies are needed in order to the scripts to work properly:
- [feh-assets-json](https://github.com/HertzDevil/feh-assets-json): HertzDevil repository containing converted version of the Fire Emblem Heroes binaries into JSON objects. This repository will be use whenever possible, and is assumed to always be up-to-date.
- [requests](https://requests.readthedocs.io/en/master/user/install/#install): A module use to perform HTTP requests. Needed in order to create or alter pages, or use the Fire Emblem Heroes Wiki API.
- [num2words](https://pypi.org/project/num2words/): A module use to convert a number into a string.
- PIL or Pillow: A module use to manipulate image. Needed for everything image related.

The next dependencies are only use by the Reverse part:
- [feh-bin](https://rubygems.org/gems/feh-bin/versions/0.1.0): A [Ruby](https://www.ruby-lang.org/en/) module use to compress and decompress FeH binaries (format `.bin.lz`).
- [pycrypto](https://pypi.org/project/pycrypto/): A module use to decrypt reward informations, as those are encrypted using an [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) in [Counter](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Counter_(CTR)) mode.

Depending what is your intent using this repository, all dependencies may not be necessaries.

### Personal Data
A `PersonalData.py` module must be created. This module is use to get some of the needed informations, such as the location of the Fire Emblem Heroes files, or the user who will be use to perform posts.

Details about this module as well as an example can be found [here](https://gitlab.com/pival1302/FehWikiBot/-/wikis/Modules#personal-data).

### JSON objects

Some modules will try to read json objects from the json folder you specified (`JSON_ASSETS_DIR_PATH`), which are not present by default on the `feh-assets-json` repository.

The json needed are those from sounds and background musics. However you can use the following python script in order to create them.

<details>
<summary>Show / Hide</summary>

```python
#! /usr/bin/env python3

from os import listdir
from os.path import isfile
from Reverse import reverseBGM, reverseSound
from util import BINLZ_ASSETS_DIR_PATH as BINLZ, JSON_ASSETS_DIR_PATH as JSON

path = BINLZ + '/Common/SRPG/StageBgm/'
for file in listdir(path):
    if isfile(path+file) and file[-7:] == '.bin.lz':
        try:
            with open(path.replace(BINLZ, JSON) + file[:-7] + '.json', 'x') as f:
                print(reverseBGM(file[:-7]), file=f)
        except FileExistsError:
            print(f"BGM file '{file[:-7]}.json' already exist")

path = BINLZ + '/Common/Sound/arc/'
for file in listdir(path):
    if isfile(path+file) and file[-7:] == '.bin.lz':
        try:
            with open(path.replace(BINLZ, JSON) + file[:-7] + '.json', 'x') as f:
                print(reverseSound(file[:-7]), file=f)
        except FileExistsError:
            print(f"Sound file '{file[:-7]}.json' already exist")
```

</details>

### Scripts

See [here](https://gitlab.com/pival1302/FehWikiBot/-/wikis/Modules) for a description of each and every scripts
