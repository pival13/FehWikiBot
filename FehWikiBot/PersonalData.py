#! /usr/bin/env python3

import os

USER = os.environ["FEH_WIKI_USERNAME"]
BOT = os.environ["FEH_WIKI_BOT"]
PASSWD = os.environ["FEH_WIKI_BOT_PASSWD"]
APK_ASSETS_DIR_PATH = os.environ["FEH_EMULATOR_ROOT"] + "/app/com.nintendo.zaba-1/base.apk/assets/"
BINLZ_ASSETS_DIR_PATH = os.environ["FEH_EMULATOR_ROOT"] + "/data/com.nintendo.zaba/files/assets/"
WEBP_ASSETS_DIR_PATH = BINLZ_ASSETS_DIR_PATH
JSON_ASSETS_DIR_PATH = os.environ["FEH_JSON_DATA_ROOT"]
