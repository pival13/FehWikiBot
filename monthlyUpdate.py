#! /usr/bin/env python3

import re
from os.path import isfile

from globals import DATA
import util
from Reverse import reverseMjolnirFacility
from wikiUtil import exportSeveralPages, getPageContent, waitSec

def createStructure(id):
    """{{Structure
    |name=
    |image=
    |description=
    |parameters0=
    |costs=
    |currency=
    |currencyX=
    |category=
    |nolv=
    }}"""
    return

def updateStructure(id):
    datas = util.fetchFehData('Common/SkyCastle/FacilityData', easySort=False)
    datas = [data for data in datas if re.sub('\\d*$','',data['id_tag']) == id]
    datas.sort(key=lambda struct: struct['level'])

    params = [str(data['a0']) for data in datas]
    costs = [str(data['cost']) for data in datas]
    currency = [data['cost_type'] for data in datas]
    currency = ['Aether Stone' if c=='STONE' else 'Heavenly Dew' if c=='DROP' else ('<!--'+c+'-->') for c in currency]

    page = getPageContent(util.getName('MID_SCF_' + id))[util.getName('MID_SCF_' + id)]
    page = re.sub(r'parameters0=[^\n|}]+','parameters0='+','.join(params),page,1)
    page = re.sub(r'costs=[^\n|}]+','costs='+';'.join(costs),page,1)
    page = re.sub(r'currency=[^\n|}]+','currency='+currency[0],page,1)
    for (idx, curr) in [(i+1,c) for (i,c) in enumerate(currency) if c != currency[0]]:
        if page.find(f'currency{idx}=') != -1:
            page = re.sub(f'currency{idx}=[^\\n|}}]+',f'currency{idx}={curr}',page,1)
        else:
            page = re.sub(f'(.*currency\\d*=[^\\n|}}]+)',f'\\1\n|currency{idx}={curr}',page,1,re.DOTALL)
    return {util.getName('MID_SCF_' + id): page}

def updateMechanism(id):
    datas = util.fetchFehDataFromAssets('Common/Mjolnir/FacilityData', easySort=False)
    datas = [data for data in datas if re.sub('\\d*','',data['id_tag']) == id]
    datas.sort(key=lambda mech: mech['level'])

    turns = []
    descs = []
    params = []
    costs = []
    for i, data in enumerate(datas):
        turns.append(str(data['turns']))
        params.append(str(data['a0']))
        costs.append(str(data['cost']))
        if 'MID_MF_' + data['id_tag'] + '_HELP' in DATA:
            descs.append(DATA['MID_MF_' + data['id_tag'] + '_HELP'].replace('\n',' '))
        elif 'MID_MF_' + id + '_HELP' in DATA:
            descs.append(DATA['MID_MF_' + id + '_HELP'].replace('\n',' '))
        else:
            descs.append(descs[-1])
    
    if all([desc == descs[0] for desc in descs]):
        desc = re.sub('^\\$a','',descs[0])
    else:
        miss1 = min([min([i for i in range(min(len(descs[0]),len(d))) if descs[0][i] != d[i]]+[min(len(descs[0]),len(d))]) for d in descs])
        miss2 = min([min([i for i in range(min(len(descs[0]),len(d))) if descs[0][-i] != d[-i]]+[min(len(descs[0]),len(d))]) for d in descs])-1
        params = [d[miss1:-miss2] for d in descs]
        desc = descs[0][:miss1] + '$a0' + descs[0][-miss2:]

    page = getPageContent(util.getName('MID_MF_' + id))[util.getName('MID_MF_' + id)]
    page = re.sub(r'description=[^\n|}]+','description='+desc,page)
    page = re.sub(r'parameters0=[^\n|}]+','parameters0='+','.join(params),page)
    page = re.sub(r'turns=[^\n|}]+','turns='+';'.join(turns if any([turn != turns[0] for turn in turns]) else [turns[0]]),page)
    page = re.sub(r'costs=[^\n|}]+','costs='+';'.join(costs),page)
    return {util.getName('MID_MF_' + id): page}

def updateFrom(update_tag):
    structData = util.readFehData('Common/SkyCastle/FacilityData/' + update_tag + '.json')
    mechanData = reverseMjolnirFacility(update_tag) or {}
    ret = {}
    for data in structData:
        tag = re.sub('\\d*$','',data['id_tag'])
        try: ret.update(updateStructure(tag))
        except: print('Failed to update structure ' + util.getName('MID_SCF_'+tag))
    for data in mechanData:
        tag = re.sub('\\d*$','',data['id_tag'])
        try: ret.update(updateMechanism(tag))
        except: print('Failed to update mechanism ' + util.getName('MID_MF_'+tag))
    return ret

if __name__ == '__main__':
    pass