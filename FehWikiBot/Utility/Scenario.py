#! /usr/bin/env python3

from typing_extensions import Self, LiteralString
from .Reader.Message import MessageReader

__all__ = 'Scenario'

class _ScenarioMeta(type):
    def __repr__(cls) -> str:
        return f"<class {cls.__name__} ({len(cls._DATA['USEN'])} EN, {len(cls._DATA['JPJA'])} JP)>"

class Scenario(metaclass=_ScenarioMeta):
    _DATA = {'USEN':{}, 'JPJA':{}}

    @classmethod
    def Conversation(cls, tag, key):
        o = cls.get(tag)
        if key not in o: return ''
        return '{{#invoke:Scenario|scenario|1=' + str(o[key]) + '}}'

    @classmethod
    def Story(cls, tag, isStory=False):
        o = cls.get(tag)
        s = '{{#invoke:Scenario|story\n'
        if 'MID_SCENARIO_OPENING' in o:
            s += '|opening=' + str(o['MID_SCENARIO_OPENING']) + '\n'
        if 'MID_SCENARIO_MAP_BEGIN' in o:
            # 1 unit speaking not from Heroes
            if isStory and o['MID_SCENARIO_MAP_BEGIN'].texts['USEN'].count('$Wm') == 1 and o['MID_SCENARIO_MAP_BEGIN'].texts['USEN'].find(',ch00_') == -1:
                if 'MID_SCENARIO_OPENING' in o:
                    s += '}}\n{{#ifeq:{{BASEPAGENAME}}|{{subst:BASEPAGENAME}}|{{#invoke:Scenario|story\n'
                else:
                    s = '{{#ifeq:{{BASEPAGENAME}}|{{subst:BASEPAGENAME}}|' + s
                s += '|map begin=' + str(o['MID_SCENARIO_MAP_BEGIN']) + '}}'
                if 'MID_SCENARIO_MAP_END' in o or 'MID_SCENARIO_ENDING' in o:
                    s += '}}\n{{#invoke:Scenario|story\n'
            else:
                s += '|map begin=' + str(o['MID_SCENARIO_MAP_BEGIN']) + '\n'
        if 'MID_SCENARIO_MAP_END' in o:
            s += '|map end=' + str(o['MID_SCENARIO_MAP_END']) + '\n'
        if 'MID_SCENARIO_ENDING' in o:
            s += '|ending=' + str(o['MID_SCENARIO_ENDING']) + '\n'
        s += '}}'
        if len([tag for tag in o if tag[13:] not in ['OPENING','MAP_BEGIN','MAP_END','ENDING']]) > 0:
            from ..Tool.globals import TODO
            print(TODO + tag + ': Others scenario tag present')
        return s

    @staticmethod
    def StoryNavbar(tag):
        # TODO: Includes: MainStory, Paralogue, GC, TT, FB, HB
        from ..Stages.Paralogues import Paralogue
        from ..Stages.MainStories import MainStory
        prev,next = None,None
        if tag[0] == 'X' and tag[1] != 'X':
            prev = Paralogue.get(tag[:-1] + str(int(tag[-1])-1))
            next = Paralogue.get(tag[:-1] + str(int(tag[-1])+1))
        elif tag[0] == 'S' and tag[1] != 'E':
            prev = MainStory.get(tag[:-1] + str(int(tag[-1])-1))
            next = MainStory.get(tag[:-1] + str(int(tag[-1])+1))
        return '{{Story Navbar|' + (prev.name if prev else '') + '|' + (next.name if next else '') + '}}'

    @staticmethod
    def Navbar(category, paralogueCategory=None):
        if paralogueCategory:
            return '{{Scenario Navbar|'+category+'|'+paralogueCategory+'}}'
        else:
            return '{{Scenario Navbar|'+category+'}}'

    @staticmethod
    def Navbox(category):
        return '{{Scenario Navbox|'+category+'}}'

    @classmethod
    def get(cls, tag: str, lang: list[LiteralString] | LiteralString = ('USEN','JPJA')) -> dict[str,Self]:
        "Return a dict of message IDs and Scenario objects"
        cls.load(tag)
        if tag not in cls._DATA['USEN']: return {}
        return {k: cls(tag,k).filter(lang) for k in cls._DATA['USEN'][tag] if k[-4:] != '_BGM' and k[-6:] != '_IMAGE'}

    @classmethod
    def load(cls, tag: str) -> bool:
        from os.path import exists, getmtime
        from json import load, dump
        from ..PersonalData import JSON_ASSETS_DIR_PATH as jsonPath, BINLZ_ASSETS_DIR_PATH as assetsPath

        loaded = False
        for lang in cls._DATA.keys():
            path = lang+'/Message/Scenario/'+tag
            if tag in cls._DATA[lang]:
                continue
            elif exists(assetsPath+path+'.bin.lz') and (not exists(jsonPath+path+'.json') or getmtime(assetsPath+path+'.bin.lz') >= getmtime(jsonPath+path+'.json')):
                parser = MessageReader.fromAssets(path+'.bin.lz')
                if not parser.isValid(): continue
                dump(parser.object, open(jsonPath+path+'.json', mode='w', encoding='utf-8'), ensure_ascii=False, indent=2)
                json = parser.object
            elif exists(jsonPath+path+'.json'):
                json = load(open(jsonPath+path+'.json', encoding="utf-8"))
            else:
                continue
            cls._DATA[lang][tag] = {}
            for o in json:
                cls._DATA[lang][tag][o['key']] = o['value']
            loaded = True

        return loaded


    def __init__(self, tag, key):
        self.load(tag)
        self._tag = tag
        self._key = key
        self._lang = self._DATA.keys()

    @property
    def langs(self) -> list[LiteralString]:
        "The languages currently in used"
        return [l for l in self._lang if self._tag in self._DATA[l]]

    @property
    def texts(self) -> dict[LiteralString,str]:
        "Returns a dict of language and raw scenario text"
        o = {}
        for l in self.langs:
            if self._tag not in self._DATA[l] or self._key not in self._DATA[l][self._tag]: continue
            o[l] = self._DATA[l][self._tag][self._key]
            if (self._key+'_BGM') in self._DATA[l][self._tag]:
                o[l] = '$Sbp' + self._DATA[l][self._tag][self._key+'_BGM'] + ',0|' + o[l]
            if (self._key+'_IMAGE') in self._DATA[l][self._tag]:
                o[l] = '$b' + self._DATA[l][self._tag][self._key+'_IMAGE'] + '|' + o[l]
        return o

    def filter(self, langs: LiteralString | list[LiteralString]) -> Self:
        if isinstance(langs, str):
            self._lang = [langs] if langs in self._lang else []
        else:
            self._lang = [l for l in self._lang if l in langs]
        return self

    def text(self, lang: LiteralString) -> str:
        "Returns the raw scenario text for the given language"
        t = self.texts
        if lang not in t: return ''
        return t[lang].replace('\n','\\n')

    def __str__(self) -> str:
        objs = self.texts
        objs = _parseObjects(objs)
        objs = _mergeObjects(objs)
        return _stringifyObjects(objs)

