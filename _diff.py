#! /usr/bin/env python3

import json
from os.path import realpath, dirname
from FehWikiBot.Utility.Messages import Messages

if __name__ == '__main__':
    old = json.load(open(realpath(dirname(__file__) + '/jsons/data.json'), encoding='UTF-8'))
    Messages.EN('M') # Load all messages
    new = Messages._DATA['USEN']

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
    open(realpath(dirname(__file__) + '/_diff.json'), 'w', encoding='UTF-8').write(s)
    json.dump(new, open(realpath(dirname(__file__) + '/jsons/data.json'), 'w', encoding='UTF-8'), indent=2, ensure_ascii=False)
