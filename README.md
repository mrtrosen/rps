# Rock Paper Scissors
**License: MIT**

This is a web based implementation of a two player game of rock, paper, scissors game, based on the following project requirements:
 - Allow two players to enter their names
 - One of the players can also be the computer, i.e. player vs computer
 - Allow each to play a turn, one at a time, during which the player selects one of the option from rock, paper, scissors
 - During each turn notify who has won and increment the scores
 - In addition to implementing basic gameplay, the user must be able to save their game


# Project Task List
- [x] Create web app and change default project setup to preferred layout
- [x] Update Django to 4.1 version (Django Cookiecutter still utilizes 4.0 release)
- [x] Validate base project setup is completed and properly runs locally
- [x] Determine gameplay strategy and document steps
- [x] Setup django app for RPS views
- [x] Create Single User Gameplay (Player vs. Computer)
- [ ] Create Player Versus Player Gameplay - 2 Players - Simple Mode (both users on same browser window)
- [ ] Create Player Versus Player Gameplay - 2 Players - Advanced Mode (Player Invite / Game Code Entry / etc)
- [ ] Update django models to allow for user game history saving
- [ ] (Future) Create Player Versus Player Gameplay - 2 Players - Simple Mode (both users on same browser window)
- [ ] (Future) Create Player Versus Player Gameplay - > 2 Players - Advanced Mode (Player Invite / Game Code Entry / etc)

# Project Thoughts
 - The decision to use the computer as a non-user is probably not the best approach. I would change out this decision and 
   create a user account for the computer so there is less complexity in the code for determining if there is a 
   real second player or not.
 - Adding additional javascript functionality using Vue.js would make the pages more dynamic, allowing for a more modern 
   web experience but was left out to worry more about the initial game play
 - The design of the site is purposely left using standard bootstrap css functionality - this was a quick to put-together
   project that didn't warrant spending a lot of time building out a full game-play design

# Project Thoughts / Considerations
The game of rock-paper-scissors is a real-time game in which 2 or more users have an option to play either a Rock, Scissors, or Paper.

Each option has a set of rules for if that option wins over another player selected option.  These rules are defined as:
 - Rock **beats** Scissor
 - Scissor **beats** Paper
 - Paper **beats** Rock

## Game Play
 - Each player, at the same time, reveals the option that they have chosen
 - If a player chooses an option that loses to another players option, that player looses that round
 - The game continues until only **ONE** player remains, having beaten all other users

If all players choose the same option during the same round that round is determined as a tie, and those players continue to the next round.


# Project Layout
This project utilizes Python and Django utilizing the [https://cookiecutter-django.readthedocs.io/en/latest/index.html](Django CookieCutter)
 project template to quickly get the development environment up and running.


# Setting Up Local Development Environment
The following steps provide an example on how to configure this project for local development.  It assumes the user:
 - is familiar with Python virtual environments and their setup
 - is familiar with Django and it's configuration/dependencies
 - is familiar with setting up a local postgres database

**The following steps are an example of setting up a local environment on a linux (Ubuntu) based environment.**

```shell
# 1.
# determine where you want to install the project code base and navigate to that directory
cd ~/work/virtualenvs/

# 2.
# clone the repo to your current directory
git clone git@github.com:mrtrosen/rps.git

# 3.
# enter the code directory and setup a python virtualenv, and activate it
cd rps
python -m venv .venv
source .venv/bin/activate

# 4.
# create the database for holding the django app tables
# this project is utilizing postgres by default
createdb rps

# 5.
# install the project python dependencies for local development
pip install -r requirements/local.txt

# 6.
# setup environment variables which will be required for running
# an example env variable file is located in .env_example
# copy that to .env and update/modify as appropriate
cp .env_example .env

# 7.
# IMPORTANT NOTE:
# make sure to edit the .env file and update settings as appropriate prior to sourcing it
source .env

# 8.
# run the database migrations
python manage.py migrate

# 9.
# create a Django superuser so you have a login to the Django Admin et.al.
# fill out the required information as prompted on the command line
python manage.py createsuperuser

# 10.
# run django runserver and load the app in a web browser
# the website will be running on:  http://localhost:8000
python manage.py runserver


# 11
# install pre-commit so it is setup for commit checking
pre-commit install


```


# Development Tasks/How To's
### Type checks

Running type checks with mypy:

    $ mypy rps

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest
