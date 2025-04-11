import marimo

__generated_with = "0.12.8"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Show status information

        This notebook is intended to show the status information of the camera I ran for the last couple days (s3is3i:4eadfd01-0eef-4567-ab01-0d6add9c9a0cs3i_id=s3i:4eadfd01-0eef-4567-ab01-0d6add9c9a0c) in something like a timeline. I do that to verify the camera has worked properly over the given interval.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ## Setup work

        Well, of course, the database has to be set up first.

        - **IMPORTANT: Remember to run the cell below to initialize the database connection.**
        - **TODO: Setup the logging here too**
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    import plotly.io as pio

    pio.templates.default = "plotly_dark"
    return mo, pd, pio, px


@app.cell
async def _():
    from exp_coord.db.connection import init_db

    await init_db()
    return (init_db,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Getting the data

        I want to get the different status information for the given period, so I am going to perform a MongoDB query to get exactly that. To do that, I need to first initialize the clien of course.
        """
    )
    return


@app.cell
async def _():
    import datetime

    from exp_coord.db.status import Status

    # Query all statuses between the 6th of april and the 11th of april
    start_time = datetime.datetime(2025, 4, 6)
    end_time = datetime.datetime(2025, 4, 12)

    statuses = await Status.find(
        Status.sent_timestamp >= start_time,
        Status.sent_timestamp <= end_time,
        fetch_links=True,  # Fetch linked documents
    ).to_list()
    statuses
    return Status, datetime, end_time, start_time, statuses


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Parsing the data

        Great, now I've got all the statuses I want. Now I need to find a way to put all the necessary data in a Pandas dataframe. The necessary columns fields are Status.statusStatus.status and Status.sent×tampStatus.sent_timestamp.
        """
    )
    return


@app.cell
def _(pd, statuses):
    df = pd.DataFrame([status.model_dump() for status in statuses])
    df = df[["status", "sent_timestamp"]]
    df
    return (df,)


@app.cell
def _(df):
    df2 = df.loc[df["status"] == "fetch", ["sent_timestamp"]]
    df2
    return (df2,)


@app.cell
def _(df2):
    df3 = df2.sort_values(by="sent_timestamp")
    df3["date_diff"] = df3["sent_timestamp"].diff()
    df3["date_diff_min"] = df3["date_diff"].dt.total_seconds() / 60
    df3
    return (df3,)


@app.cell
def _(df3, px):
    px.scatter(
        df3,
        x=[0] * len(df3),
        y="date_diff_min",
        labels={"x": "", "date_diff_minutes": "Interval (minutes)"},
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## First results.

        As we can see above, we have 6 `fetch` events, out of which all but two happened practically 10 minutes after each other. That's how it should be. I think that the two outliers are related, but I'll still have to come up with a theory of why they happened.
        """
    )
    return


if __name__ == "__main__":
    app.run()
