import argparse
import csv
import random


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

    participants_pool.remove('gene')
    for key, value in data.iteritems():
        if key == 'dennis':
            data['dennis']['match'] = 'gene'
        else:
            eligible_pool = list(set(participants_pool).difference(set(data[key]['all_exclusions'])))
            random.shuffle(eligible_pool)
            data[key]['match'] = eligible_pool[0]
            participants_pool.remove(data[key]['match'])
        print '%s: %s' % (key, value['match'])


if __name__ == '__main__':
    main()
