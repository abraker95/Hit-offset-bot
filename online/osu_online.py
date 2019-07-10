import urllib.request
import json
import io

from file.beatmap import Beatmap
from online.session_manager import SessionMgr
from online.rate_limited import rate_limited
from online.login import username, password


class OsuOnline():

    session_manager = None

    @staticmethod
    @rate_limited(rate_limit=0.5)
    def fetch_beatmap_file(beatmap_id, strio=False):
        url      = 'https://osu.ppy.sh/osu/' + str(beatmap_id)
        response = urllib.request.urlopen(url)
        data     = response.read()
        
        if not strio: return data.decode('utf-8')
        else:         return io.StringIO(data.decode('utf-8'))

    
    @staticmethod
    @rate_limited(rate_limit=3)
    def fetch_scores(beatmap_id, gamemode):
        if type(gamemode) == int:
            if   gamemode == Beatmap.GAMEMODE_OSU:   gamemode = 'osu'
            elif gamemode == Beatmap.GAMEMODE_TAIKO: gamemode = 'taiko'
            elif gamemode == Beatmap.GAMEMODE_CATCH: gamemode = 'fruits'
            elif gamemode == Beatmap.GAMEMODE_MANIA: gamemode = 'mania'
            else: raise Exception('Unknown gamemode: ' + str(gamemode))
        
        url = 'https://osu.ppy.sh/beatmaps/' + str(beatmap_id) + '/scores?type=global&mode=' + str(gamemode)
        try: response = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print('Error opening ' + url + '\n' + str(e))
            return

        data = json.loads(response.read())
        return data['scores']


    @staticmethod
    @rate_limited(rate_limit=3)
    def fetch_replay_file(gamemode, replay_id):
        if not OsuOnline.session_manager:
            OsuOnline.session_manager = SessionMgr()
            OsuOnline.session_manager.login(username, password)

        xsrf_token = OsuOnline.session_manager.get_xsrf_token()
        if xsrf_token == None: raise Exception('xsrf_token is None')

        osu_session = OsuOnline.session_manager.get_osu_session()
        if osu_session == None: raise Exception('osu_session is None')

        if type(gamemode) == int:
            if   gamemode == Beatmap.GAMEMODE_OSU:   gamemode = 'osu'
            elif gamemode == Beatmap.GAMEMODE_TAIKO: gamemode = 'taiko'
            elif gamemode == Beatmap.GAMEMODE_CATCH: gamemode = 'fruits'
            elif gamemode == Beatmap.GAMEMODE_MANIA: gamemode = 'mania'
            else: raise Exception('Unknown gamemode: ' + str(gamemode))

        url = 'https://osu.ppy.sh/scores/' + str(gamemode) + '/' + str(replay_id) + '/download'
        headers = {
            'X-CSRF-TOKEN': xsrf_token,
            'osu_session' : osu_session
        }

        print(url)

        response = OsuOnline.session_manager.get(url, headers=headers)
        return response.content