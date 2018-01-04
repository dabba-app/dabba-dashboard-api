# Dabba App

## Setup
* ##### Dependencies
    * [Docker for Mac](https://download.docker.com/mac/stable/Docker.dmg) - ensure it is running with the whale icon in the menubar
    * [Python 2.7](https://www.python.org/download/releases/2.7/)
    * *virtualenv* - `pip install virtualenv`

* ##### First Time Setup
    * `git clone https://github.com/bholagabbar/dabba-api`
    * `cd dabba-api`
    * `virtualenv venv`
    * `source venv/bin/activate`
    * `docker rm mongodb-docker-dabba && docker run --name mongodb-docker-dabba -p 27017:27017 -d mongo`
    * `sudo docker exec -it mongodb-docker-dabba mongo admin`
    * `use charts`
    * `db.createCollection("views")`
    * `exit`
* ##### Running the app
    * `python app.py`

*Mock Dashboard Setup* - Open `localhost:8080`, create a Dashboard, selected Widget Chart as C3 linechart and selected datasource as `http://localhost:8080/line` to see dashboard with mock line endpoint data=.

## Notes for Developing app further

We are using the [flask-jsondash](https://github.com/christabor/flask_jsondash) to build the dashboard. Try understanding the [example app](https://github.com/christabor/flask_jsondash/tree/master/example_app) code.

The flask-jsondash has support for custom widget which can be used to build our image widget. Have a look at the [example templates is the example app](https://github.com/christabor/flask_jsondash/tree/master/example_app/templates/examples) which contains HTML snippets to help build the image widget which will have to be added to the main html template in `/templates/layouts/base.html`.
