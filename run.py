from file.beatmap_io import BeatmapIO
from file.replay_io import ReplayIO

from online.osu_online import OsuOnline
from online.cmd_online import CmdOnline

from analysis.map_data import StdMapData
from analysis.replay_data import StdReplayData
from analysis.score_data import StdScoreData
from analysis.score_metrics import StdScoreMetrics

import discord
import time
import matplotlib.pyplot as plt


client = discord.Client()


class HitOffsetBot():

    last_run = None

    @staticmethod
    def get_hit_offsets(beatmap_id):
        beatmap  = BeatmapIO.load_beatmap(OsuOnline.fetch_beatmap_file(beatmap_id, strio=True))
        map_data = StdMapData.get_aimpoint_data(beatmap.hitobjects)
        scores   = CmdOnline.get_scores(beatmap_id, 0, beatmap.metadata.name)

        replay_data_array = []
        for score in scores:
            replay_file = score.get_replay_data_web()
            replay_data_array.append(StdReplayData.get_event_data(ReplayIO.load_replay(replay_file).play_data))

        score_data_array = [ StdScoreData.get_score_data(replay_data, map_data) for replay_data in replay_data_array ]
        per_hitobject_data = StdScoreMetrics.get_per_hitobject_score_data(score_data_array)

        return StdScoreMetrics.trans_solve_for_hit_offset(per_hitobject_data)


    @staticmethod
    @client.event
    async def on_message(msg):
        # we do not want the bot to reply to itself
        if msg.author == client.user:
            return

        if msg.content.startswith('.die'):
            await msg.channel.send('hell yea')
            exit(0)

        if msg.content.startswith('.help'):
            await msg.channel.send('Grabs map data and top 50 replays to calculate hit offsets for which half of players do better/worse than')
            await msg.channel.send('usage:')
            await msg.channel.send('.get 123456')
            await msg.channel.send('.get https://old.ppy.sh/b/123456')
            await msg.channel.send('.get https://osu.ppy.sh/beatmapsets/541289#osu/123456')

        if msg.content.startswith('.get'):
            if HitOffsetBot.last_run != None and time.time() - HitOffsetBot.last_run < 150:
                await msg.channel.send('Please wait at least 2.5 minutes since last request')
                return

            map_id = msg.content.split(' ')[-1]

            # Try just map id
            try: map_id = int(map_id)
            except:
                # Try  website beatmap link
                try: map_id = int(map_id.split('/')[-1])
                except: 
                    await msg.channel.send('invalid beatmap id or beatmap link')
                    return
            
            HitOffsetBot.last_run = time.time()
            await msg.channel.send('Please wait while I am fetching replays (~2.5 min)')
            await msg.channel.send('I will be unresponsive and might go offline but should be back when done.')
            
            try: times, hit_offsets = HitOffsetBot.get_hit_offsets(map_id)
            except Exception as e:
                await msg.channel.send('That map broke me! Blame abraker >:(')
                await msg.channel.send(str(e))
                return

            plt.clf()
            plt.plot(times, hit_offsets, lw=0.1, antialiased=True)
            plt.xlabel('time (ms)')
            plt.ylabel('average offset (ms)')
            plt.title('Top 50 players average per-hitobject offsets')
            plt.savefig('fig.png', dpi=500)

            await msg.channel.send('', file=discord.File('fig.png', filename='fig.png'))


    @staticmethod
    @client.event
    async def on_ready():
        print('Bot ready')


TOKEN = ''
client.run(TOKEN)