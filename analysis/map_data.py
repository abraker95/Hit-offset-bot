import numpy as np

from std.std_hitobject import Hitobject



class StdMapData():

    TIME = 0
    POS  = 1

    '''
    [
        [ 
            [ time, pos ],
            [ time, pos ],
            ... N score points
        ],
        [ 
            [ time, pos ],
            [ time, pos ],
            ...  N score points
        ],
        ... N hitobjects
    ]
    '''
    @staticmethod 
    def std_hitobject_to_aimpoints(std_hitobject):
        if std_hitobject.is_hitobject_type(Hitobject.CIRCLE):
            yield [ std_hitobject.time, (std_hitobject.pos.x, std_hitobject.pos.y) ]
        
        elif std_hitobject.is_hitobject_type(Hitobject.SLIDER):
            for aimpoint_time in std_hitobject.get_aimpoint_times():
                yield [ aimpoint_time, np.asarray([ std_hitobject.time_to_pos(aimpoint_time).x, std_hitobject.time_to_pos(aimpoint_time).y ]) ]

    
    @staticmethod
    def std_hitobjects_to_aimpoints(std_hitobjects):
        for hitobject in std_hitobjects:
            aimpoints = list(StdMapData.std_hitobject_to_aimpoints(hitobject))
            if len(aimpoints) > 0: yield aimpoints


    @staticmethod
    def get_aimpoint_data(std_hitobjects):
        return np.asarray(list(StdMapData.std_hitobjects_to_aimpoints(std_hitobjects)))


    @staticmethod
    def get_data_before(hitobject_data, time):
        idx_time = StdMapData.get_idx_start_time(hitobject_data, time)

        if not idx_time: return None
        if idx_time < 1: return None

        return hitobject_data[idx_time - 1][-1]


    @staticmethod
    def get_data_after(hitobject_data, time):
        idx_time = StdMapData.get_idx_end_time(hitobject_data, time)
        
        if not idx_time:                       return None
        if idx_time > len(hitobject_data) - 2: return None
            
        return hitobject_data[idx_time + 1][0]


    @staticmethod
    def time_slice(hitobject_data, start_time, end_time):
        start_idx = StdMapData.get_idx_start_time(hitobject_data, start_time)
        end_idx   = StdMapData.get_idx_end_time(hitobject_data, end_time)

        return hitobject_data[start_idx:end_idx]


    @staticmethod
    def start_times(hitobject_data):
        return np.asarray([ note[0][StdMapData.TIME] for note in hitobject_data ])


    @staticmethod
    def end_times(hitobject_data):
        return np.asarray([ note[-1][StdMapData.TIME] for note in hitobject_data ])


    @staticmethod
    def start_positions(hitobject_data):
        return np.asarray([ note[0][StdMapData.POS] for note in hitobject_data ])

    
    @staticmethod
    def end_positions(hitobject_data):
        return np.asarray([ note[-1][StdMapData.POS] for note in hitobject_data ])


    @staticmethod
    def all_positions(hitobject_data, flat=True):
        if flat: return np.asarray([ data[StdMapData.POS] for note in hitobject_data for data in note ])
        else:    return np.asarray([[data[StdMapData.POS] for data in note] for note in hitobject_data])


    @staticmethod
    def all_times(hitobject_data, flat=True):
        if flat: return np.asarray([ data[StdMapData.TIME] for note in hitobject_data for data in note ])
        else:    return np.asarray([[data[StdMapData.TIME] for data in note] for note in hitobject_data])

    
    @staticmethod
    def start_end_times(hitobject_data):
        all_times = StdMapData.all_times(hitobject_data, flat=False)
        return np.asarray([ (hitobject_times[0], hitobject_times[-1]) for hitobject_times in all_times ])


    @staticmethod
    def get_idx_start_time(hitobject_data, time):
        if not time: return None

        times = np.asarray(StdMapData.start_times(hitobject_data))
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))

    
    @staticmethod
    def get_idx_end_time(hitobject_data, time):
        if not time: return None
            
        times = np.asarray(StdMapData.end_times(hitobject_data))
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))


    @staticmethod
    def get_idx_start_time_2(hitobject_data, time):
        if not time: return None

        times = np.asarray(StdMapData.start_times(hitobject_data))
        return np.where(times >= time)[0][0]


    @staticmethod
    def get_idx_end_time_2(hitobject_data, time):
        if not time: return None
            
        times = np.asarray(StdMapData.end_times(hitobject_data))
        return np.where(times >= time)[0][0]