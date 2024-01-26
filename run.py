from config import DevelopmentConfig
from app import RssService, CustomLogger, TradesService, Factory

from flask import Flask
from flask_apscheduler import APScheduler
import os

logger = CustomLogger(name='RSS Logger')

logger.warning('Look at my eyes')

# Rss Background Service
RSS_BG: RssService = RssService(logger)
TRADES_BG: TradesService = TradesService(logger)

FACTORY = Factory(RSS_BG, TRADES_BG, logger)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

scheduler.add_job(id='RSS Scheduled Task', func=FACTORY.dataCollectionFactory,
                  trigger='interval', minutes=10)


@app.route('/')
def index():
    return "Welcome to Sentrix."


if __name__ == '__main__':
    # Only run the development server if not in production
    if os.environ.get("FLASK_ENV") != "production":
        app.run(debug=True, host='0.0.0.0', port=4030)