def _parseObjects(objs):
    import re
    from .Sound import Sound
    from ..Tool.globals import TODO

    for l,obj in objs.items():
        ss = obj.replace('$Nu', '@Summoner@').replace('$Nf', '@Friend@').replace(';','@,@').replace('\n','\\n')
        # Text color ($c{R},{G},{B},{A}|)
        ss = re.sub(r'\$c(\d+),(\d+),(\d+),(\d+)\|', lambda o: f'@c:#{int(o[1]):02X}{int(o[2]):02X}{int(o[3]):02X}@', ss.replace('$c255,255,255,255|','@c:reset@'))

        REs = [
            re.compile(r'\$(p)'), re.compile(r'\$(Sbs|Sbv|w).+?\|'), re.compile(r'\$(b|Ssp|n|E|Fi)(.+?)\|'),
            re.compile(r'\$(Sbp)(\w+),(\d+)\|'), re.compile(r'\$(Wm)([\w.―]+),(\w+),(\w+)\|'),
            re.compile(r'\$(Fo)(\d+),(\d+),(\d+),(\d+),(\d+)\|'), re.compile(r'[^$]+')
        ]
        obj = []
        objUnit = {'unit': None, 'name': '', 'expression': '', 'text': ''}
        for s in ss.split('$k'): # Tap screen ($k)
            objState = {}
            objUnit['text'] = ''
            while s != '':
                for RE in REs:
                    o = RE.match(s)
                    if o: break
                if not o:
                    print(TODO + 'Unknow tag: ' + s[:s.find('|')])
                    s = s[s.find('|')+1:]
                    continue

                match o[1] if len(o.groups()) > 0 else '_':
                    case 'b': objState['background'] = o[2]
                    case 'Sbp': objState['music'] = Sound.get(o[2]).file
                    case 'Sbs': pass # Music stop
                    case 'Sbv': pass # Music volume
                    case 'Ssp': objState['sound'] = Sound.get(o[2]).file
                    case 'Fo': objState |= {'transition': f'#{int(o[3]):02X}{int(o[4]):02X}{int(o[5]):02X}', 'alpha': o[6], 'in': o[2]}
                    case 'Fi': objState['out'] = o[2]
                    case 'w': pass # Wait?
                    case 'p': pass # Clean text
                    case 'Wm':
                        objUnit = {
                            'unit': o[3],
                            'name': o[2],
                            'expression': o[4],
                            'text': ''
                        }
                    case 'n': objUnit['name'] = o[2]
                    case 'E': objUnit['expression'] = o[2]
                    case '_': objUnit['text'] += o[0]
                    case _: print(TODO + 'Unhandled tag: ' + o[0])

                s = s[o.end():]
        
            if   'in' in objState and 'out' not in objState: objState['out'] = 0
            elif 'out' in objState and 'in' not in objState: objState |= {'transition': 'black', 'in': 0}
            elif 'in' in objState and 'out' in objState and objState['in'] == objState['out']:
                objState['time'] = objState['in']; objState.pop('in'); objState.pop('out')
            if objUnit['text'][-9:] == '@c:reset@': objUnit['text'] = objUnit['text'][:-9]

            if objState != {}: obj.append(objState)
            if objUnit['text'] != '': obj.append(objUnit.copy())

        objs[l] = obj

    return objs

