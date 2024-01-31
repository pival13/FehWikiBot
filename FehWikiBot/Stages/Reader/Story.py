#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail
from .Stage import StageReader

class StoryMapReader(IReader):
    _basePath = 'Common/SRPG/StageScenario/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x575328d11a57cb1D)
        self.readArray()
        for _ in range(nb):
            # nbDiff
            self.prepareObject()
            self.readString('id_tag')
            self.insert('url_ids', [self.getString() for _ in range(2)])
            readAvail(self, 'avail')
            self.readInt('sort_id', 0x3983F63D)
            self.readInt('num_id', 0xB8884244)
            self.readBool('paralogue', 0xB6)
            self.skip(0x05) # 0xFD3E451AEC
            self.readByte('book', 0x29)
            self.skip(0x01) # padding
            count = self.overviewInt(8, 0x092DFD01)

            # Actually, 3 objects with the following block.
            # Reading only the first here because of redundancy
            self.readArray('required')
            for _ in range(count):
                self.readString()
            self.end()
            self.skip(0x04) # required count
            self.skip(0x04) # padding
            count = self.overviewInt(0x10, 0x2F416DFF)
            self.readArray('maps')
            for i in range(count):
                # The only non-redundant elemnts. Therefore moving the object here
                self.prepareObject()
                for j in range(3):
                    arrPtr = self.overviewLong(self._stack[-2][1]-0x08 + j*0x28 - self._i)
                    if arrPtr == 0: continue
                    stage = StageReader(self._buff, arrPtr + i*0x78).object
                    self.insert(stage['diff'], stage)
                self.end()
            self.end()
            self.skip(0x08) # array of count sbyte(0x2E) (0/-1)
            self.skip(0x04) # maps count
            self.skip(0x01) # 0xC4 (isParalogue)
            self.skip(0x03) # padding
            
            self.skip(0x50) # The previous block repeated twice
            self.end()
        self.end()

ParalogueReader = StoryMapReader
StageScenarioReader = StoryMapReader
