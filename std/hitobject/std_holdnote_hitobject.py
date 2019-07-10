from misc.pos import Pos
from misc.math_utils import triangle, lerp, value_to_percent

from std.std_hitobject import Hitobject



"""
Visualizes the osu!std slider

Input: 
    beatmap_data - osu!std slider data read from the beatmap file; determines the type of slider, pos, etc
    time - The time value of the playfield; determine's slider's opacity, follow point position, etc

Output: 
    Visual display of an osu!std slider
"""
class StdHoldNoteHitobject(Hitobject):

    LINEAR1       = 'L'
    LINEAR2       = 'C'
    BEZIER        = 'B'
    CIRCUMSCRIBED = 'P'

    def __init__(self):
        self.end_time     = None    # Initialized by beatmapIO.__process_slider_timings after timing data is read
        self.pixel_length = None
        self.repeat       = None
        self.curve_type   = None

        self.to_repeat_time   = None

        self.curve_points = []  # Points that define slider in editor
        self.gen_points   = []  # The rough generated slider curve
        self.tick_times   = []  # Slider ticks/score points/aimpoints

        Hitobject.__init__(self)
        

    def time_to_percent(self, time):
        return value_to_percent(self.time, self.end_time, time)


    def time_to_pos(self, time):
        return self.percent_to_pos(self.time_to_percent(time))


    def percent_to_idx(self, percent):
        if percent <= 0.0: return 0
        if percent >= 1.0: return -1 if self.repeat == 0 else 0

        idx = percent*len(self.gen_points)
        idx_pos = triangle(idx*self.repeat, (2 * len(self.gen_points)) - 1)
        
        return int(idx_pos)


    def idx_to_pos(self, idx):
        if idx > len(self.gen_points) - 2:
            return Pos(self.gen_points[-1].x, self.gen_points[-1].y)

        percent_point = float(int(idx)) - idx
        x_pos = lerp(self.gen_points[idx].x, self.gen_points[idx + 1].x, percent_point)
        y_pos = lerp(self.gen_points[idx].y, self.gen_points[idx + 1].y, percent_point)

        return Pos(x_pos, y_pos)


    def percent_to_pos(self, percent):
        return self.idx_to_pos(self.percent_to_idx(percent))


    def get_end_time(self):
        return self.end_time


    def get_generated_curve_points(self):
        return self.gen_points


    def get_last_aimpoint_time(self):
        return self.tick_times[-1]


    def get_aimpoint_times(self):
        return self.tick_times


    def get_velocity(self):
        return self.pixel_length / (self.end_time - self.time)