def _mergeObjects(langs):
    from ..Tool.globals import WARNING
    stack = []
    for l,objs in langs.items():
        i = 0
        suffix = '' if l == 'USEN' else 'JP' if l == 'JPJA' else l
        for obj in objs:
            if 'unit' not in obj:
                # End of stack => Append to stack
                if i >= len(stack):
                    stack.append(obj)
                    i += 1
                # Same as currently => Skip (for second language onward)
                elif stack[i] == obj:
                    i += 1
                # Error (different effect | missing unit) => Move to end of stack
                else:
                    print(WARNING + f'Failed to merge {l} objects at {i}: {obj}')
                    stack.append(obj)
                    i = len(stack)
            else:
                text = obj.pop('text')
                # Same unit as previously => Merge with previous
                if i > 0 and obj == {k:v for k,v in stack[i-1].items() if k in ('unit','name','expression')}:
                    if ('text'+suffix) not in stack[i-1]:
                        stack[i-1]['text'+suffix] = [text]
                    else:
                        stack[i-1]['text'+suffix].append(text)
                # Same unit as currently => Merge with current (for second language onward)
                elif i < len(stack) and obj == {k:v for k,v in stack[i].items() if k in ('unit','name','expression')}:
                    if ('text'+suffix) not in stack[i]:
                        stack[i]['text'+suffix] = [text]
                    else:
                        stack[i]['text'+suffix].append(text)
                    i += 1
                # End of stack => Add to stack (for first language only)
                elif i == len(stack):
                    obj['text'+suffix] = [text]
                    stack.append(obj)
                    i += 1
                # Error (in stack, different unit from current and previous) => Move to end of stack
                else:
                    print(WARNING + f'Failed to merge {l} objects at {i}: {obj}')
                    obj['text'+suffix] = [text]
                    stack.append(obj)
                    i = len(stack)

    return stack

