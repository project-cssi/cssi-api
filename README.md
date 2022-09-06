<p align="left">
    <img style="display:block;text-align:center" src="./docs/logo/cssi-logo-rest-api.svg" alt="logo-text" height="100" />
    <p style="font-size: 1.2rem;">RESTful API for the CSSI Platform</p>
</p>

<!-- Badges -->
<p align="left">
  <a href="https://travis-ci.org/project-cssi/cssi-api" alt="Travis">
    <img src="https://travis-ci.org/project-cssi/cssi-api.svg?branch=master"/>
  </a>
  <a href="https://github.com/project-cssi/cssi-api/graphs/contributors" alt="Contributors">
    <img src="https://img.shields.io/github/contributors/project-cssi/cssi-api.svg?logo=github"/>
  </a>
  <a href="LICENSE.md">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" height="18">
  </a>
  <a href="https://github.com/project-cssi/cssi-api/stargazers">
    <img src="https://img.shields.io/github/stars/project-cssi/cssi-api.svg?logo=github" alt="Github stars" height="18">
  </a>
  <a href="https://github.com/project-cssi/cssi-api/network/members">
    <img src="https://img.shields.io/github/forks/project-cssi/cssi-api.svg?logo=github" alt="Github forks" height="18">
  </a>
  <a href="https://twitter.com/brion_mario">
    <img src="https://img.shields.io/twitter/follow/brion_mario.svg?label=brion_mario&style=flat&logo=twitter&logoColor=4FADFF" alt="Twitter" height="18">
  </a>
  <a href="https://app.fossa.io/projects/git%2Bgithub.com%2Fproject-cssi%2Fcssi-api?ref=badge_shield" alt="FOSSA Status">
    <img src="https://app.fossa.io/api/projects/git%2Bgithub.com%2Fproject-cssi%2Fcssi-api.svg?type=shield"/>
  </a>

</p>

# Getting Started

```bash
# clone the repository
git clone https://github.com/project-cssi/cssi-api.git

# change the directory
cd cssi-api

# install the dependencies
pip install -r requirements.txt

# create the database
python manage.py recreate_db

# add metadata to database
python manage.py create_metadata

# fire up redis server
redis-server

# start celery workers
python manage.py celery

# run the app
python manage.py runserver

```

# Built With

<a href="https://www.python.org/" title="Python"><img src="./docs/readme-resources/technologies/python.svg" alt="python" height="30" /></a>&nbsp;&nbsp;
<a href="http://flask.pocoo.org/" title="Flask"><img src="./docs/readme-resources/technologies/flask.svg" alt="flask" height="30" /></a>&nbsp;&nbsp;
<a href="https://flask-socketio.readthedocs.io/en/latest/" title="Flask SocketIO"><img src="./docs/readme-resources/technologies/flask-socketio.png" alt="redux" height="30" /></a>&nbsp;&nbsp;
<a href="https://flask-sqlalchemy.palletsprojects.com/en/2.x/" title="Flask SQL Alchemy"><img src="./docs/readme-resources/technologies/flask-sqlalchemy.png" alt="lodash" height="30" /></a>&nbsp;&nbsp;
<a href="http://www.celeryproject.org/" title="Celery"><img src="./docs/readme-resources/technologies/celery.png" alt="celery" height="50" /></a>&nbsp;&nbsp;
<a href="https://marshmallow.readthedocs.io/en/3.0/" title="Marshmallow"><img src="./docs/readme-resources/technologies/marshmallow.png" alt="marshmallow" height="50" /></a>&nbsp;&nbsp;
<a href="https://www.mysql.com/" title="MySQL"><img src="./docs/readme-resources/technologies/mysql.svg" alt="sass" height="50" /></a>&nbsp;&nbsp;
<a href="https://redis.io/" title="Redis"><img  src="./docs/readme-resources/technologies/redis.png" alt="redis" height="30" /></a>&nbsp;&nbsp;

# Releases

Please read the [RELEASES.md](./docs/RELEASES.md) guideline to learn about the process for releasing the project.

# Changelog

Please refer [CHANGELOG.md](CHANGELOG.md) to learn about the latest improvements, breaking changes and bug fixes.

# Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for contributing guidelines and to learn about our code of conduct.

# Contributors

<a href="https://github.com/project-cssi/cssi-api/graphs/contributors">
  <img src="https://contributors-img.firebaseapp.com/image?repo=project-cssi/cssi-api" />
</a>

# License

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fproject-cssi%2Fcssi-api.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fproject-cssi%2Fcssi-api?ref=badge_large)
