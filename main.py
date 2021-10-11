import argparse
import csv

# Global variables
added_data = []
all_medals = []
data_of_players = []
count_medals = 0
i = 0
result_everything = None

# Declaring arguments
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)
group = parser.add_mutually_exclusive_group()  # There is a group thanks to user has 2 different option to choose
group.add_argument('--total', nargs=1)
group.add_argument('--medals', nargs=2)
parser.add_argument('output_file', type=str)
args = parser.parse_args()


with open('data.csv') as csvfile:
    csv_reader = csv.reader(csvfile)

    for row in csv_reader:
        try:
            year = int(row[9])  # converting str year to int
        except ValueError:
            continue
        if args.total is not None:
            if int(args.total[0]) == year:
                all_medals.append(row[-1])

                data_of_players.append(row[6])
                data_of_players.append(row[-1])
        if args.medals is not None:
            if int(args.medals[1]) == year and args.medals[0] in row[6]:
                all_medals.append(row[-1])

                # Getting info from rows: name, activity type, medals
                data_of_players.append(row[1])
                data_of_players.append(row[12])
                data_of_players.append(row[-1])
                result_everything = True

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