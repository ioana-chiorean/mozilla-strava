from collections import OrderedDict

from datetime import date, datetime, timedelta
import json
import os
import requests

CLUBS = [197162, 2298]
ROOT_URL = 'https://www.strava.com/clubs/'

today = datetime.today()
today_str = today.strftime('%Y-%m-%d')
start_week = today - timedelta(days=today.weekday())
start_week_str = start_week.strftime('%Y-%m-%d')


def get(path):
    headers = {
        'Accept': 'text/javascript, application/javascript'
    }
    url = '%s%d/leaderboard/' % (ROOT_URL, path)
    res = requests.get(url, headers=headers)
    return res.json()


def get_clubs():
    for club in CLUBS:
        try:
            data = json.load(open('data/data.{}.json'.format(club), 'r'))
        except ValueError:
            data = {}
        leaderboard = get(club)
        for entry in leaderboard['data']:
            id = '%s-%s' % (start_week_str, entry['best_activities_distance_activity_id'])
            if int(entry['distance']) == 0:
                continue
            data[id] = {
                'week': start_week_str,
                'date': today_str,
                'athlete': entry['athlete_id'],
                'distance': entry['distance'],
            }

        sorted_data = OrderedDict()
        keys = sorted(data.keys())
        for key in keys:
            sorted_data[key] = data[key]

        json.dump(sorted_data, open('data/data.{}.json'.format(club), 'w'), indent=2)


def summarize():
    for filename in os.listdir('data'):
        if filename.endswith('.json'):
            file_id = filename.split('.')[1]
            data = {}
            try:
                entries = json.load(open('data/{}'.format(filename)))
            except ValueError:
                entries = {}
            for key, entry in entries.items():
                data.setdefault(entry['week'], {'distance': 0, 'athletes': 0})
                data[entry['week']]['distance'] += entry['distance']
                data[entry['week']]['athletes'] += 1

            sorted_data = OrderedDict()
            keys = reversed(sorted(data.keys()))
            for key in keys:
                sorted_data[key] = data[key]

            json.dump(sorted_data, open('summaries/summary.{}.json'.format(file_id), 'w'), indent=2)


if __name__ == '__main__':
    get_clubs()
    summarize()
