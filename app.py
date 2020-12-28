from typing import Any, Dict

from datetime import datetime
import os
import pytz
import requests

from chalice import Chalice, Cron

app = Chalice(app_name='dailyChallengeNotifier')
WEBHOOK_URL = os.environ['WEBHOOK_URL']


def get_pst_now() -> datetime:
    utc_now = datetime.now(tz=pytz.utc)
    return utc_now.astimezone(pytz.timezone('US/Pacific'))


def generate_message() -> str:
    pst_today = get_pst_now().strftime('%Y/%m/%d')
    return f'Time to take on the daily problem for {pst_today}!!'


def post_message(message: str) -> None:
    response = requests.post(WEBHOOK_URL, json={'text': message})
    app.log.info(response)


# PST 00:00 == UTC 08:00
@app.schedule(Cron(0, 8, '*', '*', '?', '*'))
def kick_job(event: Dict[str, Any]) -> None:
    post_message(generate_message())
