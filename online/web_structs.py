from misc.json_obj import JsonObj
from online.osu_online import OsuOnline

from file.beatmap_io import BeatmapIO
from file.replay_io import ReplayIO


class WebBeatmapset(JsonObj):

    def __init__(self, data):
        JsonObj.__init__(self, data)
        self.name         = self.artist + ' - ' + self.title + ' (' + self.creator + ') '
        self.web_beatmaps = None


    def get_beatmaps(self, refresh=False):
        if (self.web_beatmaps == None) or refresh:
            self.web_beatmaps = [ WebBeatmap(self.name, beatmap) for beatmap in self.beatmaps ]
        return self.web_beatmaps
        


class WebBeatmap(JsonObj):
    
    def __init__(self, name, data):
        JsonObj.__init__(self, data)
        self.name         = name + '[' + self.version + ']'
        self.web_scores   = None
        self.beatmap_file = None


    def get_scores(self, refresh=False):
        if (self.web_scores == None) or refresh:
            self.web_scores = [ WebScore(self.name, score) for score in OsuOnline.fetch_scores(self.id, self.mode) ]
        return self.web_scores


    def get_beatmap_data(self, refresh=False):
        if (self.beatmap_file == None) or refresh:
            self.beatmap_file = OsuOnline.fetch_beatmap_file(self.id, strio=True)
        return self.beatmap_file


    def download_beatmap(self, filepath):
        beatmap_data = OsuOnline.fetch_beatmap_file(self.id)
        pathname     = filepath + '/' + self.name + '.osu'
        BeatmapIO.save_beatmap(beatmap_data, pathname)



class WebScore(JsonObj):

    def __init__(self, name, data):
        JsonObj.__init__(self, data)
        self.name = name + ' ~ ' + self.user['username']
        if len(self.mods) > 0:  
            self.name += ' +' + ''.join(self.mods)
        
        self.replay_data = None
        

    def download_replay_api(self, filepath):
        replay_data = self.get_replay_data_api()
        pathname    = filepath + '/' + self.name + '.osr'
        ReplayIO.save_replay(replay_data, pathname)


    def get_replay_data_web(self):
        if self.replay_data == None:
            self.replay_data = OsuOnline.fetch_replay_file(self.beatmap['mode'], self.id)
        return self.replay_data


    def download_replay_web(self, filepath):
        replay_data = self.get_replay_data_web()
        print('Downloaded ' + str(self.name))
        pathname    = filepath + '/' + self.name + '.osr'
        ReplayIO.save_replay(replay_data, pathname)