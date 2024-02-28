# import libraries

import requests
from bs4 import BeautifulSoup
import csv
import os
from tabulate import tabulate
from qb import QuarterBack
from qb import YearStats
from qb import QuarterbackList

def print_loading_bar(progress, total):
    bar_length = 20
    progress_ratio = progress / total
    num_bar = int(progress_ratio * bar_length)
    bar = '[' + '#' * num_bar + ' ' * (bar_length - num_bar) + ']'
    return bar

def get_qb_stats(qb_list):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }

    for i in range(1970, 2024):
        loading_bar = print_loading_bar(i - 1970, 2024 - 1970)
        print("Loading stats.. {} {}/2024".format(loading_bar, i))
        url = 'https://www.nfl.com/stats/player-stats/category/passing/{}/post/all/passingyards/desc'.format(i)
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

        players = soup.find_all(class_="d3-o-player-fullname nfl-o-cta--link")
        passing_yards = soup.find_all(class_="selected")

        index = 0
        for player in players:
            if not any(qb.get_name() == player.text.strip() for qb in qb_list.get_list()):
                new_qb = QuarterBack(player.text.strip())
                qb_list.add_qb(new_qb)

            qb = next(qb for qb in qb_list.get_list() if qb.get_name() == player.text.strip())
            
            # Find all rows in the table
            rows = player.find_parent('tbody').find_all('tr')
            
            # Get the 7th row (0-based indexing)
            row = rows[index]  # Adjust index if needed
            
            # Extract touchdowns
            touchdowns = int(row.find_all('td')[6].text.strip())  # Adjust index if needed

            #Extract Interceptions
            interceptions = int(row.find_all('td')[7].text.strip())

            new_year = YearStats(i, int(passing_yards[index].text.strip()), touchdowns, interceptions, 0)
            qb.add_year(new_year)

            index += 1
        
        os.system('cls' if os.name == 'nt' else 'clear')

    return qb_list

def write_csv(file_name, qb_set):
    qb_list = qb_set.get_list()

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        for qb in qb_list:
            for year, y_object in qb.get_years().items():
                row = [qb.get_name(), year, y_object.get_passing_yards(), y_object.get_touchdowns(), y_object.get_interceptions(), y_object.get_completed_pass()]
                writer.writerow(row)

    print("File created!")

def read_csv(file_name, qb_list):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not any(qb.get_name() == row[0] for qb in qb_list.get_list()):
                new_qb = QuarterBack(row[0])
                qb_list.add_qb(new_qb)

            qb = next(qb for qb in qb_list.get_list() if qb.get_name() == row[0])

            new_year = YearStats(int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]))
            qb.add_year(new_year)
    
    return qb_list

def get_stats_by_qb(qb_list):
    qb_name = input("Enter QB Name: ").lower()

    print(qb_list.get_qb(qb_name))
    input("Enter to continue...")

def get_stats_by_year(qb_list):
    year_input = input("Enter a year: ")
    year_dict = {}

    lst = qb_list.get_list()
    for qb in lst:
        years = qb.get_years()
        for year in years.values():
            if str(year.get_year()) == str(year_input):
                year_dict[qb.get_name()] = year

    print("Stats for {} :".format(year_input))
    table_data = []
    for qb, year in year_dict.items():
        table_data.append([
            qb,
            year.get_passing_yards(),
            year.get_touchdowns(),
            year.get_interceptions(),
            "{}%".format(year.get_completed_pass())
        ])

    headers = ["Quarterback", "Passing Yards", "Touchdowns", "Interceptions", "Completed Pass"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    input("Enter to continue...")


def main():
    file_name = "all_qb_stats.csv"
    qb_list = QuarterbackList()

    if os.path.exists(file_name):
        qb_list = read_csv(file_name, qb_list)
    else:
        qb_list = get_qb_stats( qb_list)
        write_csv(file_name, qb_list)

    while True:
        print("Select option to show results: ")
        print("1. Get stats by QB")
        print("2. Get stats by Year")
        print("0. Exit")
        prompt = input()

        if prompt == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            get_stats_by_qb(qb_list)
        elif prompt == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            get_stats_by_year(qb_list)
        elif prompt == '0':
            break


main()
            
    