def _stringifyObjects(objs):
    from .Messages import Messages
    from .Units import Units

    stack = []
    for i,obj in enumerate(objs):
        # Unit object
        if 'unit' in obj:
            prev = objs[i-1] if i > 0 and 'unit' in objs[i-1] else objs[i-2] if i > 1 and 'unit' in objs[i-2] else {'unit':'','name':'','expression':''}
            unit = Units.fromFace(obj['unit'])
            o = {}

            # New unit
            if obj['unit'] != prev['unit']:
                o['unit'] = unit.name if unit else ('<!--' + obj['unit'] + '-->')
                if obj['expression'] != 'Face':
                    o['expression'] = obj['expression'][5:]
                if obj['name'] != 'M'+unit.data['id_tag']:
                    if unit.isDuo and obj['name'] == 'M'+unit.duoId:
                        o['duo'] = 1
                    elif Messages.EN(obj['name']) != Messages.EN(unit.data['id_tag']):
                        o['name'] = Messages.EN(obj['name'])
                        if 'textJP' in obj: o['nameJP'] = Messages.JP(obj['name'])
                        o.update({'name'+k[4:]: Messages.get(obj['name'], k[4:]) for k in obj.keys() if k[:4] == 'text' and k not in ('text','textJP')})

            # Same unit as before
            else:
                if obj['expression'] != prev['expression']:
                    o['expression'] = obj['expression'][5:]
                if obj['name'] != prev['name']:
                    if   unit.isDuo and obj['name'] == 'M'+unit.data['id_tag']: o['duo'] = ''
                    elif unit.isDuo and obj['name'] == 'M'+unit.duoId: o['duo'] = 1
                    else:
                        o['name'] = Messages.EN(obj['name'])
                        if 'textJP' in obj: o['nameJP'] = Messages.JP(obj['name'])
                        o.update({'name'+k[4:]: Messages.get(obj['name'], k[4:]) for k in obj.keys() if k[:4] == 'text' and k not in ('text','textJP')})

            # Text management
            textColor = ''
            while True:
                colors = [v[0][:v[0].find('@',1)+1] if v[0].find('@c:reset@') == -1 else '' for k,v in obj.items() if k[:4] == 'text' and len(v) > 0]
                if   len(colors) == 0: break
                elif len(colors) == 1:
                    k = [k for k,v in obj.items() if k[:4] == 'text' and len(v) > 0][0]
                    colors2 = [s[:s.find('@',1)+1] for s in obj[k]]
                    if all([c == colors2[0] for c in colors2]) and colors2[0][:3] == '@c:':
                        obj[k] = [colors2[0] + '\n\t'.join(obj[k]).replace(colors2[0],'')]
                    elif all([c[:3] != '@c:' for c in colors2]):
                        obj[k] = ['\n\t'.join(obj[k])]

                if colors[0][:3] == '@c:' and all([color == colors[0] for color in colors]):
                    for k in [k for k in obj.keys() if k[:4] == 'text' and len(obj[k]) > 0]: obj[k][0] = obj[k][0][len(colors[0]):]
                    if textColor != colors[0][3:-1]: o['color'] = textColor = colors[0][3:-1]
                elif textColor != '':
                    o['color'] = textColor = ''

                for k in [k for k in obj.keys() if k[:4] == 'text' and len(obj[k]) > 0]:
                    o[k] = obj[k].pop(0).replace('@c:reset@','$').replace('@','$')

                stack.append('{' + ';'.join([f"{k}={v}" for k,v in o.items()]) + '};')
                o = {}

        # Effect object
        else:
            obj = [f"{k}={v}" for k,v in obj.items() if (k,v) != ('alpha','255')]
            obj = [o.replace('.ogg','').replace('.ckb','') for o in obj]
            stack.append('{' + ';'.join(obj) + '};')

    return '[\n  ' + '\n  '.join(stack) + '\n]'
