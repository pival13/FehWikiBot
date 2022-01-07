from os.path import dirname, realpath, isfile
import sys

sys.path.insert(0, dirname(realpath(__file__)))

from .REutil  import decompress
from .Reverse import reverseFile as reverse

from .RevData  import reverseMessage
from .RevSound import reverseBGM, reverseSound

from .RevVG  import reverseVotingGauntlet
from .RevTT  import reverseTempestTrial
from .RevTB  import reverseTapBattle
from .RevGC  import reverseGrandConquests
from .RevFB  import reverseForgingBonds
from .RevRS  import reverseRokkrSieges
from .RevLL  import reverseLostLore
from .RevHoF import reverseHallOfForms
from .RevMS  import reverseMjolnirsStrike
from .RevFP  import reverseFrontlinePhalanx
from .RevPoL import reversePawnsOfLoki
from .RevHJ  import reverseHeroesJourney

def reverseMjolnirFacility(tag: str):
    from .Reverse import parseMjolnirFacility
    from .REutil import BINLZ_ASSETS_DIR_PATH

    fpath = BINLZ_ASSETS_DIR_PATH + f"/Common/Mjolnir/FacilityData/{tag}.bin.lz"
    if isfile(fpath):
        data = decompress(fpath)
        return parseMjolnirFacility(data[0x20:])

sys.path.pop(0)
