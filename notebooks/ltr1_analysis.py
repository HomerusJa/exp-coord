import marimo

__generated_with = "0.13.14"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
    # Long Test Run Analysis Notebook

    This is a notebook doing analysis on all the data from the given datetimes below.
    """
    )
    return


@app.cell
def _(datetime, mo, timedelta):
    # _tolerance = timedelta(hours=2)
    # start_time = datetime(2025, 6, 11, 19, 0) - _tolerance
    # end_time = datetime(2025, 6, 12, 16, 0)  # No tolerance here

    start_time = mo.ui.datetime(
        label="Start", value=datetime.today() - timedelta(weeks=2)
    )
    end_time = mo.ui.datetime(label="End", value=datetime.today())
    mo.hstack([start_time, end_time])
    return end_time, start_time


@app.cell
async def _(AllMessagesAndEvents, Image, Status, end_time, start_time):
    # Fetch all messages, all images and all statuses in the time period above

    all_images = await Image.find_many(
        Image.taken_at > start_time.value and Image.taken_at < end_time.value
    ).to_list()
    all_statuses = await Status.find_many(
        Status.received_timestamp > start_time.value
        and Status.received_timestamp < end_time.value
    ).to_list()
    all_messages = await AllMessagesAndEvents.find_many(
        AllMessagesAndEvents.added_at > start_time.value
        and AllMessagesAndEvents.added_at < end_time.value
    ).to_list()

    from itertools import chain as _chain

    for entry in _chain(all_images, all_statuses, all_messages):
        await entry.fetch_all_links()

    {
        "all_images": all_images,
        "all_statuses": all_statuses,
        "all_messages": all_messages,
    }
    return all_images, all_messages, all_statuses


@app.cell
def _(all_images, all_messages, all_statuses, mo):
    mo.md(
        rf"""Received {len(all_images)} images, {len(all_statuses)} statuses and a total of {len(all_messages)} messages and events."""
    )
    return


@app.cell
def _(Counter, all_messages, mo):
    mo.ui.table(
        Counter(msg.data.messageType for msg in all_messages),
        label="**Message Types**",
    )
    return


@app.cell
def _(Counter, all_messages, mo):
    mo.ui.table(
        Counter(
            msg.data.content["status"]
            for msg in all_messages
            if msg.data.messageType == "eventMessage"
            and msg.data.content["type"] == "status"
        ),
        label="**Status Event Types**",
    )
    return


@app.cell
def _(all_messages, deepcopy):
    _err_msgs = [msg for msg in all_messages if msg.data.messageType == "eventMessage" and msg.data.content["type"] == "status" and msg.data.content["status"] == "error"]
    _err_msgs = deepcopy(_err_msgs)
    _err_msgs = [msg.data for msg in _err_msgs]

    _err_msgs
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    from datetime import datetime, timedelta
    return datetime, mo, timedelta


@app.cell(hide_code=True)
async def _():
    from exp_coord.db.connection import init_db

    await init_db()
    return


@app.cell(hide_code=True)
def _():
    from exp_coord.db.image import Image
    from exp_coord.db.all_messages_and_events import AllMessagesAndEvents
    from exp_coord.db.status import Status
    return AllMessagesAndEvents, Image, Status


@app.cell(hide_code=True)
def _():
    import logging

    logging.getLogger("MARKDOWN").setLevel(logging.WARNING + 1)
    return


@app.cell(hide_code=True)
def _():
    from collections import Counter
    return (Counter,)


@app.cell(hide_code=True)
def _():
    from copy import deepcopy
    return (deepcopy,)


if __name__ == "__main__":
    app.run()
