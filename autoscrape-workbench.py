import asyncio
from datetime import datetime

from autoscrape import ManualControlScraper
import pandas as pd


async def async_autoscrape(baseurl, **kwargs):
    return await asyncio.coroutine(ManualControlScraper)(baseurl, **kwargs)


async def fetch(params, *, get_input_dataframe):
    baseurl = params["baseurl"]
    autoscrape_kwargs = dict(
        backend="requests",
        return_data=True,
        form_submit_wait=5,
        input=params.get("input"),
        save_graph=False,
        load_images=False,
        maxdepth=params.get("maxdepth", 10),
        next_match=params.get("next-match", "next"),
        leave_host=False,
        show_browser=False,
        driver="Firefox",
        form_submit_natural_click=params.get("form-submit-natural-click"),
        formdepth=params.get("formdepth", 10),
        link_priority=params.get("link-priority"),
        keep_filename=False,
        ignore_links=params.get("ignore-links"),
        form_match=params.get("form-match"),
        save_screenshots=True,
        loglevel="DEBUG",
        output=None,
        disable_style_saving=False,
        stdout=False,
    )

    crawl_data = ManualControlScraper(
        baseurl, **autoscrape_kwargs
    ).run()

    table = pd.DataFrame(
        {
            # TODO use response date, not current date
            # TODO migrate to use timestamp type, not text (will affect
            # existing users)
            "status": "",
            "url": "",
            "html": "",
            "css": "",
            "date": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        }
    )
    for row in range(len(crawl_data)):
        table.loc[row, "status"] = "OK"
        table.loc[row, "url"] = crawl_data[row]["url"]
        table.loc[row, "html"] = crawl_data[row]["html"]
        table.loc[row, "css"] = crawl_data[row]["css"]
        table.loc[row, "date"] = crawl_data[row]["date"]

    return table
