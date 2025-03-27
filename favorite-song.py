from bs4 import BeautifulSoup
import requests
import random as r

def top_n_songs(fav_song,tracks,n):
    song_list = [song for song in tracks]
    favorite_songs = []
    for song in range(n):
        nth_fav = fav_song(song_list)
        song_list.remove(nth_fav)
        favorite_songs.append(nth_fav)
        print(f"#{song+1} song: {nth_fav}") # Print out song choices as they are made
    
    for index,val in enumerate(favorite_songs):
        print(f"{index+1} : {val}") # Print out song ranking
    
    return favorite_songs


def favorite_song(tracks):
    available = [song for song in tracks]

    for i in range(len(available)-1):
        choices = r.sample(available,2)

        selection = input(f"{choices[0]} vs {choices[1]} (A vs B): ").upper()

        if selection == "A":
            available.remove(choices[1])
        elif selection == "B":
            available.remove(choices[0])
        else:
            raise ValueError(f"Invalid Input ({selection}): Enter either A or B. ")
        
    return available[0]


def get_tracklist(url):
    """Gets an Album Tracklist from MusicBrainz. Can only get the first 100 tracks in long albums"""
    
    data = requests.get(url)
    web_data = BeautifulSoup(data.content,"html.parser")

    # Filters the data to obtain track titles
    first_pass = web_data.find_all(class_="title wrap-anywhere")
    second_pass = [result.find_all("a")[0] for result in first_pass]
    track_list = [result.find_all("bdi")[0].text for result in second_pass]

    return track_list


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--mode",required=True, help="Run mode for the program. 'Single' if you only have 1 album to rank, 'Multiple' if you have a file of album links to rank")
    parser.add_argument("-i","--input_url",nargs="?",default=None,help="MusicBrainz URL for album if using mode 'Single'")
    parser.add_argument("-I","--input-file", nargs="?", default=None, help="path to list of albums if using mode 'Multiple'")
    parser.add_argument("-o","--output-file", type=str, nargs="?", default="playlist.txt", help="path to output file, if not provided creates a file called 'playlist.txt in the cwd")
    parser.add_argument("-n","--song-count", type=int, nargs="?", default=1, help="The top n songs you want from each album, default is 1")


    args = parser.parse_args()


    mode = args.mode
    url = args.input_url
    
    if args.input_file:
        input_file = pathlib.Path(args.input_file)

    output_file = pathlib.Path(args.output_file)

    number_of_songs = args.song_count
    
    if mode not in ["single","multiple"]:
        print(f"Entered mode {mode} not valid, proceeding with Single")
        mode = "single"


    if mode == "single":
        track_list = get_tracklist(url)

    else:
        tracklists = []

        try:
            with open(input_file,"r") as album_links:
                albums = album_links.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"Album URL file {input_file} does not exist. If only using one album URL use mode 'Single' instead")
            
        # Build a list of tracks for each album supplied through the file
        for album_url in albums:
            tracklists.append(get_tracklist(album_url.rstrip("\n")))

    
    if mode == "single":
        top_n_songs(favorite_song,track_list,n = number_of_songs)

    else:
        # Build a playlist from the top songs for each supplied album
        with open(output_file,"a+") as file:
            for track_list in tracklists:
                favorite_songs = top_n_songs(favorite_song,tracks = track_list,n = number_of_songs)
                for song in favorite_songs:
                    file.write(f"{song}\n")

if __name__ == "__main__":
    import argparse
    import pathlib

    main()