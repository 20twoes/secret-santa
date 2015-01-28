import argparse
import csv
import random


def get_random_number():
    iterations = random.randint(0, 100)

    out = 0
    for i in xrange(iterations):
        out += random.randint(0, 100)
    return out


def main():
    print 'Running secret santa...'
    parser = argparse.ArgumentParser()
    parser.add_argument('participants', type=argparse.FileType('rU'))
    parser.add_argument('exclusions', type=argparse.FileType('rU'))
    parser.add_argument('history', type=argparse.FileType('rU'))
    args = parser.parse_args()

    data = {}
    PARTICIPANT_NAME = 0

    with args.participants as csv_file:
        reader = csv.reader(csv_file)
        header_row = True
        for row in reader:
            if header_row:
                header_row = False
                continue
            if row[-1]:
                data[row[-1]] = {'history': [], 'exclusions': []}

    with args.exclusions as csv_file:
        reader = csv.reader(csv_file)
        header_row = True
        for row in reader:
            if header_row:
                header_row = False
                continue
            person = row[PARTICIPANT_NAME]
            if person in data:
                data[person]['exclusions'] = row[PARTICIPANT_NAME + 1:]
                data[person]['exclusions'] = [i for i in data[person]['exclusions'] if i]

    with args.history as csv_file:
        reader = csv.reader(csv_file)
        header_row = True
        for row in reader:
            if header_row:
                header_row = False
                continue
            person = row[PARTICIPANT_NAME]
            if person in data:
                data[person]['history'] = row[PARTICIPANT_NAME + 1:]
                data[person]['history'] = [i for i in data[person]['history'] if i]

    participants_pool = data.keys()

    for key, value in data.iteritems():
        data[key]['all_exclusions'] = data[key]['history'] + data[key]['exclusions'] + [key]

    for key, value in data.iteritems():
        eligible_pool = list(set(participants_pool).difference(set(data[key]['all_exclusions'])))
        data[key]['match'] = eligible_pool[get_random_number() % len(eligible_pool)]
        participants_pool.remove(data[key]['match'])

    for key, value in data.iteritems():
        print '%s: %s' % (key, value['match'])


if __name__ == '__main__':
    main()