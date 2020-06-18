# -*- coding: utf-8 -*-
import sys

from oslo_config import cfg
import PlayerManager
import RankerMachine
from oslo_service import wsgi
from gevent import pywsgi
import threading
import time

def svc():
    loader = wsgi.Loader(cfg.CONF)
    wsgi_app = loader.load_app('rank-parser')

    server = pywsgi.WSGIServer(('0.0.0.0', 8080), wsgi_app)
    server.serve_forever()

def main():
    opts = [cfg.StrOpt('NameList')]

    cfg.CONF.register_opts(opts)

    cfg.CONF(sys.argv[1:])

    t = threading.Thread(target=svc)
    t.setDaemon(True)
    t.start()

    server_names = cfg.CONF.NameList.split(',')

    playerManager = PlayerManager.PlayerManager.get_instance()
    rankerMachine = RankerMachine.RankerMachine.get_instance()

    for sn in range(len(server_names)):
        tmp = server_names[sn].split('-')
        if len(tmp) != 2:
            continue
        server = tmp[0]
        name = tmp[1]
        playerManager.addPlayer(server,name)

    while(True):
        print "start update"
        playerManager.refreshData()
        rankerMachine.refreshData(playerManager.players)
        print "stop update"
        time.sleep(3600)


    t.join()


def test():
    class T:
        def __init__(self,a):
            self.a = a
    la = []
    la.append(T(10))
    la.append(T(4))
    la.append(T(5))
    la.append(T(7))
    la.append(T(23))
    la.append(T(43))

    def soutf(elem):
        return elem.a

    la.sort(key=soutf)

    for s in la:
        print s.a


if __name__ == "__main__":
    sys.exit(main())
    #sys.exit(test())