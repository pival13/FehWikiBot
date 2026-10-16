#! /usr/bin/env python3

import json
from os.path import realpath, dirname
from FehWikiBot import Messages
from FehWikiBot.Lang.Reader import MessageReader
from FehWikiBot.PersonalData import BINLZ_ASSETS_DIR_PATH
OLD_ASSETS_DIR_PATH = BINLZ_ASSETS_DIR_PATH.replace('Data','Old/Data')

def DumpDiff(old, new):
    s = '{\n'
    keysOld = list(old.keys())
    keysNew = list(new.keys())
    diff = {'old':[],'new':[]}
    while keysOld != [] or keysNew != []:
        if   keysOld != [] and keysOld[0] not in keysNew:
            diff['old'].append(keysOld.pop(0))
        elif keysNew[0] not in keysOld:
            diff['new'].append(keysNew.pop(0))
        elif old[keysNew[0]] != new[keysNew[0]]:
            keysOld.remove(keysNew[0])
            diff['old'].append(keysNew[0])
            diff['new'].append(keysNew.pop(0))
            
        else:
            if diff['old'] != [] or diff['new'] != []:
                s += '<<<<<<< old\n'
                s += ''.join([f'    "{k}": {json.dumps(old[k], ensure_ascii=False)},\n' for k in diff['old']])
                #s += '||||||| original\n'
                s += '=======\n'
                s += ''.join([f'    "{k}": {json.dumps(new[k], ensure_ascii=False)},\n' for k in diff['new']])
                s += '>>>>>>> new\n'
                diff = {'old':[],'new':[]}
            s += f'    "{keysNew[0]}": {json.dumps(new[keysNew[0]], ensure_ascii=False)},\n'
            keysOld.remove(keysNew.pop(0))

    if diff['old'] != [] or diff['new'] != []:
        s += '<<<<<<< old\n'
        s += ''.join([f'    "{k}": {json.dumps(old[k], ensure_ascii=False)},\n' for k in diff['old']])
        #s += '||||||| original\n'
        s += '=======\n'
        s += ''.join([f'    "{k}": {json.dumps(new[k], ensure_ascii=False)},\n' for k in diff['new']])
        s += '>>>>>>> new\n'
        diff = {'old':[],'new':[]}

    s += '}'
    return s

def CreateDiffFile(path):
    old,new = '',''
    if path.find(BINLZ_ASSETS_DIR_PATH) != -1:
        new = MessageReader.fromAssets(path).object
        old = MessageReader.fromAssets(path.replace(BINLZ_ASSETS_DIR_PATH,OLD_ASSETS_DIR_PATH)).object
    else:
        old = MessageReader.fromAssets(path).object
        new = MessageReader.fromAssets(path.replace(OLD_ASSETS_DIR_PATH,BINLZ_ASSETS_DIR_PATH)).object
    old = {o['key']:o['value'] for o in old}
    new = {o['key']:o['value'] for o in new}
    s = DumpDiff(old, new)
    open(realpath(dirname(__file__) + '/_diffFile.json'), 'w', encoding='UTF-8').write(s)


def CreateDiffMessage():
    old = json.load(open(realpath(dirname(__file__) + '/jsons/data.json'), encoding='UTF-8'))
    Messages.EN('M') # Load all messages
    new = Messages._DATA['USEN']

    s = DumpDiff(old, new)
    open(realpath(dirname(__file__) + '/_diff.json'), 'w', encoding='UTF-8').write(s)
    json.dump(new, open(realpath(dirname(__file__) + '/jsons/data.json'), 'w', encoding='UTF-8'), indent=2, ensure_ascii=False)

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 1:
        CreateDiffMessage()
    else:
        CreateDiffFile(realpath(argv[1]))