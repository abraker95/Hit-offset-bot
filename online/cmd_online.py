from online.osu_online import OsuOnline
from online.web_structs import WebScore


class CmdOnline():

    @staticmethod
    def get_scores(beatmap_id, mode, name):
        return [ WebScore(name, score) for score in OsuOnline.fetch_scores(beatmap_id, mode) ]


    @staticmethod
    def get_scores_from_beatmap(beatmap):
        return CmdOnline.get_scores(beatmap.metadata.beatmap_id, beatmap.gamemode, beatmap.metadata.name)