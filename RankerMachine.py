# -*- coding: utf-8 -*-
import json
import time

class RankerMachine:

    INSTANCE = None

    @classmethod
    def get_instance(cls):
        if not RankerMachine.INSTANCE:
            RankerMachine.INSTANCE = cls()
        return RankerMachine.INSTANCE

    def __init__(self):
        self.data = self.getInitData()
        self.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    def getInitData(self):
        data = {}

        # 战士
        data['Warrior'] = {'MoltenCore':[],'BlackwingLair':[]}

        # 盗贼
        data['Rogue'] = {'MoltenCore':[],'BlackwingLair':[]}

        # 法师
        data['Mage'] = {'MoltenCore':[],'BlackwingLair':[]}

        # 猎人
        data['Hunter'] = {'MoltenCore':[],'BlackwingLair':[]}

        # 术士
        data['Warlock'] = {'MoltenCore':[],'BlackwingLair':[]}

        # 德鲁伊
        data['Druid'] = {'MoltenCore':[],'BlackwingLair':[]}

        # 骑士
        data['Paladin'] = {'MoltenCore':[],'BlackwingLair':[]}

        # 牧师
        data['Priest'] = {'MoltenCore':[],'BlackwingLair':[]}

        # 萨满
        data['Shaman'] = {'MoltenCore':[],'BlackwingLair':[]}

        return data


    def refreshData(self,players):
        data = self.getInitData()


        def rankMoltenCoreFunction(elem):
            return elem.MoltenCoreRank

        def rankBlackwingLairFunction(elem):
            return elem.BlackwingLairRank

        for server in players:
            for pkey in players[server]:
                player = players[server][pkey]
                if not data.has_key(player.playerClass):
                    continue

                data[player.playerClass]['MoltenCore'].append(player)
                data[player.playerClass]['BlackwingLair'].append(player)

        for k in data:
            data[k]['MoltenCore'].sort(key=rankMoltenCoreFunction)
            data[k]['BlackwingLair'].sort(key=rankBlackwingLairFunction)

        self.update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        self.data = data

    def printData(self):
        for k in self.data:

            str = k + " MoltenCore:"
            for p in self.data[k]['MoltenCore']:
                str = str + p.name + " "
            print str

            str = k + " BlackwingLair:"
            for p in self.data[k]['BlackwingLair']:
                str = str + p.name + " "
            print str

    def toJson(self):
        result = {}
        result['UpdateTime'] = self.update_time
        for pclass in self.data:

            result[pclass] = {}

            result[pclass]["MoltenCore"] = []
            for player in self.data[pclass]['MoltenCore']:
                ptmp = {}
                ptmp['name'] = player.name.decode('utf8')
                ptmp['score'] = player.MoltenCoreScore
                ptmp['rank'] = player.MoltenCoreRank
                ptmp['serverRank'] = player.MoltenCoreServerRank
                ptmp['url'] = player.url
                result[pclass]['MoltenCore'].append(ptmp)

            result[pclass]["BlackwingLair"] = []
            for player in self.data[pclass]['BlackwingLair']:
                ptmp = {}
                ptmp['name'] = player.name
                ptmp['score'] = player.BlackwingLairScore
                ptmp['rank'] = player.BlackwingLairRank
                ptmp['serverRank'] = player.BlackwingLairServerRank
                ptmp['url'] = player.url
                result[pclass]['BlackwingLair'].append(ptmp)

        return json.dumps(result)