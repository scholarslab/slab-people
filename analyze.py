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


def over_contents(person, func):
    """Run func over the person's contents/description."""
    person['content'] = func(person['content'])


def de_html(text):
    """This removes HTML. """
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()


tokenizer = TweetTokenizer(reduce_len=True)
def tokenize(text):
    """Break a text into tokens."""
    return tokenizer.tokenize(text)


def main():
    with open(INPUT) as fin:
        people = json.load(fin)

    for person in people:
        over_contents(person, de_html)
        over_contents(person, tokenize)

    json.dump(people, sys.stdout)


if __name__ == '__main__':
    main()
