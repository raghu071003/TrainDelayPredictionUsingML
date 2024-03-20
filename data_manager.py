# uncompyle6 version 3.9.0
# Python bytecode version base 3.6 (3379)
# Decompiled from: Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 23:11:46) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: data_manager.py
# Compiled at: 2019-01-02 14:47:47
# Size of source mod 2**32: 5216 bytes
import re, requests
from os import system
try:
    from bs4 import BeautifulSoup
except:
    system('pip install beautifulsoup4')
    from bs4 import BeautifulSoup

import csv, ast
from time import sleep

def webfetch_stations_trains(label):
    data = {}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    start_urls = {'stations':'https://www.cleartrip.com/trains/stations/list',  'trains':'https://www.cleartrip.com/trains/list?field=number&sort=up'}
    start_url = start_urls[label]
    try:
        print('opening the {} url'.format(label))
        r = requests.get(start_url)
    except:
        print('please check network connection')
        return
    else:
        soup = BeautifulSoup(r.content, 'html.parser')
        tables = soup.find_all('table')
        if not tables:
            print('No tables found on the page')
            return
        table = tables[0]  # Assuming you want to use the first table found
        rows = table.find_all('tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            data[re.sub('<.*?>', '', str(cols[0]))] = re.sub('<.*?>', '', str(cols[1]))

        div_lst = soup.find_all('div', {'class': 'pagination'})
        if div_lst:
            a_lst = div_lst[0].find_all('a', {'class': 'next_page'})
            if a_lst:
                print('.')
                r = requests.get('https://www.cleartrip.com' + a_lst[0]['href'])
                soup = BeautifulSoup(r.content, 'html.parser')

        print(label, ' extracted')
        return data


def webfetch_avg_delays(station):
    print(station)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    r = requests.get(('https://www.railyatri.in/insights/average-train-delay-at-station/' + station), headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = {}
    while True:
        div_lst = soup.find_all('div', {'class': 'pages'})
        if not len(div_lst):
            break
        scripts = soup.find_all('script')
        list_str = re.sub('<.*?>', '', str(scripts[-7])).split(';')[0].split('=')[1].strip()
        train_delay_lst = ast.literal_eval(list_str)
        for train_delay_dict in train_delay_lst:
            mtch = re.match('([0-9]+) \\(([0-9]+).*', train_delay_dict['number'])
            data[mtch.group(1)] = int(mtch.group(2))

        a = div_lst[0].find_all('a')
        if len(a) == 0 or a[1]['title'] == 'No More Data':
            break
        r = requests.get(('https://www.railyatri.in' + a[1]['href']), headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')

    return data


def update_stations_trains(label):
    data = webfetch_stations_trains(label)
    # print(f"updating {label} data")
    # with open(f"{label}.csv", 'w') as (file):
    #     writer = csv.writer(file)
    #     for code, name in data.items():
    #         writer.writerow([code, name])

    return data


def filefetch_stations_trains(label):
    data = {}
    print(('Compiling {} data'.format(label)), end='')
    sleep(5)
    with open('{}.csv'.format(label), 'r') as (file):
        reader = csv.reader(file)
        for row in reader:
            data[row[0]] = row[1]

    print(' Done...')
    return data


def update_avg_delays(stations):
    data = {}
    for station, _ in stations.items():
        data[station] = webfetch_avg_delays(station)

    # with open('train_delays.csv', 'w') as (train_delays_file):
    #     train_delays_writer = csv.writer(train_delays_file)
    #     for station_code, trains in data.items():
    #         for train_code, delay in trains.items():
    #             train_delays_writer.writerow([station_code, train_code, delay])

    # print('update successful')
    return data


def filefetch_avg_delays():
    data = {}
    print('Computing delay predictions... Please Wait', end='')
    for x in range(10):
        print('.', end='')
        sleep(1)

    with open('train_delays.csv', 'r') as (train_delays_file):
        train_delays_reader = csv.reader(train_delays_file)
        for row in train_delays_reader:
            try:
                data[row[0]][row[1]] = row[2]
            except:
                data[row[0]] = {}

    print(' Done..  \n \n GUI Started')
    return data


if __name__ == '__main__':
    stations = update_stations_trains('stations')
    update_stations_trains('trains')
    stations = filefetch_stations_trains('stations')
    trains = filefetch_stations_trains('trains')
    avg_delays = filefetch_avg_delays()