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
        input=None,
        save_graph=False,
        load_images=False,
        maxdepth=10,
        next_match=None,
        leave_host=False,
        show_browser=False,
        driver="Firefox",
        form_submit_natural_click=False,
        formdepth=None,
        link_priority=None,
        keep_filename=False,
        ignore_links=None,
        form_match=None,
        save_screenshots=True,
        loglevel="DEBUG",
        output=None,
        disable_style_saving=False,
    )
    crawl_data = await async_autoscrape(
        baseurl, **autoscrape_kwargs
    )
    table = pd.DataFrame(crawl_data)
    return table
