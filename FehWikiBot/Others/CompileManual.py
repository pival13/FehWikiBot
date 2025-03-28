#! /usr/bin/env python3

from ..Tool import Container
from .Reader.CompileManual import CompileCombatManualReader

class CompileManual(Container):
    _reader = CompileCombatManualReader

    @classmethod
    def updateExportFromAssets(cls, tag: str):
        import re
        from datetime import datetime
        from ..Tool.Wiki import Wiki
        from ..Tool.misc import waitSec
        from ..Utility.Units import Heroes
        from ..Utility.Messages import EN

        cls.load(tag)
        datas = cls._DATA.get(tag)
        if not datas: return
        name = 'Combat Manuals'
        page = Wiki.getPageContent(name)
        delim = page.find('===Limited-time===')
        start = datetime.now().strftime('%Y-%m-%dT07:00:00Z')

        for data in datas.values():
            if not data['limited']:
                if page[:delim].find(data['currency']) != -1: continue
                s = f"===Normal {data['part']}===\n"
                iGr = 0
                for firstManual in [o for o in data['targets'] if o['prev_idx'] is None]:
                    idx = data['targets'].index(firstManual)
                    s += '{| class="wikitable" style="text-align:center"\n'
                    s += '|+ ' + EN(f"MID_UNIT_EDIT_STOCK_SHOP_TREE_{data['currency']}_{iGr}") + '\n'
                    s += '! Item !! Availability !! Path\n'
                    s += '{{#invoke:CompileCombatManuals|targets|path=yes\n'
                    s += f"|item=Divine Code: Part {data['part']}\n"
                    s += '|start=' + start + '\n'
                    s += '|manuals=[\n'
                    while True:
                        manual = data['targets'][idx]
                        unit = Heroes.get(manual['reward'][0]['id_tag']).name
                        s += f"  {{unit={unit};rarity={manual['reward'][0]['rarity']};cost={manual['cost']}}};\n"
                        tmps = [o for o in data['targets'] if o['prev_idx'] == idx]
                        if tmps == []: break
                        idx = data['targets'].index(tmps[0])
                    s += ']}}\n|}\n'
                    iGr += 1

                end = page.rfind('|}\n',0,delim)+3
                page = page[:end] + s + page[end:]
                delim = page.find('===Limited-time===')

            # Limited
            else:
                if page[delim:].find(data['avail']['end']) != -1: continue
                s = ''
                if data['part'] == 1:
                    s += '|}\n'
                    s += '{| class="wikitable" style="text-align:center"\n'
                    s += f"|+ {data['avail']['end'][:4]}\n"
                    s += '! Item !! Availability !! Combat Manuals\n'
                s += '{{#invoke:CompileCombatManuals|targets\n'
                s += f"|item=Divine Code: Ephemera {data['part']}\n"
                s += '|start=' + start + '\n'
                s += '|end=' + data['avail']['end'] + '\n'
                s += '|manuals=[\n'
                for manual in data['targets']:
                    unit = Heroes.get(manual['reward'][0]['id_tag']).name
                    s += f"  {{unit={unit};rarity={manual['reward'][0]['rarity']};cost={manual['cost']}}};\n"
                s += ']}}\n'

                end = re.search(r'\|\}\n+==', page[delim:])
                page = page[:delim+end.start()] + s + page[delim+end.start():]

        waitSec(10)
        Wiki.exportPage(name, page, 'Combat manuals ('+tag+')', minor=False, create=False)
