#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail
from .Stage import StageReader

class TacticsDrillsReader(IReader):
    _basePath = 'Common/SRPG/StagePuzzle/'

    TYPE = ['Basics', 'Skill Studies', 'Grandmaster']

    def parse(self):
        nb = self.overviewLong(0x08, 0x07c8525a8f13c8558)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            readAvail(self, 'avail')
            self.readInt('sort_id', 0xBF35E827)
            self.readInt('num_id', 0xF6336EB6)
            self.insert('type', self.TYPE[self.getInt(0xF2103821)])
            self.skip(0x04) # padding
            self.insert('map', StageReader(self._buff, self.getLong()).object)
            self.end()
        self.end()

TDReader = TacticsDrillsReader
StagePuzzleReader = TacticsDrillsReader