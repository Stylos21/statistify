import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from Spotipy import SpotipyObject
import json
import DiscordUtils
# import spotipy

load_dotenv()
sp = SpotipyObject(os.getenv('ID'), os.getenv('SECRET'))

# initiating bot
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(activity=discord.Game(name=" !help"))

'''
class TrackButton(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(
        label = "More Info",
        style = discord.ButtonStyle.blurple,

    )
    async def moreInfo(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass
'''

# creating bot object
bot = Bot()

# commands
@bot.command(help="Get information about a song")
async def song (ctx, *, songName):
    song_info = sp.get_data_of_song(songName)

    name = song_info['tracks']['items'][0]['name']
    cover_url = song_info['tracks']['items'][0]['album']['images'][0]['url']
    song_url = song_info['tracks']['items'][0]['external_urls']['spotify']
    duration = song_info['tracks']['items'][0]['duration_ms']

    artists = []
    for artist in song_info['tracks']['items'][0]['artists']:
        artists.append(artist['name'])
    artists = ", ".join(artists)


    minutes = duration//60000
    seconds = (duration-minutes*60000)//1000

    embed1 = discord.Embed(
        title=name,
        url = song_url
    )
    embed1.set_image(url=cover_url)
    embed1.add_field(name="Length", value=f"{minutes}:{seconds}")
    embed1.add_field(name="Artist(s)", value=artists)

    audio_features = sp.get_audio_features_of_song(songName)[0]
    danceability = audio_features["danceability"]*100//1
    energy = audio_features["energy"]*100//1
    tempo = audio_features["tempo"]//1
    print(audio_features)

    embed2 = discord.Embed(
        title=name,
        url=song_url,
    )
    embed2.add_field(name="Danceability", value=danceability)
    embed2.add_field(name="Energy", value=energy)
    embed2.add_field(name="Tempo", value=tempo)

    await ctx.send(song_url)
    msg = await ctx.send(embed=embed1)
    view = ButtonView(msg, embed1, embed2)
    await msg.edit(embed=embed1, view=view) 
    
    


@bot.command(help="Get info about a user :D (requires their userID)")
async def userinfo (ctx, id):

    info = sp.get_user_info(id) 
    embed = discord.Embed(title=info['username'], url=info['link'], description="Everything about " + info['username'])
    try:
        embed.set_image(url=info['profpic'])
    except:
        pass
    #embed.addfield(name="Country", value=info['country'], inline = true)
    embed.add_field(name="Followers", value=info['followers'], inline = False)
    #embed.addfield(name="Email", value=info['email'], inline = false)

    await ctx.send(embed=embed)

@bot.command(help="Get data about an artist")
async def artistdata (ctx, artist):

    info1 = sp.get_artist_info1(artist)
    info2 = sp.get_artist_info2(artist)
    # print("info: " + info1)
    embed1 = discord.Embed(title=info1['names'], url=info1['url'], description="Everything about " + info1['names'])
    embed1.set_image(url=info1['image'])
    embed1.add_field(name="Followers", value=info1['followers'], inline = True)
    embed1.add_field(name="Popularity", value=info1['popularity'], inline = True)
    embed1.add_field(name="Genres", value=", ".join(info1['genres']), inline = False)
    
    files = discord.File("../Images/" + info2["image"] + ".png", filename=info2['image'] + ".png")
    print(files.filename)
    embed2 = discord.Embed(title="Top Tracks", description="Information about their Top Tracks")
    embed2.set_image(url="attachment://" +  files.filename)
    #embed2.add_field(name="Top Tracks", value=info2['popular_songs'], inline = False)
    embed2.add_field(name="Top Tracks and Their Popularity", value=('\n'.join(info2['popularity_of_songs'])), inline=False)
    
    fileEmbed = discord.Embed(title="Popular Tracks")

    #paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
    pages = [embed1, embed2]
    
    msg = await ctx.send(embed=embed1)
    view = ButtonView(msg, embed1, embed2)
    await msg.edit(embed=embed1, view=view)
    await ctx.send(file=files)
    #i think the issue is here that the paginator isnt sending the file and only the page
    #but the documentation for discordutils is down or smthing cause it isnt loading in for me
class ButtonView(discord.ui.View):
    def __init__(self, message, embed1, embed2):
        super().__init__()
        self.message = message
        self.embed1 = embed1
        self.embed2 = embed2
    
    @discord.ui.button(
        label="Overview",
        style=discord.ButtonStyle.gray,
        disabled=True)
    async def overview(self, button: discord.ui.Button, interaction: discord.Interaction):
        buttons = self.children[1]
        buttons.disabled = False
        buttons.style = discord.ButtonStyle.blurple
        button.disabled = True
        button.style = discord.ButtonStyle.gray

        await self.message.edit(embed=self.embed1, view=self) 
        # no u need it because if the user switches back to the first page the file will still be there
        # you dont need a file since the image is opnline i thinkoh ok wait no like so that line gets rid of the file?
    
    @discord.ui.button(
        label="More Data",
        style=discord.ButtonStyle.blurple,
        disabled=False)
    async def data(self, button: discord.ui.Button, interaction: discord.Interaction):
        buttons = self.children[0]
        buttons.disabled = False
        buttons.style = discord.ButtonStyle.blurple#????????????? who knew this was a color
        button.disabled = True
        button.style = discord.ButtonStyle.gray
        

        #files = discord.File("../Images/" + info2["image"] + ".png", filename=info2['image'] + ".png")
        #embed2 = discord.Embed(title="Top Tracks", description="Information about their Top Tracks")
        #embed2.set_image(url="attachment://" +  files.filename)
        #embed2.add_field(name="Top Tracks", value=info2['popular_songs'], inline = False)
        #embed2.add_field(name="Top Tracks and Their Popularity", value=('\n'.join(info2['popularity_of_songs'])), inline=False)
    
        await self.message.edit(embed=self.embed2, view=self)
#does the user call this as a cothismmand? like how does the user call this


bot.run(os.getenv('TOKEN'))
