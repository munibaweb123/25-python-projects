# what do we need to do here?


import os
import re
import string
import random

from matplotlib import artist
from graph import Graph, Vertex

def get_words_from_text(text_path):
    with open(text_path, 'r') as file:
        text = file.read() 
        # remove [text in here]
        # remove [verse 1: artist]
        # include the following line if you are doing song lyrics
        text = re.sub(r'\[(.+)\]', ' ', text)

        text = ' '.join(text.split()) # this is saying turn whitespace into spaces
        text = text.lower() # make everything to lowercase to compare stuff
        text = text.translate(str.maketrans('', '', string.punctuation))
        # now we could be complex and deal with punctuation... but there are cases where
        # you might add a period such as (Mr. Brightside), but that's not really
        # punctuation... so we just remove all the punctuation
    words = text.split()

    words = words[:1000]

    return words


def make_graph(words):
    g = Graph()
    prev_word = None
    # for each word
    for word in words:
        # check that word is in graph, and if not then add it
        word_vertex = g.get_vertex(word)

        # if there was a previous word, then add an edge if does not exist
        # if exists, increment weight by 1
        if prev_word:  # prev word should be a Vertex
            # check if edge exists from previous word to current word
            prev_word.increment_edge(word_vertex)

        prev_word = word_vertex

    g.generate_probability_mappings()
    
    return g

def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words))
    for _ in range(length):
        composition.append(word.value)
        word = g.get_next_word(word)

    return composition


def main():
    # words = get_words_from_text('texts/hp_sorcerer_stone.txt')
    songs_dir = 'songs'
    
    # Check if the songs directory exists
    if not os.path.exists(songs_dir):
        print(f"Error: The directory '{songs_dir}' does not exist.")
        return
    
    # Get a list of all artist folders
    artists = [artist for artist in os.listdir(songs_dir) if os.path.isdir(os.path.join(songs_dir, artist))]
    
    if not artists:
        print(f"Error: No artist folders found in '{songs_dir}'.")
        return
    
    # Select an artist randomly
    artist = random.choice(artists)
    print(f"Selected artist: {artist}")
    
    artist_path = os.path.join(songs_dir, artist)
    words = []
    
    # Iterate through all files in the selected artist's directory
    for song in os.listdir(artist_path):
        # Skip non-song files like .DS_Store
        if not song.endswith('.txt'):
            continue
        song_path = os.path.join(artist_path, song)
        words.extend(get_words_from_text(song_path))
        
    g = make_graph(words)
    composition = compose(g, words, 100)
    print(' '.join(composition))  # Print the generated composition

if __name__ == '__main__':
    # step 1: get words from text
    # step 2: make a graph using those words
    # step 3: get the next word for x number of words (defined by user)
    # step 4: show the user!
    words = get_words_from_text('texts/hp_sorcerer_stone.txt')
    main()