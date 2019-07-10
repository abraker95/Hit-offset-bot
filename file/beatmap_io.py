from collections import OrderedDict

from misc.math_utils import find
from file.beatmap import Beatmap

from std.std_hitobject import Hitobject
from std.std import Std

from std.hitobject.std_singlenote_io import StdSingleNoteIO
from std.hitobject.std_holdnote_io import StdHoldNoteIO
from std.hitobject.std_spinner_io import StdSpinnerIO


'''
Handles beatmap loading

Input: 
    load_beatmap - load the beatmap specified

Output: 
    metadata - information about the beatmap
    hitobjects - list of hitobjects present in the map
    timingpoints - list of timing points present in the map
'''
class BeatmapIO():

    class Section():

        SECTION_NONE         = 0
        SECTION_GENERAL      = 1
        SECTION_EDITOR       = 2
        SECTION_METADATA     = 3
        SECTION_DIFFICULTY   = 4
        SECTION_EVENTS       = 5
        SECTION_TIMINGPOINTS = 6
        SECTION_COLOURS      = 7
        SECTION_HITOBJECTS   = 8


    @staticmethod
    def init():
        BeatmapIO.SECTION_MAP = {
            BeatmapIO.Section.SECTION_GENERAL      : BeatmapIO.__parse_general_section,
            BeatmapIO.Section.SECTION_EDITOR       : BeatmapIO.__parse_editor_section,
            BeatmapIO.Section.SECTION_METADATA     : BeatmapIO.__parse_metadata_section,
            BeatmapIO.Section.SECTION_DIFFICULTY   : BeatmapIO.__parse_difficulty_section,
            BeatmapIO.Section.SECTION_EVENTS       : BeatmapIO.__parse_events_section,
            BeatmapIO.Section.SECTION_TIMINGPOINTS : BeatmapIO.__parse_timingpoints_section,
            BeatmapIO.Section.SECTION_COLOURS      : BeatmapIO.__parse_colour_section,
            BeatmapIO.Section.SECTION_HITOBJECTS   : BeatmapIO.__parse_hitobjects_section
        }


    """
    Opens a beatmap file and reads it

    Args:
        filepath: (string) filepath to the beatmap file to load
    """
    @staticmethod
    def open_beatmap(filepath=None):
        with open(filepath, 'rt', encoding='utf-8') as beatmap_file:
            beatmap = BeatmapIO.load_beatmap(beatmap_file)
        
        return beatmap


    """
    Loads beatmap data

    Args:
        beatmap_file: (string) contents of the beatmap file
    """
    @staticmethod
    def load_beatmap(beatmap_data):
        beatmap = Beatmap()
        
        BeatmapIO.__parse_beatmap_data(beatmap_data, beatmap)
        BeatmapIO.__process_timing_points(beatmap)

        if beatmap.gamemode == Beatmap.GAMEMODE_OSU:
            BeatmapIO.__process_slider_timings(beatmap)
            BeatmapIO.__process_hitobject_end_times(beatmap)
            BeatmapIO.__process_slider_tick_times(beatmap)

        else:
            raise Exception('Unsupported gamemode: ' + str(beatmap.gamemode))

        BeatmapIO.__validate(beatmap)

        return beatmap


    """
    Saves beatmap file data

    Args:
        filepath: (string) what to save the beatmap as
    """
    @staticmethod
    def save_beatmap(beatmap_data, filepath):
        with open(filepath, 'wt', encoding='utf-8') as f:
            f.write(beatmap_data)


    """
    Returns:
        MD5 checksum of the beatmap file
    """
    @staticmethod
    def get_md5(beatmap):
        pass


    @staticmethod
    def __process_hitobject_end_times(beatmap):
        beatmap.end_times = {}
        for i in range(len(beatmap.hitobjects)):
            if not beatmap.hitobjects[i].is_hitobject_type(Hitobject.CIRCLE):
                beatmap.end_times[beatmap.hitobjects[i].end_time] = i
            else:
                beatmap.end_times[beatmap.hitobjects[i].time] = i

        beatmap.end_times = OrderedDict(sorted(beatmap.end_times.items(), key=lambda x: x[0]))


    # Validates beatmap data
    @staticmethod
    def __validate(beatmap):
        pass


    @staticmethod
    def __parse_beatmap_data(beatmap_data, beatmap):
        BeatmapIO.__parse_beatmap_file_format(beatmap_data, beatmap)
        BeatmapIO.__parse_beatmap_content(beatmap_data, beatmap)

        beatmap.metadata.name = beatmap.metadata.artist + ' - ' + beatmap.metadata.title + ' (' + beatmap.metadata.creator + ') ' + '[' + beatmap.metadata.version + ']'


    @staticmethod
    def __parse_beatmap_file_format(beatmap_data, beatmap):
        line  = beatmap_data.readline()
        data  = line.split('osu file format v')
        
        try: beatmap.metadata.beatmap_format = int(data[1])
        except: return


    @staticmethod
    def __parse_beatmap_content(beatmap_data, beatmap):
        if beatmap.metadata.beatmap_format == -1: return

        section = BeatmapIO.Section.SECTION_NONE
        line    = ''
        
        while True:
            line = beatmap_data.readline()

            if line.strip() == '[General]':        section = BeatmapIO.Section.SECTION_GENERAL
            elif line.strip() == '[Editor]':       section = BeatmapIO.Section.SECTION_EDITOR
            elif line.strip() == '[Metadata]':     section = BeatmapIO.Section.SECTION_METADATA
            elif line.strip() == '[Difficulty]':   section = BeatmapIO.Section.SECTION_DIFFICULTY
            elif line.strip() == '[Events]':       section = BeatmapIO.Section.SECTION_EVENTS
            elif line.strip() == '[TimingPoints]': section = BeatmapIO.Section.SECTION_TIMINGPOINTS
            elif line.strip() == '[Colours]':      section = BeatmapIO.Section.SECTION_COLOURS
            elif line.strip() == '[HitObjects]':   section = BeatmapIO.Section.SECTION_HITOBJECTS
            elif line == '':               
                return
            else:
                BeatmapIO.__parse_section(section, line, beatmap)


    @staticmethod
    def __parse_section(section, line, beatmap):
        if section != BeatmapIO.Section.SECTION_NONE:
            BeatmapIO.SECTION_MAP[section](line, beatmap)


    @staticmethod
    def __parse_general_section(line, beatmap):
        data = line.split(':', 1)
        if len(data) < 2: return
        data[0] = data[0].strip()

        if data[0] == 'PreviewTime':
            # ignore
            return

        if data[0] == 'Countdown':
            # ignore
            return

        if data[0] == 'SampleSet':
            # ignore
            return

        if data[0] == 'StackLeniency':
            # ignore
            return

        if data[0] == 'Mode':
            beatmap.gamemode = int(data[1])
            return

        if data[0] == 'LetterboxInBreaks':
            # ignore
            return

        if data[0] == 'SpecialStyle':
            # ignore
            return

        if data[0] == 'WidescreenStoryboard':
            # ignore
            return


    @staticmethod
    def __parse_editor_section(line, beatmap):
        data = line.split(':', 1)
        if len(data) < 2: return

        if data[0] == 'DistanceSpacing':
            # ignore
            return

        if data[0] == 'BeatDivisor':
            # ignore
            return

        if data[0] == 'GridSize':
            # ignore
            return

        if data[0] == 'TimelineZoom':
            # ignore
            return


    @staticmethod
    def __parse_metadata_section(line, beatmap):
        data = line.split(':', 1)
        if len(data) < 2: return
        data[0] = data[0].strip()

        if data[0] == 'Title':
            beatmap.metadata.title = data[1].strip()
            return

        if data[0] == 'TitleUnicode':
            # ignore
            return

        if data[0] == 'Artist':
            beatmap.metadata.artist = data[1].strip()
            return

        if data[0] == 'ArtistUnicode':
            # ignore
            return

        if data[0] == 'Creator':
            beatmap.metadata.creator = data[1].strip()
            return

        if data[0] == 'Version':
            beatmap.metadata.version = data[1].strip()
            return

        if data[0] == 'Source':
            # ignore
            return

        if data[0] == 'Tags':
            # ignore
            return

        if data[0] == 'BeatmapID':
            beatmap.metadata.beatmap_id = data[1].strip()
            return

        if data[0] == 'BeatmapSetID':
            beatmap.metadata.beatmapset_id = data[1].strip()
            return


    @staticmethod
    def __parse_difficulty_section(line, beatmap):
        data = line.split(':', 1)
        if len(data) < 2: return
        data[0] = data[0].strip()

        if data[0] == 'HPDrainRate':
            beatmap.difficulty.hp = float(data[1])
            return

        if data[0] == 'CircleSize':
            beatmap.difficulty.cs = float(data[1])
            return

        if data[0] == 'OverallDifficulty':
            beatmap.difficulty.od = float(data[1])
            return

        if data[0] == 'ApproachRate':
            beatmap.difficulty.ar = float(data[1])
            return

        if data[0] == 'SliderMultiplier':
            beatmap.difficulty.sm = float(data[1])
            return

        if data[0] == 'SliderTickRate':
            beatmap.difficulty.st = float(data[1])
            return


    @staticmethod
    def __parse_events_section(line, beatmap):
        # ignore
        return


    @staticmethod
    def __parse_timingpoints_section(line, beatmap):
        data = line.split(',')
        if len(data) < 2: return

        timing_point = Beatmap.TimingPoint()
        
        timing_point.offset        = float(data[0])
        timing_point.beat_interval = float(data[1])

        # Old maps don't have meteres
        if len(data) > 2: timing_point.meter = int(data[2])
        else:             timing_point.meter = 4

        if len(data) > 6: timing_point.inherited = False if int(data[6]) == 1 else True
        else:             timing_point.inherited = False

        beatmap.timing_points.append(timing_point)


    @staticmethod
    def __parse_colour_section(self, line):
        # ignore
        return


    @staticmethod
    def __parse_hitobjects_section(line, beatmap):
        data = line.split(',')
        if len(data) < 2: return
        
        hitobject_type = int(data[3])

        if beatmap.gamemode == Beatmap.GAMEMODE_OSU:
            if Std.is_hitobject_type(hitobject_type, Hitobject.CIRCLE):
                beatmap.hitobjects.append(StdSingleNoteIO.load_singlenote(data, beatmap.difficulty))
                return

            if Std.is_hitobject_type(hitobject_type, Hitobject.SLIDER):
                beatmap.hitobjects.append(StdHoldNoteIO.load_holdnote(data, beatmap.difficulty))
                return

            if Std.is_hitobject_type(hitobject_type, Hitobject.SPINNER):
                beatmap.hitobjects.append(StdSpinnerIO.load_spinner(data, beatmap.difficulty))
                return


        else:
            raise Exception('Unsupported Gamemode: ' + str(beatmap.gamemode))


    @staticmethod
    def __process_timing_points(beatmap):
        beatmap.bpm_min = float('inf')
        beatmap.bpm_max = float('-inf')

        bpm = 0
        slider_multiplier = -100
        old_beat = -100
        base = 0

        for timing_point in beatmap.timing_points:
            if timing_point.inherited:
                    timing_point.beat_length = base

                    if timing_point.beat_interval < 0:
                        slider_multiplier = timing_point.beat_interval
                        old_beat = timing_point.beat_interval
                    else:
                        slider_multiplier = old_beat
            else:
                slider_multiplier = -100
                bpm = 60000 / timing_point.beat_interval
                timing_point.beat_length = timing_point.beat_interval
                base = timing_point.beat_interval

                beatmap.bpm_min = min(beatmap.bpm_min, bpm)
                beatmap.bpm_max = max(beatmap.bpm_max, bpm)

            timing_point.bpm = bpm
            timing_point.slider_multiplier = slider_multiplier

    
    @staticmethod
    def __process_slider_timings(beatmap):
        for hitobject in beatmap.hitobjects:
            if not hitobject.is_hitobject_type(Hitobject.SLIDER):
                continue

            try: idx_timing_point = find(beatmap.timing_points, hitobject.time, lambda timing_point: timing_point.offset)
            except:
                print(beatmap.timing_points)
                raise

            timing_point = beatmap.timing_points[idx_timing_point]

            hitobject.to_repeat_time = round(((-600.0/timing_point.bpm) * hitobject.pixel_length * timing_point.slider_multiplier) / (100.0 * beatmap.difficulty.sm))
            hitobject.end_time = hitobject.time + hitobject.to_repeat_time*hitobject.repeat


    @staticmethod
    def __process_slider_tick_times(beatmap):
        beatmap.slider_tick_times = []
        for hitobject in beatmap.hitobjects:
            if not hitobject.is_hitobject_type(Hitobject.SLIDER):
                continue

            ms_per_beat = (100.0 * beatmap.difficulty.sm)/(hitobject.get_velocity() * beatmap.difficulty.st)
            hitobject.tick_times = []

            for beat_time in range(hitobject.time, hitobject.end_time, int(ms_per_beat)):
                hitobject.tick_times.append(beat_time)
            

BeatmapIO.init()