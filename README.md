# Simple REST API based social network on Django

Object of this task is to create a simple REST API based social network in Django,
and create a bot which will demonstrate functionalities of the system according to defined rules

Task: [link](https://drive.google.com/file/d/1B26f3LMO1HqZO-7bQfpE9bSaEW0Yhhp7/view?usp=sharing)


### How to run
* Create virtual environment
```
python3 -m venv .env/
. .env/bin/activate
```
* Install requirements
```
pip install -r requirements/api.txt requirements/bot.txt
```
* Run api
```
cd social_network
./manage.py runserver
```
* Run bot
```
cd bot
python3 main.py
```
