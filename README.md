<h1 align="center" id="title">Experiment Coordinator</h1>

<p id="description">This is the experiment coordinator for my plant research project. It is an interconnect for the different parts of the application and implements some of them too. For further information reference the <a href="https://github.com/HomerusJa/submission-schueler-experimentieren">paper</a> (german work in progress).</p>

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features, split by managing features and provided tasks

<h3>Experiment Managing</h3>
*   GUI for tracking the progress
*   Task scheduling with APScheduler
*   Managing the different task-settings (Currently JSON, GUI is work in progress)
*   Resolving following tasks based on executed one

<h3>Tasks</h3>
*   Communicating with the Rhizotrone via the S3I infrastructure
*   📓 And so much more in the future... 

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone this repository</p>

```
gh repo clone https://github.com/HomerusJa/exp-coord
```

<p>2. Change to the folder of the repository</p>

```
cd path/to/repository
```

<p>3. Install the dependencies</p>

```
poetry install
```

<p>4. Customize the intervalls (Work in progress)</p>

<p>5. Run the coordinator</p>
```
poetry run python exp_coord
```
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   [APScheduler](https://github.com/agronholm/apscheduler) by [Alex Grönholm](https://github.com/agronholm), a task-scheduling-library for Python
*   [S3I](https://kwh40.pages.rwth-aachen.de/s3i/) by the [Kompetenzzentrum Wald und Holz 4.0](https://www.kwh40.de/), an IOT-message interchange protocol with an attached REST-Api
*   [Poetry](https://python-poetry.org/) by [Sébastien Eustace](http://www.sebastien-eustace.fr/)

<h2>🛡️ License:</h2>

This project is licensed under the **CC BY-NC 4.0**
