import asyncio

from autoscrape import ManualControlScraper
import pandas as pd


async def async_autoscrape(baseurl, **kwargs):
    return await asyncio.coroutine(ManualControlScraper)(baseurl, **kwargs)


async def fetch(params, *, get_input_dataframe):
    print("AutoScrape Workbench called with parameters: %s" % (params))
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
    )
    crawl_data = ManualControlScraper(
        baseurl, **autoscrape_kwargs
    )
    table = pd.DataFrame(crawl_data)
    return table
