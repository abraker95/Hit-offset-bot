# Hit-offset-bot

This bot offers a way to examine the difficulty of an osu! beatmap. Difficulty of certain patterns can be correlated with the 
variance of timed hits by players. Higher difficulty means the hits would be more all over the place while lower difficulty
means the hits would be more precise. By calculting hit offsets half of the players hit within it is possible to guage this 
correlation for every hitobject in the map.

The bot start by downloading the beatmap and top 50 replays made by players, then loads the data. It calculates hit offsets
made by each player and stacks the data for every hitobject; 50 hitoffsets for each hitobject, 1 for every replay. Finally, for
each hitobject it solves for the offset needed to have 50% of the players satisfy the condition of hitting within the offset.

The most expensive operation is collecting the replays. The bot is set to collect a replay every 3 seconds, which means it takes 
roughly 2.5 minutes to collect all replays. This is required due to rate limits for downloading replays, and doing it any faster
may result the server replying with a "too many request" error.

### Usage:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`.get [beatmap id] | [beatmap link]`

### Example usage:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`.get 123456`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`.get https://osu.ppy.sh/b/123456`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`.get https://osu.ppy.sh/beatmapsets/541289#osu/123456`


### Sample response:
![](https://i.imgur.com/adwVByh.png)
