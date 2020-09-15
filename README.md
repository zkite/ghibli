# Ghibli movie list application 
Simple python application which serves a page with movie list of Studio Ghibli.

## Task description
Write a Python application which serves a page with movie list of Studio Ghibli. 
This page should contain a plain list of all movies from the Ghibli API. 
For each movie the people that appear in it should be listed.

## Start application
    docker-compose up

## Page URL
    http://127.0.0.1:8000/ghibli/v1/movies
    
## Test application
    py.test
    
## Check code style
    flake8 --exclude=".svn,CVS,.bzr,.hg,.git,__pycache__,.tox,.eggs,*.egg,venv,tests" --ignore=E501
    
## Architecture decisions
1. Since accessing the API is a time-intensive operation I decided to implement caching via Redis.
2. Sanic framework has been used to implement task as web application.

## Things that can be improved
1. Doc strings
2. Increase code test coverage
3. Type hints
4. Check response Ghibli API format
5. Store data in DB
6. Implemet CORS and authorization

 
       