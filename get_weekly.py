from collections import OrderedDict

from datetime import date, datetime, timedelta
import json
import os
import requests

STRAVA_PUBLIC_AUTH = os.getenv('STRAVA_PUBLIC_AUTH')
CLUBS = [197162,]#, 2298]
ROOT_URL = 'https://www.strava.com/api/v3/'


def get(path, params=None):
    params = params or {}
    params.update({'per_page': 200})
    headers = {
        'Authorization': 'Bearer {}'.format(STRAVA_PUBLIC_AUTH)
    }
    res = requests.get(ROOT_URL + path, params=params, headers=headers)
    res.raise_for_status()
    return res.json()


def get_clubs():
    data = OrderedDict()
    for club in CLUBS:
        for x in range(1, 100):
            res = get('clubs/{}/activities'.format(club), params={'page': x})
            if not res:
                break

            for entry in res:
                data[entry['id']] = {
                    'athlete': entry['athlete']['id'],
                    'distance': entry['distance'],
                    'date': entry['start_date']
                }

        json.dump(data, open('data/data.{}.json'.format(club), 'w'))


def summarize():
    for filename in os.listdir('data'):
        if filename.endswith('.json'):
            file_id = filename.split('.')[1]
            data = {}
            entries = json.load(open('data/{}'.format(filename)))
            for key, entry in entries.items():
                date_obj = datetime.strptime(entry['date'], '%Y-%m-%dT%H:%M:%SZ').date()
                start_week = date_obj - timedelta(days=date_obj.weekday())
                start_week = start_week.strftime('%Y-%m-%d')

                data.setdefault(start_week, {'distance': 0, 'athletes': []})
                data[start_week]['distance'] += entry['distance']
                if entry['athlete'] not in data[start_week]['athletes']:
                    data[start_week]['athletes'].append(entry['athlete'])

            sorted_data = OrderedDict()
            keys = sorted(data.keys())
            for key in keys:
                sorted_data[key] = data[key]

            json.dump(data, open('summaries/summary.{}.json'.format(file_id), 'w'))


if __name__ == '__main__':
    get_clubs()
    summarize()
