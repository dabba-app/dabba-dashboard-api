# Dabba App

## Setup

##### Dependencies
1.[Docker for Mac](https://download.docker.com/mac/stable/Docker.dmg) - ensure it is running with the whale icon in the menubar
2.[Python 2.7](https://www.python.org/download/releases/2.7/)
3.*virtualenv* - `pip install virtualenv`

Follow these steps to get started the first time

* `git clone https://github.com/dabba-fyp/dabba-app`
* `cd dabba-app`
* `virtualenv venv`
* `source venv/bin/activate`
* `docker rm mongodb-docker-dabba && docker run --name mongodb-docker-dabba -p 27017:27017 -d mongo`
* `sudo docker exec -it mongodb-docker-dabba mongo admin`
* `use charts`
* `db.createCollection("views")`
* `exit`
* Finally, run the app - `python app.py`

