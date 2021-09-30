#! /usr/bin/env python3

import re

import util
import wikiUtil
import globals

from util import DATA as ENDATA
from MiniUnit import createMiniUnit, uploadMiniUnit, useMiniUnit

def addResplendentHeroQuotes(unit: dict):
    name = util.getName(unit['hero_id'])
    page = wikiUtil.getPageContent(name + '/Quotes')[name + '/Quotes']

    if page.find("Resplendent Hero") != -1:
        return {}

    romanized = util.fetchFehData("Common/SRPG/Person")[unit['hero_id']]['roman']
    EN = util.readFehData("USEN/Message/Character/"+romanized+"_EX01.json")
    JP = util.readFehData("JPJA/Message/Character/"+romanized+"_EX01.json")
    reg = re.compile(r'[a-zA-Z]')

    s = ["==Resplendent Hero=="]
    for (title, tag, init, count, template, extra) in [("Attack", "ATTACK", 0, 2, "Audio", None),
                                                        ("Damage", "DAMAGE", 2, 2, "Audio", None),
                                                        ("Special trigger", "SKILL", 4, 4, "Audio", None),
                                                        ("Defeat", "DEAD", 8, 1, "Audio", None),
                                                        ("Status page", "STATUS", 9, 8, "Status", lambda d: 1 if d < 4 else 4 if d < 6 else 5),
                                                        ("Turn action", "MAP", 17, 3, "Audio", None)]:
        s += ["==="+title+"===\n{{"+template+"TableHeader}}"]
        for i in range(count):
            v = f"|{extra(i)}" if extra else ""
            s += ["{{"+template+"TableRow|VOICE_{{MF|1={{BASEPAGENAME}}}}_Resplendent_"+f"{tag}_{i+1}.wav|"+(EN[init+i]["value"] if reg.search(EN[init+i]["value"]) else "")+v+"}}"]
        s += ["|}\n{{"+template+"TableHeader|ja}}"]
        for i in range(count):
            v = f"|{extra(i)}" if extra else ""
            s += ["{{"+template+"TableRow|VOICE_{{MF|1={{BASEPAGENAME}}}}_Resplendent_"+f"{tag}_{i+1}_jp.wav|"+JP[init+i]["value"]+v+"|ja}}"]
        s += ["|}\n{{Clear}}"]
    page = re.sub(r'(\{\{StoryAppearances\}\})', "\n".join(s) + "\n\\1", page)

    return {name+"/Quotes": page}

def updateResplendentHeroMisc(unit: dict):
    name = util.getName(unit['hero_id'])
    face = globals.UNITS[unit['hero_id']]['face_name2'] + 'EX01'

    createMiniUnit(unit['hero_id'], only=[face])
    uploadMiniUnit()
    page = useMiniUnit([unit['hero_id']])[name + '/Misc']
    if not page:
        page = wikiUtil.getPageContent(name + '/Misc')[name + '/Misc']

    if not re.search('Resplendent BtlFace BU\\.', page):
        page = re.sub('(BtlFace BU D.*)', f"\\1\nFile:{util.cleanStr(name)} Resplendent BtlFace BU.webp", page, 1)
    if not re.search('Resplendent BtlFace BU D\\.', page):
        page = re.sub('(Resplendent BtlFace BU.*)', f"\\1\nFile:{util.cleanStr(name)} Resplendent BtlFace BU D.webp", page, 1)

    return {name+'/Misc': page}

def updateResplendentHeroPage(unit: dict):
    name = util.getName(unit['hero_id'])
    page = wikiUtil.getPageContent([name])[name]
    JPDATA = {data['key']: data['value'] for data in util.fetchFehData("JPJA/Message/Data", None)}

    if not re.search(r'Properties\s*=[^\n|]*resplendent', page):
        add = 'resplendent,' + (util.askFor(intro='Where does Resplendent '+name+' come from') or '')
        if re.search(r'Properties\s*=\s*\w', page):
            add = ',' + add
        if page.find('Properties') != -1:
            page = re.sub(r'(Properties\s*=[^\n|]*)', '\\1'+add, page)
        else:
            page = re.sub(r'(?s)(\{\{\s*Hero Infobox.*?)\}\}', '\\1|Properties='+add+'\n}}', page)
    if page.find('resplendentStartTime') == -1:
        page = re.sub(r'(?s)(\{\{\s*Hero Infobox.*?)\}\}', '\\1|resplendentStartTime='+unit['avail_start']+'\n|resplendentEndTime='+util.timeDiff(unit['avail_finish'])+'\n}}', page)
    if page.find('resplendentArtist') == -1:
        page = re.sub(r'(artist\s*=[^\n|]*)', '\\1\n|resplendentArtist='+JPDATA['MPID_ILLUST_'+unit['hero_id'][4:]+'EX01'], page)
    if page.find('resplendentActorEN') == -1 and ENDATA['MPID_VOICE_'+unit['hero_id'][4:]+'EX01'] != ENDATA['MPID_VOICE_'+unit['hero_id'][4:]]:
        page = re.sub(r'(actorEN\s*=[^\n|]*)', '\\1\n|resplendentActorEN='+ENDATA['MPID_VOICE_'+unit['hero_id'][4:]+'EX01'], page)
    if page.find('resplendentActorJP') == -1 and JPDATA['MPID_VOICE_'+unit['hero_id'][4:]+'EX01'] != JPDATA['MPID_VOICE_'+unit['hero_id'][4:]]:
        page = re.sub(r'(actorJP\s*=[^\n|]*)', '\\1\n|resplendentActorJP='+JPDATA['MPID_VOICE_'+unit['hero_id'][4:]+'EX01'], page)
    
    return {name: page}
    

def ResplendentHero(unitId: str):
    data = globals.RESPLENDENTS[unitId] or None
    res = updateResplendentHeroPage(data)
    res.update(addResplendentHeroQuotes(data))
    res.update(updateResplendentHeroMisc(data))
    return res

def ResplendentHeroesFrom(tagId: str):
    datas = util.readFehData('Common/SubscriptionCostume/' + tagId + '.json')
    res = {}
    for data in datas:
        try:
            res.update(updateResplendentHeroPage(data))
            res.update(addResplendentHeroQuotes(data))
            res.update(updateResplendentHeroMisc(data))
        except:
            print(util.TODO + 'Error with Resplendent hero ' + util.getName(data['hero_id']))
    return res

from sys import argv
if __name__ == '__main__':
    for arg in argv[1:]:
        pages = {}
        if re.match(r'\d+_\w+', arg):
            pages = ResplendentHeroesFrom(arg)
        elif arg.find(':') != -1:
            pass
        elif arg.find('PID_') == 0:
            pages = ResplendentHero(arg)
        for page in pages:
            print(page, pages[page])