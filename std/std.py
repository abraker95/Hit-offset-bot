

class Std():

    PLAYFIELD_WIDTH  = 512  # osu!px
    PLAYFIELD_HEIGHT = 384  # osu!px

    @staticmethod
    def cs_to_px(cs):
        return (109 - 9*cs)/2


    @staticmethod
    def px_to_cs(px):
        return 2*(109 - px)/9


    @staticmethod
    def ar_to_ms(ar):
        if ar <= 5: return 1800 - 120*ar
        else:       return 1950 - 150*ar


    @staticmethod
    def ms_to_ar(ms):
        if ms >= 1200.0: return (1800 - ms) / 120.0
        else:            return (1950 - ms) / 150.0


    @staticmethod
    def od300_to_ms(od):
        return 159 - 12.0*od


    @staticmethod
    def ms_to_od300(ms):
        return (159 - ms)/12.0


    @staticmethod
    def sv_to_vel(sv, bpm):
        return (bpm / 60.0) * sv * 100

    
    @staticmethod
    def approch_circle_to_radius(cs, ar, t):
        return 4*Std.cs_to_px(cs) - 3*Std.cs_to_px(cs) * (t/max(800, Std.ar_to_ms(ar)))


    @staticmethod
    def is_hitobject_type(hitobject_type, compare):
        return hitobject_type & compare > 0


    @staticmethod
    def get_fadein_period(ar_ms, hidden_mod=False):
        if hidden_mod:
            return 0.4 * ar_ms
        else:
            return min(ar_ms, 400)


    @staticmethod
    def get_acc_from_hits(num_300_hits, num_100_hits, num_50_hits, num_misses):
        score_hits  = 50*num_50_hits + 100*num_100_hits + 300*num_300_hits
        score_total = 300*(num_misses + num_50_hits + num_100_hits + num_300_hits)
        return score_hits/score_total


    @staticmethod
    def get_time_range(hitobjects):
        try:    return (hitobjects[0].time, hitobjects[-1].end_time)
        except: return (hitobjects[0].time, hitobjects[-1].time)

        # return (self.hitobjects[0].time, list(self.end_times.keys())[-1])


    @staticmethod
    def get_aimpoints_from_hitobjects(hitobjects):
        return [ (hitobject.get_aimpoints()[0], hitobject.time_to_pos(hitobject.get_aimpoints()[0])) for hitobject in hitobjects ]