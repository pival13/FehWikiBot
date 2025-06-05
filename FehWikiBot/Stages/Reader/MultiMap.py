#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail
from .Stage import MultiStageReader

class ChainChallengeReader(IReader):
    def parse(self):
        nb = self.overviewLong(0x08, 0xE7FD048635876CE5)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            count = self.overviewInt(0x08, 0x092DFD01)
            self.readArray('required')
            for _ in range(count):
                self.readString()
            self.end()
            self.skip(0x04) # reqs count
            self.assertPadding(4)
            readAvail(self, 'avail')
            self.readBool('is_paralogue', 0x86)
            self.assertBytes(7, 0xD72A9037E824AC)
            self.readInt('sort_id', 0x69CBCDC0)
            self.readByte('book', 0x1B)
            self.assertPadding(3)
            # Modifying the order
            count = self.overviewInt(0x08, 0xE3B3C3EC)
            stages = [{} for i in range(count)]
            for _ in range(3):
                self.readPointer()
                for i in range(count):
                    reader = MultiStageReader(self._buff, self._i)
                    stage = reader.object
                    stages[i][stage['diff']] = stage
                    self._i = reader._i
                self.end()
                self.skip(0x04) # count
                self.assertPadding(4)
            self.insert('stages', stages)
            self.end()
        self.end()

class StoryChainChallengeReader(ChainChallengeReader): _basePath = 'Common/SRPG/SequentialTrialMainStory/'
CCSReader = StoryChainChallengeReader
SequentialTrialMainStoryReader = StoryChainChallengeReader

class ParalogueChainChallengeReader(ChainChallengeReader): _basePath = 'Common/SRPG/SequentialTrialSideStory/'
CCPReader = ParalogueChainChallengeReader
SequentialTrialSideStoryReader = ParalogueChainChallengeReader

class SquadAssaultReader(IReader):
    _basePath = 'Common/SRPG/SequentialTrialBind/'

    def parse(self):
        nb = self.overviewLong(0x08, 0xC83DA1C1EF4B70D1)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            count = self.overviewInt(0x08,0x092DFD01)
            self.readArray('required')
            for _ in range(count):
                self.readString()
            self.end()
            self.skip(0x04) # count
            self.assertPadding(4)
            readAvail(self, 'avail')
            self.assertBytes(4,0xC9ABD7B5)
            self.readInt('sort_id', 0x493928EF)
            self.insert('stage', MultiStageReader(self._buff,self.getLong()).object)
            self.end()
        self.end()

SAReader = SquadAssaultReader
SequentialTrialBindReader = SquadAssaultReader
