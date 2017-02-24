#!/usr/bin/env python3


"""\
Analyze the data in the descriptions of the people and dump it out in a
way that's easy to visualize with d3.
"""

# TODO basic statistics
# TODO frequencies by tag
# TODO basic statistics by tag


from collections import Counter
import json
import sys

from bs4 import BeautifulSoup
from nltk.tokenize.casual import TweetTokenizer


INPUT = 'people.json'
STOP_FILE = 'english.stopwords'


def over_contents(person, func):
    """Run func over the person's contents/description."""
    person['text'] = func(person['text'])


def over_tokens(person, func):
    """Run func over each token in the person's contents/description."""
    person['text'] = [func(token) for token in person['text']]


def de_html(text):
    """This removes HTML. """
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()


tokenizer = TweetTokenizer(reduce_len=True)
def tokenize(text):
    """Break a text into tokens."""
    return tokenizer.tokenize(text)


def normalize(token):
    """Normalize a token."""
    return token.lower()


def filter_tokens(text, stopwords):
    """Remove tokens we won't use."""
    return [
        token
        for token in text
        if token not in stopwords and len(token) > 1
        ]


def frequencies(tokens):
    """Generate counts from a list of tokens."""
    return Counter(tokens)


def corpus_frequencies(corpus):
    """With a sequence of Counter objects, get a sum."""
    counts = Counter()
    for freq in corpus:
        counts.update(freq.elements())
    return counts


def find_singletons(freqs):
    """Return a set of singleton tokens."""
    return {k for k, v in freqs.items() if v == 1}


def remove_set(text_freqs, stoplist):
    """Removes items in stoplist from text_freqs dictionary."""
    return {k: v for k, v in text_freqs.items() if k not in stoplist}


def pull_data(person):
    """This pulls the relevant data from the person structure."""
    terms = person['terms']
    if terms:
        tags = [cat['name'] for cat in terms['people-category']]
    else:
        tags = None

    return {
        'text': person['content'],
        'description': person['content'],
        'date': person['date'],
        'url': person['link'],
        'tags': tags,
        'name': person['title'],
        }


def main():
    """Process and produce the data file."""
    with open(INPUT) as fin:
        people = json.load(fin)

    with open(STOP_FILE) as fin:
        stopwords = set(normalize(token) for token in tokenize(fin.read()))

    people = [pull_data(person) for person in people]
    for person in people:
        over_contents(person, de_html)
        over_contents(person, tokenize)
        over_tokens(person, normalize)
        over_contents(person, lambda t: filter_tokens(t, stopwords))
        over_contents(person, frequencies)

    counts = corpus_frequencies(person['text'] for person in people)
    singletons = find_singletons(counts)
    for person in people:
        over_contents(person, lambda t: remove_set(t, singletons))

    json.dump(people, sys.stdout)


if __name__ == '__main__':
    main()
