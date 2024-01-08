# Project:

## Current web application:

* is parsing the data from https://codeforces.com/ via API;
* extracts and transforms the data about problems' rating, tags and id's;
* initiates instances of Problem, Tag, Contest and saves them into database (SQLAlchemy). Note: Problem-Tag many-to-many
  relationships are managed via associated model ProblemTagAssociation;
* groups Problems in Contests by rating and tags;
* update database on hourly basis
* interacts with the user via async Telegram messenger bot, where offers to find the contest by rating and tag either to
  search a problem via search code

## Notes:

* Problems are grouped in contests by rating level step of 300 (e.g. 800-1099, 1100-1399 etc)
* Each contest contains not more than 10 problems (it can contain less, but in that case it is considered to be 'unset'
  and is not being searched and/or delivered to the user)
* Each problem has multiple tags, but for the purpose of entering the contest only ONE tag is chosen, basing on the
  frequency of tag's usage (less popular tags are chosen for the contests in order to provide more diverse contest
  options
  for the user)
* Each problem can be used only in ONE contest
* Database update performs a search of a problem via search code: if the problem is found, its name and times it was
  solved are updated. If the problem is not found, a new problem in created in database


## Further steps:
* Implement logging
* Implement schema usage in DB
* Make async working DB
* Implement callback factory within Telegram bot
* Wrap in Docker


# Stack:

* Python
* API
* Celery
* Redis
* SQLAlchemy
* DB migrations: alembic
* Aiogram
* Async

## App instructions:


### To run the database update (it will be updated hourly):

* create database
* migrate: alembic upgrade head
* run celery: python.exe -m celery -A db_updater worker -l INFO -P eventlet
* run celery beat: celery -A db_updater beat --loglevel=info 
##### Notes: first db update will take around 30-40 minutes to fill in the initial data. Further updates take seconds to perform 

### To run the Telegram bot:

* run: python main.py