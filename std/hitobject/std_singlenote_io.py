from misc.pos import Pos
from std.hitobject.std_singlenote_hitobject import StdSingleNoteHitobject


class StdSingleNoteIO():

    @staticmethod
    def load_singlenote(data, difficulty):
        singlenote = StdSingleNoteHitobject()
        if not data: return singlenote

        StdSingleNoteIO.__process_hitobject_data(data, singlenote, difficulty)

        return singlenote


    @staticmethod
    def __process_hitobject_data(data, singlenote, difficulty):
        singlenote.pos            = Pos(int(data[0]), int(data[1]))
        singlenote.time           = int(data[2])
        singlenote.hitobject_type = int(data[3])

        singlenote.difficulty     = difficulty