# 🌱 Experiment Coordination

> [!WARNING]
> This project is a personal work in progress. I am sharing it on GitHub to show my work and to get feedback, but I did not set this up to be easily usable by others. If you are interested in using this project, please contact me first.

This repository contains the code for an experiment coordination system for my project on quantifying the effects of water shortage on plant root growth.

## 🛠️ Installation

`uv` makes the installation of this project very easy. Just run the following commands:

```bash
cd /path/to/exp-coord
uv sync --no-default-groups
.venv/Scripts/activate
```

This will install all dependencies and set up the virtual environment for you.

## 🧑‍💻 Development Setup

If you want to set up your development environment, that's really easy too. Again, run the following commands:

```bash
cd /path/to/exp-coord
uv sync
.venv/Scripts/activate
```

With removing the `--no-default-groups` flag, all the testing and linting dependencies will be installed.

This project uses `pre-commit` to ensure code quality. If not installed already, you can do that with:

```bash
uv tool install pre-commit
```

I'd suggest using [`pre-commit-uv`](https://pypi.org/project/pre-commit-uv/) along with `pre-commit`. To do that, run the following command:

```bash
uv tool install pre-commit --with pre-commit-uv --force-reinstall
```

Now, you can run `pre-commit install` to set up the hooks. Note that this setup runs `pyright` and `pytest` as two `pre-push` hooks, so don't wonder if pushing takes a little bit longer. This eliminates the need to set up GitHub actions, and as this is a personal project and I can live with it, you have to live with it too (-:

## 🤖 Usage

The experiment coordinator currently provides a command line interface. His documentation can be found [here](docs/cli.md).

To run a command, ensure you followed the installation instructions. If the virtual environment is activated, you can just run `exp-coord [command]`.

## 🏗️ Tech Stack

### 🗄️ Database

The database used in this project is [**MongoDB**](https://www.mongodb.com/). The reason for choosing MongoDB is that it is a NoSQL database, and the data is stored in JSON documents. This makes it easy to store and retrieve data. Also, migrations are simple since the schema is not fixed.

As an ODM, I am using [**Beanie**](https://beanie-odm.dev/), an async MongoDB ODM for Python. It is built on top of **Pydantic** and **Motor** and works well so far. One feature I am missing, though, is a good integration with **GridFS**.

### 🔐 S3I

S3I is a protocol for secure communication between IoT devices and the cloud. It is programmed and hosted by **KWH4.0** (Kompetenzzentrum Wald und Holz 4.0). More information can be found [here](https://kwh40.pages.rwth-aachen.de/s3i/).

### 📝 Logging

For logging, we are using [**loguru**](https://loguru.readthedocs.io/en/stable/), intercepting the standard logging module to also capture logs from third-party libraries. This works great, as loguru is just a great library.
