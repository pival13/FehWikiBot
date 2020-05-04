#! /usr/bin/env python3

DERIVED_SETTINGS = [
    {
        'value': [ {'name': 'squad_assault', 'diff': ['Lunatic']} ],
        'mapCond': [ {'true_lv': 50, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130} ],
        'extraCond': [ lambda groupId, index : groupId[:2] == 'SB' ]
    },

    {
        'value': [
            {'name': 'cc_story_odd1_single', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_even1_single', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_odd1_single', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_even1_single', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 30, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 35, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S0' and index == 0 and int(groupId[-1]) % 2 == 1,
            lambda groupId, index : groupId[3:5] == 'S0' and index == 0 and int(groupId[-1]) % 2 == 0,
            lambda groupId, index : groupId[3:5] == 'X0' and index == 0 and int(groupId[-1]) % 2 == 0,
            lambda groupId, index : groupId[3:5] == 'X0' and index == 0 and int(groupId[-1]) % 2 == 1
        ]
    },
    {
        'value': [
            {'name': 'cc_story_odd2_single', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_even2_single', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 31, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 36, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 41, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S0' and index == 1 and int(groupId[-1]) % 2 == 1,
            lambda groupId, index : groupId[3:5] == 'S0' and index == 1 and int(groupId[-1]) % 2 == 0
        ]
    },
    {
        'value': [
            {'name': 'cc_story_odd3_single', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_even3_single', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_odd2_single', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_even2_single', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 32, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 37, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 42, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S0' and index == 2 and int(groupId[-1]) % 2 == 1,
            lambda groupId, index : groupId[3:5] == 'S0' and index == 2 and int(groupId[-1]) % 2 == 0,
            lambda groupId, index : groupId[3:5] == 'X0' and index == 1 and int(groupId[-1]) % 2 == 0,
            lambda groupId, index : groupId[3:5] == 'X0' and index == 1 and int(groupId[-1]) % 2 == 1
        ]
    },
    {
        'value': [
            {'name': 'cc_story_odd4_single', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_even4_single', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 33, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 38, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 43, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S0' and index == 3 and int(groupId[-1]) % 2 == 1,
            lambda groupId, index : groupId[3:5] == 'S0' and index == 3 and int(groupId[-1]) % 2 == 0
        ]
    },
    {
        'value': [
            {'name': 'cc_story_odd5_single', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_even5_single', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_odd3_single', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_even3_single', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_odd1_double', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_odd2_double', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_odd1_double', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 35, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S0' and index == 4 and int(groupId[-1]) % 2 == 1,
            lambda groupId, index : groupId[3:5] == 'S0' and index == 4 and int(groupId[-1]) % 2 == 0,
            lambda groupId, index : groupId[3:5] == 'X0' and index == 2 and int(groupId[-1]) % 2 == 0,
            lambda groupId, index : groupId[3:5] == 'X0' and index == 2 and int(groupId[-1]) % 2 == 1,
            lambda groupId, index : groupId[3:5] == 'S1' and index == 0 and int(groupId[-1]) % 2 == 0,
            lambda groupId, index : groupId[3:5] == 'S1' and index == 1 and int(groupId[-1]) % 2 == 0,
            lambda groupId, index : groupId[3:5] == 'X1' and index == 0 and int(groupId[-1]) % 2 == 1
        ]
    },
    {
        'value': [
            {'name': 'cc_story_odd3_double', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_odd4_double', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_odd2_double', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 36, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 41, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 46, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S1' and index == 2,
            lambda groupId, index : groupId[3:5] == 'S1' and index == 3,
            lambda groupId, index : groupId[3:5] == 'X1' and index == 1
        ]
    },
    {
        'value': [
            {'name': 'cc_story_odd5_double', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_odd3_double', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_even2_double', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 38, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 43, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 48, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S1' and index == 4,
            lambda groupId, index : groupId[3:5] == 'X1' and index == 2,
            lambda groupId, index : groupId[3:5] == 'X1' and index == 4
        ]
    },
    {
        'value': [
            {'name': 'cc_story_even1_double', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_even2_double', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 37, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 42, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
            {'true_lv': 47, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 140}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S1' and index == 5,
            lambda groupId, index : groupId[3:5] == 'S1' and index == 6,
        ]
    },
    {
        'value': [
            {'name': 'cc_story_even3_double', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_even4_double', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 38, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 43, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
            {'true_lv': 48, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 140}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S1' and index == 7,
            lambda groupId, index : groupId[3:5] == 'S1' and index == 8,
        ]
    },
    {
        'value': [ {'name': 'cc_story_even5_double', 'diff': ['Normal', 'Hard', 'Lunatic']} ],
        'mapCond': [
            {'true_lv': 40, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
            {'true_lv': 50, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 140}
        ],
        'extraCond': [ lambda groupId, index : groupId[3:5] == 'S1' and index == 9 ]
    },
    {
        'value': [ {'name': 'cc_paralogue_even1_double', 'diff': ['Normal', 'Hard', 'Lunatic']} ],
        'mapCond': [
            {'true_lv': 37, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 42, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 47, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [ lambda groupId, index : groupId[3:5] == 'X1' and index == 3 ]
    },
    {
        'value': [ {'name': 'cc_paralogue_even3_double', 'diff': ['Normal', 'Hard', 'Lunatic']} ],
        'mapCond': [
            {'true_lv': 40, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 50, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [ lambda groupId, index : groupId[3:5] == 'X1' and index == 5 ]
    },

    {
        'value': [ {'name': 'blessed_gardens', 'diff': ['Normal']} ],
        'mapCond': [ {'true_lv': 30, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 80} ],
        'extraCond': [ lambda groupId, index : groupId[-2] == '0' ]
    },
    {
        'value': [ {'name': 'blessed_gardens', 'diff': ['Hard']} ],
        'mapCond': [ {'true_lv': 35, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 80} ],
        'extraCond': [ lambda groupId, index : groupId[-2] == '0' ]
    },
    {
        'value': [ {'name': 'blessed_gardens', 'diff': ['Lunatic']} ],
        'mapCond': [ {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 110} ],
        'extraCond': [ lambda groupId, index : groupId[-2] == '0' ]
    },
    {
        'value': [ {'name': 'blessed_gardens', 'diff': ['Infernal']} ],
        'mapCond': [ {'true_lv': 50, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 150} ],
        'extraCond': [ lambda groupId, index : groupId[-2] == '0' ]
    },
    {
        'value': [ {'name': 'blessed_grounds_odd', 'diff': ['Lunatic']} ],
        'mapCond': [ {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 110} ],
        'extraCond': [ lambda groupId, index : groupId[-2:] == '10' ]
    },
    {
        'value': [ {'name': 'blessed_grounds_odd', 'diff': ['Infernal']} ],
        'mapCond': [ {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 110} ],
        'extraCond': [ lambda groupId, index : groupId[-2] != '0' and int(groupId[-1]) % 2 == 1 ]
    },
    {
        'value': [ {'name': 'blessed_grounds_even', 'diff': ['Infernal']} ],
        'mapCond': [ {'true_lv': 50, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 150} ],
        'extraCond': [ lambda groupId, index : groupId[-2] != '0' and int(groupId[-1]) % 2 == 0 ]
    },




    {
        'value': [
            {'name': 'cc_paralogue_odd1_single_cx019', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_even1_single_cx019', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 30, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 37, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId == 'ST_X0036' and index == 0,
            lambda groupId, index : groupId == 'ST_X0037' and index == 0
        ]
    },
    {
        'value': [
            {'name': 'cc_paralogue_odd3_single_cx019', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_even3_single_cx019', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 37, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId == 'ST_X0036' and index == 2,
            lambda groupId, index : groupId == 'ST_X0037' and index == 2
        ]
    },
    {
        'value': [ {'name': 'cc_paralogue_double1_cx019', 'diff': ['Normal', 'Hard', 'Lunatic']} ],
        'mapCond': [
            {'true_lv': 37, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [ lambda groupId, index : groupId == 'ST_X1037' and index == 0 ]
    }
]

MY_DERIVED_SETTINGS = [
    {
        'value': [ {'name': 'squad_assault', 'diff': ['Lunatic']} ],
        'mapCond': [ {'true_lv': 50, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130} ],
        'extraCond': [ lambda groupId, index : groupId[:2] == 'SB' ]
    },
    {
        'value': [
            {'name': 'cc_story_single1', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_single1', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 30, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 35, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S0' and index == 0,
            lambda groupId, index : groupId[3:5] == 'X0' and index == 0
        ]
    },
    {
        'value': [ {'name': 'cc_story_single2', 'diff': ['Normal', 'Hard', 'Lunatic']} ],
        'mapCond': [
            {'true_lv': 31, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 36, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 41, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [ lambda groupId, index : groupId[3:5] == 'S0' and index == 1 ]
    },
    {
        'value': [
            {'name': 'cc_story_single3', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_single2', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 32, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 37, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 42, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S0' and index == 2,
            lambda groupId, index : groupId[3:5] == 'X0' and index == 1
        ]
    },
    {
        'value': [ {'name': 'cc_story_single4', 'diff': ['Normal', 'Hard', 'Lunatic']} ],
        'mapCond': [
            {'true_lv': 33, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 38, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 43, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [ lambda groupId, index : groupId[3:5] == 'S0' and index == 3 ]
    },
    {
        'value': [
            {'name': 'cc_story_single5', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_single3', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_double1', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_double2', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_double1', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 35, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S0' and index == 4,
            lambda groupId, index : groupId[3:5] == 'X0' and index == 2,
            lambda groupId, index : groupId[3:5] == 'S1' and index == 0,
            lambda groupId, index : groupId[3:5] == 'S1' and index == 1,
            lambda groupId, index : groupId[3:5] == 'X1' and index == 0
        ]
    },
    {
        'value': [
            {'name': 'cc_story_double3', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_double4', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_double2', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 36, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 41, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 46, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S1' and index == 2,
            lambda groupId, index : groupId[3:5] == 'S1' and index == 3,
            lambda groupId, index : groupId[3:5] == 'X1' and index == 1
        ]
    },
    {
        'value': [
            {'name': 'cc_story_double5', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_double3', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_paralogue_double5', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 38, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 43, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 48, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S1' and index == 4,
            lambda groupId, index : groupId[3:5] == 'X1' and index == 2,
            lambda groupId, index : groupId[3:5] == 'X1' and index == 4
        ]
    },
    {
        'value': [
            {'name': 'cc_story_double6', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_double7', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 37, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 42, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
            {'true_lv': 47, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 140}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S1' and index == 5,
            lambda groupId, index : groupId[3:5] == 'S1' and index == 6,
        ]
    },
    {
        'value': [
            {'name': 'cc_story_double8', 'diff': ['Normal', 'Hard', 'Lunatic']},
            {'name': 'cc_story_double9', 'diff': ['Normal', 'Hard', 'Lunatic']}
        ],
        'mapCond': [
            {'true_lv': 38, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 43, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
            {'true_lv': 48, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 140}
        ],
        'extraCond': [
            lambda groupId, index : groupId[3:5] == 'S1' and index == 7,
            lambda groupId, index : groupId[3:5] == 'S1' and index == 8,
        ]
    },
    {
        'value': [ {'name': 'cc_story_double10', 'diff': ['Normal', 'Hard', 'Lunatic']} ],
        'mapCond': [
            {'true_lv': 40, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
            {'true_lv': 50, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 140}
        ],
        'extraCond': [ lambda groupId, index : groupId[3:5] == 'S1' and index == 9 ]
    },
    {
        'value': [ {'name': 'cc_paralogue_double4', 'diff': ['Normal', 'Hard', 'Lunatic']} ],
        'mapCond': [
            {'true_lv': 37, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 42, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 47, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [ lambda groupId, index : groupId[3:5] == 'X1' and index == 3 ]
    },
    {
        'value': [ {'name': 'cc_paralogue_double6', 'diff': ['Normal', 'Hard', 'Lunatic']} ],
        'mapCond': [
            {'true_lv': 40, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 50, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [ lambda groupId, index : groupId[3:5] == 'X1' and index == 5 ]
    },
    {
        'value': [ {'name': 'blessed_gardens', 'diff': ['Normal']} ],
        'mapCond': [ {'true_lv': 30, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 80} ],
        'extraCond': [ lambda groupId, index : groupId[-2] == '0' ]
    },
    {
        'value': [ {'name': 'blessed_gardens', 'diff': ['Hard']} ],
        'mapCond': [ {'true_lv': 35, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 80} ],
        'extraCond': [ lambda groupId, index : groupId[-2] == '0' ]
    },
    {
        'value': [ {'name': 'blessed_gardens', 'diff': ['Lunatic']} ],
        'mapCond': [ {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 110} ],
        'extraCond': [ lambda groupId, index : groupId[-2] == '0' ]
    },
    {
        'value': [ {'name': 'blessed_gardens', 'diff': ['Infernal']} ],
        'mapCond': [ {'true_lv': 50, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 150} ],
        'extraCond': [ lambda groupId, index : groupId[-2] == '0' ]
    },
    {
        'value': [ {'name': 'blessed_grounds_odd', 'diff': ['Lunatic']} ],
        'mapCond': [ {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 110} ],
        'extraCond': [ lambda groupId, index : groupId[-2:] == '10' ]
    },
    {
        'value': [ {'name': 'blessed_grounds_odd', 'diff': ['Infernal']} ],
        'mapCond': [ {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 110} ],
        'extraCond': [ lambda groupId, index : groupId[-2] != '0' and int(groupId[-1]) % 2 == 1 ]
    },
    {
        'value': [ {'name': 'blessed_grounds_even', 'diff': ['Infernal']} ],
        'mapCond': [ {'true_lv': 50, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 150} ],
        'extraCond': [ lambda groupId, index : groupId[-2] != '0' and int(groupId[-1]) % 2 == 0 ]
    },




    {
        'value': [ {'name': 'cc_paralogue_single1_cx019', 'diff': ['Normal', 'Hard', 'Lunatic']} ],
        'mapCond': [
            {'true_lv': 30, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 37, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [ lambda groupId, index : (groupId == 'ST_X0036' or groupId == 'ST_X0037') and index == 0 ]
    },
    {
        'value': [ {'name': 'cc_paralogue_single3_cx019', 'diff': ['Normal', 'Hard', 'Lunatic']} ],
        'mapCond': [
            {'true_lv': 37, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [ lambda groupId, index : (groupId == 'ST_X0036' or groupId == 'ST_X0037') and index == 2 ]
    },
    {
        'value': [ {'name': 'cc_paralogue_double1_cx019', 'diff': ['Normal', 'Hard', 'Lunatic']} ],
        'mapCond': [
            {'true_lv': 37, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
            {'true_lv': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
            {'true_lv': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130}
        ],
        'extraCond': [ lambda groupId, index : groupId == 'ST_X1037' and index == 0 ]
    }
]
