import api
from webob import Request
import json
import RankerMachine
import PlayerManager


class RankDataApi(api.RestApiHandler):
    def _get(self, request, response):
        params = self._get_params(request)




        print "RankDataApi get"

        rankerMachine = RankerMachine.RankerMachine.get_instance()


        response.body = rankerMachine.toJson()



    @classmethod
    def factory(cls, global_conf, **kwargs):
        return cls()




class ForceRefreshApi(api.RestApiHandler):
    def _get(self, request, response):
        #params = self._get_params(request)

        print "ForceRefreshApi get"

        playerManager = PlayerManager.PlayerManager.get_instance()
        rankerMachine = RankerMachine.RankerMachine.get_instance()

        playerManager.refreshData()
        rankerMachine.refreshData(playerManager.players)


        response.body = json.dumps({'result': 'success'})

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return cls()


class ShowVersion():
    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        start_response("200 OK", [("Content-type", "text/plain")])
        # print environ
        req = Request(environ)
        print req.method
        print req.POST
        print req.body
        print req.authorization

        for key, value in req.params.items():
            print "key=" + str(key) + "  value=" + str(value)
        return ["Paste Deploy LAB: Version = 1.0.0", ]

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return ShowVersion()
