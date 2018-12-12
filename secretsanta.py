import argparse
import json
import random


class Gifter(object):
    def __init__(self, name):
        self.name = name
        self.exclusions = set()
        self.history = []

    def add_exclusions(self, exclusions):
        """
        exclusions : set
        """
        self.exclusions.update(exclusions)

    def add_history(self, history):
        """
        history : list
            A list of past matches in chronological order.
        """
        self.history = self.history + history


def main():
    print 'Running secret santa...'
    parser = argparse.ArgumentParser()
    parser.add_argument('participants', type=argparse.FileType('rU'))
    parser.add_argument('exclusions', type=argparse.FileType('rU'))
    parser.add_argument('history', type=argparse.FileType('rU'))
    args = parser.parse_args()

    gifters = {}

    # Parse Participants
    with args.participants as f:
        years = json.load(f)
        # Use the last data.  Could make this configurable in the future.
        year = years[-1]
        print('Year {}'.format(year['year']))

        for participant in year['participants']:
            print('participant: {}'.format(participant))
            gifters[participant] = Gifter(name=participant)

    # Parse Exclusions
    with args.exclusions as f:
        exclusion_data = json.load(f)
        for exclusions in exclusion_data:
            for person in exclusions:
                for name, gifter in gifters.iteritems():
                    if name == person:
                        gifter.add_exclusions(exclusions)

    # Parse History
    with args.history as f:
        history_data = json.load(f)

        for name, gifter in gifters.iteritems():
            history = history_data.get(name)
            if history:
                previous_matches = [i['match'] for i in sorted(history, key=lambda i: i['year'])]
                gifter.add_history(previous_matches)

    print('\n')
    print('Generating matches...')
    print('\n')

    participants = set(gifters.keys())
    matched = set()
    min_history_to_keep = 3
    for name, gifter in sorted(gifters.iteritems()):
        history_to_include_index = 0
        while True:

            history = set(gifter.history[history_to_include_index:])
            pool = participants\
                .difference(matched)\
                .difference(history)\
                .difference(gifter.exclusions)
            pool = list(pool)
            random.shuffle(pool)

            try:
                match = pool[0]
            except IndexError:
                # Start excluding the oldest history until we get a match or hit our cap.
                # print('No matches found for {} with history: {}'.format(name, history))
                if len(history) > min_history_to_keep:
                    history_to_include_index += 1
                    continue
                else:
                    print('No matches found for {}'.format(name))
                    break
            else:
                assert match not in matched
                matched.add(match)
                print('{} -> {}'.format(name, match))
                break


if __name__ == '__main__':
    main()
