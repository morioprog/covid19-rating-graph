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
            "StandingsUrl": "#",
        })
        old_rating = e['count']
    return ret


with open('index.html', mode='w') as f:
    old_rating = data[-2]['count']
    new_rating = data[-1]['count']
    f.write(f'''\
<html>
    <head>
        <title>COVID-19 Rating Graph</title>
        <meta charset="utf-8"/>
        <link href="https://fonts.googleapis.com/css?family=Lato:400,700" rel="stylesheet" type="text/css">
        <link href="https://fonts.googleapis.com/css?family=Squada+One" rel="stylesheet" type="text/css">
        <link rel="stylesheet" type="text/css" href="https://img.atcoder.jp/public/7cd93c2/css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="style.css">
        <meta property="og:url" content="https://morioprog.github.io/covid19-rating-graph/" />
        <meta property="og:type" content="website" />
        <meta property="og:title" content="COVID-19 Rating Graph" />
        <meta property="og:description" content="レーティング：{old_rating}→{new_rating} ({"+" if old_rating < new_rating else ""}{new_rating - old_rating}) {":(" if old_rating < new_rating else ":)"} ({last_update}更新)" />
        <meta property="og:site_name" content="COVID-19 Rating Graph" />
        <meta property="og:image" content="https://raw.githubusercontent.com/morioprog/covid19-rating-graph/main/img/ogp.png" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:site" content="@morio_prog" />
    </head>
    <body>
        <div>
            <div class="center">
                <h1>COVID-19 Rating Graph</h1>
                <h4>完全に<span class="emphasize">非公式</span>です。</h4>
                <canvas id="ratingStatus" width="640" height="80"></canvas><br>
                <canvas id="ratingGraph" width="640" height="360"></canvas><br>
            </div>
            <div class="ul-center">
                <ul>
                    <li>作成者: <a href="https://twitter.com/morio_prog">@morio_prog</a></li>
                    <li>GitHub: <a href="https://github.com/morioprog/covid19-rating-graph">morioprog/covid19-rating-graph</a></li>
                    <li>データ: <a href="https://github.com/tokyo-metropolitan-gov/covid19">tokyo-metropolitan-gov/covid19</a></li>
                    <li>最終更新: {last_update}</li>
                </ul>
                <a href="https://twitter.com/share"
                    data-text="東京都新規陽性者数 ({last_update[:-6]}更新)\nレーティング：{old_rating}→{new_rating} ({"+" if old_rating < new_rating else ""}{new_rating - old_rating}) {":(" if old_rating < new_rating else ":)"}\n#COVID19RatingGraph\n"
                    class="twitter-share-button"
                    data-show-count="false">
                    Tweet
                </a>
            </div>
        </div>
        <script type="text/javascript" src="https://code.createjs.com/easeljs-0.8.2.min.js"></script>
        <script type="text/javascript" src="https://img.atcoder.jp/public/fc4b538/js/lib/jquery-1.9.1.min.js"></script>
        <script type="text/javascript" src="https://img.atcoder.jp/public/ad3eaad/js/rating-graph.js"></script>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        <script>
            const rating_history = {convert_dict(data)};
        </script>
    </body>
</html>
''')

with open('ogp.html', mode='w') as f:
    f.write(f'''\
<html>
    <head>
        <meta charset="utf-8"/>
        <link href="https://fonts.googleapis.com/css?family=Lato:400,700" rel="stylesheet" type="text/css">
        <link href="https://fonts.googleapis.com/css?family=Squada+One" rel="stylesheet" type="text/css">
        <link rel="stylesheet" type="text/css" href="https://img.atcoder.jp/public/7cd93c2/css/bootstrap.min.css">
    </head>
    <body style="text-align:center;">
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
