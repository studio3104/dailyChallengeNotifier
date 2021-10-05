from typing import Any, Dict

from datetime import datetime
import logging
import os
import pytz
import requests
import textwrap

from chalice import Chalice, Cron

app = Chalice(app_name='dailyChallengeNotifier')
app.log.setLevel(logging.INFO)

WEBHOOK_URL = os.environ['WEBHOOK_URL']


def get_pst_now() -> datetime:
    utc_now = datetime.now(tz=pytz.utc)
    return utc_now.astimezone(pytz.timezone('US/Pacific'))


def generate_message() -> str:
    pst_today = get_pst_now().strftime('%Y/%m/%d')
    return textwrap.dedent(
        f"""
        Time to take on the daily problem for {pst_today}!!
        https://leetcode.com/explore/challenge/
        """
    ).strip()


def post_message(message: str) -> None:
    post_body = {
        'text': message,
    }
    response = requests.post(WEBHOOK_URL, json=post_body)
    app.log.info(response)


# UTC+0000, PDT-0700, PST-0800
@app.schedule(Cron(0, 0, '*', '*', '?', '*'))
def kick_job(event: Dict[str, Any]) -> None:
    post_message(generate_message())
