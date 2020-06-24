# -*- coding: utf-8 -*-
import Player
import DataFetcher

class PlayerManager:
    INSTANCE = None

    @classmethod
    def get_instance(cls):
        if not PlayerManager.INSTANCE:
            PlayerManager.INSTANCE = cls()
        return PlayerManager.INSTANCE

    def __init__(self):
        self.players = {}
        self.dataFetcher = DataFetcher.DataFetcher()


    def addPlayer(self,server,name):
        if not self.players.has_key(server):
            self.players[server] = {}

        self.players[server][name] = Player.Player(server,name)

    def getPlayerByClass(self,playerClass):
        result = []
        for server in self.players:
            for name in self.players[server]:
                if self.players[server][name].playerClass == playerClass:
                    result.append(self.players[server][name])

        return result
    def refreshData(self):
        for server in self.players:
            for pkey in self.players[server]:
                player = self.players[server][pkey]
                try:
                    result = self.dataFetcher.fetchData(server,pkey)
                    player.url = result['url']
                    player.playerClass = result['class']
                    if(result.has_key('Blackwing Lair')):
                        player.BlackwingLairScore = result['Blackwing Lair']['score']
                        player.BlackwingLairRank = result['Blackwing Lair']['rank']

                    if(result.has_key('Molten Core')):
                        player.MoltenCoreScore = result['Molten Core']['score']
                        player.MoltenCoreRank = result['Molten Core']['rank']
                except Exception, e:
                    pass
    def refreshServerRank(self):
        classList = {'Warrior':{'num':1200,'spec':'Fury'},
                     'Mage':{'num':1200,'spec':'Frost'},
                     'Rogue':{'num':800,'spec':'Assassination'},
                     'Hunter':{'num':500,'spec':'Marksmanship'},
                     'Warlock':{'num':300,'spec':'Destruction'},
                     'Druid':{'num':500,'spec':'Restoration'},
                     'Paladin':{'num':500,'spec':'Holy'},
                     'Priest':{'num':500,'spec':'Holy'}}

        #classList = {'Mage': {'num': 500, 'spec': 'Frost'}}

        # 熔火之心
        moltenCoreBossID = 673
        # 黑翼之巢
        blackwingLairBossID = 630
        for keyclass in classList:
            print "start update " + keyclass + " server rank data"
            players = self.getPlayerByClass(keyclass)

            _, moltenCoreResult = self.dataFetcher.fetchServerDpsData(5105,moltenCoreBossID,keyclass,classList[keyclass]['spec'],classList[keyclass]['num'])
            _, blackwingLairResult = self.dataFetcher.fetchServerDpsData(5105,blackwingLairBossID,keyclass,classList[keyclass]['spec'],classList[keyclass]['num'])


            for player in players:
                if moltenCoreResult.has_key(player.name):
                    player.MoltenCoreServerRank = moltenCoreResult[player.name]['rank']
                    player.MoltenCoreServerDPS = moltenCoreResult[player.name]['dps']
                    player.MoltenCoreServerHref = "https://classic.warcraftlogs.com/" + moltenCoreResult[player.name]['href']

                if blackwingLairResult.has_key(player.name):
                    player.BlackwingLairServerRank = blackwingLairResult[player.name]['rank']
                    player.BlackwingLairServerDPS = blackwingLairResult[player.name]['dps']
                    player.BlackwingLairServerHref = "https://classic.warcraftlogs.com/" + blackwingLairResult[player.name]['href']

            print "finish update " + keyclass + " server rank data"






    def printPlayerData(self):
        for server in self.players:
            for pkey in self.players[server]:
                player = self.players[server][pkey]
                print 'player:' + unicode(player.name.decode('utf8'))
                print 'MoltenCoreScore:' + str(player.MoltenCoreScore)
                print 'MoltenCoreRank:' + str(player.MoltenCoreRank)
                print 'MoltenCoreServerRank:' + str(player.MoltenCoreServerRank)
                print 'BlackwingLairScore:' + str(player.BlackwingLairScore)
                print 'BlackwingLairRank:' + str(player.BlackwingLairRank)
                print 'BlackwingLairServerRank:' + str(player.BlackwingLairServerRank)



if __name__ == "__main__":
    playerManager = PlayerManager()
    playerManager.addPlayer('娅尔罗','战斗天使翼')
    playerManager.addPlayer('娅尔罗','鲜血与雷鸣')

    playerManager.refreshData()

    print playerManager.players['娅尔罗']['战斗天使翼'].BlackwingLairScore
    print playerManager.players['娅尔罗']['战斗天使翼'].BlackwingLairRank
    print playerManager.players['娅尔罗']['战斗天使翼'].MoltenCoreScore
    print playerManager.players['娅尔罗']['战斗天使翼'].MoltenCoreRank

    print playerManager.players['娅尔罗']['鲜血与雷鸣'].BlackwingLairScore
    print playerManager.players['娅尔罗']['鲜血与雷鸣'].BlackwingLairRank
    print playerManager.players['娅尔罗']['鲜血与雷鸣'].MoltenCoreScore
    print playerManager.players['娅尔罗']['鲜血与雷鸣'].MoltenCoreRank