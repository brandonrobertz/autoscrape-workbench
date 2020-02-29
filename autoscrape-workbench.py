import asyncio
from datetime import datetime
import re

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
        max_pages=25,
        driver="Firefox",
        form_submit_natural_click=params.get("form-submit-natural-click"),
        formdepth=params.get("formdepth", 10),
        link_priority=params.get("link-priority"),
        ignore_links=params.get("ignore-links"),
        form_match=params.get("form-match"),
        save_screenshots=True,
        loglevel="DEBUG",
        output=None,
        disable_style_saving=False,
        stdout=True,
    )

    crawl_data = ManualControlScraper(
        baseurl, **autoscrape_kwargs
    ).run()

    html_only = []
    for data in crawl_data:
        css = data.get("css")
        html = data.get("html")
        fileclass = data.pop("fileclass", None)
        if fileclass == "downloads":
            continue
        if not re.findall('<\s*html', html, re.IGNORECASE):
            continue
        html_only.append(data)

    return pd.DataFrame(html_only), None
