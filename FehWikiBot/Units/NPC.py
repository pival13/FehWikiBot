#! /usr/bin/env python3

class NPC:
    UNITS = {
        # 'ch00_00_Eclat_X_Normal':       {'name': 'Kiran'}, # Mini unit only
        'ch00_00_Eclat_X_Avatar00':     {'id': 'EID_アバター',      'name': 'Kiran: Hero Summoner'},
        'ch00_01_Alfons_M_Stain':       {'id': 'PID_アルフォンス',  'name': 'Alfonse: Prince of Askr (Injured)'},
        'ch00_04_Veronica_F_Stain':     {'id': 'EID_ヴェロニカ',    'name': 'Veronica: Emblian Princess (Injured)'},
        'ch00_04_Veronica2_F_Enemy':    {'id': 'EID_ヴェロニカ2',   'name': 'Veronica: Princess Beset (Legendary Dark)'},
        'ch00_04_Veronica2_F_Stain':    {'id': 'EID_ヴェロニカ2',   'name': 'Veronica: Princess Rising (Injured)'},
        'ch00_05_Bruno_M_Plain':        {'id': 'PID_ブルーノ皇子',  'name': 'Bruno (Unmasked)'},
        'ch00_05_Bruno_M_PlainStain':   {'id': 'PID_ブルーノ皇子',  'name': 'Bruno (Unmasked Injured)'},
        'ch00_13_Gustaf_M_Normal':      {'id': '',                  'name': 'Gustav'},# PID_グスタフ
        'ch00_14_Henriette_F_Normal':   {'id': '',                  'name': 'Henriette'},# PID_ヘンリエッテ
        'ch00_16_Freeze_M_Normal':      {'id': 'PID_フリーズ',      'name': 'Hríd: Icy Blade (Injured)'},
        'ch00_31_Otr_M_Stain':          {'id': 'EID_オッテル',      'name': 'Ótr: Kingsbrother (Injured)'},
        'ch00_32_Fafnir2_M_Stain':      {'id': 'EID_ファフニール',  'name': 'Fáfnir: King of Desolation (Injured)'},
        'ch00_36_MysteryHood_X_Normal': {'id': '',                  'name': 'Mystery Hood'},
        'ch00_40_Elm_M_Stain':          {'id': 'EID_エルム',        'name': 'Elm: Retainer to Embla (Injured)'},
        'ch00_42_Ask_M_Disappear':      {'id': 'PID_アスク',        'name': 'Askr: God of Openness (Disappear)'},
        'ch00_43_Embla_F_Disappear':    {'id': 'EID_エンブラ',      'name': 'Embla: God of Closure (Disappear)'},
        'ch00_45_Ganglot_F_Shadow':     {'id': 'PID_ガングレト',    'name': 'Ganglöt: Death Anew (Shadow)'},
        'ch00_47_Gullveig_F_Disappear': {'id': 'EID_グルヴェイグ',   'name': 'Gullveig: Golden Seer (Disappear)'},
        'ch00_49_Heith_Normal':         {'id': 'PID_ヘイズ',        'name': 'Heiðr: Innocent Goddess'},
        'ch00_51_Njord_M_Normal':       {'id': '',                  'name': 'Njörðr'}, # PID_ニョルズ
        'ch00_59_Lerazr_M_Disappear':   {'id': 'EID_レーラズ',      'name': 'Læraðr: Quieting Heart (Disappear)'},
        'ch00_62_Rune_M_Enemy':         {'id': 'PID_ルーン',        'name': 'Rune: Source of Wisdom (Alfaðör)'},
         # This is the tag used for non-face unit on scenarios
        'ch90_02_FighterAX_M_Normal':   {'id': '', 'name': ''}
    }

    @classmethod
    def fromFace(cls, name):
        if name not in cls.UNITS: return None
        o = cls()
        o.data = {
            'id_tag': cls.UNITS[name]['id'],
            'name': cls.UNITS[name]['name']
        }
        return o

    @property
    def name(self):
        return self.data['name'] if hasattr(self, 'data') else ''

    @property
    def isDuo(self): return False
