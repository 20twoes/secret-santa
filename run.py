#! /usr/bin/python

"""

Secret Santa Simulator (SSS)

Define a list of participants.  SSS will match participants randomly.

A particpant can be a list of participants (group).  In this case, nobody will match within their group.

"""

import json
import random


PARTICIPANTS = [
    ['al', 'julie', 'ruby'],
    ['kay', 'jenn'],
    ['philip', 'chorong'],
    ['jennifer', 'mike'],
    ['regina', 'jason'],
    ['terry', 'yunhee'],
    ['dennis', 'sean', 'emily'],
    ['gloria', 'david'],
    ['jin', 'sang', 'carolina']
    ]


def valid_match(a, b):
    r = True
    if a == b:
        r = False
    else:
        for i in PARTICIPANTS:
            if isinstance(i, list) and a in i and b in i:
                r = False
    return r
                    
                
def main():
    matches = {}

    # Create a flat list of users
    users = []
    for i in PARTICIPANTS:
        if isinstance(i, list):
            for j in i:
                users.append(j)
        else:
            users.append(i)

    # The available pool of users to pick from.
    # Once a user has been picked, remove them from here.
    available = list(users)

    # Iterate through users and find a valid match
    for i in users:
        if len(available) == 1:
            if valid_match(i, match):
                matches[i] = match
                available.pop()
        else:
            while True:
                random.shuffle(available)
                match = available[-1]
                if valid_match(i, match):
                    matches[i] = match
                    available.pop()
                    break

    print json.dumps(matches, sort_keys=True, indent=4)


if __name__ == '__main__':
    main()
