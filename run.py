from flask import Flask
from flask_apscheduler import APScheduler

from config import DevelopmentConfig
from app import RssService, CustomLogger

logger = CustomLogger(name='RSS Logger')

# Rss Background Service
RSS_BG: RssService = RssService(logger)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

scheduler.add_job(id='RSS Scheduled Task', func=RSS_BG.service,
                  trigger='interval', minutes=30)


@app.route('/')
def index():
    return "Welcome to Sentrix."


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4030)
