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

    def printPlayerData(self):
        for server in self.players:
            for pkey in self.players[server]:
                player = self.players[server][pkey]
                print 'player:' + unicode(player.name.decode('utf8'))
                print 'MoltenCoreScore:' + str(player.MoltenCoreScore)
                print 'MoltenCoreRank:' + str(player.MoltenCoreRank)
                print 'BlackwingLairScore:' + str(player.BlackwingLairScore)
                print 'BlackwingLairRank:' + str(player.BlackwingLairRank)



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