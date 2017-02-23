#!/usr/bin/env python3


"""\
Analyze the data in the descriptions of the people and dump it out in a
way that's easy to visualize with d3.
"""

# TODO basic statistics
# TODO frequencies
# TODO frequencies by tag
# TODO basic statistics by tag


import json
import sys

from bs4 import BeautifulSoup
from nltk.tokenize.casual import TweetTokenizer


INPUT = 'people.json'
STOP_FILE = 'english.stopwords'


def over_contents(person, func):
    """Run func over the person's contents/description."""
    person['content'] = func(person['content'])


def over_tokens(person, func):
    """Run func over each token in the person's contents/description."""
    person['content'] = [func(token) for token in person['content']]


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


def main():
    """Process and produce the data file."""
    with open(INPUT) as fin:
        people = json.load(fin)

    with open(STOP_FILE) as fin:
        stopwords = set(normalize(token) for token in tokenize(fin.read()))

    for person in people:
        over_contents(person, de_html)
        over_contents(person, tokenize)
        over_tokens(person, normalize)
        over_contents(person, lambda t: filter_tokens(t, stopwords))

    json.dump(people, sys.stdout)


if __name__ == '__main__':
    main()
