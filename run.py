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
    #['jennifer', 'mike'],
    #['regina', 'jason'],
    ['terry', 'yunhee'],
    ['dennis', 'sean', 'emily'],
    ['gloria', 'david'],
    ['jin', 'sang', 'carolina'],
    ['gene', 'tina'],
    ['alex', 'christina'],
    'sandy'
    ]


def _valid_match(a, b):
    """
    Return false if a and b are in the same participant group,
    or if a matches itself.
    Return true otherwise.
    """
    r = True
    if a == b:
        r = False
    else:
        for i in PARTICIPANTS:
            if isinstance(i, list) and a in i and b in i:
                r = False
                break
    return r
                    
                
def _get_users():
    """
    Return a list of users by flattening out PARTICIPANTS.
    """
    r = []
    for i in PARTICIPANTS:
        if isinstance(i, list):
            for j in i:
                r.append(j)
        else:
            r.append(i)
    return r


def main():
    matches = {}
    users = _get_users()

    # The available pool of users to pick from.
    # Once a user has been picked, remove them from here.
    available_users = list(users)

    # Iterate through users and find a valid match.
    for i in users:
        while True:
            j = random.randint(0, len(available_users) - 1)
            match = available_users[j]
            if _valid_match(i, match):
                matches[i] = match
                del available_users[j]
                break

    print json.dumps(matches, sort_keys=True, indent=4)


if __name__ == '__main__':
    main()
