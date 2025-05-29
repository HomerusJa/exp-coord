import marimo

__generated_with = "0.13.14"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
    # Event Overview

    The goal of this notebook is to give an idea of how many and which events have been sent to the coordinator. For that, we will consult the MongoDB database, specifically the `all_messages_and_events` table.
    """
    )
    return


@app.cell
async def _():
    print("⏳ Connecting to the database. This might take a few seconds.")

    from exp_coord.db.connection import init_db as _init_db

    await _init_db()

    print("✅ Database connected.")
    return


@app.cell
async def _(AllMessagesAndEvents, mo):
    total_message_count = await AllMessagesAndEvents.count()

    mo.md(
        f"The experiment coordinator has received a total of **{total_message_count} messages.** "
    )
    return (total_message_count,)


@app.cell
async def _(AllMessagesAndEvents, mo, total_message_count):
    event_messages = AllMessagesAndEvents.find(
        AllMessagesAndEvents.data.messageType == "eventMessage"
    )
    event_message_count = await event_messages.count()

    mo.md(
        f"Out of these {total_message_count} messages, there were **{event_message_count} events** and **{total_message_count - event_message_count} other messages.**"
    )
    return


@app.cell
async def _(AllMessagesAndEvents, mo):
    _pipeline = [
        # Not actually needed as only events have topics
        {"$match": {"data.messageType": "eventMessage"}},
        {"$group": {"_id": "$data.topic", "count": {"$sum": 1}}},
    ]
    _raw_results = await AllMessagesAndEvents.aggregate(_pipeline).to_list()
    _counts: list[dict[str, str | int]] = [
        {"topic": item["_id"], "count": item["count"]} for item in _raw_results
    ]

    # Extract for use down below
    new_images_count = [
        item["count"]
        for item in _counts
        if item["topic"] == "plant-growth-observation_new-image"
    ][0]

    mo.vstack(
        [
            mo.md(
                f"Below, you can see the different topics and the number of times they have been received. There have been **{len(_counts)} different topics**."
            ),
            mo.ui.table(data=_counts),
        ]
    )
    return (new_images_count,)


@app.cell
async def _(AllMessagesAndEvents, mo):
    _pipeline = [
        {"$match": {"data.messageType": "eventMessage"}},
        {"$match": {"data.topic": "plant-growth-observation_status"}},
        {"$group": {"_id": "$data.content.status", "count": {"$sum": 1}}},
    ]
    _raw_results = await AllMessagesAndEvents.aggregate(_pipeline).to_list()
    _counts: list[dict[str, str | int]] = [
        {"status": item["_id"], "count": item["count"]} for item in _raw_results
    ]

    # Extract the amount of capture statuses for later use
    capture_status_count = [
        item["count"] for item in _counts if item["status"] == "capture"
    ][0]

    mo.vstack(
        [
            mo.md(
                f"This table shows the different types of statuses received and their respective count. There were **{len(_counts)} different statuses**."
            ),
            mo.ui.table(data=_counts),
        ]
    )
    return (capture_status_count,)


@app.cell
async def _(Image, capture_status_count, mo, new_images_count):
    mo.md(
        rf"""
    Great. As can be seen above, we have **{capture_status_count} captures**, but we only have received **{new_images_count} images**. This indicates a problem in that regard. Let's find out when we should have received an image but didn't!

    Also, in the image table, there are just **{await Image.count()} entries.** That's because I had a bug previously which caused two images to get lost.
    """
    )
    return


@app.cell
async def _(AllMessagesAndEvents, datetime, mo):
    _capture_messages = await AllMessagesAndEvents.find(
        AllMessagesAndEvents.data.content.status == "capture"
    ).to_list()

    _dicts = [message.model_dump() for message in _capture_messages]
    _data = [
        {"added_at": message["added_at"], **message["data"]} for message in _dicts
    ]

    for _message in _data:
        del _message["identifier"]
        del _message["messageType"]
        del _message["topic"]
        _message["timestamp"] = datetime.fromtimestamp(_message["timestamp"])

        for _key, _value in _message["content"].items():
            if not _value:
                _value = mo.md("*empty*")
            _message["content_" + _key] = _value
        del _message["content"]
        del _message["sender"]

    mo.ui.table(data=_data, pagination=False, label="**Capture Status Messages (cleaned)**")

    return


@app.cell
async def _(AllMessagesAndEvents, datetime, mo):
    _new_image_messages = await AllMessagesAndEvents.find(
        AllMessagesAndEvents.data.topic == "plant-growth-observation_new-image"
    ).to_list()

    _dicts = [message.model_dump() for message in _new_image_messages]
    _data = [
        {"added_at": message["added_at"], **message["data"]} for message in _dicts
    ]

    for _message in _data:
        del _message["identifier"]
        del _message["messageType"]
        del _message["topic"]
        _message["timestamp"] = datetime.fromtimestamp(_message["timestamp"])

        for _key, _value in _message["content"].items():
            if not _value:
                _value = mo.md("*empty*")
            _message["content_" + _key] = _value
        del _message["content"]
        _message["content_image"] = f"b64 len={len(_message["content_image"])}"
        _message["content_takenAt"] = datetime.fromtimestamp(_message["content_takenAt"])

        del _message["sender"]

    mo.ui.table(data=_data, pagination=False, label="**New Image Messages (cleaned)**")

    return


@app.cell(hide_code=True)
def _():
    from exp_coord.db.all_messages_and_events import AllMessagesAndEvents
    from exp_coord.db.image import Image
    return AllMessagesAndEvents, Image


@app.cell(hide_code=True)
def _():
    from devtools import pprint
    return


@app.cell(hide_code=True)
def _():
    from datetime import datetime
    return (datetime,)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
