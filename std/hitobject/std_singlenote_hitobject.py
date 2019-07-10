from std.std_hitobject import Hitobject



"""
Visualizes the osu!std hitcircle

Input: 
    beatmap_data - osu!std slider data read from the beatmap file; determines pos, etc
    time - The time value of the playfield; determine's hitcircle's opacity, follow point position, etc

Output: 
    Visual display of an osu!std hitcircle
"""
class StdSingleNoteHitobject(Hitobject):

    def __init__(self):
        Hitobject.__init__(self)


    def time_to_pos(self, time):
        return self.pos
        

    def get_aimpoint_times(self):
        return [ self.time ]