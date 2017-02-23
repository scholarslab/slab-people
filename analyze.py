#!/usr/bin/env python3


"""\
Analyze the data in the descriptions of the people and dump it out in a
way that's easy to visualize with d3.
"""

# TODO tokenize
# TODO basic statistics
# TODO frequencies
# TODO frequencies by tag
# TODO basic statistics by tag


import json
import sys

from bs4 import BeautifulSoup


INPUT = 'people.json'


def de_html(person):
    """This takes a person from the JSON file and removes HTML from the
    description (i.e., the content field).
    """
    content = person['content']
    soup = BeautifulSoup(content, 'html.parser')
    person['content'] = soup.get_text()


def main():
    with open(INPUT) as fin:
        people = json.load(fin)

    for person in people:
        de_html(person)

    json.dump(people, sys.stdout)


if __name__ == '__main__':
    main()
