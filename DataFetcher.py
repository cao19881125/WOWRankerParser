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

        soup = BeautifulSoup(res, 'html.parser')

        classdiv = soup.find_all(id='character-class')
        result['class'] = unicode(classdiv[0].contents[0].string).strip()


        raidRankDivs = soup.find_all('div','header-zone-box')

        for index in range(len(raidRankDivs)):
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


if __name__ == "__main__":
    data_fetcher = DataFetcher()
    result = data_fetcher.fetchData('娅尔罗','鲜血与雷鸣')
    print result
