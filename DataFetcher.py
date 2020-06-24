# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

class DataFetcher:


    # result = {
    #     'server' : "xxx",
    #     'name' : "xxx",
    #     'url' : "https://classic.warcraftlogs.com/character/cn/xxx/xxx",
    #     'class' : 'Rouge',
    #     'Blackwing Lair' : { 'score':407,'rank':121034 },
    #     'Molten Core' : {'score':456,'rank':151034}
    # }
    def fetchData(self,server,name):
        result = {
            'name':name,
            'server':server
        }

        url = "https://classic.warcraftlogs.com/character/cn/" + server + '/' + name

        result['url'] = url

        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()

        soup = BeautifulSoup(res, 'html5lib')

        classdiv = soup.find_all(id='character-class')
        result['class'] = unicode(classdiv[0].contents[0].string).strip()


        raidRankDivs = soup.find_all('div','header-zone-box')

        for index in range(len(raidRankDivs)):
            zon_name = unicode(raidRankDivs[index].find_all('div', 'header-zone-points')[0].contents[0].string).strip()
            if zon_name != "P3 & P4":
                continue
            raidName = unicode(raidRankDivs[index].find_all('div','header-zone-name')[0].contents[0].string).strip()
            score = int(unicode(raidRankDivs[index].find_all('span','primary header-rank')[0].contents[0].string))

            rank =  int(unicode(raidRankDivs[index].find_all('div','header-zone-positions')[0].find_all('span')[0].contents[0].string))
            result[raidName] = {
                'score':score,
                'rank':rank}
            # if raidName == 'Blackwing Lair':
            #     pass
            # elif raidName == 'Molten Core':
            #     pass

        return result

    # serverid: 娅尔罗:5105
    # bossid: Molten Core:673 Blackwing Lair:630
    # pclass:Warrior,Mage ...
    # pspec:Frost,Fury ...
    # num: fetch data numbers,multiple of 100
    def fetchServerDpsData(self,serverid,bossid,pclass,pspec,num):

        resultNumNmae = {}
        resultNameInfo = {}

        for i in range(num/100):
            url = "https://classic.warcraftlogs.com/zone/rankings/table/1500/bossdps/" \
                  + str(bossid) + "/3/40/2/" + pclass + "/" + pspec + "/0/" + str(serverid) + "/0/0/0/?search=&page=" \
                  + str(i + 1) + "&affixes=0&faction=1&dpstype=rdps&restricted=1"

            try:

                req = urllib2.Request(url)
                res_data = urllib2.urlopen(req)
                res = res_data.read()
            except Exception,e:
                continue

            soup = BeautifulSoup(res, 'html5lib')

            for j in range(100):
                ranknum = i*100 + j + 1
                rankid = "row-" + str(bossid) + "-" + str(ranknum)
                ranktr = soup.find_all(id=rankid)
                if(len(ranktr) > 0 and len(ranktr[0].a.contents) > 0):
                    name = unicode(ranktr[0].a.contents[0].string).encode('utf8')
                    href = unicode(ranktr[0].a.get('href')).encode('utf8')
                else:
                    continue

                dpstd = ranktr[0].find_all('td', 'players-table-dps')
                dps = 0
                if(len(dpstd) > 0 and len(dpstd[0].contents) > 0):
                    dps = float(unicode(dpstd[0].contents[0].string).strip().replace(',',''))


                resultNumNmae[ranknum] = name
                resultNameInfo[name] = {'rank':ranknum,'dps':dps, 'href':href}

        return resultNumNmae,resultNameInfo


if __name__ == "__main__":

    df = DataFetcher()
    resultNumNmae, resultNameNum = df.fetchServerDpsData(5105,673,"Mage","Frost",100)

    print resultNumNmae[1]

