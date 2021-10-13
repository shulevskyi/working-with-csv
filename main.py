import argparse
import csv
import sys
import os

# Global variables
whole_result, data_of_players, added_data, all_medals, result = [], [], [], [], []
result_everything = None
count_medals, bronze_medals, silver_medals, gold_medals, zx = 0, 0, 0, 0, 0

# Declaring arguments
parser = argparse.ArgumentParser()
parser.add_argument('file')
group = parser.add_mutually_exclusive_group()  # There is a group thanks to user has 2 different option to choose
group.add_argument('--total', nargs=1)
group.add_argument('--medals', nargs=2)
group.add_argument('--overall', nargs=1)
parser.add_argument('--output', nargs=1)
args = parser.parse_args()

if args.output is not None:
    args.output = ''.join(args.output)
    os.remove(args.output)  # Deleting the output file before the start

    class Logger(object):  # Algo that takes the output from the shell and then prints it on the chosen file for output
        def __init__(self):
            self.terminal = sys.stdout
            self.log = open(args.output, "a")

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)

        def flush(self):
            pass

    sys.stdout = Logger()

with open(str(args.file)) as csvfile:
    reader = csv.reader(csvfile)
    for rows in reader:
        result.append(rows)  # Appending data from csv to list

del result[0]  # Deleting the first unessential row

# The brain of the game
for row in result:
    year = int(row[9])  # Converting to int
    if args.total is not None:
        if int(args.total[0]) == year:
            data_of_players.append(row[6]), data_of_players.append(row[-1])
    if args.medals is not None:
        if (int(args.medals[1]) == year and (args.medals[0] in row[6] or args.medals[0] in row[7])) and 'NA' not in row[-1]:
            all_medals.append(row[-1])  # For further counting

            # Getting info from rows: name, activity type, medals
            data_of_players.append(row[1]), data_of_players.append(row[12]), data_of_players.append(row[-1])
            result_everything = True
    if args.overall is not None:
        for i in range(0, len(''.join(args.overall).split(', '))):
            if ''.join(args.overall).split(', ')[i] == row[6] or ''.join(args.overall).split(', ')[i] == row[7]:
                for i in range(1896, 2020, 4):  # The Olympic games pass every 4 years, so the step here is 4
                    if i == year:
                        all_medals.append([str(year), row[-1], row[6]])

if args.total is not None:
    a, b = 0, 2
    while b < len(data_of_players):
        added_data.append(data_of_players[a:b])
        a += 2; b += 2

    i = [i.clear() for i in added_data if 'NA' in i[1]]
    final_list = [x for x in added_data if x != []]  # If there are any empties
    for i in range(0, len(final_list)):
        print(' - '.join(final_list[i]))

if args.medals is not None:
    if not result_everything:
        print('There is wrong year or name of country'), exit()

    for i in range(0, len(all_medals)):
        if 'NA' != all_medals[i]:  # Calculating if there is any medals except NA
            count_medals += 1
            if 'Bronze' == all_medals[i]:
                bronze_medals += 1
            if 'Silver' == all_medals[i]:
                silver_medals += 1
            if 'Gold' == all_medals[i]:
                gold_medals += 1

    a, b = 0, 3
    while True:
        added_data.append(data_of_players[a:b])  # Starting from the new line
        a += 3; b += 3
        if len(added_data) == 10:
            break
    final_list = [x for x in added_data if x != []]  # Deleting empty lists if this is necessary
    for i in range(0, len(final_list)):
        print(' - '.join(final_list[i]))
    if count_medals < 10:
        print('\nCountry has less than 10 medals')
    if count_medals >= 10:
        print(f'\nBronze medals: {bronze_medals}\nSilver medals: {silver_medals}\nGold medals: {gold_medals}\n')
        print(f'Total number of medals: {count_medals}')

if args.overall is not None:
    for i in all_medals:
        if 'NA' in i[1]:
            i.clear()  # Deleting every non-medal line
        else:
            del i[1]  # Delete the medals themselves
            data_of_players.append(i)
    whole_result = [[data_of_players.count(i), i[-1], i[0]] for i in data_of_players]  # How many occurrences there

    # The loop for printing the highest score
    while zx < len(''.join(args.overall).split(', ')):
        print(f'MAX score of {max(whole_result)[1]} in {max(whole_result)[-1]}: {max(whole_result)[0]} medals')
        inx = max(whole_result)[1]
        i = [i.clear() for i in whole_result if inx in i]
        zx += 1