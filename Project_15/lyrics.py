import lyricsgenius
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file
genius = lyricsgenius.Genius(os.getenv("GENIUS_API_KEY"))

def save_lyrics(songs, artist_name, album_name):
    # Create a directory to save the lyrics
    directory = f"songs/{'_'.join(artist_name.split(' '))}"
    os.makedirs(directory, exist_ok=True)

    for i, song_title in enumerate(songs):
        try:
            # Search for the song
            song = genius.search_song(song_title, artist_name)
            if song:
                lyrics = song.lyrics
                # Save the lyrics to a file
                file_name = f"{directory}/{i+1}_{album_name}_{'-'.join(''.join(song_title.split('\'')).split(' '))}.txt"
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(lyrics)
                print(f"Lyrics saved for: {song_title}")
            else:
                print(f"Lyrics not found for: {song_title}")
        except Exception as e:
            print(f"Error fetching lyrics for {song_title}: {e}")

if __name__ == '__main__':
    # List of songs
    songs = [
        'the box',
        'down below',
        'project dreams',
        'die young',
        'boom boom room',
        'high fashion',
        'roll dice',
        'war baby',
        'every season'
    ]
    # Artist name and album name
    save_lyrics(songs, 'roddy ricch', 'Please_Excuse_Me_for_Being_Antisocial')