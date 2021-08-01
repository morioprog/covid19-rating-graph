import json
import requests
import datetime

api = "https://raw.githubusercontent.com/tokyo-metropolitan-gov/covid19/master/data/daily_positive_detail.json"
req = requests.get(api)
json = req.json()
last_update = json['date']
data = json['data']


def rate_to_color(rate):
    if rate >= 2800:
        return '#FF0000'
    if rate >= 2400:
        return '#FF8000'
    if rate >= 2000:
        return '#C0C000'
    if rate >= 1600:
        return '#0000FF'
    if rate >= 1200:
        return '#00C0C0'
    if rate >= 800:
        return '#008000'
    if rate >= 400:
        return '#804000'
    if rate > 0:
        return '#808080'
    return '#000000'


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
    S_HIGHEST = "Highestを更新してしまいました...\n"
    old_rating = data[-2]['count']
    new_rating = data[-1]['count']
    rating_diff = f"{'+' if old_rating < new_rating else ''}{new_rating - old_rating}"
    is_highest = max(e['count'] for e in data[:-1]) < data[-1]['count']
    y, m, d = map(int, last_update[:-6].split('/'))
    last_update_dt = datetime.datetime(year=y, month=m, day=d)

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
        <meta property="og:description" content="レーティング：{old_rating}→{new_rating} ({rating_diff}) {":(" if old_rating < new_rating else ":)"}\n{S_HIGHEST if is_highest else ""}({last_update}更新)" />
        <meta property="og:site_name" content="COVID-19 Rating Graph" />
        <meta property="og:image" content="https://raw.githubusercontent.com/morioprog/covid19-rating-graph/main/img/ogp.png?{int(datetime.datetime.now().timestamp())}" />
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
                    data-text="東京都新規陽性者数 ({last_update[:-6]}更新)\nレーティング：{old_rating}→{new_rating} ({rating_diff}) {":(" if old_rating < new_rating else ":)"}\n{S_HIGHEST if is_highest else ""}#COVID19RatingGraph\n"
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
    <body>
        <div style="display:flex;">
            <div style="width:640px;height:440px;">
                <canvas id="ratingStatus" width="640" height="80"></canvas><br>
                <canvas id="ratingGraph" width="640" height="360"></canvas><br>
            </div>
            <div style="width:198px;height:440px;background-color:#dddddd;text-align:center;">
                <div style="font-family:'Lato';font-size:35px;font-weight:bold;margin-top:40px;margin-bottom:10px;">{last_update[5:-6]} ({"月火水木金土日"[last_update_dt.weekday()]})</div>
                <div style="font-family:'Squada One';font-size:72px;color:{rate_to_color(old_rating)};">{old_rating}</div>
                <div style="font-size:30px;text-shadow:0.3px 0.3px 0,0.3px -0.3px 0px,-0.3px 0.3px 0,-0.3px -0.3px 0px,0.3px 0px 0px,0px 0.3px 0px,-0.3px 0px 0px,0px -0.3px 0px;">↓</div>
                <div style="font-family:'Squada One';font-size:72px;color:{rate_to_color(new_rating)};">{new_rating}</div>
                <div style="font-family:'Lato';font-size:30px;">({rating_diff})</div>
            </div>
        </div>
        <script type="text/javascript" src="https://code.createjs.com/easeljs-0.8.2.min.js"></script>
        <script type="text/javascript" src="https://img.atcoder.jp/public/fc4b538/js/lib/jquery-1.9.1.min.js"></script>
        <script type="text/javascript" src="https://img.atcoder.jp/public/ad3eaad/js/rating-graph.js"></script>
        <script>
            const rating_history = {convert_dict(data)};
        </script>
    </body>
</html>
''')
