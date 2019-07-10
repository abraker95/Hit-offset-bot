import numpy as np



class StdReplayData():

    TIME  = 0   # [ int ]   Time of event
    XPOS  = 1   # [ float ] Cursor's x-position
    YPOS  = 2   # [ float ] Cursor's y-position
    M1    = 3   # [ bool ]  Mouse 1 button flag
    M2    = 4   # [ bool ]  Mouse 2 button flag
    K1    = 5   # [ bool ]  Keyboard 1 button flag
    K2    = 6   # [ bool ]  Keyboard 2 button flag
    SMOKE = 7   # [ bool ]  Smoke button flag

    @staticmethod 
    def get_event_data(replay_events):
        
        """
        Returns:
        [
            [ time, x_pos, y_pos, m1, m2, k1, k2, smoke ],
            [ time, x_pos, y_pos, m1, m2, k1, k2, smoke ],
            [ time, x_pos, y_pos, m1, m2, k1, k2, smoke ],
            ...  N events
        ]

        A list of events with data on time, positions of cursor, and flags on various key presses
        """
        event_data = []

        m1_mask    = (1 << 0)
        m2_mask    = (1 << 1)
        k1_mask    = (1 << 2)
        k2_mask    = (1 << 3)
        smoke_mask = (1 << 4)

        for replay_event in replay_events:
            # "and not" because K1 is always used with M1; K2 is always used with M2. So make sure keys are not pressed along with mouse
            k1_pressed    = ((replay_event.keys_pressed & k1_mask) > 0)
            k2_pressed    = ((replay_event.keys_pressed & k2_mask) > 0) 
            m1_pressed    = ((replay_event.keys_pressed & m1_mask) > 0) and not k1_pressed
            m2_pressed    = ((replay_event.keys_pressed & m2_mask) > 0) and not k2_pressed
            smoke_pressed = (replay_event.keys_pressed & smoke_mask) > 0

            event = [ replay_event.t, replay_event.x, replay_event.y, m1_pressed, m2_pressed, k1_pressed, k2_pressed, smoke_pressed ]
            event_data.append(event)

        return event_data


    @staticmethod
    def component_data(event_data, data):
        event_data = np.asarray(event_data)
        return event_data[:, data]


    @staticmethod
    def press_start_times(event_data, key=None):
        """
        Returns: [ press_start_idxs, press_start_times ] = [ [ int, int, ... ], [ int, int, ... ] ]
        
        Tuple with indices in event_data where a press ends and timings where press ends.
        press_start_idxs can be used on original event_data to get full data related to start times
        like so: event_data[press_start_idxs]
        """
        event_data = np.asarray(event_data)
        
        if key == None:
            m1_idxs, m1_press_start_times = StdReplayData.press_start_times(event_data, StdReplayData.M1)
            m2_idxs, m2_press_start_times = StdReplayData.press_start_times(event_data, StdReplayData.M2)
            k1_idxs, k1_press_start_times = StdReplayData.press_start_times(event_data, StdReplayData.K1)
            k2_idxs, k2_press_start_times = StdReplayData.press_start_times(event_data, StdReplayData.K2)

            press_start_times = np.concatenate((m1_press_start_times, m2_press_start_times, k1_press_start_times, k2_press_start_times))
            press_idxs        = np.concatenate((m1_idxs, m2_idxs, k1_idxs, k2_idxs))

            sort_idxs = np.argsort(press_start_times, axis=None)
            return np.asarray([ press_idxs[sort_idxs], press_start_times[sort_idxs] ])
        else:
            times    = StdReplayData.component_data(event_data, StdReplayData.TIME)
            key_data = StdReplayData.component_data(event_data, key)

            key_changed = (key_data[1:] != key_data[:-1])
            key_changed = np.insert(key_changed, 0, 0)
            is_hold     = (key_data == 1)

            press_start_mask  = np.logical_and(key_changed, is_hold)
            press_start_times = times[press_start_mask]

            return np.asarray([ np.where(press_start_mask == 1)[0], press_start_times ])


    @staticmethod
    def press_end_times(event_data, key=None):
        """
        Returns: [ press_end_idxs, press_end_times ] = [ [ int, int, ... ], [ int, int, ... ] ]
        
        Tuple with indices in event_data where a press ends and timings where press ends.
        press_end_idxs can be used on original event_data to get full data related to end times
        like so: event_data[press_end_idxs]
        """
        event_data = np.asarray(event_data)

        if key == None:
            m1_idxs, m1_press_end_times = StdReplayData.press_end_times(event_data, StdReplayData.M1)
            m2_idxs, m2_press_end_times = StdReplayData.press_end_times(event_data, StdReplayData.M2)
            k1_idxs, k1_press_end_times = StdReplayData.press_end_times(event_data, StdReplayData.K1)
            k2_idxs, k2_press_end_times = StdReplayData.press_end_times(event_data, StdReplayData.K2)

            press_end_times = np.concatenate((m1_press_end_times, m2_press_end_times, k1_press_end_times, k2_press_end_times))
            press_idxs      = np.concatenate((m1_idxs, m2_idxs, k1_idxs, k2_idxs))

            sort_idxs = np.argsort(press_end_times, axis=None)
            return np.asarray([ press_idxs[sort_idxs], press_end_times[sort_idxs] ])
        else:
            times    = StdReplayData.component_data(event_data, StdReplayData.TIME)
            key_data = StdReplayData.component_data(event_data, key)

            key_changed = (key_data[1:] != key_data[:-1])
            key_changed = np.insert(key_changed, 0, 0)
            is_not_hold = (key_data == 0)

            press_end_mask  = np.logical_and(key_changed, is_not_hold)
            press_end_times = times[press_end_mask]
            
            return np.asarray([ np.where(press_end_mask == 1)[0], press_end_times ])

    
    @staticmethod
    def press_start_end_times(event_data, key=None):
        """
        Returns: 
        [ 
            [ press_start_idx, press_start_time, press_end_idx, press_end_time ],
            [ press_start_idx, press_start_time, press_end_idx, press_end_time ],
            ...
        ]
        """
        press_start_idx, press_start_times = StdReplayData.press_start_times(event_data, key)
        press_end_idx, press_end_times     = StdReplayData.press_end_times(event_data, key)

        return np.asarray(list(zip(press_start_idx, press_start_times, press_end_idx, press_end_times)))


    @staticmethod
    def get_idx_time(event_data, time):
        event_times = event_data[:,StdReplayData.TIME]

        idx = np.where(event_times >= time)[0]
        idx = (event_times.size - 1) if idx.size == 0 else min(idx[0] + 1, event_times.size - 1)

        return idx

    
    @staticmethod
    def get_idx_press_start_time(event_data, time, key=None):
        if not time: return None

        times = StdReplayData.press_start_times(event_data, key)
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))


    @staticmethod
    def get_idx_press_end_time(event_data, time, key=None):
        if not time: return None

        times = StdReplayData.press_end_times(event_data, key)
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))