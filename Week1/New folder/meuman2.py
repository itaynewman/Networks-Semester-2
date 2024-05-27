import requests
from collections import Counter


def find_most_common_words(url, num_words):
    # Fetch the content of the text file from the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Count the occurrences of each word
        words = response.text.split()
        word_counts = Counter(words)

        # Sort the words based on their frequencies
        sorted_words = sorted(word_counts.items(), key=get_second_item, reverse=True)

        # Extract the top N most common words
        top_words = [word for word, _ in sorted_words[:num_words]]

        # Concatenate the top words into a sentence
        sentence = ' '.join(top_words)
        return sentence
    else:
        return "Failed to fetch content from the URL"


def get_second_item(item):
    return item[1]


# Example usage:
url_of_site = "http://webisfun.cyber.org.il/nahman/files/words.txt"
num_words_ = 6
sentence1 = find_most_common_words(url_of_site, num_words_)
print(sentence1)
