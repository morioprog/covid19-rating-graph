import json
import requests
import datetime

api = "https://raw.githubusercontent.com/tokyo-metropolitan-gov/covid19/master/data/daily_positive_detail.json"
req = requests.get(api)
json = req.json()
last_update = json['date']
data = json['data']


def convert_dict(dct):
    ret = []
    old_rating = 0
    for e in dct:
        ret.append({
            "ContestName": "東京都新規陽性者数の遷移",
            "OldRating": old_rating,
            "NewRating": e['count'],
            "EndTime": datetime.datetime.strptime(e['diagnosed_date'], '%Y-%m-%d').timestamp(),
            "Place": -1,
            "StandingsUrl": "/",
        })
        old_rating = e['count']
    return ret


with open('index.html', mode='w') as f:
    f.write(f'''\
<html>
    <head>
        <title>COVID-19 Rating Graph</title>
    </head>
    <body>
        <link href="https://fonts.googleapis.com/css?family=Lato:400,700" rel="stylesheet" type="text/css">
        <link href="https://fonts.googleapis.com/css?family=Squada+One" rel="stylesheet" type="text/css">
        <link rel="stylesheet" type="text/css" href="https://img.atcoder.jp/public/7cd93c2/css/bootstrap.min.css">
        <canvas id="ratingStatus" width="640" height="80"></canvas><br>
        <canvas id="ratingGraph" width="640" height="360"></canvas><br>
        <script type="text/javascript" src="https://code.createjs.com/easeljs-0.8.2.min.js"></script>
        <script type="text/javascript" src="https://img.atcoder.jp/public/fc4b538/js/lib/jquery-1.9.1.min.js"></script>
        <script type="text/javascript" src="https://img.atcoder.jp/public/ad3eaad/js/rating-graph.js"></script>
        <script>
            const rating_history = {convert_dict(data)};
        </script>
    </body>
</html>
''')
