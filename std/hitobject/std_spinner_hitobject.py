from std.std_hitobject import Hitobject



"""
Visualizes the osu!std spinner

Input: 
    beatmap_data - osu!std slider data read from the beatmap file; determines pos, etc
    time - The time value of the playfield; determine's hitcircle's opacity, follow point position, etc

Output: 
    Visual display of an osu!std hitcircle
"""
class StdSpinnerHitobject(Hitobject):

    def __init__(self, beatmap=None):
        self.beatmap  = beatmap
        self.end_time = None

        Hitobject.__init__(self)

    
    def get_end_time(self):
        return self.end_time