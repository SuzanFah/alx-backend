#!/usr/bin/env python3
"""Flask app with internationalization, timezone and current time display"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from datetime import datetime

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class Config:
    """Config class for Flask app"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

def get_user():
    """Returns user dictionary if ID exists"""
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None

@app.before_request
def before_request():
    """Sets user as global on flask.g.user"""
    g.user = get_user()

@babel.localeselector
def get_locale():
    """Determine best match for supported languages"""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    """Determine appropriate timezone"""
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if g.user and g.user['timezone']:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    return "UTC"

@app.route('/', strict_slashes=False)
def index():
    """Route handler for the home page"""
    timezone = pytz.timezone(get_timezone())
    current_time = datetime.now(timezone)
    time_format = '%b %d, %Y, %I:%M:%S %p'
    if get_locale() == 'fr':
        time_format = '%d %b %Y à %H:%M:%S'
    formatted_time = current_time.strftime(time_format)
    return render_template('index.html', current_time=formatted_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
