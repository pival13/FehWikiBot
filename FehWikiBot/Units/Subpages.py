#! /usr/bin/env python3

import re

def QuotesPage(unit) -> str:
    from ..Lang import Quotes
    from ..Tool.globals import TODO

    key = unit.data['character_file']
    EN = Quotes.fromAssets(key, 'USEN')
    JP = Quotes.fromAssets(key, 'JPJA')

    s =  '{{HeroPage Tabs}}\n'

    QUOTE_DEFINITIONS = [('Summoning', 'JOIN'),
                         ('Castle', 'HOME'),
                         ('Friend greeting', 'FRIEND'),
                         ('Leveling up', 'LEVEL'),
                         ('Ally growth', 'SKILL'),
                         ('5★ LV. 40 conversation', 'STRONGEST')]
    if unit.data['id_tag'][0] == 'E':
        s += '<!--\n'
    for title,tag in QUOTE_DEFINITIONS:
        keys = [f'MID_{key}_{tag}{n}' for n in range(10)]
        keys = [k for k in keys if k in EN]
        if keys == []: keys = [f'MID_{key}_{tag}']
        s += '=='+title+'==\n'
        for i,k in enumerate(keys):
            if tag == 'LEVEL': s += f'===+[{4-2*i},{5-2*i}] points===\n'
            s += '{{bq|' + EN.pop(k,'').replace('$k$p','<br>').replace('\\n',' ').replace('$Nf','{{Friend}}').replace('$Nu', '{{Summoner}}') + '}}\n'
            s += '{{bq|' + JP.pop(k,'').replace('$k$p','<br>').replace('\\n','').replace('$Nf','{{Friend}}').replace('$Nu', '{{Summoner}}') + '|ja}}\n'
            s += '{{Clear}}\n'
    if unit.data['id_tag'][0] == 'E':
        s += '-->\n'

    VOICE_DEFINITIONS = [('Attack', 'ATTACK', 2),
                         ('Damage', 'DAMAGE', 2),
                         ('Special trigger', 'SKILL', 4),
                         ('Defeat', 'DEAD', 1),
                         ('Status page', 'STATUS', 8),
                         ('Turn action', 'MAP', 3)]
    i0 = 1
    for title,tag,count in VOICE_DEFINITIONS:
        template = 'Audio' if tag != 'STATUS' else 'Status'
        if tag == 'STATUS' and unit.data['id_tag'][0] == 'E':
            s += '<!--\n'
        s += '=='+title+'==\n'
        s += '{{'+template+'TableHeader}}\n'
        for i in range(count):
            s += '{{'+template+'TableRow|VOICE_{{MF|1={{BASEPAGENAME}}}}_'+tag+'_'+str(i+1)+'.wav|'
            ss = EN.pop(f'MID_{key}_VOICE{i0+i:02}', '')
            if re.search(r'[a-zA-Z]', ss): s += ss
            if tag == 'STATUS':
                s += '|' + ('1' if i<4 else '4' if i<6 else '5')
            s += '}}\n'
        s += '|}\n'
        s += '{{'+template+'TableHeader|ja}}\n'
        for i in range(count):
            s += '{{'+template+'TableRow|VOICE_{{MF|1={{BASEPAGENAME}}}}_'+tag+'_'+str(i+1)+'_jp.wav|'
            s += JP.get(f'MID_{key}_VOICE{i0+i:02}', '')
            if tag == 'STATUS':
                s += '|' + ('1' if i<4 else '4' if i<6 else '5')
            s += '|ja}}\n'
        s += '|}\n'
        s += '{{Clear}}\n'
        i0 += count
        if tag == 'MAP' and unit.data['id_tag'][0] == 'E':
            s += '-->\n'
    s += '{{StoryAppearances}}'

    if len(EN) != 0:
        print(TODO + f'Unused quotes: {EN}')
    return s


def MiscPage(unit) -> str:
    from ..Lang import Messages
    from ..Tool.misc import cleanStr

    s =  '{{HeroPage Tabs}}\n'
    s += '{{MapAppearances}}\n'
    s += '==Availability==\n{{GeneralSummonRarities}}\n{{HeroFocusList}}\n{{DistributedAvailability}}\n'
    s += '{{HeroBonusList}}\n'
    s += '{{EventAppearances}}\n'

    tipsKey = next((k for k in Messages._DATA['USEN'].keys() if k[:9] == 'MID_TIPS_' and k[-len(unit.data['id_tag'])+3:] == unit.data['id_tag'][3:]), None)
    if tipsKey:
        s += '{{Hero Tips\n'
        s += '|textUSEN=' + Messages.USEN(tipsKey).replace('\n',' ') + '\n'
        s += '|textJPJA=' + Messages.JPJA(tipsKey).replace('\n','') + '\n'
        s += '}}\n'

    s += '==Trivia==\n* \n'
    s += unit.OtherLanguage() + '\n'

    cName = cleanStr(unit.name)
    s += '==Gallery==\n<gallery>\n'
    s += f'{cName} BtlFace BU.webp\n'
    s += f'{cName} BtlFace BU D.webp\n'
    for i in range(4):
        s += f'{cName[0]}{cName[1:].lower()} pop0{i+1}.png|Meet Some of the Heroes artwork\n'
    s += '</gallery>\n'
    # s += '===Sprites===\n<gallery>\n'
    # for f in getSprites(UNITS[hero_id]):
    #     s += f[5:] + '\n'
    # for f in getSpriteSheets(UNITS[hero_id]):
    #     s = re.sub(f'({f[5:f.rindex(' ')]} Mini Unit)', f[5:] + '\n\\1', s, 1)
    # s += '</gallery>\n'

    return s
