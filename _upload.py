#!/usr/bin/env python3

import util

import json
import re
from os.path import exists

from FehWikiBot import Wiki
from FehWikiBot.PersonalData import WEBP_ASSETS_DIR_PATH
from FehWikiBot.Tool.globals import ERROR, TODO
from FehWikiBot.Tool import waitSec
from FehWikiBot.Utility.Units import Units

def upload(filepath: str, comment: str):
    name = filepath[filepath.rfind('/')+1:]
    name2 = None
    type = name[name.rfind('.')+1:]
    content = ''

    if filepath.find('/assets/') != -1:
        content += '{{Copyright game}}{{Source|assets=' + filepath[filepath.find('/assets/'):] + '}}'
    if type in (name,'lz','plist','ssbp','ssae','ckb','csb'):
        return
    elif type == 'ogg':
        if name[:3].lower() == 'bgm_':
            content += '\n[[Category:BGM files]]'
    elif type in ('webp','png'):
        data = open(filepath, 'rb').read(12)
        if data[8:12] == b'WEBP':
            name = name.replace('.png', '.webp')
        if re.search(r'/Unit/.+_[pP]air/', filepath):
            return
        if filepath.find('/Face/') != -1 or filepath.find('/Unit/') != -1:
            unit = re.search(r'/(?:Unit|Face)/([^/]+)/', filepath)[1]
            if unit[-4:] == 'EX01':
                name = 'Resplendent_' + name
                unit = unit[:-4]
            if unit[-7:] == 'airMain':
                name = Units.fromFace(unit[:-4]).name + '_Main_' + name
            elif unit[-6:] == 'airSub':
                name = Units.fromFace(unit[:-3]).name + '_Sub_' + name
            elif unit[-8:] == 'TransMap':
                name = Units.fromFace(unit[:-9]).name + '_TransformMap_' + name
            elif unit[-11:] == 'TransBattle':
                name = Units.fromFace(unit[:-12]).name + '_Transform_' + name
            elif unit[-6:] == 'Dragon':
                u = Units.fromFace(unit[:-7]) or Units.fromFace(unit[:-6]) or Units.fromFace(unit[:-6]+'Normal') or Units.fromFace(unit[:-6]+'Pair') or Units.fromFace(unit[:-6]+'Legend01') or Units.fromFace(unit[:-11])
                #                  _Dragon                                                                                                                                                                     _DarkDragon
                if u:
                    name = u.name + '_Transform_' + name
                else:
                    print(ERROR + 'Unknow name for ' + unit + ' -- ' + filepath)
                    return
            else:
                u = Units.fromFace(unit)
                if u: name = u.name + '_' + name
                else:
                    print(ERROR + 'Unknow name for ' + unit + ' -- ' + filepath)
                    return
            if filepath.find('/Unit/') != -1: content += '\n[[Category:Mini unit sprite sheets]]'
            elif filepath[-9:] == '/Face.png': content += '\n[[Category:Full Portrait files]]'
            elif filepath[-12:] == '/BtlFace.png': content += '\n[[Category:Full Attack files]]'
            elif filepath[-14:] == '/BtlFace_C.png': content += '\n[[Category:Full Special files]]'
            elif filepath[-14:] == '/BtlFace_D.png': content += '\n[[Category:Full Injured files]]'
            elif filepath[-12:] == '/Face_FC.png':
                content += '\n[[Category:Icon Portrait files]]'
                name2 = name.replace('.webp','.png')
            elif filepath[-15:] == '/BtlFace_BU.png': content += '\n[[Category:Icon Attack files]]'
            elif filepath[-17:] == '/BtlFace_BU_D.png': content += '\n[[Category:Icon Injured files]]'
            else: content += '\n[[Category:Dialog unit images]]'
            if filepath.find('/Face/') != -1 and filepath.find('EX01/') != -1: content = content[:-2] + ' of Resplendent Heroes]]'

        elif filepath.find('/Wep/') != -1:
            from FehWikiBot.Skills.Weapon import Weapon
            from PIL import Image
            o = Weapon.get(name[:-5],'sprite_wepR') or Weapon.get(name[:-5],'sprite_wepL')
            img = Image.open(filepath)
            if not o: pass
            elif name[:6] == 'wep_mg' and not exists(filepath.replace('.png','.ssbp')) and img.size == (128,64):
                if name.find('_up') == -1:
                    waitSec(5); Wiki.uploadImage('Weapon_' + o.name +    '.png', img.crop(( 0,0, 56,64)), '', 'Cropped tome sprite '+comment[comment.find('(')])
                    waitSec(5); Wiki.uploadImage('Weapon_' + o.name + '_V2.png', img.crop((56,0,128,64)), '', 'Cropped tome sprite '+comment[comment.find('(')])
                else:
                    waitSec(5); Wiki.uploadImage('Weapon_' + o.name + '_V3.png', img.crop(( 0,0, 56,64)), '', 'Cropped tome sprite '+comment[comment.find('(')])
                    waitSec(5); Wiki.uploadImage('Weapon_' + o.name + '_V4.png', img.crop((56,0,128,64)), '', 'Cropped tome sprite '+comment[comment.find('(')])
            elif name.find('_up') == -1:
                if (o.data['sprite_wepR'] == name[:-5]) ^ (o.data['wep_equip'] == 'Bow'):
                    name2 = 'Weapon_' + o.name + '.png'
                else:
                    name2 = 'Weapon_' + o.name + '_V2.png'

        elif filepath.find('/Unit_Accessory/') != -1:
            from FehWikiBot.Others.Accessory import Accessories
            if exists(filepath[:-len(name)] + '/Thumbnail.png') and name[:-5] != 'Thumbnail': return
            o = Accessories.get(filepath[filepath.rfind('/', 0, -len(name))+1:-len(name)],'sprite')
            name = o.data['sprite'] + '.webp'
            name2 = ('Accessory ' + o.name + '.png') if o else None
        elif filepath.find('/Field/') != -1 and filepath.find('/Field/Common/') == -1:
            name = 'Map_' + name
            name2 = name.replace('.webp','.png')
        elif filepath.find('/Banner_Map/') != -1 and not re.search(r'/(ST_)?CX?\d+(_C)?\.', filepath):
            name = 'Banner_' + name
        elif filepath.find('/SkyCastle/Chip/') != -1:
            name = re.search(r'/SkyCastle/Chip/(.*?)/', filepath)[1] + '_' + name
        elif filepath.find('/SkyCastle/Holiday/') != -1:
            name = re.search(r'/([^/]*)/[^/]*$', filepath)[1] + '_' + name
        elif filepath.find('/Occupation/BG/') != -1:
            content += '\n[[Category:Grand Conquests overworld map files]]'
            name = 'GC_' + name
        elif filepath.find('/Banner_SequentialMap/') != -1:
            from FehWikiBot.Events.TT import TempestTrials
            content += '\n[[Category:Tempest Trials map banners]]'
            name = 'TT_' + name
            tt = TempestTrials.get(name[3:-5])
            name2 = ('Banner ' + tt.name + '.png') if tt else None
        elif filepath.find('/UI/Trip/') != -1:
            content += '\n[[Category:Lost Lore backgrounds]]'
            name = 'Trip_' + name
        elif filepath.find('/Mjolnir/Chip/') != -1 and (filepath.find('BU.png') != -1 or filepath.find('Default.png') != -1 or filepath.find('Broken.png') != -1):
            name = re.search(r'/Mjolnir/Chip/(.*?)/', filepath)[1] + '_' + name
        elif filepath.find('/Journey/Demo/') != -1:
            name = 'Journey_' + re.search(r'/Journey/Demo/(.*?)/', filepath)[1] + '_' + name
        elif filepath.find('/Journey/Mirror/BG/') != -1:
            name = 'Journey_' + re.search(r'/Journey/Mirror/BG/(.*?)/Animation/tex/', filepath)[1] + '_' + name
        elif filepath.find('/Img_Talk/') != -1:
            if name[:5] != 'EvBg_': name = 'Talk_' + name
            name2 = 'Talk_' + name.replace('.webp','.png').replace('Talk_','')
        elif filepath.find('/Field/Common/') != -1 and re.search(name,'^wallpattern',re.IGNORECASE):
            name2 = name.replace('.webp','.png')

        elif filepath.find('/Battle/BG/') != -1: # Combat backgrounds
            return
        elif filepath.find('/TapAction/TapBattleResource/') != -1: # Tap Battle
            name = re.search(r'TapAction/TapBattleResource/(.*?)/', filepath)[1] + '_' + name
            return
        elif filepath.find('/UI/Bg_DetailedStatus/Icon_') != -1: # Icon for unit background
            return
        elif filepath.find('/UI/Icon_EliteCastle') != -1: # Icon for castle background
            return
        elif re.match(r'/BG_\d+\.png$', filepath):
            util.askFor('Here is a new kind of file')
    else:
        print(TODO, type, f, re.search(r'/([^/]+)$', filepath)[1])
        return

    waitSec(5)
    Wiki.uploadFile(name, open(filepath, 'rb'), content, comment, True)
    if name2:
        Wiki.exportPage('File:'+util.cleanStr(name2), '#REDIRECT [[File:'+util.cleanStr(name)+']]', 'Redirect', create=True)


from sys import argv
if __name__ == '__main__':
    if len(argv) != 2: exit(1)
    for f in json.load(open('jsons/newFiles.json', 'r')):
        try: upload(WEBP_ASSETS_DIR_PATH + f.replace('\\','/'), f'New file ({argv[1]})')
        except: print(ERROR + f)
    for f in json.load(open('jsons/changedFiles.json', 'r')):
        try: upload(WEBP_ASSETS_DIR_PATH + f.replace('\\','/'), f'Updated file ({argv[1]})')
        except: print(ERROR + f)