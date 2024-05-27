import re
from collections import Counter


def parse_data(file_path):
    """
    this function parses the data file and returns the data organized
    :param file_path:
    :return data file parsed:
    """
    albums = []
    songs = {}

    with open(file_path, 'r') as file:
        current_album = None
        txt = file.readlines()
        for line in txt:
            line = line.strip()
            if line.startswith('#'):
                # Parse album line
                album_line = line[1:].strip()
                album_name = album_line.split("::")[0].strip()
                albums.append(album_name)
                current_album = album_name
                songs[current_album] = []
            elif line.startswith('*'):
                # Parse song line
                song_details = line[1:].split('::')
                if len(song_details) == 4:
                    song_name = song_details[0].strip()
                    artist_name = song_details[1].strip()
                    song_length = song_details[2].strip()
                    song_lyrics = song_details[3].strip()
                    songs[current_album].append({
                        'name': song_name,
                        'artist': artist_name,
                        'length': song_length,
                        'lyrics': song_lyrics
                    })

    return albums, songs


def get_albums(albums, songs):
    """
    this function returns a string of all the albums
    :param albums:
    :param songs:
    :return:
    """
    return ', '.join(albums)


def get_songs_in_album(albums, songs, album_name):
    """
    this function returns a string of all the songs in a given album
    :param albums:
    :param songs:
    :param album_name:
    """
    if album_name in songs:
        return ', '.join([song['name'] for song in songs[album_name]])
    else:
        return 'Album not found'


def get_song_length(albums, songs, song_name):
    """
    this function returns the length of a given song
    :param albums:
    :param songs:
    :param song_name:
    :return:
    """
    for album, song_list in songs.items():
        for song in song_list:
            if song['name'] == song_name:
                return song['length']
    return 'Song not found'


def get_song_lyrics(albums, songs, song_name):
    """
    this function returns the lyrics of a given song
    :param albums:
    :param songs:
    :param song_name:
    """
    for album, song_list in songs.items():
        for song in song_list:
            if song['name'] == song_name:
                return song['lyrics']
    return 'Song not found'


def get_album_for_song(albums, songs, song_name):
    """
    this function returns the album of a given song
    :param albums:
    :param songs:
    :param song_name:
    """
    for album, song_list in songs.items():
        for song in song_list:
            if song['name'] == song_name:
                return album
    return 'Song not found'


def search_song_by_name(albums, songs, search_text):
    """
    this function returns a string of all the songs that contain the search text
    :param albums:
    :param songs:
    :param search_text:
    :return:
    """
    results = []
    for album, song_list in songs.items():
        for song in song_list:
            if search_text.lower() in song['name'].lower():
                results.append(song['name'])
    return ', '.join(results) if results else 'No songs found'


def search_song_by_lyrics(albums, songs, search_text):
    """
    this function returns a string of all the songs that contain the search text in their lyrics
    :param albums:
    :param songs:
    :param search_text:
    """
    results = []
    for album, song_list in songs.items():
        for song in song_list:
            if search_text.lower() in song['lyrics'].lower():
                results.append(song['name'])
    return ', '.join(results) if results else 'No songs found'


def get_most_common_words(albums, songs, top_n=50):
    """
    this function returns the top N most common words in the lyrics of all the songs
    :param albums:
    :param songs:
    :param top_n:
    :return:
    """
    word_counter = Counter()
    for album, song_list in songs.items():
        for song in song_list:
            words = re.findall(r'\b\w+\b', song['lyrics'].lower())
            word_counter.update(words)
    common_words = word_counter.most_common(top_n)
    return '\n'.join([f"{word}: {count}" for word, count in common_words])


def get_albums_sorted_by_length(albums, songs):
    """
    this function returns a string of all the albums sorted by their total length
    :param albums:
    :param songs:
    :return:
    """
    album_lengths = {}
    for album, song_list in songs.items():
        total_length = 0
        for song in song_list:
            minutes, seconds = map(int, song['length'].split(':'))
            total_length += minutes * 60 + seconds
        album_lengths[album] = total_length

    sorted_albums = sorted(album_lengths.items(), key=lambda x: x[1], reverse=True)
    return '\n'.join([f"{album}: {length//60}:{length%60:02d}" for album, length in sorted_albums])
