from flask import Flask, render_template, session
from datetime import datetime, timedelta
from Stats import stats_route

app = Flask(__name__)
app.secret_key = "secret_key"
app.permanent_session_lifetime = timedelta(minutes=10)

@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/Vrienden.')
def Vrienden():
    return render_template('Vrienden.html')

@app.route('/Community.')
def Community():
    return render_template('Community.html')

@app.route('/Gezondheid.')
def Gezondheid():
    return render_template('Gezondheid.html')


app.add_url_rule('/Stats', 'Stats', stats_route(), methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)

"""
Bronnen:
https://www.youtube.com/watch?v=jQjjqEjZK58


Install:
pip install requests
pip install Flask
pip install python-dotenv
"""