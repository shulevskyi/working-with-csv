import argparse
import csv

# Global variables
added_data = []
all_medals = []
data_of_players = []
count_medals = 0
i = 0
result_everything = None
result = []
whole_result = []

# Declaring arguments
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)
group = parser.add_mutually_exclusive_group()  # There is a group thanks to user has 2 different option to choose
group.add_argument('--total', nargs=1)
group.add_argument('--medals', nargs=2)
group.add_argument('--overall', nargs=1)
parser.add_argument('output_file', type=str)
args = parser.parse_args()

path = str(args.file)

with open(path) as csvfile:
    reader = csv.reader(csvfile)
    for rows in reader:
        result.append(rows)

del result[0]  # Deleting the first unessential row

for row in result:
    try:
        year = int(row[9])  # Converting to int
    except ValueError:
        continue
    if args.total is not None:
        if int(args.total[0]) == year:
            data_of_players.append(row[6])
            data_of_players.append(row[-1])
    if args.medals is not None:
        if int(args.medals[1]) == year and args.medals[0] in row[6]:
            all_medals.append(row[-1])  # For further counting

            # Getting info from rows: name, activity type, medals
            data_of_players.append(row[1])
            data_of_players.append(row[12])
            data_of_players.append(row[-1])
            result_everything = True
    if args.overall is not None:
        for i in range(0, len(''.join(args.overall).split(', '))):
            if ''.join(args.overall).split(', ')[i] == row[6]:
                for i in range(1896, 2020, 4):  # The Olympic games pass every 4 years, so the step here is 4
                    if i == year:
                        all_medals.append([str(year), row[-1], row[6]])

if args.total is not None:
    a = 0
    b = 2
    while b < len(data_of_players):
        added_data.append(data_of_players[a:b])
        a += 2
        b += 2

    for i in added_data:
        if 'NA' in i[1]:
            i.clear()
    final_list = [x for x in added_data if x != []]
    file = open(args.output_file, 'w')
    for i in range(0, len(final_list)):
        file = open(args.output_file, 'w')
        file.write(' - '.join(final_list[i]))
        print(' - '.join(final_list[i]))

if args.medals is not None:
    file = open(args.output_file, 'w')  # Creating a file, where output will be printed
    if not result_everything:
        print('There is wrong year or name of country')
        file.write('There is wrong year or name of country')
        exit()

    else:
        for i in range(0, len(all_medals)):
            if 'NA' != all_medals[i]:  # Calculating if there is any medals except NA
                count_medals += 1

        a = 0
        b = 3
        while True:
            added_data.append(data_of_players[a:b])  # Starting from the new line
            a += 3
            b += 3
            if len(added_data) == 10:
                break
        final_list = [x for x in added_data if x != []]  # Deleting empty lists if this is necessary
        for i in range(0, len(final_list)):
            print(' - '.join(final_list[i]))
            file.write(' - '.join(final_list[i]) + "\n")

        if count_medals < 10:
            print('\nCountry has less than 10 medals')
            file.write('\nCountry has less than 10 medals')
        if count_medals >= 10:
            print(f'\nTotal number of medals: {count_medals}')
            file.write(f'\nTotal number of medals: {count_medals}')
        file.close()
if args.overall is not None:
    for i in all_medals:
        if 'NA' in i[1]:
            i.clear()  # Deleting every non-medal line
        else:
            del i[1]  # Delete the medals themselves
            data_of_players.append(i)
    for i in data_of_players:
        whole_result.append([data_of_players.count(i), i[-1], i[0]])  # Finding out how many occurrences there

    file = open(args.output_file, 'w')  # Creating a file, where output will be printed

    # The loop for printing the highest score
    zx = 0
    while zx < len(''.join(args.overall).split(', ')):
        print(f'MAX score of {max(whole_result)[1]} in {max(whole_result)[-1]}: {max(whole_result)[0]} medals')
        file.write(f'MAX score of {max(whole_result)[1]} in {max(whole_result)[-1]}: {max(whole_result)[0]} medals\n')
        inx = max(whole_result)[1]
        for i in whole_result:
            if inx in i:
                i.clear()
        zx += 1
    file.close()
