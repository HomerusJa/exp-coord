# 🌱 Experiment Coordination

This repository contains the code for an experiment coordination system for my project on quantifying the effects of water shortage on plant root growth.

## 🛠️ Installation

`uv` makes the installation of this project very easy. Just run the following command:

```bash
cd /path/to/exp-coord
uv sync --no-dev
.venv/Scripts/activate
```

This will install all dependencies and set up the virtual environment for you.

## 🤖 Usage

Currently, the system doesn’t have a command-line interface. I am still working on the boilerplate implementation.

I am planning to provide:

- A one-off script that fetches data once.
- A daemon that runs in a scheduled manner.

## 🏗️ Tech Stack

### 🗄️ Database

The database used in this project is [**MongoDB**](https://www.mongodb.com/). The reason for choosing MongoDB is that it is a NoSQL database, and the data is stored in JSON documents. This makes it easy to store and retrieve data. Also, migrations are simple since the schema is not fixed.

As an ODM, I am using [**Beanie**](https://beanie-odm.dev/), an async MongoDB ODM for Python. It is built on top of **Pydantic** and **Motor** and works well so far. One feature I am missing, though, is a good integration with **GridFS**.

### 🔐 S3I

S3I is a protocol for secure communication between IoT devices and the cloud. It is programmed and hosted by **KWH4.0** (Kompetenzzentrum Wald und Holz 4.0). More information can be found [here](https://kwh40.pages.rwth-aachen.de/s3i/).

### 📝 Logging

For logging, we are using [**loguru**](https://loguru.readthedocs.io/en/stable/), intercepting the standard logging module to also capture logs from third-party libraries. This works great, as loguru is just a great library.

## 👨‍💻 Development

To start developing, setup your environment with all the extra dependencies.

```bash
cd /path/to/exp-coord
uv sync
```

Run the tests using pytest, by running:

```bash
cd /path/to/exp-coord
pytest
```

This project uses pre-commit hooks to ensure code quality. To install them, run:

```bash
pre-commit install
```
