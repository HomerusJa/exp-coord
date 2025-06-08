# 🌱 Experiment Coordination

This repository contains the code for an experiment coordination system for my project on quantifying the effects of water shortage on plant root growth.

## 🤝 Contributing

As this project is personal, I'm not set up for external contributions in the traditional sense. However, I would greatly appreciate any feedback on the code. If you have thoughts or suggestions, please feel free to start a GitHub discussion or write an email to [`jakob@schluse.com`](mailto:jakob@schluse.com)

If you're interested in running the project yourself, note that access to S3I is required. If you have access or are interested in exploring this further, don't hesitate to reach out to me directly.

## 🧑‍💻 Development Setup

If you want to set up your development environment, that's easy. Again, run the following commands:

```bash
cd /path/to/exp-coord
uv sync
```

Now activate the environment with your system specific command or be doomed to always use `uv run ...`, a command automatically activating your environment, syncing your dependencies and running whatever command you like (or a .py script, it's second use) inside the virtual environment.

By removing the `--no-default-groups` flag, all the testing and linting dependencies will be installed.

### 🔎 Setting up `pre-commit`

This project uses `pre-commit` to ensure code quality. If not installed already, you can do that with:

```bash
uv tool install pre-commit
```

I'd suggest using [`pre-commit-uv`](https://pypi.org/project/pre-commit-uv/) along with `pre-commit`. To do that, run the following command:

```bash
uv tool install pre-commit --with pre-commit-uv --force-reinstall
```

Now, you can run `pre-commit install` to set up the hooks.

Note that this setup runs `pyright` and `pytest` as two `pre-push` hooks, so don't wonder if pushing takes a little bit longer. This eliminates the need to set up GitHub actions, and as this is a personal project and I can live with it, you have to live with it too (-:

### 🔒 Setting up ggshield

This project uses [`ggshield`](https://docs.gitguardian.com/platform/gitguardian-suite/gitguardian-cli-ggshield) to automatically scan for leaked secrets in the code *before each commit*. The current setup requires a local installation of `ggshield` to be available and you to be authenticated. Reference [`ggshield`'s getting started guide](https://docs.gitguardian.com/ggshield-docs/getting-started) to quickly get up and running. Consider using `uv tool install` instead of the suggested `pipx install`. `uv` is generally faster and more modern for installing Python tools.

> [!NOTE]
> Skipping the `ggshield` check is *strongly discouraged* as it could lead to the accidental commit of sensitive information. If you absolutely must skip the check temporarily (e.g., for troubleshooting), you can set the `SKIP` environment variable like so:
>
> ```
> # Windows
> $env:SKIP="ggshield" ; git commit -m "Your commit message"
>
> # UNIX and Linux
> SKIP=ggshield git commit -m "Your commit message"
> ```

### 🧪 Running the tests

Running tests is easy too! Just run:

```bash
uv run pytest
```

You can omit the uv run if your environment is activated. If you want to run only the integration or unit tests, please use one of the following commands:

```bash
uv run pytest -m "unit"
uv run pytest -m "integration"
```

The tests are marked using `pytestmark` in the `__init__.py` file of the respective folders.

## 🤖 Usage

The experiment coordinator currently provides a command line interface. His documentation can be found [here](docs/cli.md).

To run a command, ensure you followed the installation instructions. If the virtual environment is activated, you can just run `exp-coord [command]`.

If you want to see the experiment coordinator in action, run `exp-coord run single`. This will run a single fetch against the configured message and event endpoint and take appropriate actions.

## 🏗️ Tech Stack

### 🗄️ Database

The database used in this project is [**MongoDB**](https://www.mongodb.com/). The reason for choosing MongoDB is that it is a NoSQL database, and the data is stored in JSON documents. This makes it easy to store and retrieve data. Also, migrations are simple since the schema is not fixed.

As an ODM, I am using [**Beanie**](https://beanie-odm.dev/), an async MongoDB ODM for Python. It is built on top of **Pydantic** and **Motor** and works well so far. One feature I am missing, though, is a good integration with **GridFS**. Currently, I am working around that by using CRUD functions, the ones Beanie is trying to replace... For more information on the GridFS setup, look at [this file](./src/exp_coord/db/gridfs.py).

### 🔐 S3I

S3I is a protocol for secure communication between IoT devices and the cloud. It is programmed and hosted by **KWH4.0** (Kompetenzzentrum Wald und Holz 4.0). More information can be found [here](https://kwh40.pages.rwth-aachen.de/s3i/).

In this project, S3I is used to allow communications between the different devices like the cameras or the water supply and the coordinator (this application).
