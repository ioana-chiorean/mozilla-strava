from collections import OrderedDict

from datetime import date, datetime, timedelta
import json
import os
import requests

CLUBS = [88420]
ROOT_URL = 'https://www.strava.com/clubs/'

offset = 0

today = datetime.today()
today_str = today.strftime('%Y-%m-%d')
start_week = today - timedelta(days=today.weekday()) - timedelta(days=offset*7)
start_week_str = start_week.strftime('%Y-%m-%d')


def get(path):
    headers = {
        'Accept': 'text/javascript, application/javascript'
    }
    url = '%s%d/leaderboard/' % (ROOT_URL, path)
    if offset:
        url += '?week_offset=' + str(offset)
    res = requests.get(url, headers=headers)
    return res.json()


def summarize():
    for club in CLUBS:
        filename = 'summaries/summary.{}.json'.format(club)
        try:
            data = json.load(open(filename, 'r'))
        except (ValueError, IOError):
            data = {}

        id = start_week_str
        athlete_set = set()
        data[id] = {'distance': 0, 'athletes': 0}
        leaderboard = get(club)
        for entry in leaderboard['data']:
            if int(entry['distance']) == 0:
                continue
            athlete_set.add(entry['athlete_id'])
            data[id]['distance'] = data[id]['distance'] + entry['distance']
            data[id]['athletes'] = len(athlete_set)

        sorted_data = OrderedDict()
        keys = reversed(sorted(data.keys()))
        for key in keys:
            sorted_data[key] = data[key]

        json.dump(sorted_data, open(filename, 'w'), indent=2)


if __name__ == '__main__':
    summarize()
