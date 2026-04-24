import requests
from datetime import datetime
from urllib.parse import urlparse

def check_link(url):
    try:
        start = datetime.now()

        response = requests.get(url, timeout=5)

        end = datetime.now()
        time_taken = (end - start).total_seconds()

        status = response.status_code

        if 200 <= status < 300:
            category = "Valid"
        else:
            category = "Failed"

        final_url = response.url

    except Exception as e:
        status = "Error"
        time_taken = None
        final_url = None
        category = "Failed"

    domain = urlparse(url).netloc

    return [url, status, time_taken, final_url, category, domain]