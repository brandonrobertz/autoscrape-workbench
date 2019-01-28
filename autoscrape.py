import time
import requests

import pandas as pd

from server.modules.types import ProcessResult


# in seconds
POLL_FREQ = 2
BASE_API = "http://autoscrape_flask:5000"


async def get_scraped_data(scrape_id):
    """
    Get the list of scraped files and, for each, request the
    data (base 64 encoded). Returns a DataFrame of the data
    and metadata.
    """
    list_url = "%s/files/list/%s" % (BASE_API, scrape_id)
    files_data = requests.get(list_url)

    data = {
        "files": [],
        "names": []
    }
    for record in files_data["data"]:
        file_id = record["id"]
        file_url = "%s/files/data/%s/%s" % (BASE_API, scrape_id, file_id)
        file_data = requests.get(file_url)
        data["files"].append(file_data["data"]["data"])
        data["names"].append(file_data["data"]["name"])

    return pd.DataFrame(data)


async def start_scrape(params):
    """
    Start a scrape, poll for scrape status and grab all files
    once the scrape is completed.
    """
    print("start_scrape", params)
    start_url = "%s/start" % BASE_API

    #response = requests.post(url, data=params)
    #post_data = response.json()
    #scrape_id = post_data["data"]

    #while True:
    #    print("Polling...")
    #    status_url = "%s/status/%s" % (BASE_API, scrape_id)
    #    status_data = requests.get(status_url).json()

    #    if status_data["status"] == "SUCCESSFUL":
    #        break
    #    elif status_data["status"] == "FAILURE":
    #        break
    #    elif status_data["status"] == "STARTED":
    #        b64_screenshot = status_data["data"]

    #    time.sleep(POLL_FREQ)

    # df = await get_scraped_data(scrape_id)
    return ProcessResult(dataframe={"a": [], "b": []})


async def fetch(params):
    print("fetch params", params)
    baseurl = params.get("baseurl")
    data = {
        "baseurl": baseurl,
        "form_submit_wait": 5,
        "input": None,
        "save_graph": False,
        "load_images": False,
        "maxdepth": None,
        "next_match": "next",
        "leave_host": False,
        "show_browser": False,
        "driver": "Firefox",
        "form_submit_natural_click": False,
        "formdepth": None,
        "link_priority": None,
        "keep_filename": False,
        "ignore_links": None,
        "form_match": None,
        "save_screenshots": True,
        "loglevel": "DEBUG",
        "output": "http://flask:5001/receive",
        "disable_style_saving": False
    }
    if not baseurl:
        return "You need to enter a starting URL to scrape"

    return pd.DataFrame({"time": [1]}) #await start_scrape(urls, table)


def render(table, params, *, fetch_result, **kwargs):
    # print("render", params)
    print("render params", params)
    print("render table", table)
    # print("fetch_result", fetch_result)
    if params.get("baseurl"):
        return ProcessResult(table)

    if fetch_result is None:
        return ProcessResult(table)

    else:
        return fetch_result

