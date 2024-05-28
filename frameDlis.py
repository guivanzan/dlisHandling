from dlisio import dlis
import numpy as np

class frameDlis:
    def __init__(self, archive):

        frames = dlis.load(archive)
                                
        self.frameList = []
        self.depthList = []
        self.proxyList = []
        self.meanList = []
        self.maxList = []
        self.minList = []

        self.testList = []

        for logicalFile in frames:
            for frame in logicalFile.frames:
                channelList = []
                newList = []
                for channel in frame.channels:          
                    channelInfo = {
                        'name': channel.name, 
                        'longName': channel['LONG-NAME'], 
                        'unit': channel["UNITS"]
                            }
                    channelList.append(channelInfo)

                    self.testList.append(channelInfo) # Teste
                    
                    if channel != frame.channels[0]:
                        self.proxyList.append(channelInfo)
                        newList.append(f"{channel.name}: {channel['LONG-NAME']}")
                    else:
                        self.depthList.append(channelInfo)
                        newList.append(f"{channel.name}")
                        
                self.frameList.append(newList)

        # print(self.testList)
        # print(self.depthList)

        self.unicProxyList = [{'name':'None','longName':'None', 'unit':'','value':[]}]

        for i in self.proxyList:
            if i not in self.unicProxyList:
                self.unicProxyList.append(i)

        for logicalFile in frames:
            for frame in logicalFile.frames:
                depth = frame.channels[0].curves()
                meanDepth = []
                for i in range(len(depth)-1):
                    meanDepth.append(depth[i+1]-depth[i])
                self.meanList.append(np.mean(meanDepth))
                self.maxList.append(depth[-1])
                self.minList.append(depth[0])

        for j in range(len(self.depthList)):
            self.depthList[j]['sampling'] = round(self.meanList[j], 4)
            self.depthList[j]['nyquist'] = round(1 / (self.meanList[j]*2), 2)
            self.depthList[j]['max'] = round(self.maxList[j], 2)
            self.depthList[j]['min'] = round(self.minList[j], 2)
            self.depthList[j]['step'] = round((self.maxList[j]-self.minList[j])/830, 2)
            self.depthList[j]['win'] = round((self.maxList[j]-self.minList[j])/5, 2)