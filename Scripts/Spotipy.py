import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import os
import uuid
import matplotlib
from matplotlib import pyplot as plt
from dotenv import load_dotenv
import seaborn as sns

matplotlib.use("Agg")
plt.style.use('ggplot')
load_dotenv('../.env')

class SpotipyObject:
    spotifyObj = None

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.spotifyObj = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                                                client_secret=client_secret))

    def get_data_of_song(self, query: str) -> object:
        result = self.spotifyObj.search(q=query, type="track", limit=1)
        return result

    # def get_recent_tracks() (commented out for testing)



        
    def get_user_info(self, query: str):
        result = self.spotifyObj.user(query)

        keys = ["username", "email", "followers", "profpic",
                "country", "link"]

        information = dict.fromkeys(keys)

        information["username"] = result['display_name']
        #information["email"] = (results['email'])
        information["followers"] = result['followers']['total']
        if result['images'] == []:
            information["profpic"] = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.spotify.com%2Fus%2F&psig=AOvVaw09cMZawB3lBKeTO6pfZ4s0&ust=1633915968598000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCMjKuLvZvvMCFQAAAAAdAAAAABAD"
        else:
            information["profpic"] = result['images'][0]['url']
        #information["country"] = (results['country'])
        information["link"] = result['external_urls']['spotify']

        return information
# '''
    def get_albums(self, uri: str):
        uri = str
        results = self.spotifyObj.artist_albums(uri, album_type='album')
        albums = results['items']
        albums.extend(results)

        return albums
# '''
    def search_artist(self, query: str):
        result = self.spotifyObj.search(q=query, type="artist", limit=1)
        return result

    def return_followers_of_artist (self, query: str):
        result = self.search_artist(query)['followers']['total']
        return result

    def return_popularity_of_artist (self, query: str):
        result = self.search_artist(query)['popularity']
        return result

    def return_genres_of_artist (self, query: str):
        result = self.search_artist(query)['genres']
        return result

    def format_artist_name(self, query:str):
        result = self.search_artist(query)['artists']['items'][0]['name']
        return result

    def return_id_of_artist(self, query: str):
        result = self.search_artist(query)['artists']["items"][0]["id"]
        return result


    
    def return_id_of_song(self, query:str):
        song = self.search_songs(query)
        return song['tracks']['items'][0]['id']
    
    def return_url_of_artist(self, query: str):
        result = self.search_artist(query)['artists']["items"][0]["id"]
        return result

    def search_songs(self, query: str):
        result = self.spotifyObj.search(
            q="track: " + query, type="track", limit=1)
        return result

    # def get_technical_details_of_song(self, query:)

    def search_songs_from_artist(self, query: str):
        id_of_artist = self.return_id_of_artist(query)
        result = self.spotifyObj.artist_top_tracks(artist_id=id_of_artist)
        return result

    def get_popularity_of_top_songs(self, query: str):
        pops = {}
        songs = self.search_songs_from_artist(query)['tracks']
        name = songs[0]['artists'][0]['name']
        for something in songs:
            pops[something['name'].replace(' ', '\n')] = something['popularity']
        return pops

    def sort_dict(self, dictionary):
        dictionary = dictionary.items()
        dictionary = sorted(dictionary, key=lambda elem: elem[1])
        return dictionary

    def graph_popular_songs(self, query: str):
        # countries on x-axis
        pop_nums = self.get_popularity_of_top_songs(query)
        name = self.format_artist_name(query)
        # fig = plt.figure()
        # ax = fig.add_axes([0,0,1,1])
        pop_nums = self.sort_dict(pop_nums)
        plt.rcParams.update({'font.size': 6, 'axes.labelweight': "ultralight", "font.family": "Avenir Next"})
        colors = sns.color_palette('Set2')
        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.set_facecolor('white')
        plt.title("Popular Songs by " + name)
        x = [p[0] for p in pop_nums]
        y = [p[1] for p in pop_nums]
        x_pos = [i for i, _ in enumerate(x)]
        axes = plt.bar(x_pos, y, color=colors)
        plt.xlabel("Song Names")
        # plt.yticks([])
        rects = axes.patches
        for rect, label in zip(rects, y):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2, height, label, ha="center", va="bottom")
        plt.xticks(x_pos, x)
        id = str(uuid.uuid4())
        plt.savefig("../Images/" + id + ".png")
        # plt.despine()
        plt.close()

        return id

    def get_audio_features_of_song(self, query: str): 
        id = [self.return_id_of_song(query)]
        features = self.spotifyObj.audio_features(id)
        return features

        
    def get_artist_info1(self, query: str):
        result = self.spotifyObj.search(q=query, type="artist", limit=1)['artists']['items'][0]
        
        # keys1 = ["url", "name", "followers", "popularity", "genres", "image"]
        # print(result['artists']['items'][0]['external_urls'])
        # information = result['artists']['items'][0]['external_urls'].fromkeys(keys1)
        information = {}
        information["names"] = result['name']
        information["url"] = result['external_urls']['spotify']
        information["followers"] = result['followers']['total']
        information["popularity"] = result['popularity']
        information["genres"] = result['genres']
        information["image"] = result['images'][0]['url']

        return information

    def get_artist_info2(self, query: str):
        result = self.spotifyObj.search(q=query, type="artist", limit=1)
        
        keys2 = ["popular_songs", "popularity_of_songs", "image"]

        information = dict.fromkeys(keys2)


        pops = {}
        songs = self.search_songs_from_artist(query)['tracks']

        for something in songs:
            pops[something['name']] = something['popularity']

        information["popular_songs"] = self.search_songs_from_artist(query)
        information["popularity_of_songs"] = pops
        information["image"] = self.graph_popular_songs(query)

        return information
