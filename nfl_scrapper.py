# import libraries

import requests
from bs4 import BeautifulSoup
import csv
import os

def get_qb_stats(all_players):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    
    for i in range(1970, 2024):
        url = 'https://www.nfl.com/stats/player-stats/category/passing/{}/post/all/passingyards/desc'.format(i)
        page = requests.get(url, headers=headers)
        Soup = BeautifulSoup(page.content, "html.parser")

        players = Soup.find_all(class_="d3-o-player-fullname nfl-o-cta--link")
        passing_yards = Soup.find_all(class_="selected")

        index = 0
        for player in players:
            if player.text.strip() not in all_players:
                all_players[player.text.strip()] = {}

            all_players[player.text.strip()][i] = {}
            all_players[player.text.strip()][i]['year'] = len(all_players[player.text.strip()]) 
            all_players[player.text.strip()][i]['passing_yards'] = int(passing_yards[index].text.strip())

            index += 1

    return all_players

def read_csv(file_name):
    all_players = {}
    with open(file_name, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] not in all_players:
                    all_players[row[0]] = {}
                all_players[row[0]][row[1]] = {}
                all_players[row[0]][row[1]]['year'] = int(row[2])
                all_players[row[0]][row[1]]['passing_yards'] = int(row[3])
    return all_players

def write_csv(file_name, all_players):
    with open(file_name, mode='w', newline='') as file:
            csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for player in all_players:
                for year in all_players[player]:
                    csv_writer.writerow([player, year, all_players[player][year]['year'], all_players[player][year]['passing_yards']])
    print('File created!')

def get_stats_by_year(all_players, target_year):
    player_stats = []
    for player in all_players:
        if target_year in all_players[player]:
            player_stats.append((player, all_players[player][target_year]['passing_yards']))
    print("Stats for {}:".format(target_year))
    sorted(player_stats, key=lambda x: x[1])
    for i in range(len(player_stats)):
        print("{}. {} - {} passing yards".format(i+1, player_stats[i][0], player_stats[i][1]))
    input('Press enter to continue...')

def get_stats_by_player(all_players, player):
    player_stats = []
    for year in all_players[player]:
        player_stats.append((year, all_players[player][year]['passing_yards']))
    print("Stats for {}:".format(player))
    sorted(player_stats, key=lambda x: x[0])
    for i in range(len(player_stats)):
        print("{}. {} - {} passing yards".format(i+1, player_stats[i][0], player_stats[i][1]))
    input('Press enter to continue...')
    average_yards = get_average_yards(player_stats)
    print("Average passing yards for {} is {} yearly".format(player, average_yards))
    input('Press enter to continue...')

def get_max_yards(all_players):
    max_yards = 0
    max_player = ''
    year_played = 0
    for player in all_players:
        for year in all_players[player]:
            if all_players[player][year]['passing_yards'] > max_yards:
                max_yards = all_players[player][year]['passing_yards']
                max_player = player
                year_played = year
    print("{} has the most passing yards with {} yards in {}".format(max_player, max_yards, year_played))
    input('Press enter to continue...')

def get_min_yards(all_players):
    min_yards = 10000000
    min_player = ''
    year_played = 0
    for player in all_players:
        for year in all_players[player]:
            if all_players[player][year]['passing_yards'] < min_yards:
                min_yards = all_players[player][year]['passing_yards']
                min_player = player
                year_played = year
    print("{} has the lowest passing yards with {} yards in {}".format(min_player, min_yards, year_played))
    input('Press enter to continue...')

def get_average_yards(player_stats):
    total_yards = 0
    for year in player_stats:
        total_yards += year[1]
    return total_yards / len(player_stats)


                                                                      
def main():
    file_name = 'qb_stats.csv'

    if os.path.exists(file_name):
        all_players = read_csv(file_name)
    else:
        all_players = get_qb_stats({})
        write_csv(file_name, all_players)

    while True:
        print("1. Get stats by year")
        print("2. Get stats by player")
        print("3. Get max yards")
        print("4. Get min yards")
        print("5. Exit")
        option = int(input("Enter option: "))
        if option == 1:
            year = input("Enter year: ")
            get_stats_by_year(all_players, year)
        elif option == 2:
            player = input("Enter player: ")
            get_stats_by_player(all_players, player)
        elif option == 3:
            get_max_yards(all_players)
        elif option == 4:
            get_min_yards(all_players)
        elif option == 5:
            break
        else:
            print("Invalid option")



main()
            
    